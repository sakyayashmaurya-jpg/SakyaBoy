import aiosqlite

DATABASE = "data/sakyaboy.db"


async def init_db():
    async with aiosqlite.connect(DATABASE) as db:

        # Users Table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            friendship INTEGER DEFAULT 0,
            nickname TEXT DEFAULT ''
        )
        """)

        # Messages Table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Friendship Table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS friendships (
            user_id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            messages INTEGER DEFAULT 0,
            last_seen TEXT DEFAULT '',
            mood TEXT DEFAULT 'neutral'
        )
        """)

        # Memories Table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # AI Cache Table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS ai_cache (
            question TEXT PRIMARY KEY,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()

    print("✅ Database Ready")


# ==========================
# USERS
# ==========================

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


# ==========================
# MESSAGES
# ==========================

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


# ==========================
# FRIENDSHIP SYSTEM
# ==========================

async def update_friendship(user_id):
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO friendships(user_id)
            VALUES(?)
            """,
            (user_id,)
        )

        await db.execute(
            """
            UPDATE friendships
            SET
                xp = xp + 5,
                messages = messages + 1,
                last_seen = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (user_id,)
        )

        cursor = await db.execute(
            """
            SELECT xp
            FROM friendships
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = await cursor.fetchone()

        xp = row[0]
        level = (xp // 100) + 1

        await db.execute(
            """
            UPDATE friendships
            SET level = ?
            WHERE user_id = ?
            """,
            (level, user_id)
        )

        await db.commit()


async def get_friendship(user_id):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT xp, level, messages, mood
            FROM friendships
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return await cursor.fetchone()


# ==========================
# SMART MEMORY
# ==========================

async def save_memory(user_id, key, value):
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            DELETE FROM memories
            WHERE user_id = ?
            AND memory_key = ?
            """,
            (user_id, key)
        )

        await db.execute(
            """
            INSERT INTO memories(
                user_id,
                memory_key,
                memory_value
            )
            VALUES(?, ?, ?)
            """,
            (user_id, key, value)
        )

        await db.commit()


async def get_memories(user_id):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT memory_key, memory_value
            FROM memories
            WHERE user_id = ?
            """,
            (user_id,)
        )

        rows = await cursor.fetchall()

    return {
        key: value
        for key, value in rows
    }