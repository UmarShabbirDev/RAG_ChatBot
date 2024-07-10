import os
import shutil
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

db_path = 'Chroma'
def Save_Chunks_To_Chroma(chunks: list[Document]):
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

   # db = Chroma.from_documents(chunks,OpenAIEmbeddings(api_key=''),persist_directory=db_path)
    db = Chroma.from_documents(chunks,OpenAIEmbeddings(),persist_directory=db_path)
    db.persist()
    print(f"{len(chunks)} chunks saved to {db_path}")