from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.about import About
from app.schemas.about import AboutCreate, About as AboutSchema

router = APIRouter(
    prefix="/about",
    tags=["About"]
)
#create about
@router.post("/", response_model=AboutSchema)
def create_about(about: AboutCreate,db: Session=Depends(get_db)):
    new_about=About(**about.dict())
    db.add(new_about)
    db.commit()
    db.refresh(new_about)
    return new_about
#get about
@router.get("/", response_model=AboutSchema)
def get_about(db: Session=Depends(get_db)):
    about= db.query(About).first()
    if not about:
        raise HTTPException(status_code=404, detail="About info not found")
    return about
#update
@router.put("/{about_id}", response_model=AboutSchema)
def update_about(about_id: int, updated: AboutCreate, db:Session=Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="not found")
    for key, value in updated.dict().items():
        setattr(about,key,value)
    db.commit()
    db.refresh(about)
    return about
#delete
@router.delete("/{about_id}")
def delete_about(about_id: int, db: Session=Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()

    if not about:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(about)
    db.commit()
    return {"message":"successfully deleted"}

