# Project Report: PubMed Fetcher

## **1. Project Overview**
The PubMed Fetcher is a Python-based command-line tool that fetches research papers from the PubMed API based on user queries. The tool filters papers with authors affiliated with pharmaceutical or biotech companies and outputs the results in a CSV file. The project is organized using a modular approach and utilizes Poetry for dependency management.

---

## **2. Project Structure**
The project is divided into two main components:

- **`core.py`**: Contains the core logic for interacting with the PubMed API, fetching paper IDs and details, processing author information, and saving results to a CSV file.
- **`cli.py`**: Implements a command-line interface using Typer to interact with users and call the core functions.

### **File Structure:**
```
├── cli.py                # Command-line interface
├── core.py               # Core functionality
├── README.md             # Project documentation
└── pyproject.toml        # Poetry configuration file
```

---

## **3. Methodology**
### **Step 1: Fetching Paper IDs**
The function `fetch_paper_ids` in `core.py` sends a query to the PubMed API's `esearch` endpoint to retrieve paper IDs based on a user-specified search term.

#### **API Endpoint Used:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```
#### **Key Parameters:**
- `db`: Specifies the PubMed database.
- `term`: User's search query.
- `retmax`: Maximum number of results to return.

#### **Function Code:**
```python
params = {
    "db": "pubmed",
    "term": query,
    "retmax": max_results,
    "retmode": "json"
}
response = requests.get(PUBMED_SEARCH_URL, params=params)
```

### **Step 2: Fetching Paper Details**
The function `fetch_paper_details` retrieves detailed information for each paper ID from the PubMed API's `efetch` endpoint.

#### **API Endpoint Used:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```
#### **Function Code:**
```python
params = {
    "db": "pubmed",
    "id": ",".join(paper_ids),
    "retmode": "xml"
}
response = requests.get(PUBMED_FETCH_URL, params=params)
```

### **Step 3: Processing Author Information**
The tool processes the XML response to extract relevant details about each paper, including:
- **PubMed ID**
- **Title**
- **Publication Date**
- **Non-academic Author(s)**
- **Company Affiliation(s)**
- **Corresponding Author Email**

The tool identifies non-academic authors by checking for affiliations containing keywords such as "pharmaceutical," "biotech," "company," or "corporation."

### **Step 4: Saving Results to a CSV File**
The `save_to_csv` function saves the extracted paper details to a CSV file using pandas.

#### **Function Code:**
```python
df = pd.DataFrame(papers)
df.to_csv(filename, index=False)
print(f"Results saved to {filename}")
```

---

## **4. Command-Line Interface (CLI)**
The `cli.py` file provides a command-line interface using Typer. The CLI accepts user queries and options to fetch and save research papers.

### **CLI Options:**
- **`query`**: Required argument for the search term.
- **`--file`**: Optional argument to specify the output CSV filename.
- **`--debug`**: Optional flag to enable debug mode.

#### **Example Usage:**
```bash
poetry run get-papers-list "cancer treatment" --file output.csv --debug
```

---

## **5. Tools and Libraries Used**
- **Requests**: For making HTTP requests to the PubMed API.
- **Pandas**: For handling data and exporting to CSV.
- **Typer**: For creating the command-line interface.
- **Poetry**: For dependency management and packaging.

---

## **6. Results**
The tool successfully fetches research papers from PubMed, processes author information, and filters papers with authors affiliated with pharmaceutical or biotech companies. The results are saved in a CSV file with the following columns:

| PubmedID | Title | Publication Date | Non-academic Author(s) | Company Affiliation(s) | Corresponding Author Email |
|----------|-------|------------------|------------------------|------------------------|----------------------------|
| 12345678 | Example Title | 2025 | John Doe | Pharma Corp | john.doe@pharma.com |

---

## **7. How to Run the Program Using the CLI**
### **Prerequisites**
- Python 3.8 or higher
- Poetry installed on your system

### **Steps to Run the Program**
1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

3. **Run the program using the command-line interface**
   ```bash
   poetry run get-papers-list "<query>" --file <output_file.csv>
   ```

   Replace `<query>` with your search term and `<output_file.csv>` with your desired output file name.

#### **Example Commands**
- To fetch papers related to "cancer treatment" and save the results to `output.csv`:
   ```bash
   poetry run get-papers-list "cancer treatment" --file output.csv
   ```

- To enable debug mode and see detailed execution logs:
   ```bash
   poetry run get-papers-list "cancer treatment" --file output.csv --debug
   ```

4. **View the results**
   Open the generated CSV file (`output.csv`) to view the list of research papers, including PubMed ID, title, publication date, non-academic authors, company affiliations, and corresponding author emails.

---

## **8. Challenges and Solutions**
**Challenge 1:** Handling API errors and empty responses.  
**Solution:** Implemented error handling using try-except blocks to catch request exceptions.

**Challenge 2:** Identifying non-academic authors.  
**Solution:** Used a heuristic approach to filter affiliations based on specific keywords.

---

## **9. Conclusion**
The PubMed Fetcher project demonstrates how to build a Python-based command-line tool for interacting with an external API. It showcases key skills in API integration, data processing, CLI development, and packaging using Poetry.

By following a structured approach, the project achieves the objective of fetching research papers from PubMed and filtering them based on author affiliations.

**Next Steps:**
- Publish the package on Test PyPI for further testing.
- Enhance the filtering logic to improve accuracy.
- Add more unit tests to ensure code robustness.

