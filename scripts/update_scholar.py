import requests
import os

# ====== 配置 ======
API_KEY = os.getenv("SERP_API_KEY", "MISSING_KEY")

SCHOLAR_ID = "7ICz8uAAAAAJ"
README_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))

START_TAG = "<!--START_PUBS-->"
END_TAG = "<!--END_PUBS-->"


# ====== 获取 publication ======
def fetch_publications():
    params = {
        "api_key": API_KEY,
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "num": 5
    }

    print("[INFO] Fetching publications from SerpAPI...")
    res = requests.get("https://serpapi.com/search", params=params)

    if res.status_code != 200:
        raise Exception(f"[ERROR] Failed to fetch data: {res.status_code} {res.text}")

    data = res.json()
    pubs = []

    for article in data.get("articles", []):
        title = article.get("title")
        link = article.get("link")
        year = article.get("year", "n/a")
        venue = article.get("publication") or "Unknown Venue"
        cited_info = article.get("cited_by", {})
        cited_num = cited_info.get("value", 0)
        cited_link = cited_info.get("link", "#")

        markdown_block = (
            f"🎉🎉* **[{title}]({link})**  \n"
            f"  _{year} · {venue}_  \n"
            f"  [PDF]({link}) · [Citations]({cited_link}) `{cited_num}`"
        )
        pubs.append(markdown_block)


    if not pubs:
        print("[WARNING] No publications found.")
    else:
        print("[INFO] Publications fetched:")
        for p in pubs:
            print("  -", p.splitlines()[0])

    return pubs


# ====== 更新 README.md ======
def update_readme(pubs):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_TAG)
    end = content.find(END_TAG)
    if start == -1 or end == -1:
        raise Exception("❌ START_PUBS or END_PUBS tag not found in README.md")

    new_content = (
        content[:start + len(START_TAG)] + "\n" +
        "\n\n".join(pubs) + "\n" +
        content[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("[INFO] README.md updated successfully.")


# ====== 主函数入口 ======
if __name__ == "__main__":
    pubs = fetch_publications()
    update_readme(pubs)
