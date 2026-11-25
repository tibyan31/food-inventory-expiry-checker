# main.py - start the Food Inventory Expiry Checker (run: python main.py)
from app import FoodInventoryApp

# Run only when this file is started directly
if __name__ == "__main__":
    try:
        app = FoodInventoryApp()   # create the app object
        app.run()                  # start the menu loop
    # Ctrl+C or closed input: stop politely instead of showing an error
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram stopped by the user. Goodbye!")