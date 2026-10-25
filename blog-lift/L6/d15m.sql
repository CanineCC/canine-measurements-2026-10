SELECT m."MetricsJson", m."AdvisoryRowsReported", m."AdvisoryRowsSeen", m."Score10", m."Applicable" FROM metrics.run_dimension_metrics m
WHERE m."DimensionId"='D15' AND m."RunId" IN (SELECT (data->>'RunId')::uuid FROM events.mt_doc_repositorybundle ORDER BY mt_last_modified DESC LIMIT 400) LIMIT 4;
SELECT count(*) runs, count(*) FILTER (WHERE m."MetricsJson" IS NOT NULL) with_metrics FROM metrics.run_dimension_metrics m WHERE m."DimensionId"='D15' AND m."CreatedAt" > now() - interval '30 days';
