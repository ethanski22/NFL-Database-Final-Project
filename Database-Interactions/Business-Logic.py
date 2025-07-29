import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

# Connect to Azure SQL Database
try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    print("✅ Connected to the database successfully!\n")
except Exception as e:
    print("❌ Database connection failed:", e)
    exit()

# Query for average YPA
query = """
SELECT 
    p.first_name + ' ' + p.last_name AS player_name,
    t.team_name,
    AVG(CASE WHEN ps.passing_attempts > 0 THEN 
        CAST(ps.passing_yards AS DECIMAL(10,2)) / ps.passing_attempts
    ELSE 0 END) AS avg_ypa
FROM PlayerStats ps
JOIN Player p ON ps.player_id = p.player_id
JOIN Team t ON p.team_id = t.team_id
GROUP BY p.first_name, p.last_name, t.team_name
ORDER BY avg_ypa DESC;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Business logic
def categorize(avg_ypa):
    if avg_ypa >= 8.0:
        return "Elite Passer"
    elif avg_ypa >= 6.5:
        return "Above Average"
    else:
        return "Needs Improvement"

# Display results
print("Player Performance Report\n")
print(f"{'Player':<25} {'Team':<15} {'Avg YPA':<10} {'Category'}")
print("-" * 60)


for row in rows:
    player_name = row[0]
    team_name = row[1]
    avg_ypa = float(row[2])
    category = categorize(avg_ypa)
    print(f"{player_name:<25} {team_name:<15} {avg_ypa:<10.2f} {category}")

# Close connection
cursor.close()
conn.close()

input("\nPress Enter to exit...")