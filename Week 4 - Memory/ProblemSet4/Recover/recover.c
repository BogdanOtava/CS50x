/*
https://cs50.harvard.edu/x/2023/psets/4/recover/
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Check for proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover filename.raw\n");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Create buffer - pointer to where to store the read data
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];

    // Counter for number of JPEGs found on the memory card
    int counter = 0;

    // Allocate enough bytes for the name of the file
    char *filename = malloc(8 * sizeof(char));

    // Output file
    FILE *output = NULL;

    // Loop through the data on the card and read every block of 512 bytes into a buffer
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // Check if it's the start of a new JPEG
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0)
        {
            // If it's the first JPEG
            if (counter == 0)
            {
                // Start writing the first file - 000.jpg
                sprintf(filename, "%03i.jpg", counter);
                output = fopen(filename, "w");
                fwrite(buffer, 1, BLOCK_SIZE, output);

                counter++;
            }

            // If already found a JPEG
            else if (counter > 0)
            {
                // Close the current file and open up a new file to continue writing to
                fclose(output);
                sprintf(filename, "%03i.jpg", counter);
                output = fopen(filename, "w");
                fwrite(buffer, 1, BLOCK_SIZE, output);
                counter++;
            }
        }

        // If it's not the start of a new JPEG
        else if (counter > 0)
        {
            // Keep writing to it because it's the next 512 bytes block of the current JPEG
            fwrite(buffer, 1, BLOCK_SIZE, output);
        }
    }

    // Close remaining files
    free(filename);
    fclose(file);
    fclose(output);
}
