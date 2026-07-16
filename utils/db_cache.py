import aiosqlite

from utils.logger import logger

DATABASE = "data/sakyaboy.db"


async def get_cached_reply(question):

    question = question.lower().strip()

    logger.info(f"DB Lookup -> '{question}'")

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT answer
            FROM ai_cache
            WHERE LOWER(TRIM(question)) = ?
            """,
            (question,)
        )

        row = await cursor.fetchone()

    if row:
        logger.info("SQLite Cache Found")
        return row[0]

    logger.info("SQLite Cache Not Found")
    return None


async def save_cached_reply(question, answer):

    question = question.lower().strip()

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR REPLACE INTO ai_cache
            (question, answer)
            VALUES (?, ?)
            """,
            (
                question,
                answer
            )
        )

        await db.commit()

    logger.info(f"Saved SQLite Cache -> '{question}'")


async def delete_old_cache(days=7):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            DELETE FROM ai_cache
            WHERE created_at <
            datetime('now', ?)
            """,
            (f"-{days} days",)
        )

        await db.commit()


async def cache_count():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM ai_cache
            """
        )

        row = await cursor.fetchone()

    return row[0]