# middleware.py
from fastapi import FastAPI, Request

async def extract_subdomain_middleware(request: Request, call_next):
    hostname = request.url.hostname
    subdomain = hostname.split(".")[0]  # Extract the subdomain
    request.state.subdomain = subdomain  # Attach subdomain to request state
    response = await call_next(request)
    return response
