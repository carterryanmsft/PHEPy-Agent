# TSG Gap Analysis System

Complete system for identifying Troubleshooting Guide (TSG) gaps by analyzing ICM incidents.

## Overview

This system analyzes ICM incidents from the past 6 months to identify:
- Incident categories with missing TSG coverage
- TSGs marked as ineffective by engineers
- High-severity incidents without TSG documentation
- Patterns in recurring issues needing new TSGs

## Architecture

### Components

1. **batch_icm_retriever.py** - Handles efficient ICM data retrieval
   - Tracks progress across sessions
   - Manages failed retrievals
   - Exports data in JSONL format for memory efficiency

2. **tsg_gap_analyzer.py** - Analyzes incidents for TSG gaps
   - Extracts TSG-relevant fields from full incident data
   - Categorizes incidents by problem type
   - Identifies coverage gaps and effectiveness issues

3. **tsg_gap_workflow.py** - Orchestrates the complete workflow
   - Status checking
   - Batch retrieval coordination
   - Analysis execution
   - Report generation

### Data Flow

```
Kusto Query (620 incidents)
    ↓
Batch ICM Retrieval (via MCP)
    ↓
JSONL Storage (tsg_system/data/retrieved_incidents.jsonl)
    ↓
TSG Gap Analyzer
    ↓
Reports (JSON + Markdown)
```

## Usage

### Step 1: Initialize with Incident IDs

First, retrieve incident IDs from Kusto:

```kusto
IcmDataWarehouse
| where CreatedDate >= ago(180d)
| project IncidentId
| order by CreatedDate desc
| take 620
```

Then initialize the retriever:

```python
from tsg_system.scripts.batch_icm_retriever import BatchICMRetriever

retriever = BatchICMRetriever()
incident_ids = [51000000879655, 51000000879746, ...]  # From Kusto
retriever.set_incident_ids(incident_ids)
```

### Step 2: Retrieve Incidents in Batches

Get the next batch to retrieve:

```python
from tsg_system.scripts.tsg_gap_workflow import retrieve_next_batch

batch = retrieve_next_batch(batch_size=10)
# Returns: [51000000879655, 51000000879746, ...]
```

Use MCP tool to retrieve each incident:
```python
# For each incident_id in batch:
mcp_icm_mcp_eng_get_incident_details_by_id(incidentId=incident_id)
```

Save retrieved incidents:
```python
from tsg_system.scripts.tsg_gap_workflow import process_retrieved_incidents

# After retrieving incidents
incident_list = [incident1_json, incident2_json, ...]
process_retrieved_incidents(incident_list)
```

### Step 3: Check Progress

```python
from tsg_system.scripts.tsg_gap_workflow import quick_status

quick_status()
```

Output:
```
============================================================
ICM RETRIEVAL STATUS
============================================================
Total Incidents: 620
Retrieved: 125 (20.2%)
Failed: 3
Remaining: 492
============================================================
```

### Step 4: Run Analysis (Once All Retrieved)

```python
from tsg_system.scripts.tsg_gap_workflow import run_tsg_gap_analysis

results = run_tsg_gap_analysis()
```

This generates:
- `tsg_system/reports/tsg_gap_analysis.json` - Detailed analysis data
- `tsg_system/reports/tsg_gap_report.md` - Human-readable report

## Command Line Usage

```bash
# Check status
python tsg_system/scripts/tsg_gap_workflow.py --action status

# Get next batch to retrieve
python tsg_system/scripts/tsg_gap_workflow.py --action next-batch --batch-size 10

# Run full analysis
python tsg_system/scripts/tsg_gap_workflow.py --action analyze
```

## Report Output

The analysis report includes:

### Executive Summary
- Total incidents analyzed
- TSG coverage percentage
- Effective vs ineffective TSG counts

### Severity Breakdown
- High-severity incidents without TSGs
- Distribution across severity levels

### Category Coverage
- Labeling/Classification
- Encryption/DLP
- SIT/Detection
- Scanning
- Policy
- Migration

### Gap Priorities
Ranked list of TSG gaps by:
- High-severity incidents without documentation
- Categories with low coverage (<50%)
- TSGs marked as ineffective
- Recurring issue patterns

### Most Used TSGs
- Links to most frequently referenced TSGs
- Usage counts for validation

## Data Structure

### Retrieved Incident Data (JSONL)
Each line contains a full ICM incident JSON object with:
- `id`, `title`, `severity`, `state`, `createdDate`
- `customFields` array containing:
  - "Link to TSG"
  - "TSG Effectiveness"
  - "Escalation Quality"
- `resolveData` / `mitigateData` with resolution details
- `tags`, `summary`, and other metadata

### Extracted TSG Data
Lightweight structure for analysis:
```python
{
  "incident_id": 51000000879655,
  "title": "Label migration RFC",
  "severity": 3,
  "state": "RESOLVED",
  "created_date": "2026-01-15T...",
  "tsg_link": "https://...",
  "tsg_effectiveness": false,
  "escalation_quality": "All Data Provided",
  "resolution_summary": "...",
  "tags": [...]
}
```

## Memory Efficiency

The system uses JSONL (newline-delimited JSON) for incident storage:
- **Why**: Each incident JSON is 10-15K tokens
- **Benefit**: Load and process one incident at a time
- **Trade-off**: Slower than full JSON but avoids memory issues

Batch size recommendations:
- **MCP retrieval**: 5-10 incidents per batch (token limits)
- **Local processing**: 100+ incidents (no limits)

## Integration with MCP Tools

### Required MCP Tools

1. **Kusto Query** - `mcp_kusto-mcp-ser_execute_query`
   - Get incident IDs from IcmDataWarehouse

2. **ICM Detail Retrieval** - `mcp_icm_mcp_eng_get_incident_details_by_id`
   - Fetch full incident details including TSG fields

### Token Management

Each ICM detail response is ~10-15K tokens. To stay under limits:
- Retrieve in batches of 5-10
- Save immediately to JSONL
- Extract only TSG-relevant fields for analysis

## Next Steps After Analysis

1. **Review High Priority Gaps**
   - Create TSGs for high-severity recurring issues
   - Update ineffective TSGs with better guidance

2. **Validate Coverage Metrics**
   - Check if low-coverage categories need more documentation
   - Identify if issues are truly TSG-worthy

3. **Leverage Most Used TSGs**
   - Study effective TSGs as templates
   - Ensure they're discoverable in knowledge bases

4. **Track Improvements**
   - Re-run analysis after TSG updates
   - Measure effectiveness score improvements

## Files and Directories

```
tsg_system/
├── scripts/
│   ├── batch_icm_retriever.py      # Batch retrieval manager
│   ├── tsg_gap_analyzer.py         # Gap analysis engine
│   └── tsg_gap_workflow.py         # Workflow orchestration
├── data/
│   ├── retrieved_incidents.jsonl   # Raw incident data (JSONL)
│   └── retrieval_progress.json     # Progress tracking
├── reports/
│   ├── tsg_gap_analysis.json       # Analysis results
│   └── tsg_gap_report.md           # Human-readable report
└── README.md                        # This file
```

## Example Workflow Session

```python
# Session 1: Initialize and start retrieval
from tsg_system.scripts.batch_icm_retriever import BatchICMRetriever

retriever = BatchICMRetriever()
retriever.set_incident_ids([...620 IDs from Kusto...])

# Get first batch
batch1 = retriever.get_next_batch(10)
# Retrieve using MCP, then save
# retriever.save_incident(incident_data) for each

# Session 2: Continue retrieval
batch2 = retriever.get_next_batch(10)
# Retrieve and save...

# ... Continue until all retrieved ...

# Final Session: Run analysis
from tsg_system.scripts.tsg_gap_workflow import run_tsg_gap_analysis

results = run_tsg_gap_analysis()
# Review tsg_system/reports/tsg_gap_report.md
```

## Troubleshooting

### "No incidents to retrieve" but retrieval not complete
- Check `tsg_system/data/retrieval_progress.json`
- Verify incident IDs were set with `set_incident_ids()`

### MCP tool returns error for incident ID
- Incident may not exist or access denied
- System automatically marks as failed
- Continue with next batch

### Analysis shows 0 incidents
- Verify `tsg_system/data/retrieved_incidents.jsonl` exists
- Check file is not empty
- Ensure retrieval completed before analysis

### Memory issues during analysis
- JSONL format should prevent this
- Reduce batch processing size if needed
- Clear old data files if accumulated

## Performance Notes

- **Retrieval**: ~5-10 incidents per minute (MCP rate limits)
- **Analysis**: 620 incidents in <10 seconds (local)
- **Total Time**: 1-2 hours for complete 620-incident analysis

## Contributing

When adding new categories or analysis metrics:
1. Update `TSGGapAnalyzer.add_incident()` for categorization
2. Add metrics to `analyze_gaps()` method
3. Update report generation in `generate_report()`
4. Document in this README
