import pandas

def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


def num_check(question, num_type="float", exit_code=None):
    """Checks users enter an integer / float that is more than
    zero (or the optional exit code)"""

    while True:
        response = input(question)

        # check for exit code and return it if entered
        if exit_code is not None and response == exit_code:
            return response

        # check datatype is correct and that number is more than zero
        try:
            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print("Oops - please enter a number more than 0.")

        except ValueError:
            print("Oops - please enter a valid number.")


def get_expense(exp_type, how_many=1):
    """Gets variable / fixed expenses and outputs
    a pandas DataFrame of the items, amounts, and costs"""

    # Lists for DataFrame
    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item,
    }

    while True:
        # Get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        if exp_type == "variable" and item_name == "xxx" and len(all_items) == 0:
            print("Oops - you have not entered anything. You need at least one item.")
            continue

        elif item_name == "xxx":
            break

        # Get item amount
        amount = num_check(f"How many <enter for {how_many}>: ", "integer", "")

        if amount == "":
            amount = how_many

        # Get cost per item
        cost = num_check("Price for one? ", "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(cost)  # FIXED: was all_costs (undefined)

    # Make pandas DataFrame
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate Row Cost
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    subtotal = expense_frame['Cost'].sum()

    # return the expenses DataFrame and subtotal
    return expense_frame, subtotal


# Main routine starts here

quantity_made = num_check("Quantity being made: ", "integer")

print()

print("Getting Variable costs...")
variable_panda, variable_subtotal = get_expense("variable", quantity_made)  # FIXED unpacking

print()
print(variable_panda)
print(variable_subtotal)


# Commit code
# Variable costs & subtotal