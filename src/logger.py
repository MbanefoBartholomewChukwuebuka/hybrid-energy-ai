import logging

logging.basicConfig(
    filename="energy_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_event(message):
    logging.info(f"[ENERGY SYSTEM] {message}")

def log_error(error):
    logging.error(f"[ENERGY SYSTEM ERROR] {error}")