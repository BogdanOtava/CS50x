/*
Write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
Your query should output a table with a single column for the title of each movie.
You may assume that there is only one person in the database with the name Chadwick Boseman.
*/

SELECT movies.title
FROM movies
JOIN stars
ON stars.movie_id = movies.id

JOIN people
ON people.id = stars.person_id

JOIN ratings
ON ratings.movie_id = movies.id
WHERE people.name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;
