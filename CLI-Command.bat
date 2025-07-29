::Set up environment variables for database connection
:: This batch file connects to an Azure SQL Database and executes a query to retrieve player data for
:: a specific team, in this case, the Cincinnati Bengals.

@echo off
set SERVER=data-final-server.database.windows.net
set USER=fairview
set PASSWORD=Password123!
set DATABASE=data-final-db

set QUERY=SELECT * FROM Player WHERE team_id = (SELECT team_id FROM Team WHERE team_name = 'Cincinnati Bengals');

sqlcmd -S %SERVER% -U %USER% -P %PASSWORD% -d %DATABASE% -Q "%QUERY%"
pause
