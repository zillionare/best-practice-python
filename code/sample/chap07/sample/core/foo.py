import logging


def is_windows():
    return True


def get_operating_system():
    return "Windows" if is_windows() else "Linux"


class Foo:
    def bark(self):
        return "bark"

def bar():
    logger = logging.getLogger(__name__)
    logger.info("please check if I was called")

    root_logger = logging.getLogger()
    root_logger.info("this is not intercepted")
