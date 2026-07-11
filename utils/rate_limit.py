import time

# user_id -> last message time
_last_message = {}

# user_id -> last message content
_last_content = {}

COOLDOWN = 2  # seconds


def is_rate_limited(user_id, message):

    now = time.time()

    # Same message spam
    if (
        user_id in _last_content
        and _last_content[user_id] == message
    ):
        return True

    # Cooldown
    if (
        user_id in _last_message
        and now - _last_message[user_id] < COOLDOWN
    ):
        return True

    _last_message[user_id] = now
    _last_content[user_id] = message

    return False