import aiosqlite

DATABASE = "data/sakyaboy.db"


async def init_db():
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            friendship INTEGER DEFAULT 0,
            nickname TEXT DEFAULT ''
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()

    print("✅ Database Ready")


async def save_user(user_id, username):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (user_id, username)
            VALUES (?, ?)
            """,
            (user_id, username)
        )
        await db.commit()


async def save_message(user_id, role, content):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            (user_id, role, content)
        )
        await db.commit()


async def get_history(user_id, limit=10):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )

        rows = await cursor.fetchall()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]