import pandas
from tabulate import tabulate

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

        if exit_code is not None and response == exit_code:
            return response

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

    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item,
    }

    amount = how_many
    how_much_question = "How much? $"

    while True:
        item_name = not_blank("Item Name: ")

        if exp_type == "variable" and item_name == "xxx" and len(all_items) == 0:
            print("Oops - you have not entered anything. You need at least one item.")
            continue

        elif item_name == "xxx":
            break

        if exp_type == "variable":
            amount = num_check(f"How many <enter for {how_many}>: ",
                               "integer", "")

            if amount == "":
                amount = how_many

            cost = num_check("Price for one? ", "float")

        else:
            cost = num_check(how_much_question, "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(cost)

    expense_frame = pandas.DataFrame(expenses_dict)

    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    subtotal = expense_frame['Cost'].sum()

    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    return expense_frame, subtotal


def currency(x):
    return "${:,.2f}".format(x)


# Main routine starts here

quantity_made = num_check("Quantity being made: ", "integer")

print()

print("Getting Variable costs...")
variable_expenses = get_expense("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print("Getting Fixed Costs...")
fixed_expenses = get_expense("fixed")
print()
fixed_panda = fixed_expenses[0]
fixed_subtotal = fixed_expenses[1]

print("=== Variable Expenses ===")
print(variable_panda)
print(f"Variable: ${variable_subtotal:.2f}")
print()

print("=== Fixed Expenses ===")
print(fixed_panda)
print(f"Fixed: ${fixed_subtotal:.2f}")

print()
total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")

# commit code - Working expenses