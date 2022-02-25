# https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_random(weights, random_instance = None):
    import random

    instance = random if random_instance is None else random_instance

    rnd = instance.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
