import random

def randinteger(min, max):
    return random.randint(min, max)

def randfloat(min, max):
    return random.uniform(min, max)

def randbytes(amount):
    return random.randbytes(amount)

def rand():
    return random.Random()

def randeven(min, max):
    num = 1
    while (num % 2) != 0:
        num = random.randint(min, max)
    return num

def randodd(min, max):
    num = 0
    while (num % 2) == 0:
        num = random.randint(min, max)
    return num

def randshuffle(deck):
    return random.shuffle(deck)

def randitem(deck):
    return random.choice(deck)