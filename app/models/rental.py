from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Rental(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    scooter_id: Mapped[int] = mapped_column(ForeignKey("scooter.id"))
    customer: Mapped["Customer"] = relationship(back_populates="rentals")
    scooter: Mapped["Scooter"] = relationship(back_populates="rentals")
    is_returned: Mapped[bool] = mapped_column(default=False)