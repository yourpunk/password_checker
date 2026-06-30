from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.analyzer import analyze_password
from backend.schemas import PasswordCheckRequest, PasswordCheckResponse, CriterionResponse

app = FastAPI(
    title="Password Strength Checker",
    description="Analyzes password strength based on length, character variety, and common patterns",
    version="1.0.0",
)

static_dir = Path(__file__).parent.parent / "frontend"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(static_dir / "index.html", media_type="text/html")

@app.post("/api/check", response_model=PasswordCheckResponse)
def check_password(
    request: PasswordCheckRequest):

    analysis = analyze_password(request.password)
    return PasswordCheckResponse(
        score=analysis.score,
        category=analysis.category,
        criteria=[
            CriterionResponse(
                name=c.name,
                passed=c.passed,
                points=c.points,
                max_points=c.max_points,
                message=c.message,
            )
            for c in analysis.criteria
        ],
        suggestions=analysis.suggestions,
        web_comment=analysis.web_comment,
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

