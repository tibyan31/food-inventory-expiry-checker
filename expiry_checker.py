# expiry_checker.py: compares expiry dates with today's date
from datetime import date, timedelta

from food_item import FoodItem

# System message for each expiry status
STATUS_MESSAGES = {
    "Expired": "This item has expired.",
    "Near Expiry": "Warning: This item is approaching expiry.",
    "Not Expired": "This item is not expired.",
}

# Store today's date and how many days count as "near expiry"
class ExpiryChecker:
    def __init__(self, warning_days=3):
        self.current_date = date.today()
        self.warning_days = warning_days

    # Check an item: returns the days left before expiry (negative = already expired)
    def check_expiry(self, item):
        self.current_date = date.today()    # refresh in case the date has changed
        days_left = (item.expiry_date - self.current_date).days
        return days_left

    # Return the item's status: "Expired", "Near Expiry" or "Not Expired"
    def get_expiry_status(self, item):
        days_left = self.check_expiry(item)
        if days_left < 0:
            return "Expired"
        elif days_left <= self.warning_days:
            return "Near Expiry"
        else:
            return "Not Expired"

    # Display warnings for items that are expired or near expiry
    def display_warnings(self, food_items):
        warning_count = 0
        for item in food_items:
            status = self.get_expiry_status(item)
            if status == "Expired" or status == "Near Expiry":
                warning_count = warning_count + 1
                print(f"[{status}] ID {item.item_id}: {item.name} "
                      f"(expiry date: {item.expiry_date})")
                print(f"   -> {STATUS_MESSAGES[status]}")

        if warning_count == 0:
            print("No warnings. All items have more than "
                  f"{self.warning_days} days before expiry.")
        else:
            print(f"\n{warning_count} item(s) need attention. Use them first to reduce food waste.")
            print("Note: These are date reminders only. Check storage conditions and")
            print("labels too: 'use by' is about safety, 'best before' is about quality.")


