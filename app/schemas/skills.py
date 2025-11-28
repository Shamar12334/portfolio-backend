from pydantic import BaseModel, field_serializer
import base64

class SkillBase(BaseModel):
    skill_name: str
    skill_image: bytes

    @field_serializer("skill_image")
    def encode_image(self, image_bytes):
        return base64.b64encode(image_bytes).decode()

class Skill(SkillBase):
    id: int
    class Config:
        from_attributes = True
