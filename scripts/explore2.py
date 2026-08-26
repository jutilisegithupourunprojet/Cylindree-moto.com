# -*- coding: utf-8 -*-
import requests, sys
ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)",
           "Accept": "application/sparql-results+json"}
def q(query, timeout=180):
    r = requests.get(ENDPOINT, params={"query": query, "format": "json"},
                     headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.json()["results"]["bindings"]

# A) Chercher toutes les classes dont le libelle evoque la moto
print("=== CLASSES 'moto' / 'motorcycle' ===")
cls = """
SELECT ?c ?cLabel (COUNT(DISTINCT ?i) AS ?n) WHERE {
  ?c rdfs:label ?l .
  FILTER(LANG(?l)="en" && (CONTAINS(LCASE(?l),"motorcycle") || CONTAINS(LCASE(?l),"moped") || CONTAINS(LCASE(?l),"scooter")))
  ?i wdt:P31 ?c .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?c ?cLabel HAVING(COUNT(DISTINCT ?i) > 3) ORDER BY DESC(?n) LIMIT 25
"""
try:
    for b in q(cls):
        print(f'{b["n"]["value"]:>7}  {b["c"]["value"].rsplit("/",1)[-1]:<10} {b["cLabel"]["value"]}')
except Exception as e:
    print("ERR A:", e, file=sys.stderr)

# B) Combien d'items ont un constructeur moto connu comme fabricant ?
print("\n=== ITEMS PAR CONSTRUCTEUR MOTO (tous types confondus) ===")
mk = """
SELECT ?mLabel (COUNT(DISTINCT ?i) AS ?n) WHERE {
  VALUES ?m { wd:Q9584 wd:Q188418 wd:Q181642 wd:Q6746 wd:Q26678 wd:Q37156
              wd:Q42278 wd:Q170243 wd:Q49984 wd:Q219216 wd:Q698292 }
  ?i wdt:P176 ?m .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?mLabel ORDER BY DESC(?n) LIMIT 20
"""
try:
    for b in q(mk):
        print(f'{b["n"]["value"]:>7}  {b["mLabel"]["value"]}')
except Exception as e:
    print("ERR B:", e, file=sys.stderr)
