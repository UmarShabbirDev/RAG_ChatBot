import os
import os
from ContentExtractor import Context_Extractor
from ChunkSplitter import Chunk_Splitter
from CreateDatabase import Save_Chunks_To_Chroma
from QueryData import query_data
from flask import Flask, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'Resources/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Upload_Document',methods = ['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file part.'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            documents = []
            for file_name in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, file_name)
                if os.path.isfile(file_path):
                    print(f'Processing file: {file_name}')
                    extracted_document = Context_Extractor(file_path)
                    if extracted_document:
                        documents.append(extracted_document)

            if documents:
                chunk = Chunk_Splitter(documents)
                Save_Chunks_To_Chroma(chunk)
                #Query_Data()

            return jsonify({"message": "File uploaded and processed successfully", "filename": filename}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({"message": f"File '{filename}' deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/queryData', methods=['GET'])
def query_document():
    query_text = request.args.get('query')
    if not query_text:
        return jsonify({"error": "Query parameter is missing"}), 400
    try:
        response = query_data(query_text)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)