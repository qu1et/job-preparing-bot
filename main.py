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
    PicklePersistence,
)
from handlers.greet_handlers import (
    start,
    get_answer,
    get_spec,
    get_name,
    get_sub,
    provide_payment,
)
from handlers.menu_handlers import(
    main_menu,
    get_questions_training,
    select_specialty,
    navigate_question,
)
from config.states import (
    START,
    GET_NAME,
    GET_SPEC,
    OFFER_SUB,
    PAYMENT,
    MAIN_MENU,
    QUESTIONS_MENU,
    QUIZ,
    SELECT_SPECIALTY,
    QUESTION_CARD,
)
from db.database import create_tables

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    persistent = PicklePersistence('bot_cache')
    application = (
        ApplicationBuilder().token(os.getenv("TOKEN")).persistence(persistent).post_init(create_tables).build()
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


            # main menu
            MAIN_MENU: [
                CallbackQueryHandler(callback=get_questions_training, pattern="get_questions")
            ],
            QUESTIONS_MENU: [
                CallbackQueryHandler(callback=main_menu, pattern="back_to_menu"),
            ],
            SELECT_SPECIALTY: [
                CallbackQueryHandler(callback=select_specialty, pattern="specialty_QA"),
                CallbackQueryHandler(callback=select_specialty, pattern="specialty_Backend"),
                CallbackQueryHandler(callback=select_specialty, pattern="specialty_Frontend"),
                CallbackQueryHandler(callback=main_menu, pattern="back_to_menu"),
            ],
            QUESTION_CARD: [
                CallbackQueryHandler(callback=navigate_question, pattern="next_question"),
                CallbackQueryHandler(callback=navigate_question, pattern="prev_question"),
                CallbackQueryHandler(callback=main_menu, pattern="back_to_menu"),
            ],
            QUIZ:[
            ]
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name='conv_handler'
    )

    application.add_handler(conv_handler)

    application.run_polling()
