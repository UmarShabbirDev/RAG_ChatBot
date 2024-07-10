import argparse
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
db_path = 'Chroma'
def Query_Data():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str, help="The query text")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = OpenAIEmbeddings() # api key here
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    result = db.similarity_search_with_relevance_scores(query_text, k=1)
    if len(result) == 0 or result[0][1] < 0.7:
        print("unable to find matches")
        return
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    print(context_text)
    return context_text
