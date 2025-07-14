import requests
from bs4 import BeautifulSoup

GOOGLE_SCHOLAR_URL = "https://scholar.google.com/citations?user=7ICz8uAAAAAJ&hl=en"
README_PATH = "README.md"
START_TAG = "<!--START_PUBS-->"
END_TAG = "<!--END_PUBS-->"

def fetch_publications():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(GOOGLE_SCHOLAR_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.select(".gsc_a_t a")
    years = soup.select(".gsc_a_y span")
    links = ["https://scholar.google.com" + a['href'] for a in titles]

    pubs = []
    for title, link, year in zip(titles, links, years):
        pubs.append(f"* [{title.text}]({link}) `{year.text}`")
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
