import typer
from typing import Optional
from pubmed_fetcher.core import fetch_paper_ids, fetch_paper_details, save_to_csv

app = typer.Typer()

@app.command()
def get_papers_list(query: str, file: Optional[str] = None, debug: bool = False):
    """
    Command-line interface to fetch and save research papers based on a query.
    """
    if debug:
        typer.echo("Debug mode enabled")
        typer.echo(f"Query: {query}")
        typer.echo(f"File: {file}")
        typer.echo(f"Debug: {debug}")

    typer.echo(f"Fetching papers for query: {query}")
    paper_ids = fetch_paper_ids(query)
    papers = fetch_paper_details(paper_ids)

    if file:
        save_to_csv(papers, file)
    else:
        for paper in papers:
            typer.echo(paper)

if __name__ == "__main__":
    app()