import time

# user_id -> last message timestamp
_last_message = {}

# seconds
COOLDOWN = 3


def is_on_cooldown(user_id):

    now = time.time()

    if user_id not in _last_message:
        _last_message[user_id] = now
        return False

    diff = now - _last_message[user_id]

    if diff < COOLDOWN:
        return True

    _last_message[user_id] = now
    return False