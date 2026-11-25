# Inventory class: stores and manages all food items
from datetime import date

from food_item import FoodItem


# Tell sorted() to arrange items by expiry date (used for FIFO order)
def get_expiry_date(item):
    return item.expiry_date


class Inventory:
    # Start with an empty list of food items
    def __init__(self):
        self.food_items = []

    # Add a new food item with the next ID number and return it
    def add_item(self, name, quantity, expiry_date):
        new_id = 1
        for item in self.food_items:
            if item.item_id >= new_id:
                new_id = item.item_id + 1   # next ID = highest ID + 1
        new_item = FoodItem(new_id, name, quantity, expiry_date)
        self.food_items.append(new_item)
        return new_item

    # Display all food items, earliest expiry first (FIFO: use older food first)
    def view_items(self):
        if len(self.food_items) == 0:
            print("The inventory is empty.")
            return
        print("-" * 46)
        print(f"{'ID':<5}{'Food Name':<20}{'Quantity':>8}   Expiry Date")
        print("-" * 46)
        for item in sorted(self.food_items, key=get_expiry_date):
            item.display_details()
        print("-" * 46)
        print(f"Total: {len(self.food_items)} item(s)")

    # Update the item with this ID; returns True if found, False if not
    def update_item(self, item_id, name=None, quantity=None, expiry_date=None):
        for item in self.food_items:
            if item.item_id == item_id:
                item.update_details(name, quantity, expiry_date)
                return True
        return False

    # Delete the item with this ID; returns True if found, False if not
    def delete_item(self, item_id):
        for item in self.food_items:
            if item.item_id == item_id:
                self.food_items.remove(item)
                return True
        return False


