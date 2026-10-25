WITH latest AS (
  SELECT DISTINCT ON (p."RepositoryId") p."RepositoryId", p."DimensionStatesJson", r."CorpusLanguage" AS lang
  FROM metrics.metric_points p JOIN repositories."Repositories" r ON r."Id" = p."RepositoryId"
  WHERE r."CorpusLanguage" IN ('csharp','go','rust') AND NOT r."Hidden"
    AND p."Trigger" <> 'Bridge' AND NOT p."Degraded" AND p."IncompleteReason" IS NULL AND p."DimensionStatesJson" IS NOT NULL
  ORDER BY p."RepositoryId", p."At" DESC)
SELECT lang, (SELECT count(*) FROM jsonb_each_text(l."DimensionStatesJson"::jsonb)) AS dims_listed, count(*) FROM latest l GROUP BY 1,2 ORDER BY 1,2;
