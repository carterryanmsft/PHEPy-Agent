# PHEPy Agent Memory System

**Zero-dependency persistent memory for GitHub Copilot CLI**

This system gives your PHEPy agent persistent memory across sessions, storing conversations, preferences, insights, and enabling full-text search.

---

## 🚀 Quick Start

### 1. Initialize the Database
```bash
cd agent_memory
python cli.py init
```

### 2. Check Status
```bash
python cli.py status
```

### 3. Try It Out
```bash
# Add a preference about yourself
python cli.py pref add -c work -k primary_project -v "Purview Health & Escalations"

# Add an insight
python cli.py insight add -t goal --content "Reduce ICM resolution time by 20%"

# List everything
python cli.py pref list
python cli.py insight list
```

---

## 📚 Core Concepts

### Conversations
Sessions with the agent. Each conversation has:
- Title and tags for organization
- Start and end timestamps
- Summary of what was discussed/accomplished
- All messages exchanged

### Preferences
Learned traits about you:
- **[work]** - Your projects, team, role
- **[tech]** - Preferred languages, tools, platforms
- **[workflow]** - Working style, communication preferences
- **[domain]** - Domain knowledge, expertise areas

### Insights
Important things the agent should remember:
- **goals** - Objectives you're working toward
- **decisions** - Choices you've made
- **patterns** - Recurring behaviors or situations
- **context** - Background information

### Search
Full-text search across all conversations and insights using SQLite FTS5.

---

## 🎯 Usage Examples

### Track a Session
```bash
# Start a conversation
python cli.py start -t "ICM analysis for Q1" --tags "icm,analysis,quarterly"

# Session happens (conversation_id is returned, e.g., 1)

# Add key messages (optional - for important sessions)
python cli.py msg 1 user "Analyze by-design ICMs for Sensitivity Labels team"
python cli.py msg 1 assistant "Generated HTML report with 43 ICMs analyzed"

# End it with a summary
python cli.py end 1 -s "Identified 8 documentation gaps, created prioritized report"
```

### Store Preferences
```bash
# Your role and team
python cli.py pref add -c work -k role -v "PM for Purview Escalations"
python cli.py pref add -c work -k team -v "PURVIEW\\SensitivityLabels"

# Technical preferences
python cli.py pref add -c tech -k primary_language -v "Python"
python cli.py pref add -c tech -k query_engine -v "Kusto"

# Workflow preferences
python cli.py pref add -c workflow -k report_format -v "HTML with metrics and visualizations"
python cli.py pref add -c workflow -k communication_style -v "direct and data-driven"
```

### Log Insights
```bash
# Goals
python cli.py insight add -t goal --content "Achieve 95% ICM resolution within SLA"
python cli.py insight add -t goal --content "Complete TSG coverage for top 10 escalation patterns"

# Decisions
python cli.py insight add -t decision --content "Standardized on HTML reports for stakeholder communication"

# Patterns
python cli.py insight add -t pattern --content "Most escalations occur Monday morning after weekend deployments"

# Context
python cli.py insight add -t context --content "CSSR report uses cxedata database, not IcMDataWarehouse"
```

### Search
```bash
# Find anything related to a topic
python cli.py search "sensitivity labels"
python cli.py search "documentation gaps"
python cli.py search "Q1 OKRs"
```

### View Data
```bash
# List recent conversations
python cli.py list -n 5

# Show a specific conversation
python cli.py show 3

# List all preferences by category
python cli.py pref list -c work
python cli.py pref list -c tech

# Get a specific preference
python cli.py pref get -c work -k team

# List insights by type
python cli.py insight list -t goal
python cli.py insight list -t pattern
```

---

## 🤖 Integration with Copilot CLI

The memory system is designed to be called by GitHub Copilot CLI at the start and end of each session.

### Auto-Reconnect Pattern
Add this to your `.copilot/copilot-instructions.md`:

```markdown
## Agent Memory — Auto-Reconnect

At the start of every new session, automatically load persistent memory
by running these commands from `C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory`:

\```bash
python cli.py status
python cli.py pref list
python cli.py insight list
\```

Use this context to personalize responses throughout the session.
```

### Session Logging Pattern
```markdown
## Logging Conversations

When a session involves meaningful work, log it to agent-memory:

\```bash
# Start
python cli.py start -t "<topic>" --tags "<relevant,tags>"

# Log key interactions (optional)
python cli.py msg <conv-id> user "<key user request>"
python cli.py msg <conv-id> assistant "<key action taken>"

# End with summary
python cli.py end <conv-id> -s "<brief summary>"
\```

If the user expresses a new preference or makes a decision, store it:

\```bash
python cli.py pref add -c <category> -k <key> -v "<value>"
python cli.py insight add -t <type> --content "<insight>"
\```
```

---

## 📊 Example Workflow

**Start of session:**
```bash
# Copilot CLI runs these automatically (via custom instructions)
$ python cli.py status
📊 PHEPy Agent Memory Status
   Conversations: 47 (Active: 0)
   Messages: 234
   Preferences: 18
   Insights: 23
   Database: C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory\memory.db

$ python cli.py pref list
⚙️ Preferences

[work]
   role = PM for Purview Escalations
   team = PURVIEW\SensitivityLabels
   primary_project = Purview Health & Escalations

[tech]
   primary_language = Python
   query_engine = Kusto

[workflow]
   report_format = HTML with metrics and visualizations
   communication_style = direct and data-driven
```

The agent now knows who you are, what you work on, and how you prefer to work.

**During session:**
```bash
# You: "Generate an ICM analysis report for this month"
# Agent generates report using your preferences

# If you say something like: "I prefer reports to include customer impact"
# Agent runs:
$ python cli.py pref add -c workflow -k report_includes -v "customer impact metrics"
```

**End of session:**
```bash
$ python cli.py start -t "Monthly ICM analysis and reporting" --tags "icm,analysis,monthly"
✅ Started conversation 48: Monthly ICM analysis and reporting

$ python cli.py msg 48 user "Generate ICM analysis report for January 2026"
✅ Added user message to conversation 48

$ python cli.py msg 48 assistant "Generated HTML report with 156 ICMs, identified 12 documentation gaps"
✅ Added assistant message to conversation 48

$ python cli.py end 48 -s "Created comprehensive monthly ICM report with customer impact analysis"
✅ Ended conversation 48
```

---

## 🔍 Advanced Features

### Confidence Scores
Preferences support confidence scores (0.0 to 1.0) for uncertain learned traits:
```bash
python cli.py pref add -c workflow -k preferred_chart_type -v "bar charts" --confidence 0.7
```

### Tagged Insights
Add tags to insights for better organization:
```bash
python cli.py insight add -t pattern --content "Friday deployments correlate with Monday escalations" --tags "deployment,escalation,timing"
```

### Full-Text Search
Search uses SQLite FTS5 for fast, relevant results:
- Searches messages and insights
- Ranks by relevance
- Returns snippets with context

---

## 📁 File Structure

```
agent_memory/
├── cli.py              # Main CLI interface
├── memory.db           # SQLite database (auto-created)
├── README.md           # This file
└── src/
    ├── __init__.py
    ├── db.py           # Database connection and schema
    ├── conversations.py # Conversation CRUD
    ├── preferences.py   # Preferences & insights CRUD
    └── search.py        # Full-text search
```

---

## 🎯 Best Practices

1. **Load memory at start of each session** - The agent should know who you are
2. **Log significant sessions** - Not every quick query, but meaningful work
3. **Store preferences as you learn them** - When you see patterns in user behavior
4. **Use insights for decisions and goals** - Things that affect multiple sessions
5. **Search before asking** - Check memory before asking user to repeat information
6. **Update confidence scores** - As you learn more about preferences
7. **Use descriptive titles and tags** - Makes finding things later easier

---

## 🔧 Troubleshooting

### Database not found
```bash
cd C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory
python cli.py init
```

### Clear all data (start fresh)
```bash
rm memory.db
python cli.py init
```

### View raw database
```bash
sqlite3 memory.db
.tables
SELECT * FROM preferences;
.quit
```

---

## 📖 Command Reference

### General
- `init` - Initialize database
- `status` - Show memory statistics
- `search <query>` - Search all memory

### Conversations
- `start -t <title> [--tags <tags>]` - Start conversation
- `msg <id> <role> <content>` - Add message
- `end <id> [-s <summary>]` - End conversation
- `list [-n <limit>]` - List conversations
- `show <id>` - Show conversation details

### Preferences
- `pref list [-c <category>]` - List preferences
- `pref add -c <cat> -k <key> -v <val> [--confidence <0-1>]` - Add preference
- `pref get -c <cat> -k <key>` - Get preference

### Insights
- `insight list [-t <type>]` - List insights
- `insight add -t <type> --content <text> [--tags <tags>]` - Add insight

---

## 🚀 Next Steps

1. **Initialize the system**: `python cli.py init`
2. **Seed your preferences**: Add your role, team, projects, preferences
3. **Add key insights**: Goals, decisions, important context
4. **Update Copilot instructions**: Add auto-reconnect commands
5. **Start using it**: Let the agent remember you!

---

**Version**: 1.0.0  
**Zero Dependencies**: Uses only Python 3.13+ standard library  
**Database**: SQLite with FTS5 full-text search  
**Compatible With**: GitHub Copilot CLI, any terminal-based AI assistant
