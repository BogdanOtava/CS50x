/*
Write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
Your query should output a table with a single column for the name of each person.
People with the same birth year may be listed in any order.
No need to worry about people who have no birth year listed, so long as those who do have a birth year are listed in order.
If a person appeared in more than one movie in 2004, they should only appear in your results once.
*/

SELECT DISTINCT people.name
FROM people
JOIN stars
ON stars.person_id = people.id

JOIN movies
ON movies.id = stars.movie_id
WHERE movies.year = 2004
ORDER BY people.birth;
