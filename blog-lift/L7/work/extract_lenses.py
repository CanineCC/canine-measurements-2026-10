# Reads a saved CAI survey page and writes a thin evidence bundle from the numbers the page itself publishes:
# the eight lens scores (cai-lens-gauges), the headline (cai-band-scale), the commit and rubric version (About this page).
import sys, re, json, html
page = open(sys.argv[1], encoding="utf-8").read()
keys = {"Code Health": "codeHealth", "Architecture": "architecture", "Maturity": "maturity",
        "Production-Readiness": "productionReadiness", "Security & Compliance": "securityCompliance",
        "Domain Modelling": "domainModelling", "Event-Driven": "eventDriven", "Event Sourcing": "eventSourcing",
        "Accessibility": "accessibility", "Performance": "performance"}
lenses = json.loads(html.unescape(re.search(r'<cai-lens-gauges[^>]*\slenses="([^"]*)"', page).group(1)))
headline = float(re.search(r'<cai-band-scale[^>]*\sscore="([0-9.]+)"', page).group(1))
text = html.unescape(re.sub(r"<[^>]+>", " ", page))
commit = re.search(r"Measured at commit ([0-9a-f]{40})", text).group(1)
rubric = re.search(r"Scored under (rubric-[0-9.]+)", text).group(1)
bundle = {"rubricVersion": rubric, "commit": commit, "headlineScore": headline,
          "lenses": [{"lens": keys[l["label"]], "score": l["value"], "owaWeight": 0} for l in lenses]}
json.dump(bundle, open(sys.argv[2], "w"), indent=2)
print(json.dumps(bundle, indent=2))
