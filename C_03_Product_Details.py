def num_check(question, num_type, exit_code=None):
    """Checks users enter an integer / float that is more than
    zero (or the optional exit code)"""

    if num_type == "float":
        error = "Oops - please enter a number more than 0."
    else:
        error = "Oops - please enter an integer more than 0."

    while True:
        try:

            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


# Main Routine goes here

# Loop for testing purposes
while True:
    product_name = not_blank("Product Name: ")
    quantity_made = num_check("Quantity being made: ", "integer")
    print(f"You are making {quantity_made} {product_name}")
    print()

