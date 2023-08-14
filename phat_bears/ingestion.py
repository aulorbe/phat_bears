"""Index data objects into Weaviate GenPhatBears class."""

import json
import os

import weaviate
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError



CLASS_NAME = "GenPhatBears"
OPENAI_APIKEY = os.environ['OPENAI_APIKEY']


def instantiate_client():
    return weaviate.Client(
        url="http://0.0.0.0:8080",
        additional_headers={
            "X-Openai-Api-Key": OPENAI_APIKEY
        },
    )


def split_paragraph(text, chunk_size):
    words = text.split()
    chunks = [words[i : i + chunk_size] for i in range(0, len(words), chunk_size)]
    return chunks


def create_data_objs(data):
    extended_data_objs = []
    for w in data:
        # Split up text
        text_chunks = split_paragraph(w["bio"], 100)
        text_chunks = [" ".join(t) for t in text_chunks]
        # Create data objs
        data_objs = []
        for t in text_chunks:
            single_data_obj = {"name": w.get("name"), "bio": t}
            data_objs.append(single_data_obj)
        extended_data_objs.extend(data_objs)
    return extended_data_objs


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def batch_index_objs(data_objs):
    with client.batch().configure(batch_size=5, timeout_retries=2) as batch:
        for data_obj in data_objs:
            # todo: add error handling & status bar so you know when it's finished running
            batch.add_data_object(data_obj, CLASS_NAME)



if __name__ == "__main__":
    client = instantiate_client()

    with open("data/scraped_data/bear_wiki_info.json", "r") as f:
        wiki_info = json.load(f)

    data_objs = create_data_objs(wiki_info)

    batch_index_objs(data_objs)


