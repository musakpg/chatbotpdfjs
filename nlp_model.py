from transformers import pipeline

# Load a more advanced pre-trained model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
