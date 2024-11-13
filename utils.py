# utils.py
from database import db

async def is_subdomain_available_in_db(subdomain: str) -> bool:
    """
    Checks if the given subdomain is already in use.
    """
    result = await db.organizations.find_one({"subdomain": subdomain})
    return result is None  # True if subdomain is available, False if taken


# utils.py (same file as above)
async def generate_subdomain(org_name: str) -> str:
    # Convert org_name to a valid subdomain format
    return org_name.lower().replace(" ", "-")
