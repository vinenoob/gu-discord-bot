def find_watch_word(message: str, watch_list: list) -> tuple:
    """
    Finds the first watch word/phrase from watch_list in message, respecting word boundaries.
    Supports both single-word and multi-word watch phrases.
    Returns (index, matched_watch) if found, or (-1, "") if not found.
    """
    for watch in watch_list:
        indx = message.lower().find(watch.lower())
        if indx == -1:
            continue
        end_pos = indx + len(watch)
        # Check end boundary: next char shouldn't be alphanumeric
        if end_pos < len(message) and message[end_pos].isalnum():
            continue
        # Check start boundary: previous char shouldn't be alphanumeric
        if indx > 0 and message[indx - 1].isalnum():
            continue
        return indx, watch
    return -1, ""
