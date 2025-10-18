def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

if __name__ == "__main__":
    print(escape_markdown_v2("ПРивет."))