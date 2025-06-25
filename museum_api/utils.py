def escape_tg_reserved_characters(text: str) -> str:
    """
    Escapes specific characters in text with double backslashes. Used for Telegram bot,
    if parse mode is MarkdownV2, the characters are escaped with double backslashes.

    Args:
        text (str): The input text to escape characters in

    Returns:
        str: Text with escaped characters
    """
    characters_to_escape = ['.', '!', '?', '=', '/', '-', '_', '(', ')', '[', ']', '{', '}', '|', '`', '~', '^', '$']

    for char in characters_to_escape:
        text = text.replace(char, f'\\{char}')

    return text
