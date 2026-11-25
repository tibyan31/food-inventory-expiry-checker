# food_item stores the details of one food product
from datetime import date

# Create a food item with its ID, name, quantity and expiry date
class FoodItem: 
    def __init__(self, item_id, name, quantity, expiry_date):
        self.item_id = item_id          
        self.name = name                
        self.quantity = quantity        
        self.expiry_date = expiry_date  

    # Display this food item's information as one table row
    def display_details(self):
        print(f"{self.item_id:<5}{self.name:<20}{self.quantity:>8}   {self.expiry_date}")

    # Update the food item's information (None means keep the current value)
    def update_details(self, name=None, quantity=None, expiry_date=None):
        if name is not None:
            self.name = name
        if quantity is not None:
            self.quantity = quantity
        if expiry_date is not None:
            self.expiry_date = expiry_date


