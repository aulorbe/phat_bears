from langchain.vectorstores import Weaviate
import weaviate

from langchain.chat_models import ChatOpenAI


if __name__ == "__main__":
    client = weaviate.Client(
        url="http://0.0.0.0:8080",
        additional_headers={
            "X-Openai-Api-Key": ""
        },
    )
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key="",
    )
    retriever = Weaviate(
        client=client, index_name="GenPhatBears", text_key="bio"
    ).as_retriever()

    # Conversational retrieval with memory...
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationalRetrievalChain

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )
    query = "Who is Otis"
    result = qa({"question": query})['answer']

    print('hi')
