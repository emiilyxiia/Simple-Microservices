from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .course import CourseBase

# Columbia UNI: 2–3 lowercase letters + 1–4 digits (e.g., abc1234)
UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class TeacherBase(BaseModel):
    uni: UNIType = Field(
        ...,
        description="Columbia University UNI (2–3 lowercase letters + 1–4 digits).",
        json_schema_extra={"example": "dff9"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Donald"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Ferguson"},
    )
    department: str = Field(
        ...,
        description="Department Code.",
        json_schema_extra={"example": "COMS"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "dff9@example.com"},
    )
    academic_title: Optional[str] = Field(
        None, 
        description="Academic title", 
        json_schema_extra={"example": "Professor"})
    office: Optional[str] = Field(
        None, 
        description="Office location", 
        json_schema_extra={"example": "Mudd 620"})

    # Embed courses (each with persistent course code)
    courses: List[CourseBase] = Field(
        default_factory=list,
        description="Courses taught by this teacher (each carry a unique course code).",
        json_schema_extra={
            "example": [
                {
                    "code": "COMS4701",
                    "title": "Cloud Computing",
                    "credits": 3,
                    "location": "501 Northwest Corner",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "dff9",
                    "first_name": "Donald",
                    "last_name": "Ferguson",
                    "department": "COMS",
                    "email": "dff9@example.com",
                    "academic_title": "Professor",
                    "office": None,
                    "courses": [
                        {
                          "code": "COMS4701",
                          "title": "Cloud Computing",
                          "credits": 3,
                          "location": "501 Northwest Corner",
                        }
                    ],
                }
            ]
        }
    }


class TeacherCreate(TeacherBase):
    """Creation payload for a Teacher."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "hi1234",
                    "first_name": "Hugh",
                    "last_name": "Ingrid",
                    "department": "COMS",
                    "email": "hi1234@columbia.edu",
                    "academic_title": "Teaching Assistant",
                    "office": None,
                    "courses": [
                        {
                          "code": "COMS4701",
                          "title": "Cloud Computing",
                          "credits": 3,
                          "location": "501 Northwest Corner",
                        }
                    ],
                }
            ]
        }
    }


class TeacherUpdate(BaseModel):
    """Full update for a Teacher."""
    uni: Optional[UNIType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Alice"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Bachman"})
    department: Optional[str] = Field(None, json_schema_extra={"example": "HUMA"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ab1234@newmail.com"})
    academic_title: Optional[str] = Field(None, json_schema_extra={"example": "Lecturer"})
    office: Optional[str] = Field(None, json_schema_extra={"example": "211 Mudd"})
    courses: Optional[List[CourseBase]] = Field(
        None,
        description="Replace the entire set of courses with this list.",
        json_schema_extra={
            "example": [
                {
                    "code": "HUMA1123",
                    "title": "Music Humanities",
                    "credits": 3,
                    "location": "404 Dodge Hall",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Alice", "last_name": "Bachman"},
                {
                    "courses": [
                        {
                          "code": "HUMA1123",
                          "title": "Music Humanities",
                          "credits": 3,
                          "location": "404 Dodge Hall",
                        }
                    ]
                },
            ]
        }
    }


class TeacherRead(TeacherBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Teacher ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
                    "uni": "dff9",
                    "first_name": "Donald",
                    "last_name": "Ferguson",
                    "department": "COMS",
                    "email": "dff9@example.com",
                    "academic_title": "Professor",
                    "office": None,
                    "courses": [
                        {
                          "code": "COMS4701",
                          "title": "Cloud Computing",
                          "credits": 3,
                          "location": "501 Northwest Corner",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
