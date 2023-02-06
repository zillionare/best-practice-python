import fire


def greeting(name: str):
    print(f"hi {name}")

fire.Fire({
    "greeting": greeting
})
