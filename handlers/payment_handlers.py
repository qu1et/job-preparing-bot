import uuid
from yookassa import Payment
from telegram.ext import ContextTypes
from config.config import SHOP_ID, SECRET_KEY_YOUKASSA, PRICE


async def yookassa_payment(context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("phone"):
        phone = context.user_data.get("phone")
    price = str(PRICE)
    payment_process = Payment.create(
        {
            "amount": {"value": f"{price}", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/it_vacancies_train_bot",
            },
            "capture": True,
            "description": 'Программа "Из минуса в плюс"',
            # "receipt": {
            #     "customer": {"phone": f"{phone}"},
            #     "items": [
            #         {
            #             "description": 'Программа "Из минуса в плюс"',
            #             "quantity": "1",
            #             "amount": {"value": f"{price}", "currency": "RUB"},
            #             "vat_code": "1",
            #         },
            #     ],
            # },
        },
        uuid.uuid4(),
    )

    payment_id = payment_process.id
    context.user_data["counter"] = 0
    context.user_data["payment"] = payment_process
    payment = Payment.find_one(payment_id)

    if payment.confirmation and payment.confirmation.type == "redirect":
        return payment.confirmation.confirmation_url
