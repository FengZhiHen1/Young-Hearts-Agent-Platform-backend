"""Helper script to initialize the database (creates tables).

Run with: `python scripts/init_db.py`
"""
from app.db.session import init_db


if __name__ == "__main__":
    init_db()
    print("Database initialization attempted (check dev.db or DB_URL).")
