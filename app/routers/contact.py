from fastapi import APIRouter,Depends,HTTPException,Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, Contact as ContactSchema
from app.core.rate_limiter import limiter

router = APIRouter(
    prefix="/contact",
    tags =["Contact"]
)

#create contact
@router.post("/", response_model=ContactSchema)
@limiter.limit("3/minute")
def create_contact(request: Request,contact: ContactCreate,db:Session=Depends(get_db)):
    if len(contact.name) < 2 or len(contact.name) > 50:
        raise HTTPException(400,"Invalid name length")
     
    if len(contact.email) < 2 or len(contact.email) > 50:
        raise HTTPException(400,"Invalid name length")
        
    if len(contact.message) < 2 or len(contact.message) > 50:
        raise HTTPException(400,"Invalid name length")
    
    last = db.query(Contact).order_by(Contact.id.desc()).first()
    if last and last.message == contact.message:
        raise HTTPException(400, "Duplicate message detected")
    
    new_contact= Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact
#get contact
@router.get("/", response_model=list[ContactSchema])
def get_contact(db: Session= Depends(get_db)):
    contact= db.query(Contact).all()
    return contact
#update
@router.put("/{contact_id}", response_model=ContactSchema)
def update_contact(contact_id: int,updated: ContactCreate, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contacts:
        raise HTTPException(status_code=404,detail="not found")
    for key,value in updated.dict().items():
        setattr(contacts,key,value)
    db.commit()
    db.refresh(contacts)
    return contacts
#delete
@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db:Session=Depends(get_db)):
    contacts= db.query(Contact).filter(Contact.id == contact_id).first()
    if not contacts:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(contacts)
    db.commit()
    return  {"message": "Project deleted successfully"}