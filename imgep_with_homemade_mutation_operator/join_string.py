def join_strings(strings, separator="\n"):
    """
    Joins a list of strings into a single string with a specified separator.

    :param strings: List of strings to join.
    :param separator: The separator to use between words (default is a space).
    :return: A single string containing all elements joined by the separator.
    """
    return separator.join(strings)

# Example usage:
#words = ["Hello", "world", "!"]
#result = join_strings(words)
#print(result)  # Output: Hello world !

