from fastapi import HTTPException, status
import httpx

from app.config.security import decode_access_token

COMPANY_SERVICE_URL = "http://authCompanyContainer:8002"

async def fetch_company_details(company_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{COMPANY_SERVICE_URL}/company/get-company-by-id/{company_id}")
            response.raise_for_status()  # This will raise an error for HTTP codes 4xx/5xx
            company = response.json()
            return company
        except httpx.RequestError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Request error: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error: {exc.response.text}")

async def auth_checker(token: str):
    try:
        decoded_token = decode_access_token(token)
        company_id = decoded_token.get("sub").get("id")
        company = await fetch_company_details(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))