"""
https://cs50.harvard.edu/x/2023/psets/6/mario/less/
"""

def get_height():
    """Returns the height that was given by the user."""

    while True:
        try:
            height = int(input("Height: "))

            if height > 0 and height < 9:
                return height

        except ValueError as error:
            print(error)


def print_pyramid(height):
    """Prints out the pyramid."""

    for line in range(height):
        print(" " * (height - line - 1), end="")
        print("#" * (line + 1))


# Call the function that prints the pyramid which takes as argument the function that returns the height.
print_pyramid(get_height())
