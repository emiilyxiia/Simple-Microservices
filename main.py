from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health

from models.teacher import TeacherCreate, TeacherRead, TeacherUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
teachers: Dict[UUID, TeacherRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI(
    title="Teacher/Course API",
    description="Demo FastAPI app using Pydantic v2 models for Teacher and Course",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    if course.id in courses:
        raise HTTPException(status_code=400, detail="Course with this ID already exists")
    courses[course.id] = CourseRead(**course.model_dump())
    return courses[course.id]

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    code: Optional[str] = Query(None, description="Filter by code"),
    title: Optional[str] = Query(None, description="Filter by exact title"),
    credits: Optional[int] = Query(None, ge=1, le=5, description="Filter by credits 1–5"),
    location: Optional[str] = Query(None, description="Filter by location"),
):
    results = list(courses.values())

    if code is not None:
        results = [a for a in results if a.code == code]
    if title is not None:
        results = [a for a in results if a.title == title]
    if credits is not None:
        results = [a for a in results if a.credits == credits]
    if location is not None:
        results = [a for a in results if a.location == location]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return None
# -----------------------------------------------------------------------------
# Teacher endpoints
# -----------------------------------------------------------------------------

@app.post("/teachers", response_model=TeacherRead, status_code=201)
def create_teacher(teacher: TeacherCreate):
    teacher_read = TeacherRead(**teacher.model_dump())
    teachers[teacher_read.id] = teacher_read
    return teacher_read

@app.get("/teachers", response_model=List[TeacherRead])
def list_teachers(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    department: Optional[str] = Query(None, description="Filter by department"),
    email: Optional[str] = Query(None, description="Filter by email"),
    academic_title: Optional[str] = Query(None, description="Filter by academic title"),
    office: Optional[str] = Query(None, description="Filter by office"),

    location: Optional[str] = Query(None, description="Filter by embedded course location"),
    credits: Optional[int] = Query(None, ge=1, le=5, description="Filter by embedded course credits"),
):
    results = list(teachers.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if department is not None:
        results = [p for p in results if p.department == department]
    if email is not None:
        results = [p for p in results if p.email == email]
    if academic_title is not None:
        results = [p for p in results if p.academic_title == academic_title]
    if office is not None:
        results = [p for p in results if p.office == office]

    # nested address filtering
    if location is not None:
        results = [t for t in results if any((c.location or "") == location for c in t.courses)]
    if credits is not None:
        results = [t for t in results if any(c.credits == credits for c in t.courses)]

    return results

@app.get("/teachers/{teacher_id}", response_model=TeacherRead)
def get_teacher(teacher_id: UUID):
    if teacher_id not in teachers:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teachers[teacher_id]

@app.put("/teachers/{teacher_id}", response_model=TeacherRead)
def update_teacher(teacher_id: UUID, update: TeacherUpdate):
    if teacher_id not in teachers:
        raise HTTPException(status_code=404, detail="Teacher not found")
    stored = teachers[teacher_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    teachers[teacher_id] = TeacherRead(**stored)
    return teachers[teacher_id]

@app.delete("/teachers/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: UUID):
    if teacher_id not in teachers:
        raise HTTPException(status_code=404, detail="Teacher not found")
    del teachers[teacher_id]
    return None

# # -----------------------------------------------------------------------------
# # Address endpoints
# # -----------------------------------------------------------------------------

# def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
#     return Health(
#         status=200,
#         status_message="OK",
#         timestamp=datetime.utcnow().isoformat() + "Z",
#         ip_address=socket.gethostbyname(socket.gethostname()),
#         echo=echo,
#         path_echo=path_echo
#     )

# @app.get("/health", response_model=Health)
# def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
#     # Works because path_echo is optional in the model
#     return make_health(echo=echo, path_echo=None)

# @app.get("/health/{path_echo}", response_model=Health)
# def get_health_with_path(
#     path_echo: str = Path(..., description="Required echo in the URL path"),
#     echo: str | None = Query(None, description="Optional echo string"),
# ):
#     return make_health(echo=echo, path_echo=path_echo)

# @app.post("/addresses", response_model=AddressRead, status_code=201)
# def create_address(address: AddressCreate):
#     if address.id in addresses:
#         raise HTTPException(status_code=400, detail="Address with this ID already exists")
#     addresses[address.id] = AddressRead(**address.model_dump())
#     return addresses[address.id]

# @app.get("/addresses", response_model=List[AddressRead])
# def list_addresses(
#     street: Optional[str] = Query(None, description="Filter by street"),
#     city: Optional[str] = Query(None, description="Filter by city"),
#     state: Optional[str] = Query(None, description="Filter by state/region"),
#     postal_code: Optional[str] = Query(None, description="Filter by postal code"),
#     country: Optional[str] = Query(None, description="Filter by country"),
# ):
#     results = list(addresses.values())

#     if street is not None:
#         results = [a for a in results if a.street == street]
#     if city is not None:
#         results = [a for a in results if a.city == city]
#     if state is not None:
#         results = [a for a in results if a.state == state]
#     if postal_code is not None:
#         results = [a for a in results if a.postal_code == postal_code]
#     if country is not None:
#         results = [a for a in results if a.country == country]

#     return results

# @app.get("/addresses/{address_id}", response_model=AddressRead)
# def get_address(address_id: UUID):
#     if address_id not in addresses:
#         raise HTTPException(status_code=404, detail="Address not found")
#     return addresses[address_id]

# @app.patch("/addresses/{address_id}", response_model=AddressRead)
# def update_address(address_id: UUID, update: AddressUpdate):
#     if address_id not in addresses:
#         raise HTTPException(status_code=404, detail="Address not found")
#     stored = addresses[address_id].model_dump()
#     stored.update(update.model_dump(exclude_unset=True))
#     addresses[address_id] = AddressRead(**stored)
#     return addresses[address_id]

# # -----------------------------------------------------------------------------
# # Person endpoints
# # -----------------------------------------------------------------------------
# @app.post("/persons", response_model=PersonRead, status_code=201)
# def create_person(person: PersonCreate):
#     # Each person gets its own UUID; stored as PersonRead
#     person_read = PersonRead(**person.model_dump())
#     persons[person_read.id] = person_read
#     return person_read

# @app.get("/persons", response_model=List[PersonRead])
# def list_persons(
#     uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
#     first_name: Optional[str] = Query(None, description="Filter by first name"),
#     last_name: Optional[str] = Query(None, description="Filter by last name"),
#     email: Optional[str] = Query(None, description="Filter by email"),
#     phone: Optional[str] = Query(None, description="Filter by phone number"),
#     birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
#     city: Optional[str] = Query(None, description="Filter by city of at least one address"),
#     country: Optional[str] = Query(None, description="Filter by country of at least one address"),
# ):
#     results = list(persons.values())

#     if uni is not None:
#         results = [p for p in results if p.uni == uni]
#     if first_name is not None:
#         results = [p for p in results if p.first_name == first_name]
#     if last_name is not None:
#         results = [p for p in results if p.last_name == last_name]
#     if email is not None:
#         results = [p for p in results if p.email == email]
#     if phone is not None:
#         results = [p for p in results if p.phone == phone]
#     if birth_date is not None:
#         results = [p for p in results if str(p.birth_date) == birth_date]

#     # nested address filtering
#     if city is not None:
#         results = [p for p in results if any(addr.city == city for addr in p.addresses)]
#     if country is not None:
#         results = [p for p in results if any(addr.country == country for addr in p.addresses)]

#     return results

# @app.get("/persons/{person_id}", response_model=PersonRead)
# def get_person(person_id: UUID):
#     if person_id not in persons:
#         raise HTTPException(status_code=404, detail="Person not found")
#     return persons[person_id]

# @app.patch("/persons/{person_id}", response_model=PersonRead)
# def update_person(person_id: UUID, update: PersonUpdate):
#     if person_id not in persons:
#         raise HTTPException(status_code=404, detail="Person not found")
#     stored = persons[person_id].model_dump()
#     stored.update(update.model_dump(exclude_unset=True))
#     persons[person_id] = PersonRead(**stored)
#     return persons[person_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
