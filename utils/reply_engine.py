import asyncio
import time

from groq import RateLimitError

from utils.fun import fun_reply
from utils.ai import ask_ai
from utils.humanizer import (
    random_small_reply,
    random_typing_delay
)
from utils.context_builder import build_context
from utils.logger import logger

# RAM Cache
from utils.cache import (
    get_cached_reply,
    save_cached_reply
)

# SQLite Cache
from utils.db_cache import (
    get_cached_reply as get_db_cached_reply,
    save_cached_reply as save_db_cached_reply
)

MAX_MESSAGE_LENGTH = 400


async def generate_reply(
    history,
    memories,
    level,
    clean_message
):
    start = time.perf_counter()

    # -------------------------
    # Clean Message
    # -------------------------
    clean_message = clean_message.strip().lower()

    if len(clean_message) > MAX_MESSAGE_LENGTH:
        clean_message = clean_message[:MAX_MESSAGE_LENGTH]

    # -------------------------
    # Fun Replies
    # -------------------------
    reply = fun_reply(clean_message)

    if reply:
        logger.info(f"Fun reply | {clean_message[:40]}")
        return reply

    # -------------------------
    # Random Human Reply
    # -------------------------
    reply = random_small_reply()

    if reply:
        logger.info("Random human reply")
        return reply

    # -------------------------
    # RAM Cache
    # -------------------------
    cached = get_cached_reply(clean_message)

    if cached:
        logger.info(f"RAM Cache Hit | {clean_message[:40]}")
        return cached

    # -------------------------
    # SQLite Cache
    # -------------------------
    cached = await get_db_cached_reply(clean_message)

    if cached:

        logger.info(f"SQLite Cache Hit | {clean_message[:40]}")

        # Load into RAM
        save_cached_reply(
            clean_message,
            cached
        )

        return cached

    logger.info(f"Cache Miss | {clean_message[:40]}")

    # -------------------------
    # Recent History
    # -------------------------
    history = history[-4:]

    messages = build_context(
        history=history,
        memories=memories,
        level=level,
        clean_message=clean_message
    )

    try:

        await asyncio.sleep(
            random_typing_delay()
        )

        reply = ask_ai(
            messages,
            clean_message
        )

        # -------------------------
        # Save RAM Cache
        # -------------------------
        save_cached_reply(
            clean_message,
            reply
        )

        # -------------------------
        # Save SQLite Cache
        # -------------------------
        await save_db_cached_reply(
            clean_message,
            reply
        )

        elapsed = (
            time.perf_counter() - start
        )

        logger.info(
            f"AI replied in {elapsed:.2f}s"
        )

        return reply

    except RateLimitError:

        logger.warning(
            "Groq rate limit reached."
        )

        return (
            "😭 Bhai mera AI quota abhi khatam ho gaya.\n"
            "2-5 minute baad fir try kar."
        )

    except Exception as e:

        logger.exception(e)

        return (
            "😭 Kuch technical problem aa gayi.\n"
            "Thodi der baad fir try kar."
        )
    