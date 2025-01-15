import requests
import pandas as pd
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

# Base URLs for PubMed API
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_paper_ids(query: str, max_results: int = 10) -> List[str]:
    """Fetch paper IDs from PubMed based on a query."""
    try:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        response = requests.get(PUBMED_SEARCH_URL, params=params)
        response.raise_for_status()
        return response.json()["esearchresult"]["idlist"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper IDs: {e}")
        return []

def fetch_paper_details(paper_ids: List[str]) -> List[Dict[str, Optional[str]]]:
    """Fetch detailed paper information from PubMed."""
    if not paper_ids:
        print("No paper IDs provided.")
        return []

    try:
        params = {
            "db": "pubmed",
            "id": ",".join(paper_ids),
            "retmode": "xml"
        }
        response = requests.get(PUBMED_FETCH_URL, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        papers = []

        for article in root.findall(".//PubmedArticle"):
            pubmed_id = article.find(".//PMID").text
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
            pub_date = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "N/A"

            authors = article.findall(".//Author")
            non_academic_authors = []
            company_affiliations = []
            corresponding_email = "N/A"

            for author in authors:
                affiliation = author.find(".//AffiliationInfo/Affiliation")
                if affiliation is not None:
                    affiliation_text = affiliation.text.lower()
                    if any(keyword in affiliation_text for keyword in ["pharmaceutical", "biotech", "company", "corporation"]):
                        last_name = author.find("LastName")
                        if last_name is not None:
                            non_academic_authors.append(last_name.text)
                        company_affiliations.append(affiliation.text)

                    if "corresponding" in affiliation_text and "email" in affiliation_text:
                        corresponding_email = affiliation_text.split("email:")[1].strip()

            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
                "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
                "Corresponding Author Email": corresponding_email
            })

        return papers
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper details: {e}")
        return []

def save_to_csv(papers: List[Dict[str, Optional[str]]], filename: str) -> None:
    """Save a list of papers to a CSV file."""
    if papers:
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")
    else:
        print("No papers to save.")
