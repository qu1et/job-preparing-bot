from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    START,
    GET_NAME,
    GET_SPEC,
    OFFER_SUB,
    PAYMENT,
)
from db.user_crud import (
    create_user,
    get_user,
    update_user,
)
from db.data_crud import (
    add_spec,
)
from handlers.menu_handlers import main_menu
from logs.logger import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)
    if not user:
        user = await create_user(update.effective_user.id)
        logger.info(f'Пользователь {update.effective_user.username} создан ℹ️')
    if context.user_data.get('is_subed'):
        return await main_menu(update, context)
    keyboard = [["Да", "Нет"]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Продолжим?",
        resize_keyboard=True,
    )
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Привет! Хочешь получать актуальные вакансии и получить материалы для подготовки и практики собеседований?",
        reply_markup=markup,
    )
    return START


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    keyboard = [[update.effective_user.first_name]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Как можно обращаться к тебе?",
        resize_keyboard=True,
    )
    if answer.strip().lower() == "да":
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Как можно обращаться к тебе?",
            reply_markup=markup,
        )
        return GET_NAME
    else:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Ко мне можно обратиться в любое время",
        )
        return START


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    await update_user(update.effective_user.id, "name", name)
    keyboard = [
        ["Backend", "Frontend", "Mobile", "QA"],
        ["Analytics", "Managment", "Design & UX",], 
        ["Infrastructure & DevOps", "Informations Security"],
        ["Data & ML"]
    ]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Выберите вашу специальность:",
    )
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Выберите вашу специальность",
        reply_markup=markup,
    )
    return GET_SPEC


async def get_spec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spec = update.effective_message.text
    await add_spec(update.effective_user.id, spec)
    keyboard = [["Оформить", "Отказаться"]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Желаете оформить подписку?",
        resize_keyboard=True,
    )
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Оформите подписку и получите доступ к вакансиям и тренировочным собеседованиям",
        reply_markup=markup,
    )
    return OFFER_SUB


async def get_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if answer.strip().lower() == 'оформить':
        context.user_data['is_subed'] = True
        logger.info(f'Пользователь {update.effective_user.username} перешел к оформлению подписки ℹ️')
        return PAYMENT
    else:
        logger.info(f'Пользователь {update.effective_user.username} отказался от подписки ℹ️')
        return await main_menu(update, context)


async def provide_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await main_menu(update, context)
