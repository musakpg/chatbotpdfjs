from flask import Flask, request, jsonify, render_template
import os
from pdf_parser import extract_text_from_pdf
from nlp_model import qa_pipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        # Save the text to a file for later use
        with open('uploads/context.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        return jsonify({"message": "File uploaded successfully", "text": text})
    
    return jsonify({"error": "File type not allowed"})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    # Read the context from the saved file
    with open('uploads/context.txt', 'r', encoding='utf-8') as f:
        context = f.read()
    print("Question:", question)
    print("Context:", context[:500])  # Print the first 500 characters of the context for debugging
    result = qa_pipeline(question=question, context=context)
    print("Answer:", result['answer'])
    answer = result['answer']
    return jsonify({"answer": answer})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
