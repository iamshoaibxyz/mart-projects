from fastapi import HTTPException, status
import httpx
from typing import Optional

from app.config.security import decode_access_token

COMPANY_SERVICE_URL = "http://authCompanyContainer:8002"
PRODUCT_SERVICE_URL = "http://productContainer:8004"
USER_SERVICE_URL = "http://authUserContainer:8001"
INVENTORY_SERVICE_URL = "http://inventoryContainer:8006"

async def fetch_details_by_get_method(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url)
            response.raise_for_status()  # This will raise an error for HTTP codes 4xx/5xx
            company = response.json()
            return company
        except httpx.RequestError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Request error: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error: {exc.response.text}")

async def fetch_product_detail_by_id(product_id: str):
    try:
        product = await fetch_details_by_get_method(f"{PRODUCT_SERVICE_URL}/product/get-product-by-id/{product_id}")
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")

async def fetch_stock_detail_by_id(stock_id: str):
    try:
        stock = await fetch_details_by_get_method(f"{INVENTORY_SERVICE_URL}/inventory/get-stock-by-id/{stock_id}")
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="stock not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")

async def fetch_stock_detail_by_product_id(product_id: str):
    try:
        stock = await fetch_details_by_get_method(f"{INVENTORY_SERVICE_URL} /inventory/get-stock-by-product-id/{product_id}")
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="stock not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")

async def fetch_company_detail_by_id(company_id: str):
    try:
        company = await fetch_details_by_get_method(f"{COMPANY_SERVICE_URL}/company/get-company-by-id/{company_id}")
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def fetch_details_by_get_method_2(url: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Request error: {exc}")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error: {exc.response.text}")

async def fetch_product_detail_by_id_2(product_id: str) -> Optional[dict]:
    try:
        return await fetch_details_by_get_method_2(f"{PRODUCT_SERVICE_URL}/product/get-product-by-id/{product_id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")

async def fetch_stock_detail_by_product_id_2(product_id: str) -> Optional[dict]:
    try:
        return await fetch_details_by_get_method_2(f"{INVENTORY_SERVICE_URL}/inventory/get-stock-by-product-id/{product_id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")


async def auth_checker(token: str):
    try:
        decoded_token = decode_access_token(token)
        user_id = decoded_token.get("sub").get("id")
        user = await fetch_details_by_get_method(f"{USER_SERVICE_URL}/user/get_user_by_id/{user_id}")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))



# async def fetch_company_product_detail_by_id(product_id: str, company_id: str):
#     try:
#         data = {"product_id": product_id,"company_id": company_id }
#         product = await fetch_details_by_get_method(f"{PRODUCT_SERVICE_URL}/product/get-product-by-product-and-company-id?company_id={company_id}&product_id={product_id}", )
#         if not product:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
#         return product
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"something went wrong: {e}")
 