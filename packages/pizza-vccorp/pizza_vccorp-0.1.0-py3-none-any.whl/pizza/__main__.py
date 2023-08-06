"""Allow pizza to be executable through `python -m pizza`."""
from pizza.cli import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="pizza")
