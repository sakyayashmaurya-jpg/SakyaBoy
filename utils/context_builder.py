from utils.personality import get_personality
from utils.emotions import detect_emotion
from utils.relevant_memory import get_relevant_memories


def build_context(
    history,
    memories,
    level,
    clean_message
):

    context = []

    # -------------------------
    # Personality
    # -------------------------
    context.append({
        "role": "system",
        "content": get_personality(level)
    })

    # -------------------------
    # Emotion
    # -------------------------
    emotion = detect_emotion(clean_message)

    context.append({
        "role": "system",
        "content": f"""
Current user emotion: {emotion}

Match the emotion naturally.
Don't mention the emotion explicitly.
"""
    })

    # -------------------------
    # Relevant Memories Only
    # -------------------------
    relevant_memories = get_relevant_memories(
        memories,
        clean_message
    )

    if relevant_memories:

        memory_text = "\n".join(
            f"{k}: {v}"
            for k, v in relevant_memories.items()
        )

        context.append({
            "role": "system",
            "content": f"""
Relevant user facts:

{memory_text}

Use them only when helpful.
Don't dump memories.
"""
        })

    # -------------------------
    # Recent History
    # -------------------------
    context.extend(history)

    return context