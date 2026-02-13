#!/usr/bin/env python3
"""
Continuous Improvement Activity Tracker

Track your weekly continuous improvement activities and build a habit of incremental progress.

Usage:
    python continuous_improvement_tracker.py log --week 1 --notes "Your reflection notes"
    python continuous_improvement_tracker.py status
    python continuous_improvement_tracker.py history
    python continuous_improvement_tracker.py suggest
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Activity database
ACTIVITIES = {
    1: {
        "title": "The 5-Minute Reflection",
        "category": "Reflection & Learning",
        "description": "Jot down one thing that went well and one thing you'd improve tomorrow",
        "time_minutes": 5,
    },
    2: {
        "title": 'Ask "Why?" Five Times',
        "category": "Reflection & Learning",
        "description": "Pick a recurring issue and dig into its root cause using the 5 Whys technique",
        "time_minutes": 15,
    },
    3: {
        "title": "Document One Process",
        "category": "Process Documentation",
        "description": "Choose a task you do often and write down the steps. Share it with a teammate",
        "time_minutes": 15,
    },
    4: {
        "title": "Declutter One Process",
        "category": "Process Optimization",
        "description": "Choose a workflow you use regularly. Eliminate one unnecessary step or simplify one part of it",
        "time_minutes": 10,
    },
    5: {
        "title": "One Small Experiment",
        "category": "Experimentation",
        "description": "Hypothesize a new way of doing a routine task then try it out. Track what changes",
        "time_minutes": 20,
    },
    6: {
        "title": "Try a 10-Minute Retrospective",
        "category": "Reflection & Learning",
        "description": "Reflect on a recent project or task. What went well? What could improve?",
        "time_minutes": 10,
    },
    7: {
        "title": "Eliminate One Friction Point",
        "category": "Process Optimization",
        "description": "Identify a small annoyance in your workflow and fix or simplify it",
        "time_minutes": 10,
    },
    8: {
        "title": "Ask for Feedback",
        "category": "Collaboration & Feedback",
        "description": "Request quick feedback from a peer on something you're working on",
        "time_minutes": 10,
    },
    9: {
        "title": "Automate One Repetitive Task",
        "category": "Process Optimization",
        "description": "Use a rule, template, or shortcut to save time on a recurring task",
        "time_minutes": 15,
    },
    10: {
        "title": 'Create a "Stop Doing" List',
        "category": "Process Optimization",
        "description": "Identify one habit or task that no longer adds value and stop doing it",
        "time_minutes": 5,
    },
    11: {
        "title": "Use a Checklist",
        "category": "Process Documentation",
        "description": "Create a checklist for a recurring task to reduce errors and save time",
        "time_minutes": 10,
    },
    12: {
        "title": "Try a New Tool or Feature",
        "category": "Experimentation",
        "description": "Explore a feature in a tool you use daily that you've never tried before",
        "time_minutes": 10,
    },
    13: {
        "title": "Celebrate a Small Win",
        "category": "Collaboration & Feedback",
        "description": "Acknowledge a recent improvement or success, no matter how small",
        "time_minutes": 5,
    },
    14: {
        "title": 'Ask "What If?"',
        "category": "Experimentation",
        "description": "Identify a current pain point and ask 'How might we do this differently?'",
        "time_minutes": 10,
    },
    15: {
        "title": "Shadow a Colleague",
        "category": "Collaboration & Feedback",
        "description": "Spend 15 minutes learning how someone else approaches a shared task",
        "time_minutes": 15,
    },
    16: {
        "title": 'Create a "How-To" Snippet',
        "category": "Process Documentation",
        "description": "Write a short tip or trick and share it with your team",
        "time_minutes": 5,
    },
    17: {
        "title": "Revisit a Past Mistake",
        "category": "Reflection & Learning",
        "description": "Reflect on a past misstep and identify what you learned from it",
        "time_minutes": 10,
    },
    18: {
        "title": "Visualize a Process",
        "category": "Process Documentation",
        "description": "Sketch out a workflow or decision tree to spot inefficiencies",
        "time_minutes": 15,
    },
    19: {
        "title": 'Try a "Silent Brainstorm"',
        "category": "Experimentation",
        "description": "Generate ideas individually before discussing as a group",
        "time_minutes": 10,
    },
    20: {
        "title": "Update a Template",
        "category": "Process Optimization",
        "description": "Improve a document or deck template you use often",
        "time_minutes": 10,
    },
    21: {
        "title": 'Ask "What\'s the Value?"',
        "category": "Collaboration & Feedback",
        "description": "Identify who your customer is and ask 'What do they value?'",
        "time_minutes": 10,
    },
    22: {
        "title": 'Try a "Before & After"',
        "category": "Process Optimization",
        "description": "Improve a small process and compare the results",
        "time_minutes": 15,
    },
    23: {
        "title": "Use a Feedback Grid",
        "category": "Reflection & Learning",
        "description": "Try 'Start, Stop, Continue' to reflect on a recent effort",
        "time_minutes": 10,
    },
    24: {
        "title": "Create a Quick Survey",
        "category": "Collaboration & Feedback",
        "description": "Ask your team one question to gather improvement ideas",
        "time_minutes": 5,
    },
    25: {
        "title": 'Try a "One-Minute Fix"',
        "category": "Experimentation",
        "description": "Spend 60 seconds improving something small but annoying",
        "time_minutes": 1,
    },
    26: {
        "title": 'Do a "Walkthrough"',
        "category": "Process Documentation",
        "description": "Explain a process to someone new and note where they get confused",
        "time_minutes": 15,
    },
    27: {
        "title": "End the Week with a Win",
        "category": "Reflection & Learning",
        "description": "Write down one improvement you made this week",
        "time_minutes": 5,
    },
}

DATA_FILE = Path(__file__).parent / "data" / "continuous_improvement_log.json"


def load_log() -> Dict:
    """Load the activity log from disk."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"activities": [], "start_date": None}


def save_log(log: Dict) -> None:
    """Save the activity log to disk."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(log, f, indent=2)


def get_current_week_number() -> int:
    """Get the current week number (1-52) in the year."""
    return datetime.now().isocalendar()[1]


def log_activity(week: int, notes: str, impact: Optional[str] = None) -> None:
    """Log a completed activity."""
    if week not in ACTIVITIES:
        print(f"❌ Invalid week number. Must be 1-27.")
        return

    log = load_log()
    
    # Set start date if this is the first entry
    if log["start_date"] is None:
        log["start_date"] = datetime.now().isoformat()

    activity = ACTIVITIES[week]
    entry = {
        "week": week,
        "title": activity["title"],
        "category": activity["category"],
        "completed_date": datetime.now().isoformat(),
        "notes": notes,
        "impact": impact,
    }

    log["activities"].append(entry)
    save_log(log)

    print(f"✅ Activity logged: Week {week} - {activity['title']}")
    print(f"   Notes: {notes}")
    if impact:
        print(f"   Impact: {impact}")


def show_status() -> None:
    """Show current progress and statistics."""
    log = load_log()
    completed = log["activities"]
    completed_weeks = {activity["week"] for activity in completed}

    print("\n" + "=" * 70)
    print("📊 CONTINUOUS IMPROVEMENT PROGRESS")
    print("=" * 70)

    # Overall stats
    print(f"\n🎯 Overall Progress: {len(completed_weeks)}/27 activities completed")
    
    if log["start_date"]:
        start_date = datetime.fromisoformat(log["start_date"])
        weeks_since_start = (datetime.now() - start_date).days // 7
        print(f"📅 Tracking since: {start_date.strftime('%Y-%m-%d')} ({weeks_since_start} weeks ago)")

    # Progress by category
    print("\n📂 Progress by Category:")
    categories = {}
    for week_num, activity in ACTIVITIES.items():
        cat = activity["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "completed": 0}
        categories[cat]["total"] += 1
        if week_num in completed_weeks:
            categories[cat]["completed"] += 1

    for cat, stats in sorted(categories.items()):
        bar_length = 20
        filled = int(bar_length * stats["completed"] / stats["total"])
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"  {cat:30s} {bar} {stats['completed']}/{stats['total']}")

    # Recent activities
    if completed:
        print("\n🕐 Recent Activities (last 5):")
        for activity in sorted(completed, key=lambda x: x["completed_date"], reverse=True)[:5]:
            date = datetime.fromisoformat(activity["completed_date"]).strftime("%Y-%m-%d")
            print(f"  • Week {activity['week']:2d}: {activity['title']:40s} ({date})")

    # Next suggested activity
    print("\n💡 Suggested Next Activity:")
    for week_num in range(1, 28):
        if week_num not in completed_weeks:
            activity = ACTIVITIES[week_num]
            print(f"  Week {week_num}: {activity['title']}")
            print(f"  Category: {activity['category']}")
            print(f"  Time: ~{activity['time_minutes']} minutes")
            print(f"  Description: {activity['description']}")
            break
    else:
        print("  🎉 Congratulations! You've completed all 27 activities!")
        print("  💪 Consider repeating your favorites or creating custom activities.")

    print("\n" + "=" * 70 + "\n")


def show_history(week: Optional[int] = None, category: Optional[str] = None) -> None:
    """Show activity history, optionally filtered."""
    log = load_log()
    activities = log["activities"]

    if week:
        activities = [a for a in activities if a["week"] == week]
    if category:
        activities = [a for a in activities if a["category"] == category]

    if not activities:
        print("📭 No activities found matching your criteria.")
        return

    print("\n" + "=" * 70)
    print("📜 ACTIVITY HISTORY")
    print("=" * 70 + "\n")

    for activity in sorted(activities, key=lambda x: x["completed_date"], reverse=True):
        date = datetime.fromisoformat(activity["completed_date"]).strftime("%Y-%m-%d %H:%M")
        print(f"Week {activity['week']:2d}: {activity['title']}")
        print(f"  Category: {activity['category']}")
        print(f"  Date: {date}")
        print(f"  Notes: {activity['notes']}")
        if activity.get("impact"):
            print(f"  Impact: {activity['impact']}")
        print()


def suggest_activity() -> None:
    """Suggest an activity based on progress and patterns."""
    log = load_log()
    completed_weeks = {activity["week"] for activity in log["activities"]}
    
    # Count completed by category
    category_counts = {}
    for activity in log["activities"]:
        cat = activity["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Find least-practiced category
    all_categories = set(a["category"] for a in ACTIVITIES.values())
    least_practiced = None
    min_count = float("inf")
    for cat in all_categories:
        count = category_counts.get(cat, 0)
        if count < min_count:
            min_count = count
            least_practiced = cat

    print("\n" + "=" * 70)
    print("💡 ACTIVITY SUGGESTION")
    print("=" * 70 + "\n")

    # Suggest from least-practiced category
    print(f"📊 You've practiced '{least_practiced}' the least ({min_count} times)")
    print(f"✨ Here's an activity from that category:\n")

    for week_num, activity in ACTIVITIES.items():
        if activity["category"] == least_practiced and week_num not in completed_weeks:
            print(f"Week {week_num}: {activity['title']}")
            print(f"Time: ~{activity['time_minutes']} minutes")
            print(f"Description: {activity['description']}")
            print(f"\nTo log this activity:")
            print(f'  python continuous_improvement_tracker.py log --week {week_num} --notes "Your reflection"')
            break
    else:
        # All activities in that category are done, suggest any incomplete one
        for week_num, activity in ACTIVITIES.items():
            if week_num not in completed_weeks:
                print(f"Week {week_num}: {activity['title']}")
                print(f"Category: {activity['category']}")
                print(f"Time: ~{activity['time_minutes']} minutes")
                print(f"Description: {activity['description']}")
                print(f"\nTo log this activity:")
                print(f'  python continuous_improvement_tracker.py log --week {week_num} --notes "Your reflection"')
                break

    print("\n" + "=" * 70 + "\n")


def list_activities(category: Optional[str] = None) -> None:
    """List all available activities."""
    print("\n" + "=" * 70)
    print("📋 AVAILABLE ACTIVITIES")
    print("=" * 70 + "\n")

    log = load_log()
    completed_weeks = {activity["week"] for activity in log["activities"]}

    current_category = None
    for week_num in sorted(ACTIVITIES.keys()):
        activity = ACTIVITIES[week_num]
        
        if category and activity["category"] != category:
            continue

        if current_category != activity["category"]:
            current_category = activity["category"]
            print(f"\n{current_category}")
            print("-" * 70)

        status = "✅" if week_num in completed_weeks else "⬜"
        print(f"  {status} Week {week_num:2d}: {activity['title']:40s} (~{activity['time_minutes']} min)")

    print("\n" + "=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Track your continuous improvement activities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a completed activity")
    log_parser.add_argument("--week", type=int, required=True, help="Week number (1-27)")
    log_parser.add_argument("--notes", type=str, required=True, help="Your reflection notes")
    log_parser.add_argument("--impact", type=str, help="Impact or outcome (optional)")

    # Status command
    subparsers.add_parser("status", help="Show current progress")

    # History command
    history_parser = subparsers.add_parser("history", help="View activity history")
    history_parser.add_argument("--week", type=int, help="Filter by week number")
    history_parser.add_argument("--category", type=str, help="Filter by category")

    # Suggest command
    subparsers.add_parser("suggest", help="Get a suggested activity")

    # List command
    list_parser = subparsers.add_parser("list", help="List all activities")
    list_parser.add_argument("--category", type=str, help="Filter by category")

    args = parser.parse_args()

    if args.command == "log":
        log_activity(args.week, args.notes, args.impact)
    elif args.command == "status":
        show_status()
    elif args.command == "history":
        show_history(args.week, args.category)
    elif args.command == "suggest":
        suggest_activity()
    elif args.command == "list":
        list_activities(args.category)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
