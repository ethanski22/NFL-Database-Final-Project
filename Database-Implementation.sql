CREATE TABLE Conference (
    conference_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Division (
    division_id INT IDENTITY(1,1) PRIMARY KEY,
    division_name VARCHAR(255) NOT NULL,
    conference_id INT NOT NULL,
    FOREIGN KEY (conference_id) REFERENCES Conference(conference_id)
);

CREATE TABLE Stadium (
    stadium_id INT IDENTITY(1,1) PRIMARY KEY,
    address VARCHAR(255),
    name VARCHAR(255),
    sponsor VARCHAR(255),
    max_occupancy INT
);

CREATE TABLE Team (
    team_id INT IDENTITY(1,1) PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    abbreviation VARCHAR(10),
    division_id INT NOT NULL,
    team_owner VARCHAR(255),
    stadium_id INT,
    FOREIGN KEY (division_id) REFERENCES Division(division_id),
    FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id)
);

CREATE TABLE Game (
    game_id INT IDENTITY(1,1) PRIMARY KEY,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    game_date DATETIME NOT NULL,
    stadium_id INT,
    FOREIGN KEY (home_team_id) REFERENCES Team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Team(team_id),
    FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id)
);

CREATE TABLE Player (
    player_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    team_id INT NOT NULL,
    position_id INT NOT NULL,
    jersey_number INT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

CREATE TABLE Position (
    position_id INT IDENTITY(1,1) PRIMARY KEY,
    position_code VARCHAR(2),
    description VARCHAR(255)
);

CREATE TABLE PlayerStats (
    stat_id INT IDENTITY(1,1) PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    passing_yards INT,
    rushing_yards INT,
    sacks INT,
    tackles INT,
    fumbles INT,
    interceptions INT,
    ypa DECIMAL(5,2),
    touchdowns INT,
    fieldgoals INT,
    rushing_attempts INT,
    passing_attempts INT,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

-- Insert Conference
INSERT INTO Conference (name) VALUES 
('AFC');

-- Insert Division
INSERT INTO Division (division_name, conference_id) VALUES
('AFC North', 1);

-- Insert Stadiums
INSERT INTO Stadium (address, name, sponsor, max_occupancy) VALUES
('1101 Russell St, Baltimore, MD', 'M&T Bank Stadium', 'M&T Bank', 71008),
('1 Paul Brown Stadium, Cincinnati, OH', 'Paycor Stadium', 'Paycor', 65500),
('100 Alfred Lerner Way, Cleveland, OH', 'FirstEnergy Stadium', 'FirstEnergy', 67550),
('100 Art Rooney Ave, Pittsburgh, PA', 'Acrisure Stadium', 'Acrisure', 68400);

-- Insert Teams
INSERT INTO Team (team_name, city, abbreviation, division_id, team_owner, stadium_id) VALUES
('Baltimore Ravens', 'Baltimore', 'BAL', 1, 'Steve Bisciotti', 1),
('Cincinnati Bengals', 'Cincinnati', 'CIN', 1, 'Mike Brown', 2),
('Cleveland Browns', 'Cleveland', 'CLE', 1, 'Jimmy Haslam', 3),
('Pittsburgh Steelers', 'Pittsburgh', 'PIT', 1, 'Art Rooney II', 4);

-- Insert Position
INSERT INTO Position (position_code, description) VALUES
('QB', 'Quarterback');

-- Insert Players (AFC North QBs)
INSERT INTO Player (first_name, last_name, team_id, position_id, jersey_number) VALUES
('Lamar', 'Jackson', 1, 1, 8),
('Joe', 'Burrow', 2, 1, 9),
('Deshaun', 'Watson', 3, 1, 4),
('Kenny', 'Pickett', 4, 1, 8);

-- Insert Games
INSERT INTO Game (home_team_id, away_team_id, game_date, stadium_id) VALUES
(1, 2, '2025-09-10 13:00:00', 1),
(3, 4, '2025-09-11 13:00:00', 3),
(2, 3, '2025-09-18 13:00:00', 2),
(4, 1, '2025-09-19 13:00:00', 4);

-- Insert Player Stats
INSERT INTO PlayerStats (game_id, player_id, passing_yards, rushing_yards, sacks, tackles, fumbles, interceptions, ypa, touchdowns, fieldgoals, rushing_attempts, passing_attempts) VALUES
(1, 1, 275, 60, 2, 0, 1, 0, 7.5, 3, 0, 8, 35),
(1, 2, 310, 15, 1, 0, 0, 1, 8.0, 2, 0, 4, 40),
(2, 3, 250, 10, 3, 0, 0, 2, 6.5, 1, 0, 3, 37),
(2, 4, 225, 20, 4, 0, 0, 0, 6.0, 2, 0, 5, 38),
(3, 2, 290, 30, 2, 0, 0, 1, 7.2, 3, 0, 7, 39),
(3, 3, 260, 25, 3, 0, 1, 2, 6.8, 2, 0, 6, 36),
(4, 4, 240, 40, 2, 0, 1, 1, 6.4, 1, 0, 8, 34),
(4, 1, 280, 50, 1, 0, 0, 0, 7.6, 3, 0, 10, 38);

