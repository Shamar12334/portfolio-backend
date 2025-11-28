from pydantic import BaseModel
class AboutBase(BaseModel):
    name: str 
    degree: str
    bio:    str
    profile_picture: bytes
    years_of_experience: str
    resume_url: str
class AboutCreate(AboutBase):
    pass 
class About(AboutBase):
    id:int

    class Config:
        from_attributes= True