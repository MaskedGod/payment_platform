from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.payments.models import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(
        self,
        user_id: int,
        payment_type: str,
        amount: float,
        currency: str = "EUR",
        status: str = "PENDING",
    ):
        """
        Создает новый платеж в базе данных.
        :param user_id: ID пользователя, инициировавшего платеж.
        :param payment_type: Тип платежа (например, "DEPOSIT", "WITHDRAWAL").
        :param amount: Сумма платежа.
        :param currency: Валюта платежа (по умолчанию "EUR").
        :param status: Статус платежа (по умолчанию "PENDING").
        :return: Созданный объект платежа.
        """
        new_payment = Payment(
            user_id=user_id,
            payment_type=payment_type,
            amount=amount,
            currency=currency,
            status=status,
        )
        self.session.add(new_payment)
        await self.session.commit()
        await self.session.refresh(new_payment)
        return new_payment

    async def update_payment_status(self, payment_id: int, status: str):
        """
        Обновляет статус платежа в базе данных.
        :param payment_id: ID платежа.
        :param status: Новый статус платежа.
        :return: Обновленный объект платежа.
        """
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        payment = result.scalars().first()

        if not payment:
            raise ValueError(f"Платеж с ID {payment_id} не найден")

        payment.status = status
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_payment_by_id(self, payment_id: int):
        """
        Получает платеж по его ID.
        :param payment_id: ID платежа.
        :return: Объект платежа или None, если платеж не найден.
        """
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_payments_by_user(
        self, user_id: int, limit: int = 10, offset: int = 0
    ):
        """
        Получает список платежей пользователя.
        :param user_id: ID пользователя.
        :param limit: Максимальное количество записей (по умолчанию 10).
        :param offset: Количество пропускаемых записей (по умолчанию 0).
        :return: Список платежей.
        """
        query = (
            select(Payment)
            .where(Payment.user_id == user_id)
            .order_by(Payment.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
