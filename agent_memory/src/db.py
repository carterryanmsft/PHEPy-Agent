"""Database connection and initialization"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent.parent / "memory.db"


def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_context():
    """Context manager for database connections"""
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database schema"""
    conn = get_db()
    
    # Conversations table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            summary TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Messages table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)
    
    # Preferences table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(category, key)
        )
    """)
    
    # Insights table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK (type IN ('goal', 'decision', 'pattern', 'context')),
            content TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Full-text search tables
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            content,
            content=messages,
            content_rowid=id
        )
    """)
    
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS insights_fts USING fts5(
            content,
            tags,
            content=insights,
            content_rowid=id
        )
    """)
    
    # Triggers to keep FTS in sync
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
        END
    """)
    
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
            DELETE FROM messages_fts WHERE rowid = old.id;
        END
    """)
    
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS insights_ai AFTER INSERT ON insights BEGIN
            INSERT INTO insights_fts(rowid, content, tags) VALUES (new.id, new.content, new.tags);
        END
    """)
    
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS insights_ad AFTER DELETE ON insights BEGIN
            DELETE FROM insights_fts WHERE rowid = old.id;
        END
    """)
    
    # Create indexes
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversations_start_time 
        ON conversations(start_time DESC)
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation 
        ON messages(conversation_id, timestamp)
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_preferences_category 
        ON preferences(category, key)
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_insights_type 
        ON insights(type, created_at DESC)
    """)
    
    conn.commit()
    conn.close()
