from fastapi import APIRouter, status, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import get_db
from app import models
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/admin")


from pydantic import BaseModel


class RoomMeter(BaseModel):
    id: int
    room_id: int
    water_meter: float
    electric_meter: float
    # month: datetime
    # year: int


@router.get("/")
def get_all_rooms(request: Request, db: Session = Depends(get_db)):
    # from datetime import datetime

    # meters = db.query(models.Meter)
    rooms = db.query(models.Room)

    rooms_2 = []
    for i in rooms:
        latest_meter_data = (
            db.query(models.Meter)
            .filter_by(room_id=i.id)
            .order_by(
                desc(models.Meter.created_at)
            )  # Order by 'created_at' in descending order
            .limit(2)  # Limit to the latest 2 records
            .all()
        )
        if len(latest_meter_data) == 0:
            rooms_2.append(
                RoomMeter(id=i.id, room_id=i.room_id, water_meter=0, electric_meter=0)
            )
        elif len(latest_meter_data) == 1:
            rooms_2.append(
                RoomMeter(
                    id=i.id,
                    room_id=i.room_id,
                    water_meter=(latest_meter_data[0].water_meter_value),
                    electric_meter=latest_meter_data[0].electric_meter_value,
                )
            )
        else:
            rooms_2.append(
                RoomMeter(
                    id=i.id,
                    room_id=i.room_id,
                    water_meter=(
                        latest_meter_data[0].water_meter_value
                        - latest_meter_data[1].water_meter_value
                    ),
                    electric_meter=(
                        latest_meter_data[0].electric_meter_value
                        - latest_meter_data[1].electric_meter_value
                    ),
                )
            )

    return templates.TemplateResponse(
        "meters.html",
        {
            "request": request,
            "rooms": rooms_2,
        },
    )


@router.get("/room/{room_id}")
async def get_meter_room(room_id: int, request: Request, db: Session = Depends(get_db)):
    all_meter = (
        db.query(models.Meter)
        .filter_by(room_id=room_id)
        .order_by(desc(models.Meter.created_at))
    )
    return templates.TemplateResponse(
        "room_meters.html",
        {
            "request": request,
            "all_meters": all_meter,
            "the_room_id": room_id,
        },
    )


@router.post("/create_new_record")
async def create_new_record(
    the_room_id: int = Form(...),
    water_meter: float = Form(...),
    electric_meter: float = Form(...),
    db: Session = Depends(get_db),
):
    new_record = models.Meter(
        room_id=the_room_id,
        water_meter_value=water_meter,
        electric_meter_value=electric_meter,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "craeted"}
