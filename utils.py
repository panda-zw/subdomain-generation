# utils.py (same file as above)
async def generate_subdomain(org_name: str) -> str:
    # Convert org_name to a valid subdomain format
    return org_name.lower().replace(" ", "-")
