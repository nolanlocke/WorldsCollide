# not a "real" distribution, the discretization and clamping skew it
def truncated_discrete_distribution(mean, stddev, minimum = None, maximum = None, random_instance = None):
    import random
    rnd = random if random_instance is None else random_instance
    result = round(rnd.gauss(mean, stddev))
    if minimum and result < minimum:
        return truncated_discrete_distribution(mean, stddev, minimum, maximum)
    if maximum and result > maximum:
        return truncated_discrete_distribution(mean, stddev, minimum, maximum)
    return result
