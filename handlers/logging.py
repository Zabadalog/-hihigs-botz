import logging

def set_up_logger(level: int = logging.INFO, fname: str=__name__) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        handlers=[logging.FileHandler(f"logs/{fname}.log", mode="w"),],
        datefmt="[%d-%m-%Y %H:%M:%S]"
    )
