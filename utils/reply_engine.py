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


MAX_MESSAGE_LENGTH = 400


async def generate_reply(
    history,
    memories,
    level,
    clean_message
):
    start = time.perf_counter()

    # -------------------------
    # Trim very long messages
    # -------------------------
    clean_message = clean_message.strip()

    if len(clean_message) > MAX_MESSAGE_LENGTH:
        clean_message = clean_message[:MAX_MESSAGE_LENGTH]

    # -------------------------
    # Fun Replies
    # -------------------------
    reply = fun_reply(clean_message)

    if reply:
        logger.info(
            f"Fun reply | {clean_message[:40]}"
        )
        return reply

    # -------------------------
    # Humanizer
    # -------------------------
    reply = random_small_reply()

    if reply:
        logger.info("Random human reply")
        return reply

    # -------------------------
    # Keep only recent history
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

        elapsed = time.perf_counter() - start

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