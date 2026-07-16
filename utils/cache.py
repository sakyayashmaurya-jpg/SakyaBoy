import time

# question -> (answer, timestamp)
_cache = {}

CACHE_TIME = 60 * 60  # 1 hour


def get_cached_reply(question):

    question = question.lower().strip()

    data = _cache.get(question)

    if data is None:
        return None

    reply, created = data

    # Expired
    if time.time() - created > CACHE_TIME:
        del _cache[question]
        return None

    return reply


def save_cached_reply(question, reply):

    question = question.lower().strip()

    _cache[question] = (
        reply,
        time.time()
    )


def clear_cache():
    _cache.clear()


def cache_size():
    return len(_cache)