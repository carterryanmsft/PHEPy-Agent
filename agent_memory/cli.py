#!/usr/bin/env python3
"""
PHEPy Agent Memory CLI
Zero-dependency persistent memory system for GitHub Copilot CLI
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from db import get_db, init_db
from conversations import (
    list_conversations,
    start_conversation,
    add_message,
    end_conversation,
    get_conversation,
)
from preferences import (
    list_preferences,
    add_preference,
    get_preference,
    list_insights,
    add_insight,
)
from search import search_all


def cmd_init(args):
    """Initialize the database"""
    init_db()
    print("✅ Database initialized at memory.db")


def cmd_status(args):
    """Show memory system status"""
    db = get_db()
    
    # Count conversations
    conv_count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    active_count = db.execute(
        "SELECT COUNT(*) FROM conversations WHERE end_time IS NULL"
    ).fetchone()[0]
    
    # Count messages
    msg_count = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    # Count preferences and insights
    pref_count = db.execute("SELECT COUNT(*) FROM preferences").fetchone()[0]
    insight_count = db.execute("SELECT COUNT(*) FROM insights").fetchone()[0]
    
    print("📊 PHEPy Agent Memory Status")
    print(f"   Conversations: {conv_count} (Active: {active_count})")
    print(f"   Messages: {msg_count}")
    print(f"   Preferences: {pref_count}")
    print(f"   Insights: {insight_count}")
    print(f"   Database: {Path(__file__).parent / 'memory.db'}")


def cmd_start(args):
    """Start a new conversation"""
    conv_id = start_conversation(args.title, args.tags.split(",") if args.tags else None)
    print(f"✅ Started conversation {conv_id}: {args.title}")


def cmd_msg(args):
    """Add a message to a conversation"""
    add_message(args.conversation_id, args.role, args.content)
    print(f"✅ Added {args.role} message to conversation {args.conversation_id}")


def cmd_end(args):
    """End a conversation"""
    end_conversation(args.conversation_id, args.summary)
    print(f"✅ Ended conversation {args.conversation_id}")


def cmd_list(args):
    """List recent conversations"""
    convs = list_conversations(args.limit)
    if not convs:
        print("No conversations found")
        return
    
    print("\n📋 Recent Conversations")
    for conv in convs:
        status = "🟢 Active" if conv["end_time"] is None else "⚪ Ended"
        print(f"\n{status} [{conv['id']}] {conv['title']}")
        print(f"   Started: {conv['start_time']}")
        if conv["tags"]:
            print(f"   Tags: {conv['tags']}")
        if conv["summary"]:
            print(f"   Summary: {conv['summary'][:80]}...")


def cmd_show(args):
    """Show a conversation"""
    conv = get_conversation(args.conversation_id)
    if not conv:
        print(f"❌ Conversation {args.conversation_id} not found")
        return
    
    print(f"\n📋 Conversation {conv['id']}: {conv['title']}")
    print(f"   Started: {conv['start_time']}")
    if conv["end_time"]:
        print(f"   Ended: {conv['end_time']}")
    if conv["tags"]:
        print(f"   Tags: {conv['tags']}")
    if conv["summary"]:
        print(f"   Summary: {conv['summary']}")
    
    print("\n💬 Messages:")
    for msg in conv["messages"]:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        print(f"\n{role_icon} {msg['role'].upper()} [{msg['timestamp']}]")
        print(f"   {msg['content'][:200]}...")


def cmd_pref_list(args):
    """List preferences"""
    prefs = list_preferences(args.category)
    if not prefs:
        print("No preferences found")
        return
    
    print("\n⚙️ Preferences")
    current_cat = None
    for pref in prefs:
        if pref["category"] != current_cat:
            current_cat = pref["category"]
            print(f"\n[{current_cat}]")
        
        conf = f" (confidence: {pref['confidence']:.0%})" if pref["confidence"] else ""
        print(f"   {pref['key']} = {pref['value']}{conf}")


def cmd_pref_add(args):
    """Add a preference"""
    add_preference(args.category, args.key, args.value, args.confidence)
    print(f"✅ Added preference [{args.category}] {args.key} = {args.value}")


def cmd_pref_get(args):
    """Get a preference"""
    pref = get_preference(args.category, args.key)
    if not pref:
        print(f"❌ Preference not found: [{args.category}] {args.key}")
        return
    
    print(f"{pref['value']}")


def cmd_insight_list(args):
    """List insights"""
    insights = list_insights(args.type)
    if not insights:
        print("No insights found")
        return
    
    print("\n💡 Insights")
    current_type = None
    for insight in insights:
        if insight["type"] != current_type:
            current_type = insight["type"]
            print(f"\n[{current_type}]")
        
        print(f"   • {insight['content']}")
        print(f"     [{insight['created_at']}]")


def cmd_insight_add(args):
    """Add an insight"""
    add_insight(args.type, args.content, args.tags.split(",") if args.tags else None)
    print(f"✅ Added {args.type} insight")


def cmd_search(args):
    """Search across all memory"""
    results = search_all(args.query, args.limit)
    if not results:
        print(f"No results found for: {args.query}")
        return
    
    print(f"\n🔍 Search Results for: {args.query}")
    print(f"Found {len(results)} result(s)\n")
    
    for result in results:
        print(f"[{result['type']}] {result['title']}")
        print(f"   {result['snippet'][:150]}...")
        print(f"   [{result['timestamp']}]")
        print()


def main():
    parser = argparse.ArgumentParser(description="PHEPy Agent Memory CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    subparsers.add_parser("init", help="Initialize database")
    
    # Status command
    subparsers.add_parser("status", help="Show memory status")
    
    # Start conversation
    p = subparsers.add_parser("start", help="Start a new conversation")
    p.add_argument("-t", "--title", required=True, help="Conversation title")
    p.add_argument("--tags", help="Comma-separated tags")
    
    # Add message
    p = subparsers.add_parser("msg", help="Add message to conversation")
    p.add_argument("conversation_id", type=int, help="Conversation ID")
    p.add_argument("role", choices=["user", "assistant"], help="Message role")
    p.add_argument("content", help="Message content")
    
    # End conversation
    p = subparsers.add_parser("end", help="End a conversation")
    p.add_argument("conversation_id", type=int, help="Conversation ID")
    p.add_argument("-s", "--summary", help="Conversation summary")
    
    # List conversations
    p = subparsers.add_parser("list", help="List conversations")
    p.add_argument("-n", "--limit", type=int, default=10, help="Number to show")
    
    # Show conversation
    p = subparsers.add_parser("show", help="Show conversation details")
    p.add_argument("conversation_id", type=int, help="Conversation ID")
    
    # Preferences
    p = subparsers.add_parser("pref", help="Preference commands")
    p_sub = p.add_subparsers(dest="pref_command")
    
    p_list = p_sub.add_parser("list", help="List preferences")
    p_list.add_argument("-c", "--category", help="Filter by category")
    
    p_add = p_sub.add_parser("add", help="Add preference")
    p_add.add_argument("-c", "--category", required=True, help="Category")
    p_add.add_argument("-k", "--key", required=True, help="Key")
    p_add.add_argument("-v", "--value", required=True, help="Value")
    p_add.add_argument("--confidence", type=float, default=1.0, help="Confidence (0-1)")
    
    p_get = p_sub.add_parser("get", help="Get preference")
    p_get.add_argument("-c", "--category", required=True, help="Category")
    p_get.add_argument("-k", "--key", required=True, help="Key")
    
    # Insights
    p = subparsers.add_parser("insight", help="Insight commands")
    p_sub = p.add_subparsers(dest="insight_command")
    
    p_list = p_sub.add_parser("list", help="List insights")
    p_list.add_argument("-t", "--type", help="Filter by type")
    
    p_add = p_sub.add_parser("add", help="Add insight")
    p_add.add_argument("-t", "--type", required=True, help="Type (goal, decision, pattern, context)")
    p_add.add_argument("--content", required=True, help="Insight content")
    p_add.add_argument("--tags", help="Comma-separated tags")
    
    # Search
    p = subparsers.add_parser("search", help="Search all memory")
    p.add_argument("query", help="Search query")
    p.add_argument("-n", "--limit", type=int, default=10, help="Max results")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to command handlers
    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "start": cmd_start,
        "msg": cmd_msg,
        "end": cmd_end,
        "list": cmd_list,
        "show": cmd_show,
        "search": cmd_search,
    }
    
    if args.command in commands:
        commands[args.command](args)
    elif args.command == "pref":
        if args.pref_command == "list":
            cmd_pref_list(args)
        elif args.pref_command == "add":
            cmd_pref_add(args)
        elif args.pref_command == "get":
            cmd_pref_get(args)
        else:
            parser.parse_args(["pref", "-h"])
    elif args.command == "insight":
        if args.insight_command == "list":
            cmd_insight_list(args)
        elif args.insight_command == "add":
            cmd_insight_add(args)
        else:
            parser.parse_args(["insight", "-h"])


if __name__ == "__main__":
    main()
