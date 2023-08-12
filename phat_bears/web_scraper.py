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
    # TODO: Speed up OCR proces? Takes forever
    # url = 'https://irma.nps.gov/DataStore/DownloadFile/671923'
    # # # download locally:
    # urlretrieve(url, "bears_of_brooks_river_2022.pdf")
    # # # ocr content:
    # ocrmypdf.ocr(
    #     "bears_of_brooks_river_2022.pdf",
    #     "bears_of_brooks_river_2022_ocred.pdf",
    #     force_ocr=True,
    #     output_type="pdf",
    #     progress_bar=True,
    # )
    # Load OCRed PDF
    # pdf = PyPDFLoader("bears_of_brooks_river_2022_ocred.pdf").load()
    #
    # pages_of_general_info = pdf[4:28] + [pdf[34]]
    # cleaned_pages_of_general_info = [page.page_content.replace('\n', '') for page in pages_of_general_info]
    #
    # pages_of_adult_bear_bios = pdf[35:88]
    # cleaned_pages_of_adult_bear_bios = [page.page_content.replace('\n', '') for page in pages_of_adult_bear_bios]
    # # Grab only the entries that are for particular bears:
    # identified_bears = [p for p in cleaned_pages_of_adult_bear_bios if p[:2].isdigit()]

    # -------------------------
    # | Parse fan wikis (text)|
    # -------------------------

    bear_wiki_info = []

    with open('wiki_links.txt', 'r') as f:
        for url in f:
            url = url.strip()
            page = requests.get(url)  # add error handling here
            soup = BeautifulSoup(page.content, "lxml")
            full_title = soup.title.text
            bear_id = full_title.split('|')[0].strip()
            body_text = soup.findAll('p')  # still tons of HTML tags left in here. No super easy way to clean up.
            body_text = [b.text.replace('\n', '').replace('\xa0', '') for b in body_text]
            body_text = [b for b in body_text if not b == '']
            body_text = ' '.join(body_text)  # might have to chunk up to ingest into weaviate, but not sure where
            # should do it
            bear_wiki_info.append({'id': bear_id, 'body': body_text})


    print('hi')


    # NOTE: OCRing didn't get all data. For instance, it didn't get Bear 261 or the info pg about male bears from
    # the 2022 PDF booklett


    # GENERAL PARK INFO (pdf)
    # Grab content that's general about the park --> index

    # BIOGRAPHICAL INFO ON BEARS (webpage)
    # Grab biographical content about the bears (can skip children) -->
    # Use BeautifulSoup on links in wiki_links.txt -->

        # IMAGES EXTRACTED FROM EACH BEAR'S WIKI PAGE
        # -->



###
    # TEXT (title, body):
    # soup.title.text = "001 Diver | Katmai Bearcams Wiki | Fandom"
    # soup.findAll('p')

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
