# PHEPy Agent Best Practices Guide

**Building a Persistent, Context-Aware AI Assistant for Purview Health & Escalation Operations**

**Version**: 1.0.0  
**Date**: February 11, 2026  
**Status**: ✅ Complete and Ready for Use

---

## 🎯 Executive Summary

This guide implements the **"Max Headroom" agent pattern** for PHEPy, transforming GitHub Copilot CLI from a stateless Q&A tool into a persistent AI teammate that:

- **Remembers you** across sessions (preferences, decisions, context)
- **Connects to your work** via MCP servers (ICM, ADO, Kusto, DFM)
- **Produces deliverables** (HTML reports, analysis, documentation)
- **Gets smarter over time** through session logging and learning

---

## 📦 What Was Implemented

### 1. **Agent Memory System** ✅
**Location**: `agent_memory/`

**Purpose**: Zero-dependency persistent memory using Python + SQLite

**Features**:
- Conversation tracking with messages and summaries
- Preference storage (work, tech, workflow, domain)
- Insight logging (goals, decisions, patterns, context)
- Full-text search (SQLite FTS5)

**Files**:
```
agent_memory/
├── cli.py                    # Main CLI interface
├── session_manager.py        # Quick session utilities
├── bootstrap.py              # Initial setup script
├── README.md                 # Complete usage guide
├── memory.db                 # SQLite database (auto-created)
└── src/
    ├── db.py                 # Database schema and connections
    ├── conversations.py      # Conversation management
    ├── preferences.py        # Preferences and insights
    └── search.py             # Full-text search
```

### 2. **Custom Copilot Instructions** ✅
**Location**: `C:\Users\carterryan\.copilot\copilot-instructions.md`

**Purpose**: Define agent personality, auto-load memory, configure behavior

**Features**:
- Auto-reconnect to memory at session start
- PHEPy-specific context and workflows
- MCP server descriptions and usage patterns
- Session logging guidelines
- Communication style preferences

### 3. **MCP Server Documentation** ✅
**Location**: `docs/MCP_SERVER_BEST_PRACTICES.md`

**Purpose**: Comprehensive guide to MCP server configuration and optimization

**Covers**:
- All 5 configured MCP servers (ADO, ICM, DFM, Kusto)
- Usage patterns and best practices
- Performance optimization strategies
- Caching and query optimization
- Error handling and fallbacks

### 4. **Session Management Utilities** ✅
**Location**: `agent_memory/session_manager.py`

**Purpose**: Quick commands for common session operations

**Features**:
- Quick start/end sessions
- View active session
- Recent session history
- Session statistics
- Export sessions to JSON
- Work context summary

---

## 🚀 Quick Start

### First-Time Setup (5 minutes)

**1. Initialize Agent Memory**
```bash
cd C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory
python bootstrap.py
```

This creates the database and seeds it with PHEPy defaults.

**2. Verify Setup**
```bash
python cli.py status
```

You should see:
```
📊 PHEPy Agent Memory Status
   Conversations: 0 (Active: 0)
   Messages: 0
   Preferences: 14
   Insights: 6
   Database: C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory\memory.db
```

**3. View Defaults**
```bash
python cli.py pref list
python cli.py insight list
```

**4. Add Personal Context**
```bash
# Your name
python cli.py pref add -c work -k name -v "Ryan Carter"

# Current goals
python cli.py insight add -t goal --content "Reduce ICM resolution time by 20% this quarter"

# Key decisions
python cli.py insight add -t decision --content "Standardized on HTML reports for stakeholder communication"
```

**5. Start Using It**

Open GitHub Copilot CLI:
```bash
ghcs
```

At the start of the session, the agent will **automatically**:
1. Load your preferences and insights
2. Greet you by name
3. Have context about your work

If auto-reconnect doesn't fire (rare), just say:
```
"Connect to agent memory"
```

---

## 💡 Key Concepts

### Conversations
**What**: Sessions with the agent  
**When to log**: Meaningful work (report generation, analysis, multi-step workflows)  
**When NOT to log**: Quick questions, simple file reads

**Example**:
```bash
# Start
python cli.py start -t "Friday LQ escalation report" --tags "friday,lq,icm"

# Session happens...

# End
python cli.py end 1 -s "Generated weekly LQ report, identified 12 preventable escalations"
```

### Preferences
**What**: Learned traits about you  
**Categories**: work, tech, workflow, domain  
**When to add**: When you observe patterns in user behavior

**Examples**:
```bash
python cli.py pref add -c workflow -k report_includes -v "customer impact and risk scores"
python cli.py pref add -c tech -k preferred_chart_type -v "bar charts" --confidence 0.8
python cli.py pref add -c work -k default_team -v "PURVIEW\\SensitivityLabels"
```

### Insights
**What**: Important things to remember  
**Types**: goal, decision, pattern, context  
**When to add**: Strategic information that affects multiple sessions

**Examples**:
```bash
# Goal
python cli.py insight add -t goal --content "Achieve 95% ICM resolution within SLA by Q3"

# Decision
python cli.py insight add -t decision --content "Use HTML over PDF for all reports due to better interactivity"

# Pattern
python cli.py insight add -t pattern --content "Monday ICMs often relate to weekend deployments"

# Context
python cli.py insight add -t context --content "CSSR reports use cxedata database, not IcMDataWarehouse"
```

### Search
**What**: Full-text search across all memory  
**Use for**: Finding previous work, recalling decisions, checking context

**Example**:
```bash
python cli.py search "sensitivity labels"
python cli.py search "documentation gaps"
python cli.py search "Q1 goals"
```

---

## 🔄 Typical Workflows

### Workflow 1: ICM Analysis Report

**User**: "Generate an ICM analysis report for Sensitivity Labels, last 90 days"

**Agent**:
1. ✅ **Checks memory** - Knows user prefers HTML reports with metrics
2. ✅ **Knows the team** - "PURVIEW\\SensitivityLabels" from preferences
3. ✅ **Generates query** - Uses sub-agent: `sub_agents/icm_agent/icm_agent.py`
4. ✅ **Executes via MCP** - Kusto MCP against IcMDataWarehouse
5. ✅ **Caches results** - Saves to `data/by_design_results.json`
6. ✅ **Generates report** - HTML with metrics, visualizations, recommendations
7. ✅ **Logs session** - Conversation with summary

**Agent logs**:
```bash
python cli.py start -t "ICM analysis - Sensitivity Labels 90d" --tags "icm,analysis,sensitivity-labels"
python cli.py msg 1 assistant "Generated report with 43 ICMs, 8 doc gaps identified"
python cli.py end 1 -s "Created prioritized ICM analysis report with recommendations"
```

### Workflow 2: Friday LQ Report

**User**: "Generate the Friday low quality escalation report"

**Agent**:
1. ✅ **Recognizes pattern** - Has seen this workflow before
2. ✅ **Uses cached preferences** - Report format, metrics to include
3. ✅ **Executes workflow** - `sub_agents/run_friday_lq_analysis.py`
4. ✅ **Queries via MCP** - ICM MCP and Kusto MCP
5. ✅ **Generates HTML** - Follows established template
6. ✅ **Logs session**

### Workflow 3: New User Request

**User**: "I need reports to always include a 'Next Steps' section"

**Agent**:
```bash
# Stores new preference
python cli.py pref add -c workflow -k report_sections -v "Must include 'Next Steps' section"

# Confirms to user
"✅ I'll include a 'Next Steps' section in all future reports."
```

Next time a report is generated, the agent automatically includes it.

---

## 🎯 Best Practices

### For Agents (Copilot CLI)

**Session Start**:
1. ✅ Auto-load memory (via custom instructions)
2. ✅ Greet user by name
3. ✅ Reference recent work if relevant

**During Session**:
1. ✅ Use preferences to guide behavior
2. ✅ Store new preferences as learned
3. ✅ Log important decisions as insights
4. ✅ Search memory before asking user for info

**Session End** (for meaningful work):
1. ✅ Log conversation with descriptive title
2. ✅ Add key messages if significant
3. ✅ Summarize outcomes
4. ✅ Store any new goals or decisions

### For Users

**Seed Your Memory**:
- Add your preferences early (work style, communication preferences)
- Log your goals (OKRs, quarterly objectives)
- Add domain context (key databases, team structures, important links)

**Be Explicit About Preferences**:
- "I prefer charts over tables"
- "Always include customer impact in reports"
- "Keep responses concise and action-oriented"

**Review Your Memory**:
```bash
# Weekly check
python session_manager.py stats
python session_manager.py context

# Monthly audit
python cli.py insight list
python cli.py pref list
```

**Search Before Asking**:
```bash
# Before asking "What database do I use for CSSR reports?"
python cli.py search "CSSR database"
```

---

## 📊 MCP Server Integration

### Configured Servers

1. **o365exchange** (ADO) - Work items, bugs, features
2. **ASIM-Security** (ADO) - Security work items
3. **ICM MCP ENG** - Incidents and escalations
4. **enterprise-mcp** - DFM support cases
5. **kusto-mcp** - Kusto query engine

### Usage Patterns

**ICM Queries**:
```python
# Get incident details
mcp_icm_mcp_eng_get_incident(incidentId="728221759")

# Get AI summary
mcp_icm_mcp_eng_get_ai_summary(incidentId="728221759")

# Get customer impact
mcp_icm_mcp_eng_get_impacted_customers(incidentId="728221759")
```

**Kusto Queries**:
```python
# Execute KQL
mcp_kusto_execute_query(
    clusterUrl="https://icmcluster.kusto.windows.net",
    database="IcMDataWarehouse",
    query="<your KQL>",
    maxRows=1000
)
```

**ADO Queries**:
```python
# Use WIQL
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE ..."
```

**Best Practices**:
- ✅ Cache expensive queries in `data/`
- ✅ Use `maxRows` to limit result sets
- ✅ Add time filters to queries
- ✅ Test queries in Kusto Explorer first
- ✅ Log query patterns as insights

See [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) for details.

---

## 🔧 Utilities

### Session Manager

**Location**: `agent_memory/session_manager.py`

**Quick commands**:
```bash
# Start a session
python session_manager.py start "Monthly ICM analysis" --tags "icm,monthly"

# View active session
python session_manager.py active

# Recent sessions
python session_manager.py recent -n 10

# Session stats
python session_manager.py stats

# Work context
python session_manager.py context

# Export session
python session_manager.py export 5 -o exports/session_5.json
```

### Memory CLI

**Location**: `agent_memory/cli.py`

**Full reference**: See [agent_memory/README.md](../agent_memory/README.md)

**Common commands**:
```bash
# Status
python cli.py status

# Preferences
python cli.py pref list
python cli.py pref add -c <cat> -k <key> -v "<val>"
python cli.py pref get -c <cat> -k <key>

# Insights
python cli.py insight list
python cli.py insight add -t <type> --content "<text>"

# Conversations
python cli.py list
python cli.py show <id>

# Search
python cli.py search "<query>"
```

---

## 📁 File Structure

```
PHEPy/
├── agent_memory/                    # Persistent memory system
│   ├── cli.py                       # Main CLI
│   ├── session_manager.py           # Quick utilities
│   ├── bootstrap.py                 # Initial setup
│   ├── README.md                    # Usage guide
│   ├── memory.db                    # SQLite database
│   ├── exports/                     # Exported sessions
│   └── src/                         # Python modules
│       ├── db.py
│       ├── conversations.py
│       ├── preferences.py
│       └── search.py
│
├── .copilot/                        # Custom instructions (user home)
│   └── copilot-instructions.md      # Agent personality & behavior
│
├── docs/
│   ├── MCP_SERVER_BEST_PRACTICES.md # MCP configuration guide
│   └── AGENT_BEST_PRACTICES.md      # This file
│
├── sub_agents/                      # Specialized agents
│   ├── icm_agent/
│   ├── support_case_manager/
│   └── ...
│
├── mcp.json                         # MCP server configuration
├── GETTING_STARTED.md               # Workspace quick start
└── README.md                        # Workspace overview
```

---

## 🚨 Troubleshooting

### Memory Not Loading

**Symptom**: Agent doesn't know who you are at session start

**Fix**:
```bash
# In Copilot CLI, just say:
"Connect to agent memory"

# Or manually run:
cd C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory
python cli.py status
python cli.py pref list
python cli.py insight list
```

### Database Not Found

**Symptom**: `FileNotFoundError: memory.db`

**Fix**:
```bash
cd C:\Users\carterryan\OneDrive - Microsoft\PHEPy\agent_memory
python cli.py init
```

### MCP Server Not Responding

**Symptom**: "MCP server timeout" or "Connection failed"

**Fix**:
1. Check if package is installed: `npm list -g | grep <package>`
2. Check Azure CLI auth: `az login`
3. Restart Copilot CLI: Exit and run `ghcs` again
4. Use cached data as fallback

### Performance Issues

**Symptom**: Queries taking 30+ seconds

**Fix**:
1. Add `maxRows` parameter to Kusto queries
2. Add time filters (e.g., `ago(90d)`)
3. Use cached results when available
4. Log pattern as insight for future optimization

---

## 📖 Learning Resources

### Agent Memory System
- [agent_memory/README.md](../agent_memory/README.md) - Complete usage guide
- `session_manager.py --help` - Quick utilities
- `cli.py --help` - Full CLI reference

### MCP Servers
- [docs/MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md)
- `mcp.json` - Current configuration

### PHEPy Workspace
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Quick start
- [CAPABILITY_MATRIX.md](../CAPABILITY_MATRIX.md) - Full features
- [INDEX.md](../INDEX.md) - Documentation index

### GitHub Copilot CLI
- `ghcs` and press `?` for help
- Shift+Tab to toggle plan mode
- Ctrl+Y to view current plan

---

## 🎓 Advanced Topics

### Custom Evaluators

Create custom logic for evaluating preferences:

```python
# In agent memory system
def evaluate_preference_confidence(key, value, historical_usage):
    """Adjust confidence scores based on usage patterns"""
    if historical_usage > 10:
        return 1.0
    elif historical_usage > 5:
        return 0.8
    else:
        return 0.6
```

### Session Templates

Pre-configure common session types:

```bash
# ICM analysis template
python cli.py start -t "ICM Analysis - <team>" --tags "icm,analysis,<team-tag>"

# Friday report template
python cli.py start -t "Friday LQ Report - <date>" --tags "friday,lq,weekly"

# Risk report template
python cli.py start -t "Risk Report - <customer-type>" --tags "risk,<customer-type>,monthly"
```

### Automated Insights

Use cron/Task Scheduler to generate weekly insights:

```python
# weekly_insights.py
from agent_memory.src.insights import add_insight

# Analyze last week's sessions
# Extract patterns
# Add insights automatically
```

---

## ✅ Success Metrics

**How to know it's working**:

1. ✅ Agent greets you by name at session start
2. ✅ Agent knows your preferences without asking
3. ✅ Agent references previous work when relevant
4. ✅ You don't repeat context across sessions
5. ✅ Reports match your style automatically
6. ✅ Search finds previous decisions quickly
7. ✅ Session stats show consistent usage

**Key metrics to track**:
```bash
# Run weekly
python session_manager.py stats

# Check:
- Active sessions vs inactive (should be mostly inactive)
- Average messages per session (higher = more meaningful work)
- This week's session count (consistency)
- Preference count (should grow over time)
- Insight count (should grow with important decisions)
```

---

## 🔄 Maintenance

### Weekly
- Review session stats
- Archive old exports
- Check for stale preferences

### Monthly
- Audit preferences for accuracy
- Review and consolidate insights
- Update custom instructions if workflow changes
- Update MCP server packages: `npm update -g`

### As Needed
- Add new preferences as you discover patterns
- Delete obsolete insights
- Export important sessions for documentation
- Update confidence scores

---

## 🚀 Next Steps

1. **Initialize the system**: `python bootstrap.py`
2. **Add personal context**: Preferences, goals, decisions
3. **Start a session**: `ghcs` and verify auto-reconnect
4. **Do some work**: Generate a report or analysis
5. **Log the session**: `session_manager.py start/end`
6. **Review your memory**: `python cli.py status`
7. **Search and verify**: `python cli.py search "<topic>"`

---

## 📞 Support & Feedback

**Issues or Questions?**  
- Check [agent_memory/README.md](../agent_memory/README.md) for detailed usage
- Check [MCP_SERVER_BEST_PRACTICES.md](MCP_SERVER_BEST_PRACTICES.md) for MCP issues
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (if available)

**Improvements?**  
- Log insights about workflow improvements
- Update custom instructions with new patterns
- Document new best practices in this file

---

**Version**: 1.0.0  
**Last Updated**: February 11, 2026  
**Author**: Based on "Max Headroom" pattern by Ron Mills  
**Workspace**: PHEPy - Purview Product Health & Escalation  
**License**: Microsoft Internal Use
