"""Console script for docker_example."""

import fire


def help():
    print("docker_example")
    print("=" * len("docker_example"))
    print("Skeleton project created by Python Project Wizard (ppw)")

def main():
    fire.Fire({
        "help": help
    })


if __name__ == "__main__":
    main() # pragma: no cover
