from sqlalchemy import Column, String, Integer, LargeBinary
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(200), nullable=False)
    skill_image = Column(LargeBinary, nullable=False)
