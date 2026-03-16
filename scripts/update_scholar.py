import json
from pathlib import Path
from urllib.request import urlopen

SCHOLAR_JSON_URL = (
    "https://cdn.jsdelivr.net/gh/Bowen12137/Bowen12137.github.io@google-scholar-stats/gs_data.json"
)
README_PATH = Path(__file__).resolve().parent.parent / "README.md"
START_TAG = "<!--START_PUBS-->"
END_TAG = "<!--END_PUBS-->"
MAX_PUBLICATIONS = 5


def fetch_publications():
    print(f"[INFO] Fetching citation data from {SCHOLAR_JSON_URL}...")
    with urlopen(SCHOLAR_JSON_URL, timeout=30) as response:
        data = json.load(response)

    publications = list((data.get("publications") or {}).values())
    publications.sort(
        key=lambda pub: (
            int(pub.get("num_citations", 0) or 0),
            int((pub.get("bib") or {}).get("pub_year", 0) or 0),
        ),
        reverse=True,
    )

    pubs = []
    author_id = data.get("scholar_id", "7ICz8uAAAAAJ")
    for pub in publications[:MAX_PUBLICATIONS]:
        bib = pub.get("bib") or {}
        title = bib.get("title", "Untitled")
        year = bib.get("pub_year", "n/a")
        venue = bib.get("citation") or bib.get("venue") or "Unknown Venue"
        citations = pub.get("num_citations", 0)
        paper_id = pub.get("author_pub_id", "")
        pub_url = pub.get("pub_url") or (
            f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={author_id}&citation_for_view={paper_id}"
            if paper_id
            else "#"
        )
        cited_url = pub.get("citedby_url") or "#"
        if cited_url.startswith("/"):
            cited_url = f"https://scholar.google.com{cited_url}"

        markdown_block = (
            f"🎉🎉* **[{title}]({pub_url})**  \n"
            f"  _{year} · {venue}_  \n"
            f"  [Scholar]({pub_url}) · [Citations]({cited_url}) `{citations}`"
        )
        pubs.append(markdown_block)

    if not pubs:
        raise RuntimeError("[ERROR] No publications found in scholar data.")

    print("[INFO] Publications fetched:")
    for p in pubs:
        print("  -", p.splitlines()[0])
    return pubs


def update_readme(pubs):
    content = README_PATH.read_text(encoding="utf-8")
    start = content.find(START_TAG)
    end = content.find(END_TAG)
    if start == -1 or end == -1:
        raise RuntimeError("START_PUBS or END_PUBS tag not found in README.md")

    new_content = (
        content[: start + len(START_TAG)]
        + "\n"
        + "\n\n".join(pubs)
        + "\n"
        + content[end:]
    )
    README_PATH.write_text(new_content, encoding="utf-8")
    print("[INFO] README.md updated successfully.")


if __name__ == "__main__":
    update_readme(fetch_publications())
