import pandas as pd
import requests
from scholarly import scholarly
from Bio import Entrez

Entrez.email = "seu-email@exemplo.com"  # necessário para usar a API do PubMed

# ----------------------------
# PubMed via Entrez
# ----------------------------

def buscar_artigos_pubmed(tema, max_results=5):
    handle = Entrez.esearch(db="pubmed", term=tema, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]

    artigos = []
    if ids:
        summaries = Entrez.esummary(db="pubmed", id=",".join(ids))
        results = Entrez.read(summaries)
        for r in results:
            artigos.append({
                "Título": r.get("Title"),
                "Autores": r.get("AuthorList", ["Desconhecido"]),
                "Ano": r.get("PubDate", "N/A")[:4],
                "Fonte": "PubMed"
            })
    return pd.DataFrame(artigos)

# ----------------------------
# PatentsView API
# ----------------------------

def buscar_patentes(tema, max_results=5):
    url = "https://api.patentsview.org/patents/query"
    query = {
        "q": {"_text_any": {"patent_title": tema}},
        "f": ["patent_title", "patent_number", "patent_date"],
        "o": {"per_page": max_results}
    }
    response = requests.post(url, json=query)
    data = response.json()

    patentes = []
    for p in data.get("patents", []):
        patentes.append({
            "Título da Patente": p["patent_title"],
            "Número": p["patent_number"],
            "Ano": p["patent_date"][:4],
            "Fonte": "PatentsView"
        })
    return pd.DataFrame(patentes)

# ----------------------------
# Google Scholar via scholarly
# ----------------------------

def buscar_google_scholar(tema, max_results=5):
    search_query = scholarly.search_pubs(tema)
    artigos = []
    for i in range(max_results):
        try:
            result = next(search_query)
            artigos.append({
                "Título": result.get("bib", {}).get("title"),
                "Autores": result.get("bib", {}).get("author"),
                "Ano": result.get("bib", {}).get("pub_year"),
                "Fonte": "Google Scholar"
            })
        except StopIteration:
            break
    return pd.DataFrame(artigos)

# ----------------------------
# Dados Públicos via GitHub
# ----------------------------

def carregar_dados_publicos():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df = df[["location", "date", "new_cases", "new_deaths"]]
    df["date"] = pd.to_datetime(df["date"])
    return df