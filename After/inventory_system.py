"""Inventory Management System with safe and clean design."""

import json
from datetime import datetime
from typing import Dict, List


# Global dictionary to store stock data
STOCK_DATA: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0,
             logs: List[str] | None = None) -> None:
    """Add a quantity of an item to the inventory."""
    if not isinstance(item, str) or not isinstance(qty, int):
        return

    STOCK_DATA[item] = STOCK_DATA.get(item, 0) + qty
    log_entry = f"{datetime.now()}: Added {qty} of {item}"
    if logs is not None:
        logs.append(log_entry)


def remove_item(item: str, qty: int) -> None:
    """Remove a quantity of an item from the inventory."""
    if not isinstance(item, str) or not isinstance(qty, int):
        return

    try:
        STOCK_DATA[item] -= qty
        if STOCK_DATA[item] <= 0:
            del STOCK_DATA[item]
    except KeyError:
        # Item does not exist, ignore safely
        pass


def get_quantity(item: str) -> int:
    """Get the current quantity of an item."""
    return STOCK_DATA.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            STOCK_DATA.clear()
            STOCK_DATA.update(data)
    except FileNotFoundError:
        STOCK_DATA.clear()
    except json.JSONDecodeError:
        STOCK_DATA.clear()


def save_data(file: str = "inventory.json") -> None:
    """Save the inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(STOCK_DATA, f, indent=4)


def print_data() -> None:
    """Print a formatted inventory report."""
    print("\nItems Report")
    for item, qty in STOCK_DATA.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items with stock below the threshold."""
    return [item for item, qty in STOCK_DATA.items() if qty < threshold]


def main() -> None:
    """Example flow to demonstrate inventory system usage."""
    add_item("apple", 10)
    add_item("banana", 2)
    remove_item("apple", 3)
    print(f"Apple stock: {get_quantity('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
