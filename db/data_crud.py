import aiosqlite

async def add_spec(id_tg: int, spec: str):
    async with aiosqlite.connect('data.db') as conn:
        await conn.execute('INSERT INTO data (user_id, profession) VALUES (?, ?)', (id_tg, spec,))
        await conn.commit()
    return True
