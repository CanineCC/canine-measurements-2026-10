WITH pts AS (
  SELECT DISTINCT ON (p."RepositoryId", s."ScannerVersion") p."RepositoryId", p."RunId", p."ProductionLoc", r."CorpusLanguage" AS lang, s."ScannerVersion" AS engine
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId" JOIN scans.scan_run_index s ON s."ScanRunId" = p."RunId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden" AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL
    AND s."ScannerVersion" IN ('measure-2026.10.3+preprod-fddbc92cb8df','preprod-fe8540b5da9b')
  ORDER BY p."RepositoryId", s."ScannerVersion", p."At" DESC),
a AS (SELECT * FROM pts WHERE engine LIKE 'measure-2026.10.3%'), b AS (SELECT * FROM pts WHERE engine = 'preprod-fe8540b5da9b')
SELECT a.lang, count(*) paired, percentile_cont(0.5) WITHIN GROUP (ORDER BY a."ProductionLoc") loc_103, percentile_cont(0.5) WITHIN GROUP (ORDER BY b."ProductionLoc") loc_fe85,
  count(*) FILTER (WHERE a."ProductionLoc" = b."ProductionLoc") same_loc
FROM a JOIN b USING ("RepositoryId") GROUP BY 1 ORDER BY 1;
SELECT r."CorpusLanguage", s."ScannerVersion", min(s."CompletedAt"), max(s."CompletedAt"), count(*) FROM scans.scan_run_index s JOIN repositories."Repositories" r ON r."Id"=s."RepositoryId"
WHERE s."ScannerVersion" IN ('measure-2026.10.3+preprod-fddbc92cb8df','measure-2026.10.6+preprod-d36780c2d857','preprod-fe8540b5da9b') AND r."CorpusLanguage" IN ('csharp','go','rust') GROUP BY 1,2 ORDER BY 2,1;
