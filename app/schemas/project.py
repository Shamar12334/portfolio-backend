from pydantic import BaseModel,field_serializer
import base64
class ProjectBase(BaseModel):
    title: str
    description: str
    github_url: str | None = None
    live_url: str | None = None
    tech_stack: str | None= None
    project_image: bytes | None = None

    @field_serializer("project_image")
    def encode_image(self, value: bytes):
        if value is None:
            return None
        return base64.b64encode(value).decode()

class Project(ProjectBase):
    id : int

    class Config:
        from_attributes=True