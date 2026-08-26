# -*- coding: utf-8 -*-
"""Exploration Wikidata : que contient reellement la base sur les motos ?"""
import requests, json, sys

ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "MotoDirectoryResearch/0.1 (contact: viktordu84@gmail.com)",
    "Accept": "application/sparql-results+json",
}

def q(query, timeout=120):
    r = requests.get(ENDPOINT, params={"query": query, "format": "json"},
                     headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.json()["results"]["bindings"]

# 1) Combien d'items sont des motos (instance of / subclass of motorcycle Q34493) ?
count_q = """
SELECT (COUNT(DISTINCT ?m) AS ?n) WHERE {
  ?m wdt:P31/wdt:P279* wd:Q34493 .
}
"""
try:
    res = q(count_q)
    print("MOTOS (P31/P279* Q34493) :", res[0]["n"]["value"])
except Exception as e:
    print("ERREUR count:", e, file=sys.stderr)
    sys.exit(1)

# 2) Quelles proprietes sont les plus utilisees sur ces items ?
props_q = """
SELECT ?p ?pLabel (COUNT(*) AS ?n) WHERE {
  ?m wdt:P31/wdt:P279* wd:Q34493 .
  ?m ?prop ?v .
  ?p wikibase:directClaim ?prop .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
}
GROUP BY ?p ?pLabel
ORDER BY DESC(?n)
LIMIT 45
"""
print("\n=== PROPRIETES LES PLUS PRESENTES ===")
for b in q(props_q, timeout=180):
    pid = b["p"]["value"].rsplit("/", 1)[-1]
    print(f'{b["n"]["value"]:>7}  {pid:<8} {b["pLabel"]["value"]}')
