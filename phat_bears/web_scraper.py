import json
import os
import time
import urllib.request
from urllib.error import URLError

# import timer as timer
from PIL import Image

from llama_index import download_loader
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ocrmypdf
from langchain.document_loaders import PyPDFLoader


if __name__ == "__main__":
    # -----------------------------------------
    # | Parse official 2022 PDF (extract text)|
    # -----------------------------------------
    if not os.path.exists("../data_sources/bears_of_brooks_river_2022.pdf"):
        url = "https://irma.nps.gov/DataStore/DownloadFile/671923"

        # download locally:
        urlretrieve(url, "../data_sources/bears_of_brooks_river_2022.pdf")

        # ocr content:
        ocrmypdf.ocr(
            "../data_sources/bears_of_brooks_river_2022.pdf",
            "../data_sources/bears_of_brooks_river_2022_ocred.pdf",
            force_ocr=True,
            output_type="pdf",
            progress_bar=True,
        )

    # Load OCRed PDF
    pdf = PyPDFLoader("../data_sources/bears_of_brooks_river_2022_ocred.pdf").load()

    pages_of_general_info = pdf[4:28] + [pdf[34]]
    cleaned_pages_of_general_info = [
        page.page_content.replace("\n", "") for page in pages_of_general_info
    ]
    with open(
        "../scraped_data/general_park_info.json", mode="w", encoding="utf-8"
    ) as json_file:
        json.dump(cleaned_pages_of_general_info, json_file)

    # Not dealing with this for now.... too complicated to match w/the wiki info; might do later
    # pages_of_adult_bear_bios = pdf[35:88]
    # cleaned_pages_of_adult_bear_bios = [page.page_content.replace('\n', '') for page in pages_of_adult_bear_bios]
    # # Grab only the entries that are for particular bears:
    # identified_bears = [p for p in cleaned_pages_of_adult_bear_bios if p[:2].isdigit()]

    # -------------------
    # | Parse fan wikis |
    # -------------------
    bear_wiki_info = []

    with open("../data_sources/wiki_links.txt", "r") as f:
        for url in f:
            url = url.strip()
            page = requests.get(url)  # add error handling here
            soup = BeautifulSoup(page.content, "lxml")

            # ________
            # | Text |
            # --------
            full_title = soup.title.text
            bear_id = full_title.split("|")[0].strip()
            # body_text = soup.findAll('p')  # still tons of HTML tags left in here. No super easy way to clean up.
            # body_text = [b.text.replace('\n', '').replace('\xa0', '') for b in body_text]
            # body_text = [b for b in body_text if not b == '']
            # body_text = ' '.join(body_text)  # might have to chunk up to ingest into weaviate, but not sure where
            # # should do it
            # bear_wiki_info.append({'id': bear_id, 'body': body_text})

            # ----------
            # | Images |
            # ----------
            image_counter = 0
            for link in soup.select("img[src^=http]"):
                # todo: repopulate whole folder tomo & reindex
                if image_counter <= 40:
                    lnk = link["src"]
                    try:
                        urllib.request.urlretrieve(
                            lnk,
                            f"../scraped_data/bear_wiki_images"
                            f"/{bear_id.replace(' ', '')}_{image_counter}.jpg",
                        )
                        image_counter += 1

                    except URLError:
                        time.sleep(3)
                        urllib.request.urlretrieve(
                            lnk,
                            f"../scraped_data/bear_wiki_images"
                            f"/{bear_id.replace(' ', '')}_{image_counter}.jpg",
                        )
                        image_counter += 1

    with open(
        "../scraped_data/bear_wiki_info.json", mode="w", encoding="utf-8"
    ) as json_file:
        json.dump(bear_wiki_info, json_file)


""" 
NOTES:
    - OCRing didn't get all data. For instance, it didn't get Bear 261 or the info pg about male bears from the 2022 
    PDF booklet
    - There are *a lot* of bear_wiki_images in the wiki pages... takes a long time to download them all; should optimize
    - Some wiki URLs contained foward slashes in them, so Python thought they were paths & couldn't retrieve the 
    images (e.g. https://katmai-bearcams.fandom.com/wiki/902_%22Fifi%22_/_%22Bonsai%22)
    
"""

# IMAGES:
"""
import urllib.request
from PIL import Image

# GET LINKS FOR IMAGES:
for link in soup.select("img[src^=http]"):
lnk = link["src"]

# TEST LINK:
url = 'https://static.wikia.nocookie.net/katmai-bearcams/images/5/5c/DIVER_1_PIC_YEAR_UNKNOWN_KNP%26P_FLICKR_ALBUM_02.jpg/revision/latest/scale-to-width-down/310?cb=20180325140908'

urllib.request.urlretrieve(url, "test.jpg")

img = Image.open(r"test.jpg")
img.show()
"""
