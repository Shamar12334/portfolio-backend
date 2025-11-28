from sqlalchemy import Column,String,Integer,Text,DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Contact(Base):
    __tablename__= "contacts"

    id =Column(Integer,primary_key=True,index=True)
    name= Column(String(200),nullable=False)
    email = Column(Text,nullable=False)
    message= Column(Text,nullable=False)
    time_stamp= Column(DateTime(timezone=True),server_default=func.now())