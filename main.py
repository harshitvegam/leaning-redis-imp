import uvicorn
from app.main import app
from app.config.logging import logger
def main():
    logger.info("Hello from product-order-service!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8086)
