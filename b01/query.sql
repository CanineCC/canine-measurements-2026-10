-- B1, "Findings count is not analysis depth": per-repository counts, production corpus, C#/Go/Rust.
-- Read-only. Each repository at its most recent complete scan that recorded each dimension, taken at the cut-off below.
with repos as (
  select (data->>'RepositoryId')::uuid rid, data->'State'->>'Language' lang
  from events.mt_doc_admincorpusrepositorydocument
  where data->'State'->>'Language' in ('csharp','go','rust') and coalesce((data->>'Hidden')::bool,false)=false
), latest as (
  select distinct on (s."RepositoryId") s."RepositoryId" rid, s."ScanRunId" run, s."Repository" repo, s."Commit" sha,
         s."MeasuredLoc" loc, s."ScannerVersion" ver, s."CompletedAt" done
  from scans.scan_run_index s join repos r on r.rid=s."RepositoryId"
  where s."Status"='completed' and s."DegradedAt" is null and s."CompletedAt" is not null
    and s."CompletedAt" < timestamptz '2026-11-21 20:16:24+01'
    and exists (select 1 from metrics.run_dimension_metrics x where x."RunId"=s."ScanRunId")
  order by s."RepositoryId", s."CompletedAt" desc
)
select r.lang language, l.repo repository, l.sha "commit", to_char(l.done at time zone 'UTC','YYYY-MM-DD') scanned,
  split_part(l.ver,'+',1) engine, coalesce(l.loc,0) production_loc, coalesce(sum(m."FindingCount"),0) findings
from latest l join repos r on r.rid=l.rid
left join metrics.run_dimension_metrics m on m."RunId"=l.run
group by r.lang,l.repo,l.sha,l.done,l.ver,l.loc
order by 1,2;
