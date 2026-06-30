from pydantic import BaseModel, Field

class PasswordCheckRequest(BaseModel):
    password: str = Field(..., max_length=256)

class CriterionResponse(BaseModel):
    name: str
    passed: bool
    points: int
    max_points: int
    message: str

class PasswordCheckResponse(BaseModel):
    score: int
    category: str
    criteria: list[CriterionResponse]
    suggestions: list[str]
    web_comment: str = ""