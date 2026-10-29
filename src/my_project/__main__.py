"""Entry point: `python -m my_project` or the `my-project` command."""

from my_project import __version__


def main() -> None:
    print(f"my-project {__version__}")


if __name__ == "__main__":
    main()
