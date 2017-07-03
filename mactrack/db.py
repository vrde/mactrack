import sqlite3
import logging


log = logging.getLogger(__name__)


FILENAME = 'mactrack.db'

TABLES = {
    'beacons': '''CREATE TABLE beacons (
        id TEXT PRIMARY KEY,
        dt TEXT,
        dbm INTEGER,
        sa TEXT,
        sa_resolved TEXT,
        lat REAL,
        lon REAL)'''
}

INSERTS = {
    'beacons': '''INSERT INTO beacons (
        id,
        dt,
        dbm,
        sa,
        sa_resolved,
        lat,
        lon)
        VALUES (?, ?, ?, ?, ?, ?, ?)'''
}


def get_conn():
    return sqlite3.connect(FILENAME)


def create_tables():
    conn = get_conn()
    cursor = conn.cursor()

    for table, query in TABLES.items():
        log.info('Create table "%s"', table)
        cursor.execute(query)

    conn.close()


def insert_beacon(conn, id_, dt, dbm, sa, sa_resolved, lat, lon):
    cursor = conn.cursor()
    cursor.execute(INSERTS['beacons'], (id_, dt, dbm, sa, sa_resolved, lat, lon))
    conn.commit()
