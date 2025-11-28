from sqlalchemy import Column,String, Text,Integer,LargeBinary
from app.core.database import Base

class About(Base):
    __tablename__="about"
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String(200),nullable=False)
    degree=Column(Text,nullable=False)
    bio =Column(Text,nullable=False)
    profile_picture=Column(LargeBinary,nullable=False)
    years_of_experience=Column(String(200),nullable=False)
    resume_url=Column(Text,nullable=False)