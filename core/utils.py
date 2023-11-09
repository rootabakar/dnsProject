import random
import string
import re


def verification(uri):
    if uri.endswith(".sn"):
        return True
    else:
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, uri):
            octets = uri.split('.')
            for octet in octets:
                if not (0 <= int(octet) <= 255):
                    return False
            return True
        else:
            return False


def generation_char():
    length = 5
    letters = string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
