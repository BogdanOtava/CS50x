"""
https://cs50.harvard.edu/x/2023/psets/6/cash/
"""

def main():
    dollars = get_input()
    amount = get_coins(dollars)

    print(amount)


def get_input():
    """Prompts user for a positive float. Returns that amount times 100 as an integer."""

    while True:
        try:
            dollars = float(input("Change owed: "))

            if dollars > 0:
                return int(dollars * 100)

        except ValueError as error:
            print(error)


def get_coins(dollars):
    """Returns the smallest number of coins that can be given for the change owed."""

    counter = 0

    # Loop through a list that contains all coins available.
    for coin in [25, 10, 5, 1]:
        # Divide the dollars by each coin and store integer result in a temporary variable.
        amount = int(dollars / coin)
        # Substract from dollars that result multiplied by the coin.
        dollars -= amount * coin
        # Add to counter the result of the division.
        counter += amount

        # Break out of the loop when dollars reach 0.
        if dollars == 0:
            break

    return counter


if __name__ == "__main__":
    main()
