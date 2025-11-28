from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.skills import Skill
from app.schemas.skills import Skill as SkillSchema

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

# CREATE SKILL
@router.post("/", response_model=SkillSchema)
async def create_skills(
    skill_name: str = Form(...),
    skill_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    img_bytes = await skill_image.read()

    new_skill = Skill(
        skill_name=skill_name,
        skill_image=img_bytes
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


# GET ALL SKILLS
@router.get("/", response_model=list[SkillSchema])
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    # return [] instead of 404 for empty
    return skills


# UPDATE SKILL
@router.put("/{skill_id}", response_model=SkillSchema)
async def update_skills(
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
        skill.skill_image = await skill_image.read()

    db.commit()
    db.refresh(skill)
    return skill


# DELETE SKILL
@router.delete("/{skill_id}")
def delete_skills(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"message": "successfully deleted"}
