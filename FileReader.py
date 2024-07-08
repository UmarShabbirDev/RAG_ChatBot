import os
from docx import Document
from langchain_community.document_loaders import PyPDFLoader

def context_extractor(file_path):
    text_extension =['.txt']
    pdf_extension = ['.pdf']
    docx_extension = ['.docx']
    text = ''
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in text_extension:
        with open(file_path, 'r') as f:
            text = f.read()
        return text
    elif file_extension in pdf_extension:
        pdf_loader = PyPDFLoader(file_path)
        pages = pdf_loader.load()  # Correctly load the PDF pages
        for page in pages:
            text += page.page_content  # Access the content of each page correctly
            text += '\n'
        return text
    elif file_extension in docx_extension:
        doc = Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(text)
    else:
        print('File extension not supported')

file_path = r'D:\Check\Table_prerequisites_MSc_DaCS.pdf'  # Change this to the path of your file
extracted_text = context_extractor(file_path)

# Print the extracted text
print(extracted_text)