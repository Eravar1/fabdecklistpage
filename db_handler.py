import psycopg2
from psycopg2 import sql, pool
from config import DB_CONFIG
import logging
import threading
from contextlib import contextmanager

class DatabaseHandler:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_pool()
        return cls._instance
        
    def _init_pool(self):
        """Initialize the connection pool"""
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,  # Adjust based on your needs
            **DB_CONFIG
        )
        logging.info("Database connection pool initialized")
    
    @contextmanager
    def _get_cursor(self):
        """Context manager for getting a cursor"""
        conn = self.pool.getconn()
        try:
            with conn:
                with conn.cursor() as cursor:
                    yield cursor
        finally:
            self.pool.putconn(conn)
    
    def execute_query(self, query, params=None, fetch=False):
        """Generic query execution method"""
        with self._get_cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
    
    def add_tournament(self, name, url, date=None, region=None):
        """Add a tournament with proper conflict handling"""
        query = sql.SQL("""
            INSERT INTO tournaments (name, url, date, region)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
            RETURNING id
        """)
        result = self.execute_query(query, (name, url, date, region), fetch=True)
        return result[0][0] if result else None
    
    def add_player(self, name):
        """Add a player with proper conflict handling and return type"""
        query = sql.SQL("""
            INSERT INTO players (name)
            VALUES (%s)
            ON CONFLICT (name) DO UPDATE
            SET name = EXCLUDED.name
            RETURNING id
        """)
        result = self.execute_query(query, (name,), fetch=True)
        return result[0][0] if result else None

    def get_player_id(self, name):
        """Get player ID by name with proper return type handling"""
        query = sql.SQL("SELECT id FROM players WHERE name = %s")
        result = self.execute_query(query, (name,), fetch=True)
        return result[0][0] if result else None

    def add_decklist(self, player_id, tournament, hero, decklist_url):
        """Add decklist with proper return type handling"""
        query = sql.SQL("""
            INSERT INTO decklists (player_id, tournament, hero, decklist_url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (player_id, tournament) DO UPDATE
            SET hero = EXCLUDED.hero,
                decklist_url = EXCLUDED.decklist_url
            RETURNING id
        """)
        result = self.execute_query(query, (player_id, tournament, hero, decklist_url), fetch=True)
        return result[0][0] if result else None 

    def get_player_decklists(self, player_name):
        """Get all decklists for a player"""
        query = sql.SQL("""
            SELECT d.hero, d.decklist_url, d.tournament
            FROM decklists d
            JOIN players p ON d.player_id = p.id
            WHERE p.name = %s
            ORDER BY d.tournament DESC
        """)
        return self.execute_query(query, (player_name,), fetch=True)
    
    def close(self):
        """Close all connections in the pool"""
        self.pool.closeall()
        logging.info("Database connection pool closed")