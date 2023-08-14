"""Scrape text data from various web sources to create data objects for future ingestion into Weaviate."""

import json

import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    # -------------------
    # | Parse fan wikis |
    # -------------------
    bear_wiki_info = []

<<<<<<< HEAD
    with open("data/data_sources/wiki_links.txt", "r") as f:
=======
    with open("../data/data_sources/wiki_links.txt", "r") as f:
>>>>>>> main
        for url in f:
            url = url.strip()
            page = requests.get(url)  # add error handling here
            soup = BeautifulSoup(page.content, "lxml")

            # ________
            # | Text |
            # --------
            full_title = soup.title.text
            bear_id = full_title.split("|")[0].strip()
            body_text = soup.findAll(
                "p"
            )
            body_text = [
                b.text.replace("\n", "").replace("\xa0", "") for b in body_text
            ]
            body_text = [b for b in body_text if not b == ""]
            body_text = " ".join(body_text)
            bear_wiki_info.append({"name": bear_id, "bio": body_text})

    with open(
<<<<<<< HEAD
            "data/scraped_data/bear_wiki_info.json", mode="w", encoding="utf-8"
=======
            "../data/scraped_data/bear_wiki_info.json", mode="w", encoding="utf-8"
>>>>>>> main
    ) as json_file:
        json.dump(bear_wiki_info, json_file)
