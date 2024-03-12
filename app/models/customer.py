from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rentals: Mapped["Rental"] = relationship(back_populates="customer")
    name: Mapped[str]
    email: Mapped[str] = mapped_column(db.String(50))
    phone: Mapped[str] = mapped_column(db.String(25))
