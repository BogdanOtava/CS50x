/*
https://cs50.harvard.edu/x/2023/psets/5/speller/
*/

// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 1000;

// Counter for the number of words in the dictionary
int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain a hash value
    int index = hash(word);

    // Cursor to move through the linked lists
    node *cursor = table[index];

    // Access linked list at that index in the hash table and traverse it
    while (cursor != NULL)
    {
        // If the word is found return true, else move cursor to the next node
        if (strcasecmp(cursor->word, word) != 0)
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // This is the function I came up with, it's not as fast as the staff's implementation but significantly faster than the one from the distribution code
    int points = 0;

    for (int i = 0, len = strlen(word); i < len; i++)
    {
        points += toupper(word[i]) - 'A';
    }

    return points % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    // Read strings from file one at a time
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create a new node for each word
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // Copy word into node and set the next node to NULL
        strcpy(n->word, word);
        n->next = NULL;

        // Hash word to obtain a hash value
        int index = hash(word);

        // Insert node into hash table in the corresponding bucket
        n->next = table[index];
        table[index] = n;
        counter++;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Cursor to move through the linked lists
    node *cursor = NULL;

    // Iterating through the buckets of the hash table
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];

        // Iterate through the linked lists and free the allocated memory for it's nodes
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;

            free(temp);
        }
    }

    return true;
}
