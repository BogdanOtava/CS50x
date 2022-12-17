#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through rows
    for (int row = 0; row < height; row++)
    {
        // Loop through columns
        for (int column = 0; column < width; column++)
        {
            // Round out the values of each pixel
            int avgGray = round((image[row][column].rgbtBlue + image[row][column].rgbtGreen + image[row][column].rgbtRed) / 3.0);

            // Change pixel color to new color
            image[row][column].rgbtRed = avgGray;
            image[row][column].rgbtGreen = avgGray;
            image[row][column].rgbtBlue = avgGray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through rows
    for (int row = 0; row < height; row++)
    {
        // Loop through columns
        for (int column = 0; column < width; column++)
        {
            // Make the sepia color for each pixel
            int sepiaRed = round(.393 * image[row][column].rgbtRed + .769 * image[row][column].rgbtGreen + .189 * image[row][column].rgbtBlue);
            int sepiaGreen = round(.349 * image[row][column].rgbtRed + .686 * image[row][column].rgbtGreen + .168 * image[row][column].rgbtBlue);
            int sepiaBlue = round(.272 * image[row][column].rgbtRed + .534 * image[row][column].rgbtGreen + .131 * image[row][column].rgbtBlue);

            // Change value to 255 if bigger than that
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Change pixel color to sepia color
            image[row][column].rgbtRed = sepiaRed;
            image[row][column].rgbtGreen = sepiaGreen;
            image[row][column].rgbtBlue = sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through rows
    for (int row = 0; row < height; row++)
    {
        // Loop through the first half of columns in each row
        for (int column = 0; column < width / 2; column++)
        {
            // Store the left column in a temporary variable;
            RGBTRIPLE temp = image[row][column];
            // Move the right column in the left spot
            image[row][column] = image[row][width - column - 1];
            // Move the left column in the right spot
            image[row][width - column - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare image variable
    RGBTRIPLE temp[height][width];

    // Loop through rows
    for (int row = 0; row < height; row++)
    {
        // Loop through columns
        for (int column = 0; column < width; column++)
        {
            // Duplicate the original image
            temp[row][column] = image[row][column];
        }
    }

    // Loop through rows
    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            // // Initialize the variables
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;

            float counter = 0;

            // Loop through the surrounding pixels for each pixel (3x3 grid)
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    // Check for the pixel to be in the grid and skip if it isn't
                    if (row + i < 0 || row + i >= height)
                    {
                        continue;
                    }
                    if (column + j < 0 || column + j >= width)
                    {
                        continue;
                    }
                    // Add to sum
                    sumRed += temp[row + i][column + j].rgbtRed;
                    sumGreen += temp[row + i][column + j].rgbtGreen;
                    sumBlue += temp[row + i][column +j].rgbtBlue;

                    counter++;
                }
            }

            // Add the blur effect to the original image
            image[row][column].rgbtRed = round(sumRed / counter);
            image[row][column].rgbtGreen = round(sumGreen / counter);
            image[row][column].rgbtBlue = round(sumBlue / counter);
        }
    }
}
