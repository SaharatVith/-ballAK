from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app import models

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/")
def get_rooms_page_management(request: Request, db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return templates.TemplateResponse(
        "room_management.html", {"request": request, "rooms": rooms}
    )


@router.get("/{room_id}/edit")
def room_edit_management(room_id: str, request: Request, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    return templates.TemplateResponse(
        "room_edit.html", {"request": request, "room": room}
    )


class UpdateRoom(BaseModel):
    room_id: str
    cover: str
    description: str
    room_type: str
    price: str
    is_available: bool


@router.post("/update")
def room_update(
    room_id: str = Form(...),
    cover: str = Form(...),
    description: str = Form(...),
    room_type: str = Form(...),
    price: str = Form(...),
    is_available: bool = Form(default=False),
    db: Session = Depends(get_db),
):
    room_query = db.query(models.Room).filter(models.Room.room_id == room_id)
    # update data
    room_query.update(
        UpdateRoom(
            room_id=room_id,
            cover=cover,
            description=description,
            room_type=room_type,
            price=price,
            is_available=is_available,
        ).model_dump(),
        synchronize_session=False,
    )
    db.commit()  # commit database
    return {"message": "updated"}


@router.post("/")
def create_new_room(
    room_id: str = Form(...),
    cover: str = Form(...),
    description: str = Form(...),
    room_type: str = Form(...),
    price: str = Form(...),
    is_available: bool = Form(...),
    db: Session = Depends(get_db),
):
    new_room = models.Room(
        room_id=room_id,
        cover=cover,
        description=description,
        room_type=room_type,
        price=price,
        is_available=is_available,
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return {"message": "created"}


@router.post("/delete")
def delete_room(room_id: str = Form(...), db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id)
    if room.first() == None:
        return {"message": "failed"}
    room.delete(synchronize_session=False)
    db.commit()
    return {"message": "deleted"}
