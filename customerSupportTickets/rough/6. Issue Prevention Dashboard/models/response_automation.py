import pickle

def load_notebook_from_pkl(text):
    try:
        with open('C:/Users/Asus/Desktop/dashboard/data/Response_automation_trial.pkl', 'rb') as f:
            response_data = pickle.load(f)
        return response_data.get(text, {"sentiment": "neutral"})
    except Exception as e:
        return {"error": str(e)}

def preprocess_text(text):
    return text.lower().strip()

def get_product_subject(subject):
    return f"Extracted Product from Subject: {subject}"

def get_product_body(body):
    return f"Extracted Product from Body: {body}"
