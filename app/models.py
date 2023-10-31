from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    Text,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, nullable=False)
    room_id = Column(String, nullable=False)
    cover = Column(String, nullable=False)
    description = Column(String, nullable=True)
    room_type = Column(String, nullable=False)
    price = Column(Float, default=0)
    is_available = Column(Boolean, server_default="TRUE", default=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    room_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    message = Column(Text, nullable=True)

    # room_id: str
    # name: str
    # id_number: str
    # phone: str
    # message: str


class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))

    # Define a relationship to link an InvoiceItem to an Invoice
    invoice = relationship("Invoice", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_paid = Column(Boolean, default=False)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    items = relationship("InvoiceItem", back_populates="invoice")
