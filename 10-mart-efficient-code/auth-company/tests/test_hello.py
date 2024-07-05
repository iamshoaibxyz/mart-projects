# from app.main import app
# from starlette.testclient import TestClient

def test_hello_world(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Company Auth soursecode"}

# def test_read_main()->None:
#     client = TestClient(app=app)
#     response = client.get("/")
#     assert response.status_code == 200
    # assert response.json() == {"Hello": "World"}