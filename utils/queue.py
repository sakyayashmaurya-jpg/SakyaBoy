import asyncio

# Maximum AI requests processed at the same time.
# Start with 2. You can increase later if needed.
_ai_semaphore = asyncio.Semaphore(2)


async def run_ai(task):

    async with _ai_semaphore:
        return await task()