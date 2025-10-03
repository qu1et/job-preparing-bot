import aiosqlite

async def add_spec(id_tg: int, spec: str):
    async with aiosqlite.connect('data.db') as conn:
        await conn.execute('INSERT INTO data (user_id, profession) VALUES (?, ?)', (id_tg, spec,))
        await conn.commit()
    return True

async def get_user(id: int):
    async with aiosqlite.connect('data.db') as conn:
        user = await conn.execute('SELECT * FROM users WHERE id = ?', (id,))
        return await user.fetchone()
    
async def update_user(id_tg: int, data: str):
    async with aiosqlite.connect('data.db') as conn:
        await conn.execute(f'UPDATE users SET spec = ? WHERE id = ?', (data, id))
        await conn.commit()
    return True