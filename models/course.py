from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints

# Course Code: 4 uppercase letters + 4 digits (e.g. COMS4701)
CourseCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]

class CourseBase(BaseModel):
    id: UUID = Field(
      default_factory=uuid4,
      description="Persistent Course ID (server-generated).",
      json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    code: CourseCode = Field(
        ...,
        description="Columbia University Course Code (4 uppercase letters + 4 digits).",
        json_schema_extra={"example": "COMS4701"},
    )
    title: str = Field(
        ...,
        description="Course title.",
        json_schema_extra={"example": "Cloud Computing"},
    )
    credits: int = Field(
        ...,
        ge=1, le=5,
        description="Number of course credits.",
        json_schema_extra={"example": 3},
    )
    location: Optional[str] = Field(
        None,
        description="Room and building of the class location, if assigned.",
        json_schema_extra={"example": "501 Northwest Corner"},
    )
  
    model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "code": "COMS4701",
                        "title": "Cloud Computing",
                        "credits": 3,
                        "location": "501 Northwest Corner",
                    }
                ]
            }
        }


class CourseCreate(CourseBase):
    """Creation payload for a Course. ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "code": "COMS4111",
                    "title": "Introduction to Databases",
                    "credits": 3,
                    "location": "417 International Affairs Building",
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Full update. All fields are optional"""
    code: Optional[str] = Field(None, description="olumbia University Course Code (4 uppercase letters + 4 digits).")
    title: Optional[str] = Field(None, description="Course title.")
    credits: Optional[int] = Field(None, ge=1, le=5, description="Number of course credits.")
    location: Optional[str] = Field(None, description="Room and building of the class location, if assigned.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "COMS4701",
                    "title": "Cloud Computing",
                    "credits": 3,
                    "location": "501 Northwest Corner",
                },
                {"location": "417 International Affairs Building"},
            ]
        }
    }

# Server representation returned to clients.
class CourseRead(CourseBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "code": "COMS4701",
                    "title": "Cloud Computing",
                    "credits": 3,
                    "location": "501 Northwest Corner",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
