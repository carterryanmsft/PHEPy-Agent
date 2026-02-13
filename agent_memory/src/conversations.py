"""Conversation management functions"""

from datetime import datetime
from db import get_db


def start_conversation(title, tags=None):
    """Start a new conversation"""
    db = get_db()
    tags_str = ",".join(tags) if tags else None
    cursor = db.execute(
        "INSERT INTO conversations (title, tags) VALUES (?, ?)",
        (title, tags_str)
    )
    db.commit()
    return cursor.lastrowid


def add_message(conversation_id, role, content):
    """Add a message to a conversation"""
    db = get_db()
    db.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, role, content)
    )
    db.commit()


def end_conversation(conversation_id, summary=None):
    """End a conversation"""
    db = get_db()
    db.execute(
        "UPDATE conversations SET end_time = CURRENT_TIMESTAMP, summary = ? WHERE id = ?",
        (summary, conversation_id)
    )
    db.commit()


def list_conversations(limit=10):
    """List recent conversations"""
    db = get_db()
    cursor = db.execute("""
        SELECT id, title, start_time, end_time, summary, tags
        FROM conversations
        ORDER BY start_time DESC
        LIMIT ?
    """, (limit,))
    
    return [dict(row) for row in cursor.fetchall()]


def get_conversation(conversation_id):
    """Get a conversation with its messages"""
    db = get_db()
    
    # Get conversation
    cursor = db.execute("""
        SELECT id, title, start_time, end_time, summary, tags
        FROM conversations
        WHERE id = ?
    """, (conversation_id,))
    
    conv_row = cursor.fetchone()
    if not conv_row:
        return None
    
    conv = dict(conv_row)
    
    # Get messages
    cursor = db.execute("""
        SELECT role, content, timestamp
        FROM messages
        WHERE conversation_id = ?
        ORDER BY timestamp
    """, (conversation_id,))
    
    conv["messages"] = [dict(row) for row in cursor.fetchall()]
    return conv


def get_active_conversation():
    """Get the most recent active conversation"""
    db = get_db()
    cursor = db.execute("""
        SELECT id, title, start_time, tags
        FROM conversations
        WHERE end_time IS NULL
        ORDER BY start_time DESC
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    return dict(row) if row else None
