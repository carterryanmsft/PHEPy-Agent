"""Preferences and insights management"""

from db import get_db


def list_preferences(category=None):
    """List preferences, optionally filtered by category"""
    db = get_db()
    
    if category:
        cursor = db.execute("""
            SELECT category, key, value, confidence, updated_at
            FROM preferences
            WHERE category = ?
            ORDER BY category, key
        """, (category,))
    else:
        cursor = db.execute("""
            SELECT category, key, value, confidence, updated_at
            FROM preferences
            ORDER BY category, key
        """)
    
    return [dict(row) for row in cursor.fetchall()]


def add_preference(category, key, value, confidence=1.0):
    """Add or update a preference"""
    db = get_db()
    db.execute("""
        INSERT INTO preferences (category, key, value, confidence)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(category, key) DO UPDATE SET
            value = excluded.value,
            confidence = excluded.confidence,
            updated_at = CURRENT_TIMESTAMP
    """, (category, key, value, confidence))
    db.commit()


def get_preference(category, key):
    """Get a specific preference"""
    db = get_db()
    cursor = db.execute("""
        SELECT category, key, value, confidence, updated_at
        FROM preferences
        WHERE category = ? AND key = ?
    """, (category, key))
    
    row = cursor.fetchone()
    return dict(row) if row else None


def list_insights(insight_type=None):
    """List insights, optionally filtered by type"""
    db = get_db()
    
    if insight_type:
        cursor = db.execute("""
            SELECT type, content, tags, created_at
            FROM insights
            WHERE type = ?
            ORDER BY created_at DESC
        """, (insight_type,))
    else:
        cursor = db.execute("""
            SELECT type, content, tags, created_at
            FROM insights
            ORDER BY type, created_at DESC
        """)
    
    return [dict(row) for row in cursor.fetchall()]


def add_insight(insight_type, content, tags=None):
    """Add an insight"""
    db = get_db()
    tags_str = ",".join(tags) if tags else None
    db.execute("""
        INSERT INTO insights (type, content, tags)
        VALUES (?, ?, ?)
    """, (insight_type, content, tags_str))
    db.commit()


def get_recent_insights(limit=10):
    """Get most recent insights across all types"""
    db = get_db()
    cursor = db.execute("""
        SELECT type, content, tags, created_at
        FROM insights
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    
    return [dict(row) for row in cursor.fetchall()]
