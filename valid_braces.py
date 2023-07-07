# Check if the braces aren't closed or have invalid order
def valid_braces(string):
    braces = {"(": ")", "{": "}", "[": "]", "<": ">"}
    string = [i for i in string if i in "(){}[]<>"]
    matches = {}
    try:
        for symbol in string:
            matches.setdefault(symbol, 0)
            for opener, closer in braces.items():
                if symbol in opener:
                    matches[opener] += 1
                if symbol in closer:
                    matches[opener] -= 1
    except KeyError:
        return False
    print(matches.items())
    return not any(matches.values())
