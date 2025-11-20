from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pdf_report import generate_report_pdf
from ai_analyze import analyze_images
import uuid, os

app = FastAPI()
UPLOADS = "uploads"
RESULTS = "results"
os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

@app.post("/analyze/")
async def analyze(
    face_image: UploadFile,
    body_image: UploadFile = None,
    gender: str = Form(...),
    interests: str = Form(...),
    budget: int = Form(...),
    lifestyle: str = Form(...),
    mbti: str = Form(...),
    language: str = Form("th")
):
    session_id = str(uuid.uuid4())
    # Save images
    face_path = f"{UPLOADS}/{session_id}_face.jpg"
    with open(face_path, "wb") as f:
        f.write(await face_image.read())
    body_path = None
    if body_image:
        body_path = f"{UPLOADS}/{session_id}_body.jpg"
        with open(body_path, "wb") as f:
            f.write(await body_image.read())
    # AI analyze (mock logic)
    result = analyze_images(face_path, body_path, gender, interests, budget, lifestyle, mbti)
    pdf_path = f"{RESULTS}/{session_id}_report.pdf"
    generate_report_pdf(pdf_path, result, gender)
    return JSONResponse({"result": result, "pdf_url": f"/download/{session_id}_report.pdf"})

@app.get("/download/{fname}")
async def get_pdf(fname: str):
    return FileResponse(f"{RESULTS}/{fname}", media_type='application/pdf')