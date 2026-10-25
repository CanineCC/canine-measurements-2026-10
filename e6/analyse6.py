#!/usr/bin/env python3
"""WP-40 §E6 analysis, exactly as frozen (tag wp40-e5-freeze, amendments 1-2).

Primary: held-and-behaviour-passed rate, G minus U, 95 % bootstrap over METHODS.
Secondary: tokens G/U (geometric mean of per-method ratios); target complexity after; change in total
complexity of the touched files; cost and wall time. Runs whose gate could not judge (baseline_failing,
gate error, missing gate.json) are excluded from the rates and COUNTED.

Usage: analyse6.py [runs_dir]   (default: runs/main next to this file). Writes results6.json beside it.
"""
import json, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "runs" / "main"
JUDGED = {"held", "did_not_clear", "moved", "build_failed", "target_missing", "no_change"}
SEED, B = 20261025, 10000


def load():
    runs, excluded = [], defaultdict(int)
    for d in sorted(p for p in RUNS.iterdir() if p.is_dir()):
        mid, arm, rep = d.name.split("-")
        gate_path, metrics_path = d / "gate.json", d / "metrics.json"
        if not gate_path.exists():
            excluded["no gate.json"] += 1
            continue
        gate = json.loads(gate_path.read_text())
        outcome = gate.get("outcome")
        if outcome not in JUDGED:
            excluded[str(outcome)] += 1
            continue
        metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
        wall = d / "wall-seconds.txt"
        runs.append({
            "mid": mid, "arm": arm, "rep": int(rep), "outcome": outcome,
            "behaviour": gate.get("behaviour"),
            "success": outcome == "held" and gate.get("behaviour") == "passed",
            "target_after": gate.get("target_cognitive_after"),
            "touched_delta": (gate["touched_total_cognitive_after"] - gate["touched_total_cognitive_before"])
            if gate.get("touched_total_cognitive_after") is not None and gate.get("touched_total_cognitive_before") is not None
            else None,
            "tokens": metrics.get("total_tokens"), "cost": metrics.get("cost_usd"),
            "wall": float(wall.read_text().strip()) if wall.exists() else None,
        })
    return runs, dict(excluded)


def per_method(runs, key, agg=statistics.mean):
    out = defaultdict(dict)
    for (mid, arm) in {(r["mid"], r["arm"]) for r in runs}:
        vals = [r[key] for r in runs if r["mid"] == mid and r["arm"] == arm and r[key] is not None]
        if vals:
            out[mid][arm] = agg(vals)
    return out


def bootstrap(mids, stat):
    rng = random.Random(SEED)
    draws = sorted(stat([rng.choice(mids) for _ in mids]) for _ in range(B))
    return draws[int(0.025 * B)], draws[int(0.975 * B) - 1]


def main():
    runs, excluded = load()
    rates = per_method(runs, "success")
    both = sorted(m for m, a in rates.items() if "G" in a and "U" in a)
    diff = lambda ms: statistics.mean(rates[m]["G"] - rates[m]["U"] for m in ms)
    primary = diff(both)
    lo, hi = bootstrap(both, diff)

    toks = per_method(runs, "tokens")
    tok_mids = sorted(m for m, a in toks.items() if "G" in a and "U" in a and a["U"] > 0)
    geo = lambda ms: math.exp(statistics.mean(math.log(toks[m]["G"] / toks[m]["U"]) for m in ms))
    tlo, thi = bootstrap(tok_mids, geo)

    by_arm = lambda key, arm: [r[key] for r in runs if r["arm"] == arm and r[key] is not None]
    outcomes = {arm: {o: sum(1 for r in runs if r["arm"] == arm and r["outcome"] == o) for o in sorted(JUDGED)}
                for arm in ("G", "U")}
    behaviour_failed = {arm: sum(1 for r in runs if r["arm"] == arm and r["behaviour"] == "failed") for arm in ("G", "U")}
    result = {
        "runs_judged": len(runs), "excluded": excluded, "methods_with_both_arms": len(both),
        "rate": {arm: statistics.mean(r["success"] for r in runs if r["arm"] == arm) for arm in ("G", "U")},
        "primary_G_minus_U": primary, "primary_ci95": [lo, hi], "loss_condition_fires": lo <= 0 <= hi,
        "tokens_G_over_U_geomean": geo(tok_mids), "tokens_ci95": [tlo, thi], "token_methods": len(tok_mids),
        "outcomes": outcomes, "behaviour_failed": behaviour_failed,
        "target_after_median": {arm: statistics.median(by_arm("target_after", arm)) for arm in ("G", "U")},
        "touched_delta_median": {arm: statistics.median(by_arm("touched_delta", arm)) for arm in ("G", "U")},
        "cost_usd_total": {arm: sum(by_arm("cost", arm)) for arm in ("G", "U")},
        "wall_median_s": {arm: statistics.median(by_arm("wall", arm)) for arm in ("G", "U")},
        "per_method_rate": {m: rates[m] for m in both},
    }
    (HERE / "results6.json").write_text(json.dumps(result, indent=1))
    print(json.dumps({k: v for k, v in result.items() if k != "per_method_rate"}, indent=1))


if __name__ == "__main__":
    main()
