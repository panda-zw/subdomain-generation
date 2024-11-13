# models.py
from pydantic import BaseModel, Field

class OrganizationRequest(BaseModel):
    name: str = Field(..., example="Awesome Inc.")
    subdomain: str = Field(..., example="awesome")