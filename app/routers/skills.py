from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
from app.core.database import get_db
from app.models.skills import Skill
from app.schemas.skills import Skill as SkillSchema

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

# Directory to save uploaded images
UPLOAD_DIR = "static/skills"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# CREATE SKILL
# -----------------------------
@router.post("/", response_model=SkillSchema)
def create_skill(
    skill_name: str = Form(...),
    skill_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    skill_image_url = None
    if skill_image:
        file_path = os.path.join(UPLOAD_DIR, skill_image.filename)
        with open(file_path, "wb") as f:
            f.write(skill_image.file.read())
        skill_image_url = f"/{file_path}"

    new_skill = Skill(
        skill_name=skill_name,
        skill_image_url=skill_image_url
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


# -----------------------------
# GET ALL SKILLS
# -----------------------------
@router.get("/", response_model=list[SkillSchema])
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return skills  # empty list if none


# -----------------------------
# GET SINGLE SKILL
# -----------------------------
@router.get("/{skill_id}", response_model=SkillSchema)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


# -----------------------------
# UPDATE SKILL
# -----------------------------
@router.put("/{skill_id}", response_model=SkillSchema)
def update_skill(
    skill_id: int,
    skill_name: str = Form(...),
    skill_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill.skill_name = skill_name

    if skill_image:
        file_path = os.path.join(UPLOAD_DIR, skill_image.filename)
        with open(file_path, "wb") as f:
            f.write(skill_image.file.read())
        skill.skill_image_url = f"/{file_path}"

    db.commit()
    db.refresh(skill)
    return skill


# -----------------------------
# DELETE SKILL
# -----------------------------
@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"message": "successfully deleted"}
