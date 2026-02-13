# ICM Agent

**Standalone sub-agent for analyzing ICM (Incident Management) data to identify patterns, documentation gaps, and improvement opportunities.**

---

## Quick Start

### 1. Generate Query
```bash
python icm_agent.py --team "PURVIEW\\SensitivityLabels" --days 180
```

This will display the Kusto query to execute.

### 2. Execute Query via MCP
Use GitHub Copilot to execute the query via `mcp_kusto-mcp-ser_execute_query` tool, or run it in Kusto Explorer.

### 3. Save Results
Save query results as `data/by_design_results.json`

### 4. Run Analysis
```bash
python icm_agent.py --from-file data/by_design_results.json
```

This will generate an HTML report in the `reports/` directory.

---

## Features

### 🔍 Analysis Types
- **By Design Analysis** - Identify documentation gaps
- **Incident Trends** - Track volumes over time
- **Top Issues** - Most frequent problems
- **Pattern Detection** - Group similar incidents

### 📊 Reports
- Visual HTML reports with metrics
- Prioritized recommendations
- Customer impact analysis
- Actionable next steps

### ⚙️ Flexible Configuration
- Customizable team names
- Adjustable time windows
- Priority thresholds
- Report formatting

---

## Directory Structure

```
icm_agent/
├── icm_agent.py                # Main agent script
├── icm_config.json             # Configuration
├── AGENT_INSTRUCTIONS.md       # Detailed role & responsibilities
├── CAPABILITIES.md             # Full capabilities matrix
├── README.md                   # This file
├── queries/                    # Query templates
│   └── by_design_analysis.kql
├── data/                       # Query results (cached)
│   └── *.json
└── reports/                    # Generated reports
    └── icm_analysis_*.html
```

---

## Usage Examples

### Basic Analysis
```bash
# Use default team and 180-day window
python icm_agent.py
```

### Custom Team
```bash
# Analyze different team
python icm_agent.py --team "PURVIEW\\DLP" --days 90
```

### Offline Analysis
```bash
# Use pre-saved data
python icm_agent.py --from-file data/my_results.json
```

### Custom Configuration
```bash
# Use custom config file
python icm_agent.py --config my_config.json
```

---

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--team` | Team name to analyze | From config |
| `--days` | Days to look back | 180 |
| `--from-file` | Load from JSON file | None (generates query) |
| `--config` | Path to config file | icm_config.json |

---

## Configuration

Edit `icm_config.json` to customize:

```json
{
  "default_team": "PURVIEW\\SensitivityLabels",
  "default_days_back": 180,
  "teams": [
    "PURVIEW\\SensitivityLabels",
    "PURVIEW\\DLP"
  ],
  "priority_thresholds": {
    "critical": {
      "min_count": 10,
      "min_customers": 5
    }
  }
}
```

---

## Output

### HTML Report Sections
1. **Summary Metrics**
   - Total incidents
   - Unique issue types
   - Customers affected
   - Critical documentation gaps

2. **Top Issues Table**
   - Issue title
   - Occurrence count
   - Customer impact
   - Recurring status

3. **Recommendations**
   - Priority level
   - Specific actions
   - Business justification

### Report Location
Reports saved to: `reports/icm_analysis_<timestamp>.html`

---

## Integration with Other Agents

### Receives Data From
- **Kusto Expert (Jacques)** - Query execution
- **Escalation Manager** - Incident context

### Provides Data To
- **Purview Product Expert** - Known issues
- **Work Item Manager** - Bug priorities
- **Documentation Team** - Content gaps

---

## Troubleshooting

### No Data Returned
- Verify team name format: `"PURVIEW\\TeamName"`
- Check date range (incidents may be outside window)
- Ensure Kusto access permissions

### Query Errors
- Validate team name exists in ICM
- Check database connectivity
- Review query syntax in queries/ folder

### Empty Reports
- Ensure data file has results
- Check JSON format is valid
- Verify file path is correct

---

## Advanced Usage

### Python API
```python
from icm_agent import ICMAgent

# Initialize
agent = ICMAgent()

# Load data
agent.load_from_file('data/results.json')

# Run analysis
analysis = agent.analyze_by_design_patterns()

# Generate report
report_path = agent.generate_report()

# Access results
print(analysis['summary'])
for rec in analysis['recommendations']:
    print(f"{rec['priority']}: {rec['issue']}")
```

### Custom Queries
Add new queries in `queries/` folder and extend `icm_agent.py`:

```python
def get_custom_query(self, params):
    query = f"""
    // Your custom KQL query here
    """
    return query
```

---

## Maintenance

### Weekly
- Run by design analysis
- Review recommendations
- Track documentation updates

### Monthly
- Review query performance
- Update team configurations
- Validate priority thresholds

### Quarterly
- Add new query templates
- Enhance recommendation logic
- Update documentation

---

## Version History

- **v1.0** (Feb 5, 2026) - Initial release
  - By Design analysis
  - Incident trends
  - Top issues report
  - HTML report generation

---

## Support & Feedback

**Owner:** Carter Ryan  
**Location:** `sub_agents/icm_agent/`  
**Status:** ✅ Production Ready

For issues or feature requests, update TODO.md or contact the PHEPy team.

---

## Related Documentation

- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Detailed agent role
- [CAPABILITIES.md](CAPABILITIES.md) - Full capabilities matrix
- [../README.md](../README.md) - Sub-agents overview
- [../../TODO.md](../../TODO.md) - Planned enhancements
