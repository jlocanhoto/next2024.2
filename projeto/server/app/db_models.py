from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(sql.String(255))
    email: Mapped[str] = mapped_column(sql.String(255))
    phone: Mapped[str] = mapped_column(sql.String(255))
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=sql.func.now())
