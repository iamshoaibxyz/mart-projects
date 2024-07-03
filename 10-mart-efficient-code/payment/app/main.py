from fastapi import FastAPI

app : FastAPI = FastAPI(servers=[{"url":"http://127.0.0.1:8003"}])

@app.get("/")
def root():
    return {"message": "Payment soursecode"}