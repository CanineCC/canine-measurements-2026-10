SELECT "CorpusLanguage", count(*) AS repos, count(*) FILTER (WHERE NOT "Hidden") AS visible FROM repositories."Repositories" GROUP BY 1 ORDER BY 2 DESC;
SELECT "PrimaryLanguage", count(DISTINCT "RepositoryId") AS repos, count(*) AS points, max("At") AS last FROM metrics.metric_points GROUP BY 1 ORDER BY 2 DESC LIMIT 30;
SELECT date_trunc('month',"At") AS m, count(*) pts, count(*) FILTER (WHERE "Degraded") deg, count("DeterministicFindingCount") det, count("PublicFindingCount") pub, count("DimensionStatesJson") ds FROM metrics.metric_points GROUP BY 1 ORDER BY 1;
SELECT date_trunc('month',"CreatedAt") m, count(DISTINCT "RunId") runs, count(*) rows FROM metrics.run_dimension_metrics GROUP BY 1 ORDER BY 1;
SELECT date_trunc('month',"CreatedAt") m, count(DISTINCT "RunId") runs, count(*) rows FROM metrics.run_findings GROUP BY 1 ORDER BY 1;
