import json
import os

import weaviate


def split_paragraph(text, chunk_size):
    words = text.split()
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    return chunks


if __name__ == "__main__":
    client = weaviate.Client(
        url="http://0.0.0.0:8080",
        additional_headers={
            'X-Openai-Api-Key': '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'

        }
    )

    class_name = 'GenPhatBears'

    with open("../scraped_data/bear_wiki_info.json", 'r') as f:
        wiki_info = json.load(f)

    extended_data_objs = []
    for w in wiki_info:
        # Split up text
        text_chunks = split_paragraph(w['bio'], 100)
        text_chunks = [' '.join(t) for t in text_chunks]
        # Create data objs
        data_objs = []
        for t in text_chunks:
            single_data_obj = {'name': w.get('name'),
                               'bio': t}
            data_objs.append(single_data_obj)
        extended_data_objs.extend(data_objs)

    with client.batch().configure(batch_size=5, timeout_retries=2) as batch:
        for data_obj in extended_data_objs:
            batch.add_data_object(data_obj, class_name)

    print('hi')

