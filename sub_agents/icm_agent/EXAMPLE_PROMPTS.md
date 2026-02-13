# ICM Agent - Example Prompts

Use these prompts with the ICM Agent or through the PHEPy orchestrator to analyze incident patterns.

---

## Basic Queries

### 1. Run By Design Analysis
```
Run the by design analysis for the last 6 months
```
**What it does:** Identifies documentation gaps from incidents marked "By Design"

### 2. Analyze Specific Team
```
Analyze by design incidents for PURVIEW\DLP team over the last 90 days
```
**What it does:** Focuses analysis on a specific team with custom time window

### 3. Use Cached Data
```
Run ICM analysis using the data file data/by_design_results.json
```
**What it does:** Analyzes previously saved query results

---

## Report Generation

### 4. Generate Full Report
```
Generate a full by design report with recommendations
```
**What it does:** Creates HTML report with metrics, top issues, and action items

### 5. Identify Critical Gaps
```
Show me the critical documentation gaps from recent incidents
```
**What it does:** Filters and prioritizes high-impact issues

### 6. Customer Impact Analysis
```
Which by design issues are affecting the most customers?
```
**What it does:** Sorts issues by customer count

---

## Trend Analysis

### 7. Incident Trends
```
Show incident trends for the last 6 months
```
**What it does:** Displays volume patterns over time

### 8. Top Recurring Issues
```
What are the top 10 recurring issues this quarter?
```
**What it does:** Identifies most frequent problems

### 9. Resolution Patterns
```
How are incidents being resolved? Show breakdown by HowFixed
```
**What it does:** Analyzes resolution methods

---

## Advanced Queries

### 10. Multi-Team Comparison
```
Compare by design incidents across all Purview teams
```
**What it does:** Batch analysis across multiple teams

### 11. Severity Analysis
```
Show by design incidents by severity level
```
**What it does:** Breaks down issues by Sev2/3/4

### 12. Long-Running Issues
```
Which issues have persisted for more than 90 days?
```
**What it does:** Identifies chronic problems needing attention

---

## Specific Scenarios

### 13. Weekly Review
```
Run the weekly by design review for my team
```
**What it does:** Standard weekly documentation gap check

### 14. Sprint Planning
```
Give me the top 5 by design issues to prioritize this sprint
```
**What it does:** Prioritized list for planning

### 15. Executive Summary
```
Create an executive summary of by design incidents this month
```
**What it does:** High-level metrics and key insights

---

## Integration Prompts

### 16. Link to Bugs
```
Show by design issues that should be bugs instead
```
**What it does:** Identifies misclassified incidents

### 17. Documentation Roadmap
```
Create a documentation roadmap based on by design patterns
```
**What it does:** Prioritized list of doc work needed

### 18. Customer Impact Report
```
Which customers are most affected by by design limitations?
```
**What it does:** Customer-centric impact analysis

---

## Command Line Examples

### Basic Usage
```bash
# Default analysis (180 days, default team)
python icm_agent.py

# Custom time window
python icm_agent.py --days 90

# Specific team
python icm_agent.py --team "PURVIEW\\DLP"

# Combined
python icm_agent.py --team "PURVIEW\\eDiscovery" --days 60
```

### With Data Files
```bash
# Use cached results
python icm_agent.py --from-file data/by_design_results.json

# Custom config
python icm_agent.py --config my_config.json

# Full workflow
python icm_agent.py --team "PURVIEW\\SensitivityLabels" --days 180
# (execute query via MCP)
# (save results to data/)
python icm_agent.py --from-file data/results.json
```

---

## Python API Examples

### Simple Analysis
```python
from icm_agent import ICMAgent

agent = ICMAgent()
results = agent.run_by_design_analysis(days_back=90)
print(results['status'])
```

### Custom Configuration
```python
from icm_agent import ICMAgent

agent = ICMAgent(config_path='custom_config.json')
agent.load_from_file('data/results.json')
analysis = agent.analyze_by_design_patterns()

for rec in analysis['recommendations']:
    print(f"[{rec['priority']}] {rec['issue']}")
    print(f"  Action: {rec['action']}")
```

### Generate Multiple Reports
```python
from icm_agent import ICMAgent

teams = ["PURVIEW\\SensitivityLabels", "PURVIEW\\DLP", "PURVIEW\\eDiscovery"]

for team in teams:
    agent = ICMAgent()
    agent.config['default_team'] = team
    results = agent.run_by_design_analysis(team_name=team, days_back=90)
    print(f"Report for {team}: {results.get('report_path')}")
```

---

## Orchestrator Integration

### Via PHEPy Orchestrator
```
@icm-agent analyze by design incidents for sensitivity labels
```

```
@icm-agent show me the top documentation gaps this month
```

```
@icm-agent generate a report on recurring by design issues
```

---

## Tips & Best Practices

### Time Windows
- **30 days:** Quick recent check
- **90 days:** Quarterly review
- **180 days:** Comprehensive pattern detection
- **365 days:** Annual trends

### Team Names
Always use the full path format:
- ✅ `PURVIEW\\SensitivityLabels`
- ✅ `PURVIEW\\DLP`
- ❌ `SensitivityLabels` (will not work)

### Data Caching
Save query results to avoid re-querying:
```bash
# Run once with query generation
python icm_agent.py --days 180 > query.kql

# Execute in Kusto, save as data/results.json

# Analyze multiple times
python icm_agent.py --from-file data/results.json
python icm_agent.py --from-file data/results.json --config alt_config.json
```

---

## Troubleshooting Prompts

### No Results
```
Why am I getting no results from the by design analysis?
```
**Check:** Team name format, date range, data availability

### Query Errors
```
The Kusto query is failing with error 400
```
**Check:** Team name exists in ICM, database permissions

### Empty Reports
```
The report is empty even though I have data
```
**Check:** JSON file format, data structure

---

## Next Steps After Analysis

### 1. Documentation Work
- Create FAQ entries for top issues
- Update product docs with limitations
- Add tooltips/help text to UI

### 2. Product Improvements
- File DCRs for high-impact items
- Review UX for confusing behaviors
- Enhance error messages

### 3. Proactive Communication
- Blog posts explaining common confusions
- Customer education webinars
- Release notes for behavior changes

---

**Last Updated:** February 5, 2026  
**Version:** 1.0
