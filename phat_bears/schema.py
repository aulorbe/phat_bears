import weaviate

bears_schema = {
  "classes": [
    {
      "class": "PhatBears",
      "moduleConfig": {
        "multi2vec-clip": {
          "imageFields": [
            "image"
          ],
          "textFields": [
            "name",
            "bio"
          ],
        }
      },
      "properties": [
        {
          "dataType": [
            "text"
          ],
          "name": "name"
        },
{
          "dataType": [
            "text"
          ],
          "name": "bio"
        },
        {
          "dataType": [
            "blob"
          ],
          "name": "image"
        }
      ],
      "vectorIndexType": "hnsw",
      "vectorizer": "multi2vec-clip"
    }
  ]
}

if __name__ == "__main__":
    client = weaviate.Client(
        url="http://0.0.0.0:8080",
    )
    client.schema.create(bears_schema)


