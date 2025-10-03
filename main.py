import logging
import os
from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from handlers.greet_handlers import (
    start,
    get_answer,
    get_spec,
    get_name,
    get_sub,
    provide_payment,
)
from config.states import (
    START,
    GET_NAME,
    GET_SPEC,
    OFFER_SUB,
    PAYMENT,
)
from db.database import create_tables

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(os.getenv("TOKEN")).post_init(create_tables).build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_answer,
                ),
            ],
            GET_NAME: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_name,
                )
            ],
            GET_SPEC: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_spec,
                )
            ],
            OFFER_SUB: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_sub,
                )
            ],
            PAYMENT: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=provide_payment,
                )
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
