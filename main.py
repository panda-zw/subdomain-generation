# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from middleware import extract_subdomain_middleware
from models import OrganizationRequest
from utils import generate_subdomain
from database import is_subdomain_valid, add_subdomain

app = FastAPI()

app.middleware("http")(extract_subdomain_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-organization")
async def create_organization(request: OrganizationRequest):
    # Generate the subdomain based on the organization name
    subdomain = await generate_subdomain(request.name)

    # Check if subdomain already exists
    if await is_subdomain_valid(subdomain):
        raise HTTPException(status_code=400, detail="Subdomain already exists.")

    # Add the subdomain to the Redis cache
    await add_subdomain(subdomain)

    return {"message": "Organization created successfully", "subdomain": subdomain}


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ws_ping_interval=300, ws_ping_timeout=300, reload=True)