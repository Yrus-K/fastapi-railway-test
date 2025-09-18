from fastapi import FastAPI, HTTPException
import json
import logging
import os

# ✅ Setup logging
logging.basicConfig(level=logging.INFO)
logging.info("🚀 FastAPI app is starting...")

app = FastAPI()

# ✅ Load invoice data safely with error handling
invoices = []
invoice_file = "invoices.json"

if os.path.exists(invoice_file):
    try:
        with open(invoice_file, "r") as f:
            invoices = json.load(f)
            logging.info(f"✅ Loaded {len(invoices)} invoices")
    except json.JSONDecodeError as e:
        logging.error(f"❌ Failed to parse JSON: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error loading invoices: {e}")
else:
    logging.warning(f"⚠️ Invoice file '{invoice_file}' not found")

# ✅ Root endpoint to confirm API is running
@app.get("/")
def read_root():
    return {"message": "Invoice API is running"}

# ✅ Get a specific invoice by ID
@app.get("/invoice/{invoice_id}")
def get_invoice(invoice_id: str):
    for invoice in invoices:
        if invoice.get("invoice_id") == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")

# ✅ Get all pending invoices
@app.get("/pending")
def get_pending_invoices():
    pending = [inv for inv in invoices if inv.get("status", "").lower() == "pending"]
    return {"pending_invoices": pending}

# ✅ Health check endpoint for monitoring
@app.get("/health")
def health_check():
    return {"status": "ok"}