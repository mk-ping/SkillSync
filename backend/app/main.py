from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.resumes import router as resumes_router
from app.api.jobs import router as jobs_router
from app.api.ranking import router as ranking_router
from app.api.candidates import router as candidates_router
from app.api.auth import router as auth_router
from app.api.feedback import router as feedback_router

app = FastAPI(
    title="SkillSync API",
    description="Hybrid ML-based candidate ranking & recruitment intelligence platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(ranking_router)
app.include_router(candidates_router)
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "SkillSync API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
