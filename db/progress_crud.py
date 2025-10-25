import aiosqlite


async def add_progress(user_id: int, question_num: int, category: str):
    async with aiosqlite.connect("data.db") as conn:
        await conn.execute(
            "INSERT INTO questions_progress (user_id, question_id, category) VALUES (?, ?, ?)",
            (user_id, question_num, category),
        )
        await conn.commit()
    return True


async def update_progress(user_id: int, question_num: int, category: str):
    async with aiosqlite.connect("data.db") as conn:
        await conn.execute(
            """UPDATE questions_progress
                SET question_num = ?
                WHERE user_id = ? AND category = ?""",
            (question_num, user_id, category),
        )
        await conn.commit()
    return True


async def get_progress(user_id: int, category: str):
    async with aiosqlite.connect("data.db") as conn:
        question = await conn.execute(
            "SELECT question_num FROM questions_progress WHERE user_id = ? AND category = ?",
            (user_id, category),
        )
        return await question.fetchone()


async def delete_progress(user_id: int, category: str):
    async with aiosqlite.connect("data.db") as conn:
        await conn.execute(
            "DELETE FROM questions_progress WHERE user_id = ? AND category = ?",
            (user_id, category),
        )
        await conn.commit()
    return True
