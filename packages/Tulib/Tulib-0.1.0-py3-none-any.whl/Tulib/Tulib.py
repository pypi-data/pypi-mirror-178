def W2L(words):
    """
    Creates a list from a given string, seperating each word by a space.

    :param words: String the list is created with.
    :type words: str

    :return: A list of words got from the string.
    :rtype: list
    """

    word = ""
    wordlist = []
    for char in words:
        if char == " ":
            if word != "":
                wordlist.append(word)
            word = ""
        else:
            word += char
    if word != "":
        wordlist.append(word)
    return wordlist
