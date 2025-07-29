import pyodbc
import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    print("Connected to the database successfully!\n")
except Exception as e:
    print("Database connection failed:", e)
    exit()

def search_team_by_name(cursor):
    team_fragment = input("Enter part of the team's name to search (e.g., 'bengals'): ").strip().lower()

    query = """
    SELECT 
        team_name,
        city,
        abbreviation,
        team_owner
    FROM Team
    WHERE LOWER(team_name) LIKE ?
    """

    like_pattern = f"%{team_fragment}%"
    try:
        cursor.execute(query, (like_pattern,))
        rows = cursor.fetchall()

        if not rows:
            print("\nNo teams found matching that name.\n")
            return

        print("\nMatching Teams:\n")
        print(f"{'Team Name':<20} {'City':<15} {'Abbreviation':<15} {'Owner':<25}")
        print("-" * 75)

        for row in rows:
            # row[0] = team_name, row[1] = city, row[2] = abbreviation, row[3] = team_owner
            print(f"{row[0]:<20} {row[1]:<15} {row[2]:<15} {row[3]:<25}")
        print()
    except Exception as e:
        print("An error occurred while searching for teams:", e)


def search_player_by_name(cursor):
    name_fragment = input("Enter part of the player's name to search (e.g., 'joe'): ").strip().lower()

    query = """
    SELECT 
        p.first_name,
        p.last_name,
        t.team_name,
        p.jersey_number
    FROM Player p
    JOIN Team t ON p.team_id = t.team_id
    WHERE LOWER(p.first_name) LIKE ? OR LOWER(p.last_name) LIKE ?
    """

    like_pattern = f"%{name_fragment}%"
    try:
        cursor.execute(query, (like_pattern, like_pattern))
        rows = cursor.fetchall()

        if not rows:
            print("\nNo players found matching that name.\n")
            return

        print("\nSearch Results:\n")
        print(f"{'Player':<25} {'Team':<20} {'Jersey #':<10}")
        print("-" * 60)

        for row in rows:
            player_name = f"{row[0]} {row[1]}"
            team_name = row[2]
            jersey_number = row[3]
            print(f"{player_name:<25} {team_name:<20} {jersey_number:<10}")
        print()
    except Exception as e:
        print("An error occurred while searching for players:", e)

def main_menu(cursor):
    while True:
        print("\nWhat would you like to search?")
        print("1. Teams")
        print("2. Players")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            search_team_by_name(cursor)
        elif choice == '2':
            search_player_by_name(cursor)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the menu
main_menu(cursor)

# Clean up DB connection
cursor.close()
conn.close()
print("Database connection closed.")
