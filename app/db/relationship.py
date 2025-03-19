from sqlalchemy.orm import relationship
from app.users.models import User
from app.payments.models import Payment

# Определяем отношения ПОСЛЕ загрузки моделей
User.payments = relationship(
    "Payment", back_populates="user", cascade="all, delete-orphan"
)
Payment.user = relationship("User", back_populates="payments")
