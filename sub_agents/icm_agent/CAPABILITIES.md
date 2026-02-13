# ICM Agent - Capabilities Matrix

**Last Updated:** February 13, 2026

## Overview
This document outlines the complete capabilities of the ICM Agent, including supported queries, analyses, and output formats.

---

## Core Capabilities

| Capability | Description | Status | Priority |
|------------|-------------|--------|----------|
| **By Design Analysis** | Identify documentation gaps from "By Design" incidents | ✅ Complete | P0 |
| **Documentation Gap Analysis** 🆕 | Analyze closed ICMs to generate TSG and Learn doc recommendations | ✅ Complete | P0 |
| **Incident Trends** | Track incident volumes over time | ✅ Complete | P0 |
| **Top Issues Report** | Most frequent problems by count | ✅ Complete | P0 |
| **Resolution Pattern Analysis** | How issues are being resolved | ✅ Complete | P1 |
| **Customer Impact Scoring** | Quantify customer impact | ✅ Complete | P1 |
| **Recommendation Engine** | Generate actionable next steps | ✅ Complete | P0 |
| **HTML Report Generation** | Visual, interactive reports | ✅ Complete | P0 |
| **CSV Export** | Data export for further analysis | 🔄 Planned | P1 |
| **Automated Scheduling** | Weekly/monthly automated runs | 🔄 Planned | P2 |
| **Email Distribution** | Send reports to stakeholders | 🔄 Planned | P2 |

---

## NEW: Documentation Gap Analysis Workflow 🆕

**Added:** February 13, 2026

### Purpose
Analyze closed ICM incidents where Prevention Type is "Public Documentation" or "TSG Update" to identify documentation gaps and generate concrete, ready-to-paste recommendations for both internal TSGs and public Learn documentation.

### How It Works
1. **Fetch incidents** via ICM MCP server (closed, with specified Prevention Types)
2. **Extract structured data** (symptoms, root cause, mitigation, error codes, etc.)
3. **Discover related TSGs** via Azure DevOps MCP server
4. **Discover related Learn docs** via web search
5. **Identify gaps** across 7 topic areas (symptom, detection, mitigation, etc.)
6. **Generate recommendations** with ready-to-paste text for TSG and Learn updates
7. **Produce reports** (per-incident and consolidated)

### Gap Types Detected
- **Missing**: Documentation doesn't exist
- **Outdated**: Documentation is obsolete
- **Ambiguous**: Documentation is unclear
- **Incomplete**: Partial coverage only
- **Incorrect**: Documentation is wrong
- **Not customer-safe**: Contains internal info
- **Coverage mismatch**: TSG vs Learn inconsistency

### Usage

#### Analyze Specific Incidents
```bash
python icm_agent.py --doc-gaps --incident-ids 626495494 626495495 626495496
```

#### Query for Incidents
```bash
python icm_agent.py --doc-gaps --days 90 --team-filter PURVIEW
```

#### Programmatic Use
```python
from icm_agent import ICMAgent

agent = ICMAgent()
results = agent.run_doc_gap_analysis(
    incident_ids=['626495494', '626495495']
)
# or
results = agent.run_doc_gap_analysis(
    query_params={
        'days_back': 90,
        'prevention_types': ['Public Documentation', 'TSG Update'],
        'team_filter': 'PURVIEW'
    }
)
```

### Output Reports
1. **Per-Incident Report**: Detailed analysis with doc alignment matrix, recommendations, work item proposals
2. **Consolidated Report**: Summary across all incidents with gap distribution and prioritization

### MCP Tools Required
- `mcp_icm_mcp_eng_get_incident_details` - Fetch incident data
- `mcp_o365exchange-_search_code` - Search for TSGs in ADO
- `mcp_o365exchange-_wiki_get_page` - Retrieve TSG content
- `fetch_webpage` - Search Learn documentation

### Quality & Safety
- **PII Sanitization**: Removes customer names, emails, tenant IDs
- **Public/Internal Separation**: TSG recommendations may include internal tools; Learn recommendations are customer-safe only
- **Traceability**: All recommendations link back to source ICM

### See Also
- [DOC_GAP_WORKFLOW_README.md](DOC_GAP_WORKFLOW_README.md) - Detailed workflow guide
- [icm_doc_gap_analyzer.py](icm_doc_gap_analyzer.py) - Implementation

---

## Query Templates

### 1. By Design Analysis
**Purpose:** Identify documentation gaps and customer confusion patterns

**Parameters:**
- `team_name`: Owning team (e.g., "PURVIEW\\SensitivityLabels")
- `days_back`: Time window (default: 180 days)

**Output Fields:**
- Title (issue description)
- Count (number of occurrences)
- FirstSeen/LastSeen (date range)
- SampleIncidents (example incident IDs)
- AffectedCustomers (unique customer count)
- SeverityBreakdown (Sev2/3/4 distribution)
- DaysBetween (duration of issue)
- IsRecurring (Yes/No based on count > 5)

**Use Cases:**
- Weekly documentation review
- Product improvement prioritization
- Customer education planning

---

### 2. Incident Trends
**Purpose:** Monitor incident volume and patterns over time

**Parameters:**
- `team_name`: Owning team
- `days_back`: Time window (default: 180 days)

**Output Fields:**
- CreateDate (weekly bins)
- TotalIncidents
- Sev2Count, Sev3Count, Sev4Count
- UniqueCustomers
- AvgTTR_Hours (average time to resolve)

**Use Cases:**
- Capacity planning
- Detect incident spikes
- Measure process improvements

---

### 3. Top Issues
**Purpose:** Identify most frequent problems requiring attention

**Parameters:**
- `team_name`: Owning team
- `days_back`: Time window (default: 180 days)
- `top_n`: Number of issues to return (default: 20)

**Output Fields:**
- Title
- Count
- UniqueCustomers
- SampleIncidents
- HowFixedBreakdown
- AvgTTR_Days
- Priority (Critical/High/Medium/Low)

**Use Cases:**
- Sprint planning
- Bug prioritization
- Resource allocation

---

## Analysis Features

### Pattern Detection
- Group similar incidents by title
- Detect recurring issues (>5 occurrences)
- Identify long-duration problems (>90 days)
- Calculate customer impact scores

### Prioritization Logic
```python
Priority = Critical:  Count >= 10 AND Customers >= 5
Priority = High:      Count >= 5 AND Customers >= 3
Priority = Medium:    Count >= 3
Priority = Low:       Count < 3
```

### Recommendation Generation
Automated recommendations based on:
- Incident count thresholds
- Customer impact
- Time duration
- Resolution patterns

---

## Report Formats

### HTML Report
**Features:**
- Visual metric cards
- Interactive tables
- Color-coded priorities
- Responsive design
- Print-friendly layout

**Sections:**
- Executive summary metrics
- Top issues table
- Actionable recommendations
- Detailed data tables

### JSON Export
**Features:**
- Complete analysis results
- Machine-readable format
- Integration-friendly
- Timestamped data

### CSV Export (Planned)
**Features:**
- Flat data structure
- Excel-compatible
- Pivot table ready

---

## Integration Capabilities

### Input Sources
- **Kusto Query Results** - Primary data source
- **JSON Files** - Cached/offline analysis
- **Configuration Files** - Team and parameter settings

### Output Destinations
- **File System** - Local report storage
- **Browser** - Auto-open reports
- **Email** (Planned) - Automated distribution
- **SharePoint** (Planned) - Centralized repository

### API Integration Points
- Load data from MCP Kusto tool
- Export to other agents (Purview Product Expert, Work Item Manager)
- Trigger from orchestrator agent

---

## Performance Metrics

### Query Performance
- Typical query time: 5-15 seconds
- Max rows recommended: 1000
- Optimal time window: 30-180 days

### Analysis Speed
- Pattern detection: <1 second
- Report generation: <2 seconds
- End-to-end workflow: <20 seconds (with pre-loaded data)

### Scale Limits
- Tested with: 1000+ incidents
- Recommended batch size: 500 per team
- Multi-team support: Yes (run separately)

---

## Advanced Features

### Customization Options
1. **Custom Queries** - Add new KQL templates
2. **Report Themes** - Customize HTML styling
3. **Filter Logic** - Adjust priority thresholds
4. **Data Transformations** - Add calculated fields

### Extensibility
- Plugin architecture for new analyses
- Template system for reports
- Configuration-driven behavior
- Modular query builder

---

## Limitations & Constraints

### Current Limitations
- Requires manual Kusto query execution
- Single team per analysis run
- No real-time streaming data
- English-only report output

### Planned Enhancements
- Multi-team batch processing
- Automated Kusto query execution
- Real-time dashboards
- Localized reports

---

## Testing & Validation

### Test Scenarios
1. ✅ By Design analysis with sample data
2. ✅ Report generation with empty data
3. ✅ Multiple team analysis
4. ✅ Large dataset handling (1000+ records)
5. 🔄 Automated scheduling (planned)

### Quality Assurance
- Input validation on all parameters
- Error handling for missing data
- Graceful degradation
- Logging and diagnostics

---

## Usage Examples

### Basic Usage
```bash
# Analyze last 6 months
python icm_agent.py --team "PURVIEW\\SensitivityLabels" --days 180

# Quick 30-day check
python icm_agent.py --days 30

# Use cached data
python icm_agent.py --from-file data/results.json
```

### Advanced Usage
```python
from icm_agent import ICMAgent

# Initialize with custom config
agent = ICMAgent(config_path='custom_config.json')

# Run analysis
results = agent.run_by_design_analysis(
    team_name="PURVIEW\\DLP",
    days_back=90
)

# Access specific insights
print(results['analysis']['summary'])
print(results['analysis']['recommendations'])
```

---

## Maintenance Schedule

### Daily
- No automated tasks

### Weekly
- Run by design analysis
- Review new recommendations
- Update documentation priorities

### Monthly
- Review query performance
- Update team configurations
- Validate report accuracy

### Quarterly
- Add new query templates
- Enhance analysis algorithms
- User feedback incorporation

---

**Document Version:** 1.0  
**Last Updated:** February 5, 2026  
**Maintained By:** Carter Ryan  
**Status:** ✅ Production Ready
