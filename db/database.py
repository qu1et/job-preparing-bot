import aiosqlite


async def create_tables(app):
    conn = await aiosqlite.connect("data.db")
    await conn.execute('''CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_tg INTEGER UNIQUE NOT NULL,
                        name TEXT(100) NULL,
                        sub_end_date DATETIME NULL,
                        sub_ban_date DATETIME NULL)''')
    await conn.commit()

    await conn.execute('''CREATE TABLE IF NOT EXISTS data(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       profession TEXT NULL,
                       FOREIGN KEY(user_id) REFERENCES users(id))''')
    await conn.commit()
    await conn.close()
