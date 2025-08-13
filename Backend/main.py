# backend/main.py
import sys
import os
from fastapi import FastAPI, UploadFile, File
import pandas as pd

# Add project root to sys.path so we can import combined
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from combined.combined import load_csv_safe, generate_combined_topics

app = FastAPI(title="Podcast Topic Recommender API")

@app.get("/")
def home():
    return {"message": "Podcast Topic Recommender API is running!"}

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    topics = df.iloc[:, 0].dropna().tolist()
    return {"uploaded_topics": topics}

@app.get("/generate")
def generate_topics():
    topics = generate_combined_topics()
    return {"combined_topics": topics, "count": len(topics)}
