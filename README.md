# phat_bears

Follow the sections in order to get the app up and running. Yay Fat Bears! 

## Environment
In a virtual environment of your choice, from the root directory, run `pip install -r requirements.txt`.

## Weaviate component
Ensure you have Docker installed & it's up and running. 

Run `docker-compose up` to get this demo's Weaviate engine up and running with the correct configs.

### Populating your Weaviate engine
In terminal, run `chmod +x startup.sh` to ensure you can run the necessary Bash script.

Then run `./startup.sh` (in terminal). 

You can navigate to `https://console.weaviate.cloud/query` and execute some GraphQL queries to your documents 
trickling in, e.g.

```
{
  Get{
    GenPhatBears(
      nearText: {
        concepts: ["bear"],
      	
      }
      limit: 5
      where: {
        path: ["name"],
        operator: Equal,
        valueText: "480 Otis"
      }
    ){
      name
      bio
    }
  }
}
```

## Flask component
Once your Weaviate engine has all the data in it, you're ready to go! Start the app by running `flask --app app run` 
on terminal.

You'll be prompted to input your OpenAI API key. 
