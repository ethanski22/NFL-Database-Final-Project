-- This SQL query retrieves the average yards per attempt (YPA) for each player in each team,
-- grouped by conference, division, and team. It calculates the average YPA only for players
-- who have passing attempts greater than zero, ensuring that the division by zero does not occur.

SELECT 
    conf.name AS conference_name,
    d.division_name,
    t.team_name,
    p.first_name,
    p.last_name,
    AVG(CASE 
            WHEN ps.passing_attempts > 0 THEN 
                CAST(ps.passing_yards AS DECIMAL(10,2)) / ps.passing_attempts
            ELSE 0 
        END) AS avg_ypa
FROM PlayerStats ps
JOIN Player p ON ps.player_id = p.player_id
JOIN Team t ON p.team_id = t.team_id
JOIN Division d ON t.division_id = d.division_id
JOIN Conference conf ON d.conference_id = conf.conference_id
GROUP BY conf.name, d.division_name, t.team_name, p.first_name, p.last_name
ORDER BY conf.name, d.division_name, t.team_name, avg_ypa DESC;