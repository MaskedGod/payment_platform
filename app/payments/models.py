# from sqlalchemy import DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from datetime import datetime, timezone

# from app.db.database import Base


# class Payment(Base):
#     __tablename__ = "payments"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     payment_type: Mapped[str] = mapped_column(String(20))
#     amount: Mapped[float] = mapped_column(Integer)
#     currency: Mapped[str] = mapped_column(String(3), default="EUR")
#     status: Mapped[str] = mapped_column(String(20), default="PENDING")
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
#     )

# user: Mapped["User"] = relationship("User", back_populates="payments")
