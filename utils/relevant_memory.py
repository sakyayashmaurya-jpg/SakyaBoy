def get_relevant_memories(memories, message):

    if not memories:
        return {}

    msg = message.lower()

    keywords = {
        "game": ["game", "play", "minecraft", "gaming"],
        "favorite_game": ["game", "play", "minecraft", "gaming"],

        "food": ["food", "eat", "hungry", "dinner", "lunch", "breakfast"],
        "favorite_food": ["food", "eat", "hungry", "dinner", "lunch", "breakfast"],

        "music": ["song", "music", "singer", "playlist"],
        "favorite_singer": ["song", "music", "singer", "playlist"],

        "pet": ["dog", "cat", "pet", "animal"],

        "birthday": ["birthday", "born", "age"],

        "youtube": ["youtube", "channel", "video", "upload"],
        "youtube_channel": ["youtube", "channel", "video", "upload"],
    }

    relevant = {}

    for key, value in memories.items():

        if key in keywords:

            if any(word in msg for word in keywords[key]):
                relevant[key] = value

    return relevant