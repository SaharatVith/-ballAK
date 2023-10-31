from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
