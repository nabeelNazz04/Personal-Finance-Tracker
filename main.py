import pandas as pd
import csv
from datetime import datetime
from data_entry import get_category, get_amount, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    # Define the name of the CSV file where financial data will be stored
    CSV_FILE = 'finance_data.csv'
    
    # Define the columns that will be used in the CSV file
    COLUMNS = ['date', 'amount', 'category', 'description']
    
    # Define the date format
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """
        Initializes the CSV file by creating it if it doesn't exist.
        """
        try:
            # Try reading the CSV file using pandas
            df = pd.read_csv(cls.CSV_FILE)
            if df.empty:
                # If the file is empty, recreate it with the defined columns
                df = pd.DataFrame(columns=cls.COLUMNS)
                df.to_csv(cls.CSV_FILE, index=False)
                print(f"CSV file '{cls.CSV_FILE}' recreated successfully.")
        except FileNotFoundError:
            # If the file does not exist, create a new one with the defined columns
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"CSV file '{cls.CSV_FILE}' created successfully.")

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Adds a new entry to the CSV file.
        """
        # Create a dictionary for the new entry
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category.lower(),  # Standardize category to lowercase
            'description': description
        }
        
        # Open the CSV file in append mode ('a') to add the new entry
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        
        # Print a confirmation message
        print("Entry added successfully.")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        """
        Retrieves transactions within a specified date range.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(cls.CSV_FILE)
            
            if df.empty:
                print("No transactions found in the CSV file.")
                return
            
            # Convert the 'date' column to datetime objects
            df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)
            
            # Parse the input start and end dates
            start_date = datetime.strptime(start_date, cls.FORMAT)
            end_date = datetime.strptime(end_date, cls.FORMAT)
            
            # Create a mask to filter rows within the date range
            mask = (df['date'] >= start_date) & (df['date'] <= end_date)
            filtered_df = df.loc[mask]
            
            if filtered_df.empty:
                print("No transactions found in the given date range.")
            else:
                # Print the filtered transactions
                print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
                print(filtered_df.to_string(index=False, formatters={
                    'date': lambda x: x.strftime(cls.FORMAT)
                }))
                
                # Calculate total income, expense, and net savings
                total_income = filtered_df[filtered_df['category'] == 'income']['amount'].sum()
                total_expense = filtered_df[filtered_df['category'] == 'expense']['amount'].sum()
                print(f"Total income: ${total_income:.2f}")
                print(f"Total expense: ${total_expense:.2f}")
                print(f"Net savings: ${(total_income - total_expense):.2f}")
            
            return filtered_df
        
        except Exception as e:
            print(f"An error occurred: {e}")

def add():
    """
    Collects user input for a transaction and adds it to the CSV file.
    """
    # Initialize the CSV file
    CSV.initialize_csv()

    # Get user input for each field
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or press Enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    # Add the entry to the CSV file
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    # Ensure the 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'], format=CSV.FORMAT)
    
    # Set the date column as the index
    df.set_index("date", inplace=True)
    
    # Create income and expense DataFrames
    income_df = (
        df[df["category"] == "income"]
        .resample("D")  # Resample to daily frequency
        .sum()
        .reindex(df.index, fill_value=0)  # Fill missing dates with 0
    )
    expense_df = (
        df[df["category"] == "expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    
    # Plot using matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
def add_sample_data():
    """
    Adds sample financial data to the CSV file for testing and plotting.
    """
    # Define sample data as a list of dictionaries
    sample_data = [
        {"date": "24-07-2024", "amount": 567, "category": "income", "description": "tip"},
        {"date": "07-07-2024", "amount": 2000.0, "category": "income", "description": "wage"},
        {"date": "02-07-2024", "amount": 2000.0, "category": "expense", "description": "tour"},
        {"date": "15-06-2024", "amount": 1500.0, "category": "income", "description": "freelance"},
        {"date": "10-06-2024", "amount": 300.0, "category": "expense", "description": "groceries"},
        {"date": "05-06-2024", "amount": 500.0, "category": "expense", "description": "rent"},
        {"date": "01-06-2024", "amount": 1200.0, "category": "income", "description": "bonus"},
        {"date": "28-05-2024", "amount": 800.0, "category": "expense", "description": "utilities"},
        {"date": "20-05-2024", "amount": 3000.0, "category": "income", "description": "salary"},
        {"date": "15-05-2024", "amount": 450.0, "category": "expense", "description": "transport"},
        {"date": "10-05-2024", "amount": 200.0, "category": "expense", "description": "dining"},
        {"date": "05-05-2024", "amount": 1000.0, "category": "income", "description": "investment"},
        {"date": "01-05-2024", "amount": 750.0, "category": "expense", "description": "shopping"},
        {"date": "25-04-2024", "amount": 2500.0, "category": "income", "description": "freelance"},
        {"date": "20-04-2024", "amount": 120.0, "category": "expense", "description": "gym membership"},
        {"date": "15-04-2024", "amount": 1500.0, "category": "expense", "description": "vacation"},
        {"date": "10-04-2024", "amount": 3000.0, "category": "income", "description": "salary"},
        {"date": "05-04-2024", "amount": 600.0, "category": "expense", "description": "medical bills"},
        {"date": "01-04-2024", "amount": 100.0, "category": "expense", "description": "entertainment"},
        {"date": "25-03-2024", "amount": 4000.0, "category": "income", "description": "bonus"},
        {"date": "20-03-2024", "amount": 900.0, "category": "expense", "description": "car repair"},
        {"date": "15-03-2024", "amount": 2000.0, "category": "income", "description": "freelance"},
        {"date": "10-03-2024", "amount": 350.0, "category": "expense", "description": "groceries"},
        {"date": "05-03-2024", "amount": 1500.0, "category": "expense", "description": "rent"},
        {"date": "01-03-2024", "amount": 2500.0, "category": "income", "description": "salary"},
    ]

    # Append each entry to the CSV file
    for entry in sample_data:
        CSV.add_entry(entry["date"], entry["amount"], entry["category"], entry["description"])
    print("Sample data added successfully!")
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Add sample data for testing")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add()
        elif choice == "2":
            # Allow the user to input the date range dynamically
            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")
            filtered_df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == 'y':
                plot_transaction(filtered_df)
        elif choice == "3":
            add_sample_data()
        elif choice == "4":
            print("Exiting....")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main() #used to protect the main function from importing