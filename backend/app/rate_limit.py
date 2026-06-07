from time import time
from fastapi import Request, HTTPException

RATE_LIMIT = 10
WINDOW = 3600

request_log = {}

def check_rate_limit(request: Request, premium: bool):
    if premium:
        return  # unlimited access

    ip = request.client.host
    now = time()

    timestamps = request_log.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: max 10 requests per hour"
        )

    timestamps.append(now)
    request_log[ip] = timestamps
