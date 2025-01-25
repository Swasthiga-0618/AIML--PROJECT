from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.sentiment_access import load_notebook_from_pkl
from models.issue_escalation import should_escalate
from models.response_automation import preprocess_text, get_product_subject, get_product_body
import requests

# Initialize the FastAPI app
app = FastAPI()

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21370772/2krymin/"

class Ticket(BaseModel):
    subject: str
    body: str
    customer_email: str

@app.post("/process-ticket/")
async def process_ticket(ticket: Ticket):
    try:
        # Preprocess ticket data
        processed_subject = preprocess_text(ticket.subject)
        processed_body = preprocess_text(ticket.body)

        # Sentiment analysis
        sentiment_result = load_notebook_from_pkl(processed_body)
        if not isinstance(sentiment_result, dict) or "sentiment" not in sentiment_result:
            raise ValueError("Invalid response from sentiment analysis model")

        # Issue escalation
        priority = should_escalate(processed_body)
        if not isinstance(priority, str):  # Assuming priority should be a string
            raise ValueError("Invalid priority calculated by issue escalation model")

        escalation_required = load_notebook_from_pkl(priority)
        if not isinstance(escalation_required, bool):  # Assuming escalation should be a boolean
            raise ValueError("Invalid response for escalation requirement")

        # Extract product information
        product_subject = get_product_subject(processed_subject)
        product_body = get_product_body(processed_body)

        # Generate response
        response = {
            "customer_email": ticket.customer_email,
            "sentiment": sentiment_result["sentiment"],
            "escalation_required": escalation_required,
            "priority": priority,
            "product_details": {
                "from_subject": product_subject,
                "from_body": product_body
            }
        }

        # Construct payload for Zapier webhook
        zapier_payload = {
            "To": ticket.customer_email,
            "Cc": "",
            "Subject": f"Issue Report: {product_subject}",
            "Body type": "plain",
            "Body": (
                f"Hello,\n\n"
                f"We've received your ticket regarding: {product_subject}.\n\n"
                f"Here are the details:\n\n"
                f"Sentiment: {sentiment_result['sentiment']}\n"
                f"Escalation Required: {escalation_required}\n"
                f"Priority: {priority}\n"
                f"Issue Details: {product_body}\n\n"
                f"Thank you for bringing this to our attention.\n\n"
                f"Regards,\nSupport Team"
            )
        }
        # Send to Zapier
        zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json=zapier_payload)
        zapier_response.raise_for_status()

        return response

    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Failed to send data to Zapier: {str(req_err)}")
    except ValueError as val_err:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(val_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/")
def root():
    return {"message": "Ticket Processing API is running. Use POST /process-ticket/ to process a ticket."}
