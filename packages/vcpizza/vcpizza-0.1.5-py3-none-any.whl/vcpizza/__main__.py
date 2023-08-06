"""Allow vcpizza to be executable through `python -m vcpizza`."""
from vcpizza.cli import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="vcpizza")
