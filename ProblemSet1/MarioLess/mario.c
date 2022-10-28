#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Declare height:
    int height;

    // Get height from user:
    do
    {
        height = get_int("Height: ");
    } while (height < 1 || height > 8);

    // Outer loop / Switch to next line of the pyramid after printing the spaces and blocks:
    for (int line = 0; line < height; line++)
    {
        // Print the spaces:
        for (int space = height - 1; space > line; space--)
        {
            printf(" ");
        }

        // Print the block:
        for (int block = 0; block <= line; block++)
        {
            printf("#");
        }

        // Go to the next line:
        printf("\n");
    }
}
