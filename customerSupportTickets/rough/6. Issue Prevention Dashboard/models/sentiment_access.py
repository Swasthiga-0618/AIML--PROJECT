import pickle

# Load the pickle file and define the function to analyze sentiment
PICKLE_FILE_PATH = 'C:/Users/Asus/Desktop/dashboard/data/sentiment_analysis_gemini.pkl'

# Load the model from the pickle file
try:
    with open(PICKLE_FILE_PATH, "rb") as file:
        sentiment_model = pickle.load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load the sentiment model: {str(e)}")

def load_notebook_from_pkl(input_text: str):
    """
    Use the loaded model to analyze sentiment of the input text.

    Args:
        input_text (str): Text to analyze.

    Returns:
        dict: A dictionary containing the sentiment result, e.g., {"sentiment": "Positive"}.
    """
    if not isinstance(input_text, str):
        raise ValueError("Input text must be a string")

    # Assuming the model has a `predict` method or similar logic
    try:
        sentiment = sentiment_model.predict([input_text])[0]  # Adjust based on the model's API
        return {"sentiment": sentiment}
    except Exception as e:
        return {"error": f"Failed to process input text: {str(e)}"}
    