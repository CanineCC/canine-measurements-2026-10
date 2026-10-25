WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", p."At", p."ProductionLoc", p."PrimaryLanguage", p."Trigger", p."RubricVersion", p."DimensionStatesJson", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC
), f AS (
  SELECT l.*, (SELECT sum(coalesce(m."FindingCount",0)) FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId") AS findings,
         (SELECT count(*) FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId") AS dim_rows,
         (SELECT count(*) FROM jsonb_each_text(l."DimensionStatesJson"::jsonb) e WHERE e.value = 'measured') AS dims_measured,
         (SELECT count(*) FROM jsonb_each_text(l."DimensionStatesJson"::jsonb) e WHERE e.value <> 'n/a') AS dims_applicable,
         (SELECT count(*) FROM jsonb_each_text(l."DimensionStatesJson"::jsonb) e) AS dims_listed,
         s."ScannerVersion"
  FROM latest l LEFT JOIN scans.scan_run_index s ON s."ScanRunId" = l."RunId"
), g AS (SELECT * FROM f WHERE dim_rows > 0)
SELECT lang, count(*) AS repos,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY findings) AS findings_median,
  round(avg(findings),1) AS findings_mean,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY findings) AS findings_p25,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY findings) AS findings_p75,
  max(findings) AS findings_max, min(findings) AS findings_min,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY "ProductionLoc") AS loc_median,
  count(*) FILTER (WHERE "ProductionLoc" > 0) AS repos_with_loc,
  round((percentile_cont(0.5) WITHIN GROUP (ORDER BY findings * 1000.0 / nullif("ProductionLoc",0)))::numeric, 2) AS per_kloc_median,
  round((sum(findings) * 1000.0 / nullif(sum("ProductionLoc") FILTER (WHERE "ProductionLoc">0),0))::numeric, 2) AS pooled_per_kloc,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY dims_measured) AS dims_measured_median,
  round(avg(dims_measured),2) AS dims_measured_mean,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY dims_applicable) AS dims_applicable_median,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY dims_listed) AS dims_listed_median,
  min("At") AS oldest_run, max("At") AS newest_run
FROM g GROUP BY lang ORDER BY lang;
-- population accounting
WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."RunId", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC)
SELECT r."CorpusLanguage", count(*) AS corpus_repos, count(l."RepositoryId") AS with_clean_point,
  count(l."RepositoryId") FILTER (WHERE EXISTS (SELECT 1 FROM metrics.run_dimension_metrics m WHERE m."RunId" = l."RunId")) AS with_dim_rows
FROM repositories."Repositories" r LEFT JOIN latest l ON l."RepositoryId" = r."Id"
WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden" GROUP BY 1 ORDER BY 1;
SELECT DISTINCT "Trigger" FROM metrics.metric_points;
