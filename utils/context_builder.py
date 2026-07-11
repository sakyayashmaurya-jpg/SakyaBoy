from utils.personality import get_personality
from utils.emotions import detect_emotion


def build_context(
    history,
    memories,
    level,
    clean_message
):

    context = []

    # Personality
    context.append({
        "role": "system",
        "content": get_personality(level)
    })

    # Emotion
    emotion = detect_emotion(clean_message)

    context.append({
        "role": "system",
        "content": f"""
Current user emotion: {emotion}

Match the emotion naturally.
Don't mention the emotion explicitly.
"""
    })

    # Memories
    if memories:

        memory_text = "\n".join(
            f"{k}: {v}"
            for k, v in memories.items()
        )

        context.append({
            "role": "system",
            "content": f"""
Known user facts:

{memory_text}

Use them only when relevant.
Don't dump memories.
"""
        })

    context.extend(history)

    return context