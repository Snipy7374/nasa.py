from redis import Redis
from functools import wraps
from inspect import getfullargspec

# change redis to redis host
redis = Redis(host="redis", port=6379)
TTL = 3600 # in seconds

def cache_variation_1(key: str):
    """
    Redis cache decorator that optionally injects two arguments into the wrapped function.

    Optionally injects "cache" and "key" keyword arguments. Where cache is the cached
    value if present.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = redis.get(key)
            argspec = getfullargspec(func).args
            if "key" in argspec:    
                kwargs["key"] = key
            if "cache" in argspec:
                kwargs["cache"] = cache
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_variation_2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = '-'.join([func.__name__] + list(args))
        cache = redis.get(key)

        if cache is None:
            value = func(*args, **kwargs)
            redis.set(name=key, value=value, ex=TTL)
        else:
            value = cache
        
        return value
    return wrapper