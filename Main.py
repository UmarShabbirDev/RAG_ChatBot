import os
from ContentExtractor import Context_Extractor
from ChunkSplitter import Chunk_Splitter
from CreateDatabase import Save_Chunks_To_Chroma
from QueryData import Query_Data

# Path to the Resources folder
resources_folder = 'Resources'


# Check if the Resources folder exists
if os.path.exists(resources_folder) and os.path.isdir(resources_folder):
    documents = []
    # Iterate over all files in the Resources folder
    for file_name in os.listdir(resources_folder):
        file_path = os.path.join(resources_folder, file_name)
        if os.path.isfile(file_path):
            print(f'Processing file: {file_name}')
            extracted_document = Context_Extractor(file_path)
            if extracted_document:
                documents.append(extracted_document)

    if documents:
        chunk = Chunk_Splitter(documents)
        Save_Chunks_To_Chroma(chunk)
        Query_Data()
else:
    print(f'Resources folder not found')

