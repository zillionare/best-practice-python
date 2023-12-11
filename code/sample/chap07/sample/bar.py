from sample.core.foo import Foo, is_windows


def my_bark() -> str:
    foo = Foo()
    return foo.bark()


def get_operating_system() -> str:
    return "Windows" if is_windows() else "Linux"
