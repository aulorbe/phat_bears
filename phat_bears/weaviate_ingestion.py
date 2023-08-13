import weaviate

if __name__ == "__main__":
    # todo: set OPENAI_APIKEY env var (or put in docker-compose file)
    client = weaviate.Client("http://localhost:8080")
    schema = client.schema.get()
    print("hi")