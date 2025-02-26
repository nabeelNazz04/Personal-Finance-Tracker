from datetime import datetime

# Define the date format
DATE_FORMAT = "%d-%m-%Y"

# Define categories
CATEGORY = {"I": "income", "E": "expense"}

def get_date(prompt, allow_default=False):
    """
    Prompts the user to enter a date or use today's date as default.
    Ensures the date is in the correct format.
    """
    date_str = input(prompt)
    if allow_default and not date_str:
        # Return today's date in the specified format
        return datetime.today().strftime(DATE_FORMAT)

    try:
        # Parse the input date string into a datetime object
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        # Return the date as a formatted string
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)

def get_amount():
    """
    Prompts the user to enter a valid amount.
    Ensures the amount is a positive, non-zero number.
    """
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive, non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()  # Recursively call until valid input is provided

def get_category():
    """
    Prompts the user to select a category ('I' for income, 'E' for expense).
    Ensures the input is valid.
    """
    category = input("Enter the category ('I' for income or 'E' for expense): ").upper()
    if category in CATEGORY:
        return CATEGORY[category]
    print("Invalid category. Please try again.")
    return get_category()

def get_description():
    """
    Prompts the user to enter an optional description.
    Returns the description as a string.
    """
    return input("Enter a description (optional): ")
