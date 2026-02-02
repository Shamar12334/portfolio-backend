from pydantic import BaseModel

class SkillBase(BaseModel):
    skill_name: str
    skill_image_url: str | None = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int

    class Config:
        from_attributes = True
