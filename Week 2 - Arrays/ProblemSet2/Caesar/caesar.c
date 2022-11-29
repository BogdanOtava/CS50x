/*
https://cs50.harvard.edu/x/2022/psets/2/caesar/
*/

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string arg);
char rotate(char chr, int key);

int main(int argc, string argv[])
{
    // Check for the argument count to be exactly 2
    if (!(argc == 2))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check for the second argument to be a digit
    if (!(only_digits(argv[1])))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Get user input
    string plaintext = get_string("plaintext: ");

    // Print output
    printf("ciphertext: ");
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        printf("%c", rotate(plaintext[i], atoi(argv[1])));
    }
    printf("\n");
}

// Checks that the argument is only digits from 0 to 9
bool only_digits(string arg)
{
    if (isdigit(arg[0]))
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Shifts 'char' by the 'key' value
char rotate(char chr, int key)
{
    // if 'char' is a letter, shift it by 'key' value
    if (isalpha(chr))
    {
        if (isupper(chr))
        {
            return (chr - 'A' + key) % 26 + 'A';
        }
        if (islower(chr))
        {
            return (chr - 'a' + key) % 26 + 'a';
        }

        return 0;
    }
    // if 'char' is anything else, return 'char' as is
    else
    {
        return chr;
    }
}
