/*
Write a SQL query to list all movies released in 2010 and their ratings, in descending order by rating.
For movies with the same rating, order them alphabetically by title.
Your query should output a table with two columns, one for the title of each movie and one for the rating of each movie.
Movies that do not have ratings should not be included in the result.
*/

SELECT movies.title, ratings.rating
FROM movies
JOIN ratings
ON ratings.movie_id = movies.id
WHERE ratings.rating IS NOT NULL
AND year = 2010
ORDER BY ratings.rating DESC, movies.title ASC;
