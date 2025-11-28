from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# CREATE PROJECT
@router.post("/", response_model=ProjectSchema)
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    github_url: str = Form(None),
    live_url: str = Form(None),
    tech_stack: str = Form(None),
    project_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    img_bytes = await project_image.read() if project_image else None

    new_project = Project(
        title=title,
        description=description,
        github_url=github_url,
        live_url=live_url,
        tech_stack=tech_stack,
        project_image= img_bytes
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# GET ALL PROJECTS
@router.get("/", response_model=list[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects  # never return 404, just empty list


# GET SINGLE PROJECT
@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# UPDATE PROJECT
@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    title: str = Form(...),
    description: str = Form(...),
    github_url: str = Form(None),
    live_url: str = Form(None),
    tech_stack: str = Form(None),
    project_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update text fields
    project.title = title
    project.description = description
    project.github_url = github_url
    project.live_url = live_url
    project.tech_stack = tech_stack

    # Update image if provided
    if project_image:
        project.project_image = await project_image.read()

    db.commit()
    db.refresh(project)
    return project


# DELETE PROJECT
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "successfully deleted"}
