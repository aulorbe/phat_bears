import json
import os

import weaviate
import cv2
import base64


if __name__ == "__main__":
    # Chunk_032 image
    # test_img = cv2.imread('../scraped_data/bear_wiki_images/032Chunk_0.jpg')
    # jpg_img = cv2.imencode('.jpg', test_img)
    # b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')

    # Chunk_032 text
    with open("../scraped_data/bear_wiki_info.json", 'r') as f:
        test = json.load(f)
    chunk_bio_data = test[0]

    # Split up text
    def split_paragraph(text, chunk_size):
        words = text.split()
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        return chunks
    #
    text_chunks = split_paragraph(chunk_bio_data['bio'], 1000)
    text_chunks = [' '.join(t) for t in text_chunks]

    data_objs = []
    for t in text_chunks:
        single_data_obj = {'name': chunk_bio_data.get('name'),
                           'bio': t}
        data_objs.append(single_data_obj)

    # Ingest
    client = weaviate.Client(
        url="http://0.0.0.0:8080",
        additional_headers={
            'X-Openai-Api-Key': ''

        }
    )
    class_name = 'GenPhatBears'

    with client.batch().configure(batch_size=5, timeout_retries=2) as batch:
        for data_obj in data_objs:
            batch.add_data_object(data_obj, class_name)

    print('hi')

