import requests
from bs4 import BeautifulSoup

GOOGLE_SCHOLAR_URL = "https://scholar.google.com/citations?user=7ICz8uAAAAAJ&hl=en"
README_PATH = "README.md"
START_TAG = "<!--START_PUBS-->"
END_TAG = "<!--END_PUBS-->"

def fetch_publications():
    response = requests.get(GOOGLE_SCHOLAR_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select(".gsc_a_t a")
    links = ["https://scholar.google.com" + a['href'] for a in titles]
    pubs = []
    for a, link in zip(titles, links):
        title = a.get_text()
        pubs.append(f"* [{title}]({link})")
    return pubs[:5]  # Top 5

def update_readme(pubs):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_TAG)
    end = content.find(END_TAG)
    if start == -1 or end == -1:
        raise Exception("Start or end tag not found in README.md")

    new_content = (
        content[:start + len(START_TAG)] + "\n" +
        "\n".join(pubs) + "\n" +
        content[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    pubs = fetch_publications()
    update_readme(pubs)
