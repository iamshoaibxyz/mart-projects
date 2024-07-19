from fastapi import HTTPException, status
import httpx

COMPANY_SERVICE_URL = "http://authCompanyContainer:8002"
PRODUCT_SERVICE_URL = "http://productContainer:8004"
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

async def fetch_company_detail_by_id(company_id: str):
    try:
        company = await fetch_details_by_get_method(f"{COMPANY_SERVICE_URL}/company/get-company-by-id/{company_id}")
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
