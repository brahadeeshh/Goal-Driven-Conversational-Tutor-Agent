import sqlite3
from datetime import datetime

DB_NAME = "tutor.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            subject TEXT,
            target TEXT,
            duration INTEGER,
            level TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_goal(student_name, subject, target, duration, level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO goals
        (student_name, subject, target, duration, level, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        subject,
        target,
        duration,
        level,
        datetime.now().isoformat()
    ))

    goal_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return goal_id


def save_progress(goal_id, topic, score, total, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO progress
        (goal_id, topic, score, total, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        goal_id,
        topic,
        score,
        total,
        status,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_progress(goal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, score, total, status
        FROM progress
        WHERE goal_id = ?
    """, (goal_id,))

    results = cursor.fetchall()

    conn.close()

    return results