def include(text, items):
    for item in items:
        if item in text:
            return True
    return False


def includeNumber(text):
    return include(text, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])


def removeQuotation(token):
    return token.replace("\"", "").replace("\'", "")


def type_convert(token):
    if includeNumber(token) and include(token, ".") and not include(token, ["\"", "\'"]):
        return float(token)
    elif includeNumber(token) and include(token, ".") and include(token, ["\"", "\'"]):
        return removeQuotation(token)

    elif includeNumber(token) and not include(token, ".") and not include(token, ["\"", "\'"]):
        return int(token)
    elif includeNumber(token) and not include(token, ".") and include(token, ["\"", "\'"]):
        return removeQuotation(token)
    else:
        return token


def lex(text):
    pos = 0
    letters = list(text)
    token = ""
    tokens = []

    while not pos >= len(letters):
        c = str(letters[pos])
        if c.isspace():
            tokens.append(type_convert(token))
            token = ""
        else:
            token += c
        pos += 1

    if token != "":
        tokens.append(type_convert(token))

    return tokens
