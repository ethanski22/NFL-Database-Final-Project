# search_player.py
# command to run:
# python search_player.py --name "Mahomes"

import argparse
import psycopg2

def search_player(name):
    conn = psycopg2.connect(database="nfl", user="your_user", password="your_pass")
    cur = conn.cursor()
    query = """
        SELECT p.first_name, p.last_name, t.team_name, pos.position_code, p.jersey_number
        FROM Player p
        JOIN Team t ON p.team_id = t.team_id
        JOIN Position pos ON p.position_id = pos.position_id
        WHERE LOWER(p.first_name || ' ' || p.last_name) LIKE LOWER(%s);
    """
    cur.execute(query, (f"%{name}%",))
    for row in cur.fetchall():
        print(f"{row[0]} {row[1]} - {row[2]} ({row[3]} #{row[4]})")
    cur.close()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Player name to search for")
    args = parser.parse_args()

    if args.name:
        search_player(args.name)
