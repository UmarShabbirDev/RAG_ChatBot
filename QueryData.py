import argparse
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from LLMResponse import GetChatgptResponse
db_path = 'Chroma'


def query_data(query_text):

    embedding_function = OpenAIEmbeddings()  # api key here
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

    retrieved_docs = retriever.get_relevant_documents(query_text)
    if not retrieved_docs:
        print("Unable to find matches")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"Answer the following question based on the provided context:\n\nContext:\n{context_text}\n\nQuestion: {query_text}"
    response = GetChatgptResponse(prompt)
    return response