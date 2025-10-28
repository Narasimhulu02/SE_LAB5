"""Inventory management system module.

This module provides basic operations for managing stock data:
- Adding and removing items
- Loading and saving inventory data from JSON files
- Checking for low-stock items
- Printing reports
"""

import json
from datetime import datetime
from typing import Dict, List

# Global variable to store inventory data
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0,
             logs: List[str] | None = None) -> None:
    """Add a quantity of an item to the stock."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove a quantity of an item from the stock safely."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Ignore missing items
        pass


def get_qty(item: str) -> int:
    """Return the quantity of a given item."""
    return stock_data.get(item, 0)


def load_data(file_path: str = "inventory.json") -> None:
    """Load inventory data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        stock_data.clear()
        stock_data.update(data)
    except FileNotFoundError:
        stock_data.clear()


def save_data(file_path: str = "inventory.json") -> None:
    """Save inventory data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(stock_data, file, indent=4)


def print_data() -> None:
    """Print the current inventory report."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items with quantity below a given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Main entry point for testing inventory operations."""
    add_item("apple", 10)
    add_item("banana", 2)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
