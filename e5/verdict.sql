WITH r AS (SELECT '{"Value": "REPO"}'::jsonb AS repo),
res AS (SELECT e.data->>'Fingerprint' AS fp, (e.data->>'At')::timestamptz AS at, e.data->>'AgentName' AS agent
        FROM events.mt_events e, r WHERE e.type = 'FindingClaimStateChanged' AND e.data->>'Kind' = 'AgentResolved' AND e.data->'RepositoryId' = r.repo),
runs AS (SELECT e.seq_id, coalesce((e.data->>'StartedAt')::timestamptz, (e.data->>'At')::timestamptz) AS started,
                coalesce((e.data->>'FindingsAreTheFullLedger')::boolean, false) AND NOT coalesce((e.data->>'Degraded')::boolean, false) AS ok
         FROM events.mt_events e, r WHERE e.type = 'ScanRunIngested' AND e.data->'RepositoryId' = r.repo),
dec AS (SELECT res.*, (SELECT seq_id FROM runs WHERE ok AND started > res.at ORDER BY started LIMIT 1) AS dseq,
                      (SELECT seq_id FROM runs WHERE ok AND started <= res.at ORDER BY started DESC LIMIT 1) AS pseq,
                      (SELECT started FROM runs WHERE ok AND started > res.at ORDER BY started LIMIT 1) AS dstart FROM res),
fps AS (SELECT e.seq_id, f->>'Fingerprint' AS fp, f->>'DimensionId' AS dim
        FROM events.mt_events e, jsonb_array_elements(e.data->'Findings') f
        WHERE e.seq_id IN (SELECT dseq FROM dec UNION SELECT pseq FROM dec)),
st AS (SELECT seq_id, data->'DimensionStates' AS ds FROM events.mt_events WHERE seq_id IN (SELECT dseq FROM dec)),
v AS (SELECT dec.*, coalesce(dd.dim, pd.dim) AS dim,
        CASE WHEN dec.dseq IS NULL THEN 'unverified'
             WHEN dd.fp IS NOT NULL THEN 'did_not_clear'
             WHEN pd.dim IS NULL THEN 'absent_dimension_unknown'
             WHEN st.ds ->> pd.dim = 'measured' THEN 'cleared'
             ELSE 'absent_not_measured' END AS verdict
      FROM dec LEFT JOIN fps dd ON dd.seq_id = dec.dseq AND dd.fp = dec.fp
               LEFT JOIN fps pd ON pd.seq_id = dec.pseq AND pd.fp = dec.fp
               LEFT JOIN st ON st.seq_id = dec.dseq)
SELECT verdict, dim, count(*) AS n, count(DISTINCT fp) AS fingerprints,
       round(avg(extract(epoch FROM dstart - at) / 3600)::numeric, 1) AS mean_hours_to_verdict, min(at)::date AS first, max(at)::date AS last
FROM v GROUP BY 1, 2 ORDER BY 1, 3 DESC;
