/*
Write a SQL query that returns the average energy of songs that are by Drake.
Your query should output a table with a single column and a single row containing the average energy.
You should not make any assumptions about what Drake’s artist_id is.
*/

SELECT AVG(energy) 
FROM songs
WHERE artist_id = (
    SELECT id 
    FROM artists 
    WHERE name = "Drake");
