# app.py - FoodInventoryApp class: the menu that connects Inventory and ExpiryChecker
from datetime import date, datetime

from inventory import Inventory, get_expiry_date
from expiry_checker import ExpiryChecker, STATUS_MESSAGES


# Input validation functions (keep asking until the input is valid)

# Ask for text; blank is only allowed when allow_blank is True (returns None)
def get_text(prompt, allow_blank=False):
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        elif allow_blank:
            return None
        else:
            print("  Error: This field cannot be empty.")


# Ask for a whole number between minimum and maximum
def get_number(prompt, minimum, maximum=None, allow_blank=False):
    while True:
        text = input(prompt).strip()
        if text == "" and allow_blank:
            return None
        try:
            number = int(text)
        except ValueError:
            print("  Error: Please enter a whole number.")
            continue
        if number < minimum or (maximum is not None and number > maximum):
            if maximum is None:
                print(f"  Error: The number must be {minimum} or more.")
            else:
                print(f"  Error: Please enter a number from {minimum} to {maximum}.")
        else:
            return number


# Ask for a date in YYYY-MM-DD format and return it as a date object
def get_date(prompt, allow_blank=False):
    while True:
        text = input(prompt).strip()
        if text == "" and allow_blank:
            return None
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("  Error: Invalid date. Use YYYY-MM-DD, e.g. 2026-12-31")


# Ask a yes/no question; returns True for yes and False for no
def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        else:
            print("  Error: Please type y or n.")


# Find an item in the inventory by its ID; returns None if not found
def find_item(inventory, item_id):
    for item in inventory.food_items:
        if item.item_id == item_id:
            return item
    return None


# ---------- FoodInventoryApp class ----------

class FoodInventoryApp:
    # Create the inventory and the expiry checker used by the app
    def __init__(self):
        self.inventory = Inventory()
        self.expiry_checker = ExpiryChecker(warning_days=3)

    # Display the main menu
    def display_menu(self):
        print("\n" + "=" * 46)
        print("      FOOD INVENTORY EXPIRY CHECKER")
        print("      Supporting SDG 2: Zero Hunger")
        print("=" * 46)
        print(f"Today: {date.today()}   Items: {len(self.inventory.food_items)}")
        print("-" * 46)
        print("1. Add food item")
        print("2. View all food items")
        print("3. Update food item")
        print("4. Delete food item")
        print("5. Check expiry status")
        print("6. Display expiry warnings")
        print("7. Exit")
        print("-" * 46)

    # Execute the application: show the menu and handle choices until the user exits
    def run(self):
        running = True
        while running:
            self.display_menu()
            choice = get_number("Enter your choice (1-7): ", 1, 7)
            running = self.handle_choice(choice)
            if running:
                input("\nPress Enter to continue...")
        print("\nThank you for reducing food waste and supporting SDG 2. Goodbye!")

    # Process the selected menu option; returns False when the user chooses Exit
    def handle_choice(self, choice):
        # Option 1: add a new food item
        if choice == 1:
            print("\n--- ADD FOOD ITEM ---")
            name = get_text("Food name: ").title()
            quantity = get_number("Quantity: ", 1)
            expiry_date = get_date("Expiry date (YYYY-MM-DD): ")
            if expiry_date < date.today() and not get_yes_no(
                    "This date has already passed. Add anyway? (y/n): "):
                print("Item not added.")
                return True
            item = self.inventory.add_item(name, quantity, expiry_date)
            status = self.expiry_checker.get_expiry_status(item)
            print(f"'{item.name}' added with ID {item.item_id}. Status: {status}")
            print(f"-> {STATUS_MESSAGES[status]}")

        # Option 2: view all food items (earliest expiry first)
        elif choice == 2:
            print("\n--- ALL FOOD ITEMS ---")
            self.inventory.view_items()

        # Option 3: update an item (press Enter to keep the current value)
        elif choice == 3:
            print("\n--- UPDATE FOOD ITEM ---")
            self.inventory.view_items()
            if len(self.inventory.food_items) == 0:
                return True
            item_id = get_number("Enter the item ID to update (0 to cancel): ", 0)
            item = find_item(self.inventory, item_id)
            if item_id == 0:
                print("Cancelled.")
            elif item is None:
                print(f"Error: No item with ID {item_id}.")
            else:
                print("Press Enter to keep the current value.")
                name = get_text(f"New name [{item.name}]: ", allow_blank=True)
                if name is not None:
                    name = name.title()
                quantity = get_number(f"New quantity [{item.quantity}]: ", 1, allow_blank=True)
                expiry_date = get_date(f"New expiry date [{item.expiry_date}]: ", allow_blank=True)
                self.inventory.update_item(item_id, name, quantity, expiry_date)
                print("Item updated:")
                item.display_details()

        # Option 4: delete an item after the user confirms
        elif choice == 4:
            print("\n--- DELETE FOOD ITEM ---")
            self.inventory.view_items()
            if len(self.inventory.food_items) == 0:
                return True
            item_id = get_number("Enter the item ID to delete (0 to cancel): ", 0)
            item = find_item(self.inventory, item_id)
            if item_id == 0:
                print("Cancelled.")
            elif item is None:
                print(f"Error: No item with ID {item_id}.")
            elif get_yes_no(f"Delete '{item.name}'? (y/n): "):
                self.inventory.delete_item(item_id)
                print(f"'{item.name}' deleted.")
            else:
                print("Cancelled. Nothing was deleted.")

        # Option 5: show the expiry status of every item, then a summary
        elif choice == 5:
            print("\n--- EXPIRY STATUS CHECK ---")
            total = len(self.inventory.food_items)
            if total == 0:
                print("The inventory is empty.")
                return True
            counts = {"Expired": 0, "Near Expiry": 0, "Not Expired": 0}
            for item in sorted(self.inventory.food_items, key=get_expiry_date):
                days_left = self.expiry_checker.check_expiry(item)
                status = self.expiry_checker.get_expiry_status(item)
                counts[status] = counts[status] + 1
                item.display_details()
                print(f"     Days left: {days_left} | {status} | {STATUS_MESSAGES[status]}")
            need_attention = counts["Expired"] + counts["Near Expiry"]
            percent = need_attention / total * 100
            print("-" * 46)
            print(f"Expired: {counts['Expired']}  Near Expiry: {counts['Near Expiry']}  "
                  f"Not Expired: {counts['Not Expired']}")
            print(f"{need_attention} of {total} item(s) ({percent:.0f}%) need attention.")

        # Option 6: show warnings for expired and near-expiry items only
        elif choice == 6:
            print("\n--- EXPIRY WARNINGS ---")
            if len(self.inventory.food_items) == 0:
                print("The inventory is empty.")
            else:
                self.expiry_checker.display_warnings(
                    sorted(self.inventory.food_items, key=get_expiry_date))

        # Option 7: exit the application
        else:
            return False

        return True



