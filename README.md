# phat_bears

Follow the sections in order to get the app up and running. Yay Fat Bears! 

## Environment
In a virtual environment of your choice, from the root directory, run `pip install -r requirements.txt`.

## Weaviate component
Ensure you have Docker installed & it's up and running. 

Run `docker-compose up` to get this demo's Weaviate engine up and running with the correct configs.

### Populating your Weaviate engine
** need a paid openai key
Run `export OPENAI_APIKEY=<your API key>` to set the environment variable necessary for Weaviate to work.
Run `echo $OPENAI_APIKEY` to ensure it worked (you'll see the key in your terminal if it worked.)

In terminal, run `chmod +x startup.sh` to ensure you can run the necessary Bash script.

Then run `./startup.sh` (in terminal). Alternatively, you can manually run the python scripts in the `phat_bears` dir,
in the 
following order:
- `gen_schema.py`
- `web_scraper.py`
- `ingestion.py`
  
(There is an example of the scraped data in `data/scraped_data`, if you want to see the expected output and/or use 
  that JSON file instead of running `web_scraper.py`.)

You can navigate to `https://console.weaviate.cloud/query` and execute some GraphQL queries to your documents 
trickling in (you'll be prompted to make an account, if you haven't already).

Sample GraphQL query you can use:

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

Note: This chat bot stores your chat history! This means that you can issue follow-up questions like "Tell me more 
about him," and the app will know which bear you're referencing.

### Sample questions to inspire you!
- Who is Otis?
- Why is Otis so popular?
- Does Holly have children? If so, what are their identification numbers?


