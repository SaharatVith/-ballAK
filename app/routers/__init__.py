from fastapi import APIRouter
from app.routers import manager
from app.routers import room, invoice

router = APIRouter()

router.include_router(router=manager.router)
router.include_router(router=room.router, prefix="/room")
router.include_router(router=invoice.router, prefix="/invoice")
