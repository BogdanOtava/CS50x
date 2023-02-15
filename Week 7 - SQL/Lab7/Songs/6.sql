/*
Write a SQL query that lists the names of songs that are by Post Malone.
Your query should output a table with a single column for the name of each song.
You should not make any assumptions about what Post Malone’s artist_id is.
*/

SELECT name 
FROM songs
WHERE artist_id = (
    SELECT id 
    FROM artists 
    WHERE name = "Post Malone");
