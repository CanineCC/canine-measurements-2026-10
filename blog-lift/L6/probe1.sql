SELECT jsonb_object_keys(data) k, count(*) FROM events.mt_doc_repositorybundle GROUP BY 1 ORDER BY 1;
SELECT jsonb_object_keys(data->'SprintPlan') k, count(*) FROM events.mt_doc_repositorybundle WHERE jsonb_typeof(data->'SprintPlan')='object' GROUP BY 1;
SELECT id, data->'SprintPlan'->'Tickets'->0 AS t0, data->'SprintPlan'->'Tickets'->1 AS t1, jsonb_array_length(data->'SprintPlan'->'Tickets') n FROM events.mt_doc_repositorybundle WHERE jsonb_typeof(data->'SprintPlan'->'Tickets')='array' ORDER BY mt_last_modified DESC LIMIT 3;
