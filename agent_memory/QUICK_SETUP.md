# 🚀 Quick Setup: PHEPy Agent Memory System

**5-minute setup for persistent AI assistant capabilities**

---

## What You're Setting Up

A **persistent memory system** that makes GitHub Copilot CLI remember:
- Who you are (name, role, team, preferences)
- What you work on (projects, goals, decisions)
- How you prefer to work (communication style, report formats)
- Past conversations and insights

---

## Prerequisites

✅ GitHub Copilot CLI installed (`ghcs` command works)  
✅ Python 3.13+ installed  
✅ PHEPy workspace location: `C:\Users\carterryan\OneDrive - Microsoft\PHEPy`

---

## Step 1: Initialize (2 minutes)

```bash
# Navigate to agent_memory folder
cd "C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory"

# Run bootstrap script
python bootstrap.py
```

**Expected output**:
```
🚀 Bootstrapping PHEPy Agent Memory...
✅ Database created at memory.db
✅ Default preferences added
✅ Default insights added
```

---

## Step 2: Verify (1 minute)

```bash
# Check status
python cli.py status
```

**You should see**:
```
📊 PHEPy Agent Memory Status
   Conversations: 0 (Active: 0)
   Messages: 0
   Preferences: 14
   Insights: 6
```

```bash
# View what was seeded
python cli.py pref list
python cli.py insight list
```

---

## Step 3: Personalize (2 minutes)

**Add your name**:
```bash
python cli.py pref add -c work -k name -v "Ryan Carter"
```

**Add a current goal**:
```bash
python cli.py insight add -t goal --content "Reduce average ICM resolution time by 20% this quarter"
```

**Add a recent decision**:
```bash
python cli.py insight add -t decision --content "Standardized on HTML reports for all stakeholder communication"
```

---

## Step 4: Test It (1 minute)

**Start Copilot CLI**:
```bash
ghcs
```

**At session start, the agent should automatically**:
- Run memory commands to load your context
- Greet you by name
- Reference your preferences

**If it doesn't auto-load**, just say:
```
"Connect to agent memory"
```

Or manually run:
```bash
cd agent_memory
python cli.py status
python cli.py pref list
python cli.py insight list
```

---

## ✅ You're Done!

The agent now knows who you are and will remember context across sessions.

---

## 💡 Quick Commands

**Status check**:
```bash
cd agent_memory
python cli.py status
```

**Add a preference**:
```bash
python cli.py pref add -c <category> -k <key> -v "<value>"

# Examples:
python cli.py pref add -c workflow -k report_style -v "HTML with embedded charts"
python cli.py pref add -c tech -k preferred_language -v "Python"
```

**Add an insight**:
```bash
python cli.py insight add -t <type> --content "<text>"

# Types: goal, decision, pattern, context
# Examples:
python cli.py insight add -t pattern --content "Sensitivity Labels team has most by-design ICMs"
python cli.py insight add -t context --content "Use IcMDataWarehouse for ICM queries"
```

**Search everything**:
```bash
python cli.py search "<query>"
```

**Log a session** (after meaningful work):
```bash
# Start
python cli.py start -t "Monthly ICM analysis" --tags "icm,analysis"

# End
python cli.py end 1 -s "Generated report with 43 ICMs, identified 8 doc gaps"
```

---

## 📖 Full Documentation

- **Complete Guide**: [docs/AGENT_BEST_PRACTICES.md](../docs/AGENT_BEST_PRACTICES.md)
- **Memory System**: [agent_memory/README.md](README.md)
- **Custom Instructions**: `C:\Users\carterryan\.copilot\copilot-instructions.md`
- **MCP Servers**: [docs/MCP_SERVER_BEST_PRACTICES.md](../docs/MCP_SERVER_BEST_PRACTICES.md)

---

## 🆘 Troubleshooting

### "Database not found"
```bash
cd agent_memory
python cli.py init
```

### "Auto-reconnect not working"
In Copilot CLI session, just say:
```
"Connect to agent memory"
```

### "Python not found"
Install Python 3.13+:
```bash
winget install Python.Python.3.14
```

---

**Setup time**: ~5 minutes  
**Result**: Persistent AI assistant that remembers you! 🎉
