from pydantic import BaseModel
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    email: str 
    message : str
class ContactCreate(ContactBase):
    pass 
class Contact(ContactBase):
    id:int
    time_stamp: datetime

    class Config:
        from_attributes=True