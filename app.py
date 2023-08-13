from flask import Flask, render_template, request, redirect, url_for, session
import weaviate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Weaviate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


app = Flask(__name__)

app.secret_key = "test"


def create_weaviate_client(api_key):
    return weaviate.Client(
        url="http://0.0.0.0:8080",
        additional_headers={"X-Openai-Api-Key": api_key},
    )


def create_llm(api_key):
    return ChatOpenAI(
        temperature=0,
        openai_api_key=api_key,
    )


def create_retriever(client):
    return Weaviate(
        client=client, index_name="GenPhatBears", text_key="bio"
    ).as_retriever()


def get_qa():
    api_key = session.get("api_key")

    client = create_weaviate_client(api_key=api_key)
    if not client.is_ready():
        err_msg = "Issue with Weaviate. Check connection"
        return err_msg

    llm = create_llm(api_key=api_key)
    retriever = create_retriever(client)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )
    return qa


QA = None


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/process_api_key", methods=["POST"])
def process_api_key():
    api_key = request.form.get("api_key")

    # Store the API key in the session
    session["api_key"] = api_key

    global QA  # Needs to be global in order to keep chat history.
    QA = get_qa()

    return redirect(url_for("search_page"))


@app.route("/search_page", methods=["GET"])
def search_page():
    return render_template("search.html")


@app.route("/search_results", methods=["GET"])
def search_results():
    query = request.args.get("query")

    if QA is None:
        return "QA object not initialized"

    result = QA({"question": query})["answer"]
    return render_template("search.html", query=query, result=result)
