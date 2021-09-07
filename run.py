import gspread
from google.oauth2.service_account import Credentials 
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figure from user
    """
    while True:
        print("Please enter sales data from last market.")
        print("Data should be six numbers, separated by commas")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
        

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 value
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Ivalid data: {e}, please try again. \n")
        return False

    return True

    
def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet ipdated succesffully. \n")

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_data)
    print("Surplus worksheet updated succesffully. \n")

def update_worksheet(data, worksheet):
    """
    Update all worksheets for given user data
    """
    print(f"Updating {worksheet} worksheet....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each sandwich
    
    Positive surplus indicates waste
    Negative surplus indicates extra made when stock ran out
    """
    print("Calculating surplus data")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects collumsn of data from worksheet, of last 5 entries for 
    each sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")


    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    Create the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "stock")
    sales_columns = get_last_5_entries_sales()
    stock _data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "sales")

print("Welcome to Love Sandwiches Data Automation")
main()

