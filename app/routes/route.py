from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.config import manager
from app.db.db_action import get_user_by_token, get_db
from app.pydantic_models.pydantic import Message
from app.db.models import Student, Teacher, Course, Enrollment

router = APIRouter()

@router.websocket("/classes/{class_id}/ws/{token}")
async def class_chat(websocket: WebSocket, class_id: int, token: str):
    try:
        user = get_user_by_token(token)
        await manager.connect(class_id, user.username, websocket)
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    except:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return
    try:
        while True:
            data = await websocket.receive_json()
            msg = Message(**data)
            await manager.broadcast(class_id, msg, user.username)
    except WebSocketDisconnect:
        manager.disconnect(class_id, user.username)

@router.post("/students", response_model=list[Student])
def create_student(student: Student, db: Session = Depends(get_db)):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/students", response_model=list[Student])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/teachers", response_model=list[Teacher])
def create_teacher(teacher: Teacher, db: Session = Depends(get_db)):
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.get("/teachers", response_model=list[Teacher])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()

@router.post("/courses", response_model=list[Course])
def create_course(course: Course, db: Session = Depends(get_db)):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/courses", response_model=list[Course])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.post("/enrollments", response_model=list[Enrollment])
def create_enrollment(enrollment: Enrollment, db: Session = Depends(get_db)):
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.get("/enrollments", response_model=list[Enrollment])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()