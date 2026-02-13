# Agent System Documentation Index

**Complete guide to PHEPy's persistent AI assistant capabilities**

---

## 🚀 Start Here

### New Users
1. **[agent_memory/QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md)** ⭐ **START HERE**
   - 5-minute setup guide
   - Step-by-step instructions
   - Verification steps
   - Quick commands reference

### Power Users
2. **[AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md)**
   - Complete implementation guide
   - Key concepts and workflows
   - Advanced topics
   - Success metrics

---

## 📚 Core Documentation

### Implementation Guide
- **[AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md)** (800+ lines)
  - What the system does
  - How to use it
  - Best practices
  - Troubleshooting
  - Typical workflows

### Memory System
- **[agent_memory/README.md](../agent_memory/README.md)** (429 lines)
  - Complete CLI reference
  - Usage examples
  - Integration patterns
  - Command reference

### MCP Servers
- **[MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md)** (634 lines)
  - All 5 MCP servers documented
  - Configuration and optimization
  - Usage patterns
  - Performance tuning
  - Error handling

### Custom Instructions
- **[C:\Users\carterryan\.copilot\copilot-instructions.md](../../.copilot/copilot-instructions.md)** (453 lines)
  - Agent personality
  - Auto-reconnect configuration
  - PHEPy-specific context
  - MCP server descriptions
  - Communication style

---

## 🔧 Tools & Utilities

### Command-Line Tools

**Main CLI** - `agent_memory/cli.py`
```bash
# Core operations
python cli.py init                    # Initialize database
python cli.py status                  # Show memory status
python cli.py search <query>          # Search all memory

# Conversations
python cli.py start -t <title>        # Start session
python cli.py end <id> -s <summary>   # End session
python cli.py list                    # List sessions
python cli.py show <id>               # Show details

# Preferences
python cli.py pref list               # List all
python cli.py pref add -c <cat> -k <key> -v <val>
python cli.py pref get -c <cat> -k <key>

# Insights
python cli.py insight list            # List all
python cli.py insight add -t <type> --content <text>
```

**Session Manager** - `agent_memory/session_manager.py`
```bash
# Quick operations
python session_manager.py start <title>   # Quick start
python session_manager.py active          # Show active
python session_manager.py recent          # Recent sessions
python session_manager.py stats           # Statistics
python session_manager.py context         # Work context
python session_manager.py export <id>     # Export to JSON
```

**Bootstrap** - `agent_memory/bootstrap.py`
```bash
# One-command setup
python bootstrap.py
```

---

## 📖 Documentation by Topic

### Getting Started
1. [QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md) - 5-minute setup
2. [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Quick Start
3. [Memory System README](../agent_memory/README.md) § Usage Examples

### Core Concepts
- **Conversations**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Key Concepts
- **Preferences**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Preferences
- **Insights**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Insights
- **Search**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Search

### Usage Patterns
- **Session Tracking**: [Memory System README](../agent_memory/README.md) § Track a Session
- **Preference Storage**: [Memory System README](../agent_memory/README.md) § Store Preferences
- **Insight Logging**: [Memory System README](../agent_memory/README.md) § Log Insights
- **Work Context**: [session_manager.py](../agent_memory/session_manager.py) - `context` command

### Integration
- **Copilot CLI**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Integration
- **MCP Servers**: [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md)
- **Sub-Agents**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Workflows
- **Custom Instructions**: [copilot-instructions.md](../../.copilot/copilot-instructions.md)

### Advanced Topics
- **Query Optimization**: [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) § Performance
- **Caching Strategy**: [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) § Caching
- **Session Templates**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Advanced
- **Automated Insights**: [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Advanced

### Troubleshooting
- [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Troubleshooting
- [QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md) § Troubleshooting
- [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) § Error Handling

---

## 🎯 Quick Reference by Task

### "I want to set this up"
→ [agent_memory/QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md)

### "How do I use the CLI?"
→ [agent_memory/README.md](../agent_memory/README.md) § Command Reference

### "What can this do?"
→ [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § What Was Implemented

### "How do I log a session?"
→ [Memory System README](../agent_memory/README.md) § Track a Session

### "How do I add preferences?"
→ [Memory System README](../agent_memory/README.md) § Store Preferences

### "How do MCP servers work?"
→ [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md)

### "The agent doesn't remember me"
→ [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Troubleshooting

### "How do I search my memory?"
→ [Memory System README](../agent_memory/README.md) § Search

### "I want to see recent sessions"
→ `python session_manager.py recent`

### "How do I optimize performance?"
→ [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) § Performance

---

## 📊 Implementation Details

### What Was Built
- [AGENT_IMPLEMENTATION_SUMMARY.md](AGENT_IMPLEMENTATION_SUMMARY.md)
  - Complete inventory
  - File structure
  - Before/after comparison
  - Success metrics

### Technical Architecture
- Database schema: [agent_memory/src/db.py](../agent_memory/src/db.py)
- Conversation management: [agent_memory/src/conversations.py](../agent_memory/src/conversations.py)
- Preferences: [agent_memory/src/preferences.py](../agent_memory/src/preferences.py)
- Search: [agent_memory/src/search.py](../agent_memory/src/search.py)

---

## 🔄 Workflow Examples

### Daily Operation
1. Start Copilot CLI: `ghcs`
2. Agent auto-loads memory (or say "connect to agent memory")
3. Work on tasks (reports, analysis, etc.)
4. Agent learns preferences automatically
5. End session (automatic logging for meaningful work)

### Adding Context
```bash
# Add preference
cd agent_memory
python cli.py pref add -c workflow -k report_format -v "HTML with charts"

# Add goal
python cli.py insight add -t goal --content "Reduce ICM resolution time by 20%"

# Add decision
python cli.py insight add -t decision --content "Use HTML reports for stakeholders"
```

### Reviewing Memory
```bash
# Status
python cli.py status

# Recent work
python session_manager.py recent

# Context summary
python session_manager.py context

# Search
python cli.py search "sensitivity labels"
```

---

## 📁 File Structure

```
PHEPy/
├── agent_memory/                         # Memory system
│   ├── cli.py                            # Main CLI (336 lines)
│   ├── session_manager.py                # Session utilities (234 lines)
│   ├── bootstrap.py                      # Setup script (98 lines)
│   ├── README.md                         # Usage guide (429 lines)
│   ├── QUICK_SETUP.md                    # 5-min setup (142 lines)
│   ├── memory.db                         # SQLite database (auto-created)
│   ├── exports/                          # Exported sessions
│   └── src/                              # Python modules
│       ├── __init__.py
│       ├── db.py                         # Database (152 lines)
│       ├── conversations.py              # Conversations (87 lines)
│       ├── preferences.py                # Preferences (94 lines)
│       └── search.py                     # Search (73 lines)
│
├── docs/
│   ├── AGENT_BEST_PRACTICES.md           # Complete guide (857 lines)
│   ├── MCP_SERVER_BEST_PRACTICES.md      # MCP guide (634 lines)
│   ├── AGENT_IMPLEMENTATION_SUMMARY.md   # What was built (summary)
│   └── AGENT_DOCUMENTATION_INDEX.md      # This file
│
├── .copilot/                             # User home directory
│   └── copilot-instructions.md           # Custom instructions (453 lines)
│
├── mcp.json                              # MCP server config
├── README.md                             # Updated with agent section
└── GETTING_STARTED.md                    # Updated with agent setup
```

**Total**: 3,592 lines of code and documentation

---

## 🏆 Key Features

### Persistence
- ✅ Conversations with full history
- ✅ Preferences with confidence scores
- ✅ Insights (goals, decisions, patterns, context)
- ✅ Full-text search (SQLite FTS5)

### Integration
- ✅ GitHub Copilot CLI auto-reconnect
- ✅ 5 MCP servers configured
- ✅ PHEPy-specific workflows
- ✅ Sub-agent integration

### Usability
- ✅ 5-minute setup
- ✅ Zero external dependencies
- ✅ Intuitive CLI
- ✅ Comprehensive docs

---

## 💡 Tips

**For New Users**:
1. Start with [QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md)
2. Run bootstrap to seed defaults
3. Add your personal preferences
4. Start using Copilot CLI
5. Let it learn from your sessions

**For Power Users**:
1. Read [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) completely
2. Study [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) for optimization
3. Use `session_manager.py` for quick operations
4. Review stats weekly
5. Export important sessions

**For Maintainers**:
1. Check [AGENT_IMPLEMENTATION_SUMMARY.md](AGENT_IMPLEMENTATION_SUMMARY.md) for inventory
2. Review database schema in [db.py](../agent_memory/src/db.py)
3. Update custom instructions as workflows evolve
4. Add new MCP servers to [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md)

---

## 📞 Support

**Getting Started Issues**:
- Check [QUICK_SETUP.md](../agent_memory/QUICK_SETUP.md) § Troubleshooting
- Verify database exists: `python cli.py status`

**Usage Questions**:
- Check [Memory System README](../agent_memory/README.md)
- Check [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Key Concepts

**Technical Issues**:
- Check [AGENT_BEST_PRACTICES.md](AGENT_BEST_PRACTICES.md) § Troubleshooting
- Check [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) § Error Handling

---

**Last Updated**: February 11, 2026  
**Status**: ✅ Complete  
**Pattern**: "Max Headroom" Persistent Agent  
**Workspace**: PHEPy
