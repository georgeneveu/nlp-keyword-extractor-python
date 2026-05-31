# NLP Keyword Extractor Python
	
Extract keywords from text with python NLP. This scirpt extracts key entities and keyword phrases from web pages. It scrapes a given URL, cleans HTML content, applies spaCy NLP for named entity recognition and noun phrase extraction, filters noise, and returns structured insights for SEO, content analysis, and topic discovery.

## 🚀 Features

- Scrapes content from any given URL
- Removes navigation, ads, and irrelevant HTML elements
- Extracts named entities (PERSON, ORG, GPE)
- Generates keyword phrases using noun chunks
- Filters noise and duplicates
- Returns structured insights from raw web content

## 🧠 How It Works

1. Fetches HTML content from a target URL
2. Parses page using BeautifulSoup
3. Removes scripts, headers, footers, and sidebars
4. Detects main content block
5. Processes text with spaCy NLP model
6. Extracts:
   - Named Entities
   - Repeated keyword phrases (noun chunks)
7. Outputs clean lists of insights

## 📦 Requirements

Install dependencies:

```bash
pip install requests beautifulsoup4 spacy
````

Download spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

## ▶️ Usage

Run the script:

```bash
python main.py
```

Make sure to update the URL inside the script:

```python
URL = "https://example.com"
```

## 📊 Output Example

```
=== ENTITIES ===
Google
New York
John Smith

=== KEY PHRASES ===
cause and effect essays
academic writing structure
essay examples
```

## ⚙️ Configuration

You can customize:

* `URL` → target webpage
* `ALLOWED_LABELS` → entity types to extract
* `bad_phrases` → noise filtering rules
* keyword frequency threshold

## 🧩 Use Cases

* SEO content analysis
* Keyword research
* Topic clustering
* Competitive content analysis
* NLP learning projects

## 📌 Notes

* This is a heuristic-based extractor (not a full crawler or SEO suite)
* Works best on long-form article pages
* Some websites may block scraping

Built for NLP-based web content extraction and SEO analysis.

