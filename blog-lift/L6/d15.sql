SELECT b.data->>'RepositoryId' AS repo, coalesce(p."DimensionStatesJson"::jsonb->>'D15', '(no state)') AS d15,
  (SELECT m."FindingCount" FROM metrics.run_dimension_metrics m WHERE m."RunId" = p."RunId" AND m."DimensionId"='D15' LIMIT 1) AS d15_findings
FROM events.mt_doc_repositorybundle b
LEFT JOIN metrics.metric_points p ON p."RunId"::text = b.data->>'RunId'
WHERE NOT coalesce((b.data->>'IsSecurityWatch')::boolean, false) AND jsonb_typeof(b.data->'SprintPlan'->'Tickets')='array'
ORDER BY 1;
