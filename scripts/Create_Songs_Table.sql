use Spotify;

create table Songs
(
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
    song_id CHAR(50),
	song_name CHAR(1000),
    danceability FLOAT,
    energy FLOAT,
    musical_key TINYINT,
    loudness FLOAT,
    musical_mode TINYINT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_ms INT,
    time_signature TINYINT,
    num_sections SMALLINT,
    explicit TINYINT,
    popular TINYINT,
    PRIMARY KEY (id)
)