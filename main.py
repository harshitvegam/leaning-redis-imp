import uvicorn
from app.main import app

def main():
    print("Hello from product-order-service!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8086)
