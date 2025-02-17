TRUNCATE TABLE CompilationTracks, Compilations, Tracks, ArtistAlbums, Albums, ArtistGenres, Artists, Genres RESTART IDENTITY CASCADE;

INSERT INTO Genres (id, name) VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Jazz');

INSERT INTO Artists (id, name) VALUES
(1, 'Queen'),
(2, 'Adele'),
(3, 'Miles Davis'),
(4, 'Nirvana');

INSERT INTO Albums (id, title, release_year, artist_id) VALUES
(1, 'A Night at the Opera', 1975, 1),
(2, '21', 2011, 2),
(3, 'Kind of Blue', 1959, 3);

INSERT INTO Tracks (id, title, duration, album_id) VALUES
(1, 'Bohemian Rhapsody', 354, 1),
(2, 'Someone Like You', 285, 2),
(3, 'So What', 540, 3),
(4, 'Smells Like Teen Spirit', 301, 4),
(5, 'Rolling in the Deep', 228, 2),
(6, 'Come As You Are', 219, 4);


SELECT title, duration FROM Tracks
ORDER BY duration DESC
LIMIT 1;

SELECT title FROM Tracks
WHERE duration >= 210;

SELECT title FROM Compilations
WHERE release_year BETWEEN 2018 AND 2020;

SELECT name FROM Artists
WHERE name NOT LIKE '% %';

SELECT title FROM Tracks
WHERE title ILIKE '%мой%' OR title ILIKE '%my%';

SELECT g.name, COUNT(ag.artist_id) 
FROM Genres g
JOIN Artist_Genres ag ON g.id = ag.genre_id
GROUP BY g.name;

SELECT COUNT(t.id) 
FROM Tracks t
JOIN Albums a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

SELECT a.title, AVG(t.duration) 
FROM Albums a
JOIN Tracks t ON a.id = t.album_id
GROUP BY a.title;

SELECT name FROM Artists
WHERE id NOT IN (
    SELECT artist_id FROM Albums WHERE release_year = 2020
);

SELECT DISTINCT c.title 
FROM Compilations c
JOIN Compilation_Tracks ct ON c.id = ct.compilation_id
JOIN Tracks t ON ct.track_id = t.id
JOIN Albums a ON t.album_id = a.id
JOIN Artists ar ON a.artist_id = ar.id
WHERE ar.name = 'Queen';

