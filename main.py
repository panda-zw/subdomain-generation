# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from middleware import extract_subdomain_middleware
from models import OrganizationRequest
from utils import is_subdomain_available, generate_subdomain
from database import db

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

    # Check if the subdomain is already in use
    is_available = await is_subdomain_available(subdomain)
    if not is_available:
        raise HTTPException(status_code=400, detail="Subdomain is already in use.")

    # Insert the new organization document
    new_org = {"name": request.name, "subdomain": subdomain}
    await db.organizations.insert_one(new_org)

    return {"message": "Organization created successfully", "subdomain": subdomain}


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ws_ping_interval=300, ws_ping_timeout=300, reload=True)