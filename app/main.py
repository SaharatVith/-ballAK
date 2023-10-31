from fastapi import FastAPI, Request, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app import models
from app.routers import router
from pydantic import BaseModel

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "rooms": rooms}
    )


@app.get("/room/detail/{room_id}")
def room_detail(room_id: str, request: Request, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    return templates.TemplateResponse(
        "room_detail.html", {"request": request, "room": room}
    )


@app.get("/contract")
def room_detail(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "contract.html",
        {
            "request": request,
        },
    )


@app.post("/contract/create")
async def submit_form(
    room_id: str = Form(...),
    name: str = Form(...),
    id_number: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    new_contract = models.Contract(
        room_id=room_id, name=name, id_number=id_number, phone=phone, message=message
    )

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return {"message": "Form submitted successfully"}


app.include_router(router=router, prefix="/admin")
