import json

import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    # -------------------
    # | Parse fan wikis |
    # -------------------
    bear_wiki_info = []

    with open("../data/data_sources/wiki_links.txt", "r") as f:
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
            )  # still tons of HTML tags left in here. No super easy way to clean up.
            body_text = [
                b.text.replace("\n", "").replace("\xa0", "") for b in body_text
            ]
            body_text = [b for b in body_text if not b == ""]
            body_text = " ".join(body_text)
            bear_wiki_info.append({"name": bear_id, "bio": body_text})

    with open(
            "../data/scraped_data/bear_wiki_info.json", mode="w", encoding="utf-8"
    ) as json_file:
        json.dump(bear_wiki_info, json_file)


""" 
NOTES:
    - Some wiki URLs contained forward slashes in them, so Python thought they were paths & couldn't retrieve the 
    images (e.g. https://katmai-bearcams.fandom.com/wiki/902_%22Fifi%22_/_%22Bonsai%22)
    
"""
