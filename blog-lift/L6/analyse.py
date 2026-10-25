#!/usr/bin/env python3
"""L6: on how many repositories does churn weighting change the top 5 tasks compared with gain/effort alone?

Input: tickets.out (prod-query log of tickets.sql): every repository's current sprint-plan tickets, which are the
consolidated top-8 of the CHURN-WEIGHTED ranking (gain / effort x churn weight), in served order (tid).
For each ticket the RankReason carries the task's own score gain (0.1 pts), its own effort and the churn lift (whole %).

Weighted order = the served order. Unweighted order = the same tickets re-sorted by own gain / effort weight
(Low 1, Medium 2, High 4), ties by gain desc then dimension id (the engine's own tie-breaks; the final tie-break on
the action text, which the ticket title carries ahead of any fold suffix).

Outcomes per repository with at least one ticket:
  no-signal   : every ticket lift 0 -> the two orders are identical by construction.
  changed     : the re-sorted top 5 of the served tickets differs from the served top 5. This is PROVEN: if the true
                unweighted top 5 equalled the served top 5, it would also be the top 5 of any subset containing it.
  unchanged   : re-sorted top 5 equals served top 5 AND no task outside the served 8 can intrude: such a task has
                weighted key <= the smallest served weighted key B, and unweighted key <= weighted key, so if the
                5th unweighted key >= B it cannot enter. Applies automatically when an unlock row is present
                (the ranked list was exhausted before the cap).
  undetermined: re-sorted top 5 equals served top 5 but intrusion from beyond the cap cannot be excluded.
Sensitivity: rounding (gain +-0.05, lift +-0.5 %) and folded tickets (a folded member's own gain/effort is not in the
sprint plan, so its unweighted key is anywhere in [host key, ImpactPoints/1]) are explored by 200 random draws per
repository; a repository whose outcome is not the same in every draw is counted as rounding-sensitive.
"""
import random, re, sys, json
from collections import defaultdict, Counter

EW = {"low": 1.0, "medium": 2.0, "high": 4.0}
src = sys.argv[1]
rows = []
for line in open(src, encoding="utf-8"):
    parts = [p.strip() for p in line.rstrip("\n").split("|")]
    if len(parts) != 15 or not re.match(r"^[0-9a-f]{8}-", parts[0]):
        continue
    repo, run, completed, engine, lang, tid, dim, effort, impact, unlocks, gain, own_eff, lift, folded, title = parts
    rows.append(dict(repo=repo, run=run, completed=completed, engine=engine, lang=lang, tid=int(tid), dim=dim,
                     effort=effort.lower(), impact=float(impact) if impact else 0.0, unlocks=unlocks == "true",
                     gain=float(gain) if gain else None, own_eff=own_eff or None,
                     lift=int(lift) if lift not in ("", None) else None, folded=folded == "1", title=title))

by_repo = defaultdict(list)
for r in rows:
    by_repo[r["repo"]].append(r)

def evaluate(ranked, complete, rng=None):
    """Return 'changed' / 'unchanged' / 'undetermined' for one repository's ranked (non-unlock) tickets."""
    keys = []
    wkeys = []
    gains = []
    shared = {}
    for t in ranked:
        g, e, l = t["gain"], EW[t["own_eff"]], t["lift"]
        if rng is not None:
            # tasks of one dimension with the same printed gain are taken as genuinely equal (same formula):
            # they share one perturbation, so only the engine's own text tie-break orders them.
            off = shared.setdefault((t["dim"], t["gain"]), rng.uniform(-0.05, 0.05))
            g = max(0.0, g + off)
            l = max(0.0, l + rng.uniform(-0.5, 0.5)) if l > 0 else 0.0
        u = g / e
        if t["folded"]:
            hi = t["impact"] / 1.0
            u = rng.uniform(u, max(u, hi)) if rng is not None else u
        keys.append(u)
        gains.append(g)
        wkeys.append((g / e) * (1 + l / 100.0))
    served = list(range(len(ranked)))
    resorted = sorted(served, key=lambda i: (-keys[i], -gains[i], ranked[i]["dim"], ranked[i]["title"]))
    k = min(5, len(ranked))
    if resorted[:k] != served[:k]:
        return "changed", set(resorted[:k]) != set(served[:k]), resorted[0] != 0
    if complete:
        return "unchanged", False, False
    fifth = keys[resorted[k - 1]]
    bound = min(wkeys)
    return ("unchanged" if fifth >= bound else "undetermined"), False, False

summary = Counter()
robust = Counter()
detail = []
skipped = Counter()
rng = random.Random(20261025)
for repo, ts in by_repo.items():
    ts.sort(key=lambda t: t["tid"])
    if any(t["gain"] is None or t["own_eff"] not in EW or t["lift"] is None for t in ts if not t["unlocks"]):
        skipped["no RankReason basis (older run)"] += 1
        continue
    ranked = [t for t in ts if not t["unlocks"]]
    complete = any(t["unlocks"] for t in ts)
    if not ranked:
        skipped["no ranked task"] += 1
        continue
    signal = any(t["lift"] > 0 for t in ranked)
    lifted_top5 = sum(1 for t in ranked[:5] if t["lift"] > 0)
    if not signal:
        outcome, setdiff, topdiff = "no-signal", False, False
        sensitive = False
    else:
        outcome, setdiff, topdiff = evaluate(ranked, complete)
        _ev = [evaluate(ranked, complete, rng) for _ in range(200)]
        draws = {e[0] for e in _ev}
        robust["any draw: changed (or undetermined)"] += any(e[0] != "unchanged" for e in _ev) or outcome != "unchanged"
        robust["any draw: different SET"] += any(e[1] for e in _ev) or setdiff
        robust["any draw: different #1"] += any(e[2] for e in _ev) or topdiff
        sensitive = draws != {outcome}
        robust["changed in every draw" if draws | {outcome} == {"changed"} else
               "unchanged in every draw" if draws | {outcome} == {"unchanged"} else
               "depends on rounding/fold"] += 1
        if draws | {outcome} == {"changed"}:
            robust["  of which a different SET in top 5"] += setdiff
            robust["  of which a different #1"] += topdiff
    summary[outcome] += 1
    if outcome == "changed":
        summary["changed: different SET in top 5"] += setdiff
        summary["changed: different #1"] += topdiff
        summary["changed: rounding-sensitive"] += sensitive
    if outcome in ("unchanged", "undetermined"):
        summary[f"{outcome}: rounding-sensitive"] += sensitive
    detail.append(dict(repo=repo, run=ts[0]["run"], completed=ts[0]["completed"], engine=ts[0]["engine"],
                       lang=ts[0]["lang"], ranked=len(ranked), complete=complete, signal=signal,
                       lifted_in_top5=lifted_top5, outcome=outcome, set_differs=setdiff, first_differs=topdiff,
                       rounding_sensitive=sensitive, folded_in_top5=sum(t["folded"] for t in ranked[:5])))

repos_total = len(by_repo)
print(f"repositories with tickets: {repos_total}")
for k, v in skipped.items():
    print(f"skipped, {k}: {v}")
for k in ["no-signal", "changed", "changed: different SET in top 5", "changed: different #1", "changed: rounding-sensitive",
          "unchanged", "unchanged: rounding-sensitive", "undetermined", "undetermined: rounding-sensitive"]:
    print(f"{k}: {summary[k]}")
sig = [d for d in detail if d["signal"]]
print(f"with churn signal: {len(sig)}")
print("with signal, top-5 rows carrying a lift (distribution):", dict(sorted(Counter(d['lifted_in_top5'] for d in sig).items())))
print("completed range:", min(d["completed"] for d in detail), "..", max(d["completed"] for d in detail))
# recent window: runs completed in the last 30 days
recent = [d for d in detail if d["completed"] >= "2026-09-25"]
c = Counter(d["outcome"] for d in recent)
print(f"recent (completed >= 2026-09-25): {len(recent)} repos -> {dict(c)}; set differs {sum(d['set_differs'] for d in recent)}, #1 differs {sum(d['first_differs'] for d in recent)}")
print("by engine:")
for eng, n in Counter(d["engine"] for d in detail).most_common(8):
    sub = [d for d in detail if d["engine"] == eng]
    print(f"  {eng or '(none)'}: {n} -> {dict(Counter(d['outcome'] for d in sub))}")
print("robust classification of repos with a lifted task in the served 8:")
for k, v in robust.items():
    print(f"  {k}: {v}")
json.dump(detail, open(sys.argv[2], "w"), indent=0)
