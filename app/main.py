from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base , engine

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="backend API for my personal portfolio"
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
# Routers
from app.routers import (
    status,
    auth,
    project_router,
    about_router,
    skills_router,
    contact_router
)
app.include_router(status.router)
app.include_router(project_router)
app.include_router(about_router)
app.include_router(skills_router)
app.include_router(contact_router)
app.include_router(auth.router)

# Normal GET root
@app.get("/")
def read_root():
    return {"Hello": "fastapi backend running!"}
@app.head("/")
def head_root():
    return {}