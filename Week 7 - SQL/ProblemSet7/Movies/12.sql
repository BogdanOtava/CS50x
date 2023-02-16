/*
Write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
Your query should output a table with a single column for the title of each movie.
You may assume that there is only one person in the database with the name Johnny Depp.
You may assume that there is only one person in the database with the name Helena Bonham Carter.
*/

SELECT movies.title
FROM movies
JOIN stars
ON stars.movie_id = movies.id

JOIN people
ON people.id = stars.person_id
WHERE people.name = "Johnny Depp"

INTERSECT

SELECT movies.title
FROM movies
JOIN stars
ON stars.movie_id = movies.id

JOIN people
ON people.id = stars.person_id
WHERE people.name = "Helena Bonham Carter";
