from collections import defaultdict

# Har user ki recent conversation
conversation_history = defaultdict(list)

MAX_HISTORY = 20


def add_message(user_id, role, content):
    conversation_history[user_id].append({
        "role": role,
        "content": content
    })

    if len(conversation_history[user_id]) > MAX_HISTORY:
        conversation_history[user_id].pop(0)


def get_history(user_id):
    return conversation_history[user_id]