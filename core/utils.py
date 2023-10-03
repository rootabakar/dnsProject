import random
import string


def verification(uri):
    if uri.endswith(".sn"):
        return True
    else:
        return False


def generation_char():
    length = 5
    letters = string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
