import asyncio
import time

from utils.fun import fun_reply
from utils.ai import ask_ai
from utils.humanizer import (
    random_small_reply,
    random_typing_delay
)
from utils.context_builder import build_context
from utils.logger import logger


async def generate_reply(
    history,
    memories,
    level,
    clean_message
):
    start = time.perf_counter()

    # Fun replies first
    reply = fun_reply(clean_message)

    if reply:
        logger.info(
            f"Fun reply | Message: {clean_message}"
        )
        return reply

    # Random human replies
    reply = random_small_reply()

    if reply:
        logger.info(
            "Random human reply used"
        )
        return reply

    # Build AI Context
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
            f"AI replied in {elapsed:.2f}s | User: {clean_message[:40]}"
        )

        return reply

    except Exception as e:

        logger.exception(
            f"AI Error: {e}"
        )

        return "Abe 😭 mera dimaag thoda hang ho gaya... ek baar fir bol."