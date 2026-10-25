WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", p."At", p."ProductionLoc", p."DimensionStatesJson", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC
), f AS (
  SELECT l.*, s."ScannerVersion", date_trunc('month', l."At") AS month,
    (SELECT sum(coalesce(m."FindingCount",0)) FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId") AS findings,
    (SELECT count(*) FROM jsonb_each_text(l."DimensionStatesJson"::jsonb) e WHERE e.value = 'measured') AS dims_measured
  FROM latest l LEFT JOIN scans.scan_run_index s ON s."ScanRunId" = l."RunId")
SELECT lang, month, count(*) repos, count(DISTINCT "ScannerVersion") engines,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY findings) findings_median, round(avg(findings),1) findings_mean,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY "ProductionLoc") loc_median,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY dims_measured) dims_measured_median
FROM f GROUP BY 1,2 ORDER BY 1,2;
WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC)
SELECT s."ScannerVersion", count(*) FILTER (WHERE lang='csharp') cs, count(*) FILTER (WHERE lang='go') go, count(*) FILTER (WHERE lang='rust') rust
FROM latest l LEFT JOIN scans.scan_run_index s ON s."ScanRunId" = l."RunId" GROUP BY 1 ORDER BY 2+3+4 DESC LIMIT 25;
-- the ten largest per language, by findings and by LOC (size check)
WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", p."ProductionLoc", r."CorpusLanguage" AS lang, r."Owner"||'/'||r."Name" AS repo
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC),
f AS (SELECT l.*, (SELECT sum(coalesce(m."FindingCount",0)) FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId") findings FROM latest l),
rk AS (SELECT f.*, row_number() OVER (PARTITION BY lang ORDER BY findings DESC) rn_hi, row_number() OVER (PARTITION BY lang ORDER BY findings ASC, repo) rn_lo FROM f)
SELECT lang, repo, findings, "ProductionLoc", CASE WHEN rn_hi<=3 THEN 'top' ELSE 'bottom' END AS tail FROM rk WHERE rn_hi<=3 OR rn_lo<=3 ORDER BY lang, findings DESC;
-- correlation of findings with size, per language
WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", p."ProductionLoc", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC),
f AS (SELECT l.*, (SELECT sum(coalesce(m."FindingCount",0)) FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId") findings FROM latest l)
SELECT lang, count(*) n, round(corr(findings, "ProductionLoc")::numeric,3) pearson_raw, round(corr(ln(findings+1), ln("ProductionLoc"+1))::numeric,3) pearson_log FROM f GROUP BY 1 ORDER BY 1;
