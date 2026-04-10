import logging

# Create logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)  # capture all levels

# Formatter (log format)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# File handler (save logs to file)
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)  # only INFO and above to file
file_handler.setFormatter(formatter)

# Console handler (print logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)