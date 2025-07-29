# Business Logic for NFL Player Performance Report. Begins by connecting to Azure SQL Database,
# executing a SQL query to retrieve average yards per attempt (YPA) for players, categorizing their performance,
# and displaying the results in a formatted report. The script uses environment variables for database credentials
# and handles exceptions during the database connection process. The SQL query is read from an external file.

# Imports
import pyodbc
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

# Connect to Azure SQL DB
try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    print("Connected to the database successfully!\n")
except Exception as e:
    print("Database connection failed:", e)
    exit()

# Query for average YPA via Sql-Queries.sql
with open(r"C:\Users\joshn\NFL-Database-Final-Project\Database-Interactions\Sql-Queries.sql", "r") as file:
    query = file.read()

cursor.execute(query)

rows = cursor.fetchall()

# Business logic
def categorize(avg_ypa):
    if avg_ypa >= 8.0:
        return "Elite"
    elif avg_ypa >= 6.5:
        return "Above Average"
    else:
        return "Needs Improvement"

# Display results
print("Player Performance Report\n")
print(f"{'Player':<25} {'Team':<15} {'Avg YPA':<10} {'Category'}")
print("-" * 60)


for row in rows:
    conference_name = row[0]
    division_name = row[1]
    team_name = row[2]
    player_name = f"{row[3]} {row[4]}"
    avg_ypa = float(row[5])
    category = categorize(avg_ypa)

    print(f"{player_name:<25} {team_name:<15} {avg_ypa:<10.2f} {category}")


# Close connection
cursor.close()
conn.close()