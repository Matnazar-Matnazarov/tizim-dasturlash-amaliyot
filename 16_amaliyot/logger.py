import logging
import traceback

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def log_error(e: IndexError) -> None:
    print("Exception type:", type(e))
    print("Exception:", e)
    print("Exception object:", e.__traceback__)
    logging.error("\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
