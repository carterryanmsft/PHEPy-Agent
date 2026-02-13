"""Full-text search across all memory"""

from db import get_db


def search_all(query, limit=10):
    """Search across messages and insights"""
    db = get_db()
    results = []
    
    # Search messages
    cursor = db.execute("""
        SELECT 
            m.id,
            m.content,
            m.timestamp,
            c.title as conversation_title
        FROM messages_fts mf
        JOIN messages m ON m.id = mf.rowid
        JOIN conversations c ON c.id = m.conversation_id
        WHERE messages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    for row in cursor.fetchall():
        results.append({
            "type": "message",
            "title": row["conversation_title"],
            "snippet": row["content"],
            "timestamp": row["timestamp"],
        })
    
    # Search insights
    cursor = db.execute("""
        SELECT 
            i.id,
            i.type,
            i.content,
            i.tags,
            i.created_at
        FROM insights_fts if
        JOIN insights i ON i.id = if.rowid
        WHERE insights_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    for row in cursor.fetchall():
        results.append({
            "type": f"insight ({row['type']})",
            "title": f"{row['type'].title()} Insight",
            "snippet": row["content"],
            "timestamp": row["created_at"],
        })
    
    return results[:limit]


def search_messages(conversation_id, query):
    """Search within a specific conversation"""
    db = get_db()
    cursor = db.execute("""
        SELECT 
            m.role,
            m.content,
            m.timestamp
        FROM messages_fts mf
        JOIN messages m ON m.id = mf.rowid
        WHERE m.conversation_id = ? AND messages_fts MATCH ?
        ORDER BY rank
    """, (conversation_id, query))
    
    return [dict(row) for row in cursor.fetchall()]
