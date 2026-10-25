SELECT b.data->>'RepositoryId' AS repo, (m."MetricsJson"::jsonb->>'hotspot_count') AS hotspots, (m."MetricsJson"::jsonb->>'shallow_history') AS shallow
FROM events.mt_doc_repositorybundle b
LEFT JOIN metrics.run_dimension_metrics m ON m."RunId"::text = b.data->>'RunId' AND m."DimensionId"='D15'
WHERE NOT coalesce((b.data->>'IsSecurityWatch')::boolean, false) AND jsonb_typeof(b.data->'SprintPlan'->'Tickets')='array'
ORDER BY 1;
