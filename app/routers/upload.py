from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import Project  # or Skill/About depending on where you want to store
import uuid
import shutil

router = APIRouter(prefix="/upload", tags=["Upload"])

# Helper: upload file to "remote" (for now, local folder + return URL)
UPLOAD_FOLDER = "uploads"

def save_file_locally(file: UploadFile) -> str:
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = f"{UPLOAD_FOLDER}/{filename}"

    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    # Pretend URL (can be replaced with S3, Cloudinary, etc.)
    url = f"/{UPLOAD_FOLDER}/{filename}"
    return url

@router.post("/project-image/{project_id}")
def upload_project_image(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    url = save_file_locally(file)
    project.project_image_url = url
    db.commit()
    db.refresh(project)
    return {"url": url, "project_id": project.id}
