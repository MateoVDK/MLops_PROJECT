from time import time
from fastapi import Request

RATE_LIMIT = 10
WINDOW = 3600

request_log = {}

def check_rate_limit(request: Request, premium: bool):
    # Premium users have unlimited access
    if premium:
        return True, None

    ip = request.client.host
    now = time()

    timestamps = request_log.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW]

    if len(timestamps) >= RATE_LIMIT:
        return False, "max 10 requests per hour for free users"

    timestamps.append(now)
    request_log[ip] = timestamps

    return True, None
