WITH pts AS (
  SELECT DISTINCT ON (p."RepositoryId", s."ScannerVersion") p."RepositoryId", p."RunId", p."ProductionLoc", p."DimensionStatesJson", r."CorpusLanguage" AS lang, s."ScannerVersion" AS engine
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId" JOIN scans.scan_run_index s ON s."ScanRunId" = p."RunId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
    AND s."ScannerVersion" IN ('measure-2026.10.3+preprod-fddbc92cb8df','measure-2026.10.6+preprod-d36780c2d857','preprod-fe8540b5da9b')
  ORDER BY p."RepositoryId", s."ScannerVersion", p."At" DESC),
f AS (SELECT pts.*, (SELECT sum(coalesce(m."FindingCount",0)) FROM metrics.run_dimension_metrics m WHERE m."RunId" = pts."RunId") findings,
  (SELECT count(*) FROM jsonb_each_text(pts."DimensionStatesJson"::jsonb) e WHERE e.value = 'measured') dims_measured FROM pts)
SELECT engine, lang, count(*) repos, percentile_cont(0.5) WITHIN GROUP (ORDER BY findings) findings_median, round(avg(findings),1) findings_mean,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY "ProductionLoc") loc_median,
  round((percentile_cont(0.5) WITHIN GROUP (ORDER BY findings*1000.0/nullif("ProductionLoc",0)))::numeric,2) per_kloc_median,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY dims_measured) dims_measured_median
FROM f WHERE findings IS NOT NULL GROUP BY 1,2 ORDER BY 1,2;
