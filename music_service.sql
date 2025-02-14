CREATE TABLE Genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE ArtistGenres (
    artist_id INT REFERENCES Artists(id) ON DELETE CASCADE,
    genre_id INT REFERENCES Genres(id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE Albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL
);

CREATE TABLE ArtistAlbums (
    artist_id INT REFERENCES Artists(id) ON DELETE CASCADE,
    album_id INT REFERENCES Albums(id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE Tracks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration TIME NOT NULL,
    album_id INT REFERENCES Albums(id) ON DELETE CASCADE
);

CREATE TABLE Compilations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL
);

CREATE TABLE CompilationTracks (
    compilation_id INT REFERENCES Compilations(id) ON DELETE CASCADE,
    track_id INT REFERENCES Tracks(id) ON DELETE CASCADE,
    PRIMARY KEY (compilation_id, track_id)
);


INSERT INTO Genres (name) VALUES 
('Rock'),
('Pop'),
('Jazz');

INSERT INTO Artists (name) VALUES 
('Queen'),
('Adele'),
('Miles Davis');

INSERT INTO ArtistGenres (artist_id, genre_id) VALUES
(1, 1), -- Queen играет Rock
(2, 2), -- Adele исполняет Pop
(3, 3); -- Miles Davis играет Jazz

INSERT INTO Albums (title, release_year) VALUES
('A Night at the Opera', 1975),
('21', 2011),
('Kind of Blue', 1959);

INSERT INTO ArtistAlbums (artist_id, album_id) VALUES
(1, 1), -- Queen выпустили "A Night at the Opera"
(2, 2), -- Adele выпустила "21"
(3, 3); -- Miles Davis выпустил "Kind of Blue"

INSERT INTO Tracks (title, duration, album_id) VALUES
('Bohemian Rhapsody', '00:05:55', 1),
('Rolling in the Deep', '00:03:48', 2),
('So What', '00:09:22', 3);

INSERT INTO Compilations (title, release_year) VALUES
('Greatest Hits', 2020);

INSERT INTO CompilationTracks (compilation_id, track_id) VALUES
(1, 1), -- "Bohemian Rhapsody" в "Greatest Hits"
(1, 2); -- "Rolling in the Deep" в "Greatest Hits"





