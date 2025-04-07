from pydantic import BaseModel
from typing import Optional


class PodcastResponse(BaseModel):
    status: str
    session_id: str
    download_url: Optional[str] = None


class ErrorResponse(BaseModel):
    status: str
    detail: str
