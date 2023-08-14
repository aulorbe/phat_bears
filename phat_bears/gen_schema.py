"""Create schema for Phat Bears project."""

import weaviate

gen_bears_schema = {
    "classes": [
        {
            "class": "GenPhatBears",
            "moduleConfig": {
                "generative-openai": {
                    "model": "gpt-3.5-turbo",
                }
            },
            "properties": [
                {"dataType": ["text"], "name": "name"},
                {"dataType": ["text"], "name": "bio"},
            ],
        }
    ]
}

if __name__ == "__main__":
    client = weaviate.Client(
        url="http://0.0.0.0:8080",
    )
    client.schema.create(gen_bears_schema)
