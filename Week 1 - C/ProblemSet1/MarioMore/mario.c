/*
https://cs50.harvard.edu/x/2023/psets/1/mario/more/
*/

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Declare height variable
    int height;

    // Get user input
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Outer loop / Switch to the next line of the pyramid after printing the spaces and blocks
    for (int line = 0; line < height; line++)
    {
        // Print the spaces
        for (int space = height - 1; space > line; space--)
        {
            printf(" ");
        }

        // Print the left blocks
        for (int left_blocks = 0; left_blocks <= line; left_blocks++)
        {
            printf("#");
        }

        // Print the two spaces between the blocks
        printf("  ");

        // Print the right blocks
        for (int right_blocks = 0; right_blocks <= line; right_blocks++)
        {
            printf("#");
        }

        // Go to the next line
        printf("\n");
    }
}
