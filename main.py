import requests
from bs4 import BeautifulSoup
import spacy
import re
from collections import Counter

# ------------------------
# CONFIG
# ------------------------
URL = "https://www.grammarly.com/blog/academic-writing/cause-and-effect-essay/"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Helps avoid basic bot blocking

# ------------------------
# LOAD SPACY MODEL
# ------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # Better practice: specify exact error + exit cleanly
    print("❌ Install model first: python -m spacy download en_core_web_sm")
    exit()

# ------------------------
# FETCH PAGE
# ------------------------
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# ------------------------
# REMOVE UNNECESSARY ELEMENTS
# (navigation, ads, scripts, layout noise)
# ------------------------
for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
    tag.decompose()

# ------------------------
# FIND MAIN CONTENT BLOCK
# heuristic: choose largest text-heavy container
# ------------------------
def find_main_content(soup):
    candidates = []

    for div in soup.find_all(["article", "main", "section", "div"]):
        text = div.get_text(" ", strip=True)

        # Skip very small blocks (likely irrelevant)
        if len(text) < 1000:
            continue

        # Skip navigation-like blocks (too many links)
        if len(div.find_all("a")) > 50:
            continue

        candidates.append((len(text), div))

    if not candidates:
        return None

    # return largest text block
    return max(candidates, key=lambda x: x[0])[1]

content = find_main_content(soup)

if not content:
    raise Exception("❌ Content not found")

# ------------------------
# CLEAN TEXT FUNCTION
# ------------------------
def clean_text(text):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ------------------------
# NOISE FILTER
# ------------------------
def is_noise(text):
    bad_phrases = [
        "table of contents",
        "skip to content",
        "toggle",
        "related posts",
        "advertisement",
        "subscribe",
        "cookie",
        "privacy policy"
    ]
    text = text.lower()
    return any(p in text for p in bad_phrases)

# ------------------------
# NLP EXTRACTION
# ------------------------
ALLOWED_LABELS = {"PERSON", "ORG", "GPE"}

entities = []
keywords = []

# Extract from headings, paragraphs, and list items
for el in content.find_all(["h1", "h2", "h3", "p", "li"]):
    text = clean_text(el.get_text())

    if not text or is_noise(text):
        continue

    doc = nlp(text)

    # -------- Named Entity Recognition --------
    for ent in doc.ents:
        if ent.label_ in ALLOWED_LABELS and len(ent.text) > 3:
            entities.append(ent.text.strip())

    # -------- Keyword extraction (noun chunks) --------
    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower().strip()

        # Filter low-quality phrases
        if (
            len(phrase) > 4
            and not phrase.isdigit()
            and not phrase.startswith(("this", "that", "these", "those"))
        ):
            keywords.append(phrase)

# ------------------------
# DEDUPLICATION + SCORING
# ------------------------
entities = sorted(set(entities))

keyword_counts = Counter(keywords)

# Keep only repeated phrases (signal boost)
top_keywords = [
    kw for kw, count in keyword_counts.items() if count >= 2
]

# ------------------------
# OUTPUT
# ------------------------
print("\n=== ENTITIES ===")
for e in entities:
    print(e)

print("\n=== KEY PHRASES ===")
for kw in sorted(top_keywords):
    print(kw)
