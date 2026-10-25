SELECT b.data->>'RepositoryId' AS repo, b.data->>'RunId' AS run, (b.data->>'CompletedAt') AS completed, s."ScannerVersion" AS engine, r."CorpusLanguage" AS lang,
  (t->>'Id')::int AS tid, t->>'DimensionId' AS dim, t->>'Effort' AS effort, (t->>'ImpactPoints') AS impact, (t->>'Unlocks') AS unlocks,
  substring(t->>'RankReason' from 'score gain \(([0-9.]+) pts\)') AS own_gain,
  substring(t->>'RankReason' from 'divided by ([a-z]+) effort') AS own_effort,
  coalesce(substring(t->>'RankReason' from 'lifted ([0-9]+)%'), CASE WHEN t->>'RankReason' LIKE '%no change-frequency signal%' THEN '0' END) AS lift,
  CASE WHEN t->>'Title' LIKE '%same root cause also lifts%' THEN 1 ELSE 0 END AS folded,
  translate(t->>'Title', E'|\n\r', '/  ') AS title
FROM events.mt_doc_repositorybundle b
CROSS JOIN LATERAL jsonb_array_elements(CASE WHEN jsonb_typeof(b.data->'SprintPlan'->'Tickets')='array' THEN b.data->'SprintPlan'->'Tickets' ELSE '[]'::jsonb END) t
LEFT JOIN scans.scan_run_index s ON s."ScanRunId"::text = b.data->>'RunId'
LEFT JOIN repositories."Repositories" r ON r."Id"::text = b.data->>'RepositoryId'
WHERE NOT coalesce((b.data->>'IsSecurityWatch')::boolean, false)
ORDER BY 1, tid;
