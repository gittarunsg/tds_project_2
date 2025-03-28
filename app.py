from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import pandas as pd
import tempfile
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    file: UploadFile = File(None),
):
    try:
        # Logic to process question and file
        if "unzip" in question.lower() and "csv" in question.lower():
            if not file:
                raise HTTPException(400, "File required")
            
            # Process ZIP and CSV
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, file.filename)
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                
                # Extract CSV
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)
                
                # Find CSV and read 'answer' column
                for extracted_file in os.listdir(tmpdir):
                    if extracted_file.endswith('.csv'):
                        df = pd.read_csv(os.path.join(tmpdir, extracted_file))
                        answer = df['answer'].iloc[0]
                        return {"answer": str(answer)}
        
        # Add more question handlers here
        
        return {"answer": "No matching logic found"}
    
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
