from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.core.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="backend API for my personal portfolio"
)

# Attach rate limiter
app.state.limiter = limiter

# Add SlowAPI middleware ONCE
app.add_middleware(SlowAPIMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle 429 rate limit response
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests — slow down."},
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

# HEAD route for uptime checks — MUST BE EXEMPT
@limiter.exempt
@app.head("/")
def head_root():
    return JSONResponse(status_code=200)
