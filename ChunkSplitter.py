from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
def Chunk_Splitter(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} into {len(chunks)} chunks")

    return chunks
