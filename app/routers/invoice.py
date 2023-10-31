from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app import models
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/")
def get_all_invoice(request: Request, db: Session = Depends(get_db)):
    invoices = db.query(models.Invoice).all()
    return templates.TemplateResponse(
        "invoice.html", {"request": request, "invoices": invoices}
    )


@router.get("/{id}")
def get_invoice(id: str, request: Request, db: Session = Depends(get_db)):
    # Query the Invoice by ID
    invoice = db.query(models.Invoice).filter(models.Invoice.id == id).first()

    # Query the associated InvoiceItems by referencing the relationship (assuming you've defined the relationship in your SQLAlchemy models)
    invoice_items = invoice.items  # Assuming the relationship is named 'invoice_items'
    total_price = sum([(i.price * i.quantity) for i in invoice_items])
    # print(inv)
    # invoice_sum =

    return templates.TemplateResponse(
        "invoice_management.html",
        {
            "request": request,
            "invoice": invoice,
            "invoice_items": invoice_items,
            "total_price": total_price,
        },
    )


@router.post("/create_item")
def create_new_invoice_item(
    invoice_id: int = Form(...),
    description: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    invoice_item = models.InvoiceItem(
        description=description, quantity=quantity, price=price, invoice_id=invoice_id
    )
    db.add(invoice_item)
    db.commit()
    db.refresh(invoice_item)

    return {"message": "created invoice item"}


class UpdateInvoiceItem(BaseModel):
    description: str
    quantity: int
    price: float


@router.post("/update_item")
def update_invoice_item(
    id: int = Form(...),
    description: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    invoice_item = (
        db.query(models.InvoiceItem).filter(models.InvoiceItem.id == id).first()
    )
    if invoice_item:
        invoice_item.description = description
        invoice_item.quantity = quantity
        invoice_item.price = price
        db.commit()
        return {"message": "Invoice item updated"}
    else:
        return {"message": "Invoice item not found"}


@router.post("/delete_item")
def delete_item(id: int = Form(...), db: Session = Depends(get_db)):
    invoice_item = db.query(models.InvoiceItem).filter(models.InvoiceItem.id == id)
    invoice_item.delete(synchronize_session=False)
    db.commit()
    return {"message": "Invoice item delete"}


@router.post("/paid")
def paid_invoice(id: int = Form(...), db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == id).first()
    invoice.is_paid = True
    invoice.paid_at = datetime.now()
    db.commit()
    return {"message": "This invoice is paid"}


@router.post("/new_invoice/create")
def create_new_invoice_only(title: str = Form(...), db: Session = Depends(get_db)):
    print(title)
    _new_invoice = models.Invoice(title=title)
    db.add(_new_invoice)
    db.commit()
    db.refresh(_new_invoice)

    return {"message": "Created invoice"}
