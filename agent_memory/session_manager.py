#!/usr/bin/env python3
"""
Agent Session Manager - Quick utilities for managing Copilot CLI sessions
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add agent_memory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agent_memory" / "src"))

from db import get_db
from conversations import start_conversation, end_conversation, list_conversations
from preferences import add_preference, list_preferences
from insights import add_insight, list_insights

WORKSPACE_ROOT = Path(__file__).parent.parent


def quick_start(title, tags=None):
    """Quick start a session and return the conversation ID"""
    conv_id = start_conversation(title, tags)
    print(f"✅ Session started: {conv_id}")
    print(f"   Title: {title}")
    if tags:
        print(f"   Tags: {', '.join(tags)}")
    print("\n💡 To log messages:")
    print(f"   python agent_memory/cli.py msg {conv_id} user \"<message>\"")
    print(f"   python agent_memory/cli.py msg {conv_id} assistant \"<response>\"")
    print("\n💡 To end session:")
    print(f"   python agent_memory/cli.py end {conv_id} -s \"<summary>\"")
    return conv_id


def quick_end(conv_id, summary):
    """Quick end a session"""
    end_conversation(conv_id, summary)
    print(f"✅ Session ended: {conv_id}")
    print(f"   Summary: {summary}")


def active_session():
    """Get the active session info"""
    db = get_db()
    cursor = db.execute("""
        SELECT id, title, start_time, tags
        FROM conversations
        WHERE end_time IS NULL
        ORDER BY start_time DESC
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    if not row:
        print("No active session")
        return None
    
    print(f"🟢 Active Session: {row['id']}")
    print(f"   Title: {row['title']}")
    print(f"   Started: {row['start_time']}")
    if row['tags']:
        print(f"   Tags: {row['tags']}")
    return row['id']


def recent_sessions(limit=5):
    """Show recent sessions"""
    convs = list_conversations(limit)
    if not convs:
        print("No sessions found")
        return
    
    print(f"\n📋 Recent Sessions (last {limit})")
    for conv in convs:
        status = "🟢" if conv['end_time'] is None else "⚪"
        print(f"\n{status} [{conv['id']}] {conv['title']}")
        print(f"   Started: {conv['start_time']}")
        if conv['end_time']:
            print(f"   Ended: {conv['end_time']}")
        if conv['tags']:
            print(f"   Tags: {conv['tags']}")
        if conv['summary']:
            print(f"   Summary: {conv['summary'][:60]}...")


def session_stats():
    """Show session statistics"""
    db = get_db()
    
    # Total sessions
    total = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    
    # Active
    active = db.execute("SELECT COUNT(*) FROM conversations WHERE end_time IS NULL").fetchone()[0]
    
    # This week
    this_week = db.execute("""
        SELECT COUNT(*) FROM conversations 
        WHERE start_time >= datetime('now', '-7 days')
    """).fetchone()[0]
    
    # Total messages
    messages = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    # Avg messages per session
    avg_messages = round(messages / total, 1) if total > 0 else 0
    
    print("\n📊 Session Statistics")
    print(f"   Total sessions: {total}")
    print(f"   Active now: {active}")
    print(f"   This week: {this_week}")
    print(f"   Total messages: {messages}")
    print(f"   Avg messages/session: {avg_messages}")


def work_context():
    """Show current work context (preferences + recent insights)"""
    print("\n⚙️ Work Context\n")
    
    # Key preferences
    prefs = list_preferences()
    if prefs:
        print("📌 Key Preferences:")
        for cat in ['work', 'tech', 'workflow']:
            cat_prefs = [p for p in prefs if p['category'] == cat]
            if cat_prefs:
                print(f"\n[{cat}]")
                for p in cat_prefs[:3]:  # Top 3 per category
                    print(f"   {p['key']}: {p['value']}")
    
    # Recent insights
    db = get_db()
    cursor = db.execute("""
        SELECT type, content, created_at
        FROM insights
        ORDER BY created_at DESC
        LIMIT 5
    """)
    
    insights = cursor.fetchall()
    if insights:
        print("\n💡 Recent Insights:")
        for insight in insights:
            print(f"\n[{insight['type']}] {insight['content'][:60]}...")
            print(f"   {insight['created_at']}")


def export_session(conv_id, output_file=None):
    """Export a session to JSON"""
    db = get_db()
    
    # Get conversation
    cursor = db.execute("""
        SELECT id, title, start_time, end_time, summary, tags
        FROM conversations
        WHERE id = ?
    """, (conv_id,))
    
    conv_row = cursor.fetchone()
    if not conv_row:
        print(f"❌ Session {conv_id} not found")
        return
    
    conv = dict(conv_row)
    
    # Get messages
    cursor = db.execute("""
        SELECT role, content, timestamp
        FROM messages
        WHERE conversation_id = ?
        ORDER BY timestamp
    """, (conv_id,))
    
    conv['messages'] = [dict(row) for row in cursor.fetchall()]
    
    # Output
    if output_file is None:
        output_file = WORKSPACE_ROOT / "agent_memory" / "exports" / f"session_{conv_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conv, f, indent=2)
    
    print(f"✅ Session exported to: {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Session Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    # Quick start
    p = subparsers.add_parser("start", help="Quick start a session")
    p.add_argument("title", help="Session title")
    p.add_argument("--tags", help="Comma-separated tags")
    
    # Quick end
    p = subparsers.add_parser("end", help="Quick end active session")
    p.add_argument("conv_id", type=int, help="Conversation ID")
    p.add_argument("summary", help="Summary")
    
    # Active
    subparsers.add_parser("active", help="Show active session")
    
    # Recent
    p = subparsers.add_parser("recent", help="Show recent sessions")
    p.add_argument("-n", "--limit", type=int, default=5, help="Number to show")
    
    # Stats
    subparsers.add_parser("stats", help="Show session statistics")
    
    # Context
    subparsers.add_parser("context", help="Show work context")
    
    # Export
    p = subparsers.add_parser("export", help="Export session to JSON")
    p.add_argument("conv_id", type=int, help="Conversation ID")
    p.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "start":
        tags = args.tags.split(",") if args.tags else None
        quick_start(args.title, tags)
    elif args.command == "end":
        quick_end(args.conv_id, args.summary)
    elif args.command == "active":
        active_session()
    elif args.command == "recent":
        recent_sessions(args.limit)
    elif args.command == "stats":
        session_stats()
    elif args.command == "context":
        work_context()
    elif args.command == "export":
        export_session(args.conv_id, args.output)


if __name__ == "__main__":
    main()
