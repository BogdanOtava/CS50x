/*
https://cs50.harvard.edu/x/2023/labs/1/
*/

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int start;
    int end;
    int years;

    do
    {
        start = get_int("Start size: ");
    }
    while (start < 9);

    // Prompt for end size
    do
    {
        end = get_int("End size: ");
    }
    while (end < start);

    // Calculate number of years until we reach threshold
    for (years = 0; start < end; years++)
    {
        start = start + (start / 3) - (start / 4);
    }

    // Print number of years
    printf("Years: %i\n", years);
}
