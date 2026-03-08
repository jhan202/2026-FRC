import pandas
from tabulate import tabulate
from datetime import date
import math


# Functions go here
def make_statement(statement, decoration):
    """Emphasizes headings by adding decoration
    at the start and end"""
    return f"{decoration * 3} {statement} {decoration * 3}"


def yes_no_check(question):
    while True:
        response = input(question).lower()
        if response in ["yes", "y"]:
            return "yes"
        elif response in ["no", "n"]:
            return "no"
        else:
            print("Please enter yes or no.")


def instructions():
    print(make_statement("Instructions", "ℹ️"))

    print('''
For each holder enter:
- Their name
- Their age
- Their payment method (cash/credit)

The program will record the ticket sale and calculate the
ticket cost (and the profit).

Once you have either sold all of the tickets or entered the 
exit code ('xxx'), the program will display the ticket
sales information and write the data to a text file.

It will also choose one lucky ticket holder who wins the 
draw (their ticket is free).
    ''')


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
    """Formats numbers as currency ($#.##)"""
    return "${:,.2f}".format(x)


def profit_goal(total_costs):
    """Calculate profit goal work out profit goal and total sales required"""
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while True:

        # ask for profit goal...
        response = input("What is your profit goal(eg $500 or 50%):")

        # check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            #Get amount (everything after the $)
            amount = response[1:]


        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount(everything before the %)
            amount = response [:-1]

        # check is last character is %
        elif response[-1] == "$":
            profit_type = "$"
            # Get amount (everything before the $)
            amount = response[:-1]

        else:
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue


        if profit_type == "unknown" and amount <= 100:
            dollar_type = yes_no_check(f"Do you mean ${amount:.2f}.  ie{amount:.2f} dollars?, ")

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "amount" and amount <= 100:
            percent_type = yes_no_check(f"DO you mean {amount}%? , y / n:")
            if percent_type == "yes":
                profit_type = "$"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


def round_up(amount, round_val):
    """Rounds amount to desired hole number"""
    return int(math.ceil(amount / round_val)) * round_val




# Main routine goes here

fixed_subtotal = 0
fixed_panda_string = ""

make_statement("Fund raising calculator", "🎞️")

print()
want_instructions = yes_no_check("Do you want instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ", "integer")

print("Let's get the variable expenses...")
variable_expenses = get_expense("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print()
has_fixed = yes_no_check("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expense("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: {total_expenses:.2f}"

# Get profile Goal here.
target = profit_goal(total_expenses)
sales_target = total_expenses + target

# Calculate minimum selling price and round
# it to nearest desired dollar amount
selling_price = (total_expenses + target) / quantity_made
round_to = num_check("Round to: ", 'integer')
suggested_price = round_up(selling_price, round_to)

today = date.today()

day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

main_heading_string = f"Fund Raising Calculator ({product_name}) {day}/{month}/{year}"
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = "Variable Expenses"
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = "Fixed Expenses"
    fixed_subtotal_string = f"Fixed Expenses Subtotal: ${fixed_subtotal:.2f}"

    # set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = "You have no Fixed Expenses"
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

selling_price_heading = make_statement("Selling price Calculations","=")
profit_goal_string = f"Profit Goal: ${target:.2f}"
sales_target_string = f"\nTotal Sales Needed: ${sales_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_price:.2f}"
suggested_price_string = make_statement(f"Suggested Selling Price: "
                                        f"${suggested_price:.2f}", "*")


# List of strings to be outputted / written to file
to_write = [main_heading_string , quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string,
            profit_goal_string, sales_target_string,
            minimum_price_string,"\n", suggested_price_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)
file_name = f"{product_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)


text_file = open(write_to, "w+")

# write the items to file
for item in to_write:
    text_file.write(str(item))
    text_file.write("\n")

text_file.close()


