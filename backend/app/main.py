from fastapi import FastAPI

app = FastAPI(
    title="SkillSync API",
    description="Hybrid ML-based candidate ranking & recruitment intelligence platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"status": "ok", "service": "SkillSync API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}