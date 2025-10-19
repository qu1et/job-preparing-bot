from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    SELECT_SPECIALTY,
    QUESTION_CARD,
    MAIN_MENU,
)
from db.question_crud import (
    get_questions,
)
from utils.markdown_redactor import (
    escape_markdown_v2,
)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = [
        [InlineKeyboardButton("Тренировка вопросов", callback_data="get_questions")],
        [InlineKeyboardButton("Подписка", callback_data="manage_subscribtion")],
        [InlineKeyboardButton("Тренажер собеседований", callback_data="get_training")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if query:
        await update.callback_query.edit_message_text(
            text="Меню", reply_markup=markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_user.id, text="Меню", reply_markup=markup
        )
    return MAIN_MENU


async def get_questions_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = [
        [InlineKeyboardButton("QA", callback_data="specialty_QA")],
        [InlineKeyboardButton("Backend", callback_data="specialty_Backend")],
        [InlineKeyboardButton("Frontend", callback_data="specialty_Frontend")],
        [InlineKeyboardButton("Назад ⬅️", callback_data="back_to_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if query:
        await update.callback_query.edit_message_text(
            text="Выберите специальность для изучения вопросов:",
            reply_markup=markup,
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Выберите специальность для изучения вопросов:",
            reply_markup=markup,
        )
    return SELECT_SPECIALTY


async def select_specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    specialty = query.data.replace("specialty_", "")
    questions = await get_questions(specialty)
    
    if not questions:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=f"Вопросы для специальности {specialty} пока не добавлены."
        )
        return await get_questions_training(update, context)

    context.user_data['questions'] = questions
    context.user_data['current_question_index'] = 0
    context.user_data['specialty'] = specialty
    return await show_question_card(update, context)


async def show_question_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    questions = context.user_data.get('questions', [])
    current_index = context.user_data.get('current_question_index', 0)
    if not questions or current_index >= len(questions):
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Вопросы не найдены."
        )
        return await get_questions_training(update, context)
    question = questions[current_index]

    keyboard = []
    nav_buttons = []
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Предыдущий", callback_data="prev_question"))
    if current_index < len(questions) - 1:
        nav_buttons.append(InlineKeyboardButton("Следующий ➡️", callback_data="next_question"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")])
    markup = InlineKeyboardMarkup(keyboard)
    card_text = f"📋 **Вопрос {current_index + 1} из {len(questions)}**\n\n"
    card_text += f"**{escape_markdown_v2(question[1])}**\n\n"
    card_text += f"*{escape_markdown_v2(question[2])}*\n\n"
    card_text += f"**Ответ:**\n||{escape_markdown_v2(question[3])}||"
    
    if query:
        await update.callback_query.delete_message()
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=card_text,
            reply_markup=markup,
            parse_mode="MarkdownV2"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=card_text,
            reply_markup=markup,
            parse_mode="MarkdownV2"
        )
    return QUESTION_CARD


async def navigate_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    current_index = context.user_data.get('current_question_index', 0)
    if query.data == "next_question":
        context.user_data['current_question_index'] = current_index + 1
    elif query.data == "prev_question":
        context.user_data['current_question_index'] = current_index - 1
    return await show_question_card(update, context)

