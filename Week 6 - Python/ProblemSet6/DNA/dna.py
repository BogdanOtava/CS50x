"""
https://cs50.harvard.edu/x/2023/psets/6/dna/
"""

import csv
import sys

def main():

    database = []
    results = {}

    # Check for command-line usage.
    if len(sys.argv) != 3:
        print("Usage: python dna.py DATABASE SEQUENCE")

    # Read database file into a variable.
    with open(sys.argv[1]) as file:
        reader = csv.reader(file)

        for row in reader:
            database.append(row)

    # Read DNA sequence file into a variable.
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence.
    # Get the STRs from the CSV file by iterating through the row starting from 1 so we omit 'name'.
    for i in range(1, len(database[0])):
        # Each iteration save the STR in a variable.
        subsequence = "".join(x for x in database[0][i])

        # In the 'results' dictionary, save each STR along with the length of the longest run.
        results[subsequence] = longest_match(sequence, subsequence)

    # Convert the results of the STRs to a list containing only the values.
    sequence_dna = list(results.values())

    # Check database for matching profiles by iterating through the CSV file and getting the STRs for each person.
    for person in database[1:][0:]:
        # Save the STR values to a list.
        person_dna = [int(i) for i in person[1:]]

        # Compare the two lists and print the name of the person if there's a match.
        if person_dna == sequence_dna:
            sys.exit(person[0])

    # Print 'No match' if there wasn't a match.
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence.
    for i in range(sequence_length):

        # Initialize count of consecutive runs.
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence.
        # If a match, move substring to next potential match in sequence.
        # Continue moving substring and checking for matches until out of consecutive matches.
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring.
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring.
            else:
                break

        # Update most consecutive matches found.
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found.
    return longest_run


if __name__ == "__main__":
    main()
