from dataclasses import dataclass
import aiosqlite
from questions import QUESTION

@dataclass
class Question:
    id: int
    question_title: str
    question_body: str
    answer: str
    image_name: str



async def create_question(**kwargs) -> Question:
    async with aiosqlite.connect("data.db") as conn:
        conn.row_factory = aiosqlite.Row
        
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        
        print(f'Inserting: {columns} with values {values}')
        await conn.execute(f"INSERT INTO questions ({columns}) VALUES ({placeholders})", values)
        await conn.commit()
    return True


async def get_question(id: int) -> Question:
    async with aiosqlite.connect("data.db") as conn:
        conn.row_factory = aiosqlite.Row
        res = await conn.execute("SELECT * FROM questions WHERE id = ?", (id,))
        obj = await res.fetchone()
        return Question(**obj)


async def update_question(id: int, **kwargs):
    async with aiosqlite.connect("data.db") as conn:
        conn.row_factory = aiosqlite.Row
        for param, value in kwargs.items():
            await conn.execute(f"UPDATE questions SET {param} = ? WHERE id = ?", (value, id))
        await conn.commit()
    return True


async def delete_question(id: int):
    async with aiosqlite.connect("data.db") as conn:
        await conn.execute("DELETE FROM questions WHERE id = ?", (id,))
        await conn.commit()
    return True


if __name__ == "__main__":
    import asyncio
    from questions import QUESTION

    async def main():
        for value in QUESTION.values():
            await create_question(**{"question_title": value["question_title"], "question_body": value["question_body"], "answer": value["answer"], "category": value["category"]})

    asyncio.run(main())
