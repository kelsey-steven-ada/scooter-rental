from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Scooter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rentals: Mapped["Rental"] = relationship(back_populates="scooter")
    model: Mapped[str]
    charge_percent: Mapped[float]
