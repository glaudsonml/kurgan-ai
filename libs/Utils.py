import random
import sys, os
import string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def id_gen():
    return ''.join(random.choice("0123456789") for _ in range(4)) 