from functools import lru_cache


@lru_cache()
def name_generator(prefix: str) -> str:
    """
    Return a generator of unique names with the given prefix.
    """
    n = 0
    while True:
        n += 1
        yield '%s%d' % (prefix, n)
