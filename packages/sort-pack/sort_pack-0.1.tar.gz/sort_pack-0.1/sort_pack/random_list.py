import random as r


def generation_list(length):
    return [r.randint(-10, 10) for _ in range(length+1)]
