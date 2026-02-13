# TSG Gap Analysis - Incident ID Collection

This file tracks the incident IDs to be retrieved for TSG gap analysis.

## Query Used

```kusto
IcmDataWarehouse
| where CreatedDate >= ago(180d)
| project IncidentId
| order by CreatedDate desc
| take 620
```

## Status

- **Query Date**: 2026-02-04
- **Time Range**: Past 180 days (6 months)
- **Expected Count**: 620 incidents
- **Retrieved Count**: 0

## Sample Incident IDs Already Retrieved

From previous session:
- 51000000879655
- 51000000879746
- 51000000879362
- 741203392
- 51000000878019
- 51000000877201

## Next Steps

1. Execute Kusto query to get full list of 620 incident IDs
2. Initialize BatchICMRetriever with incident IDs
3. Retrieve incidents in batches of 10
4. Run TSG gap analysis once complete

## Alternative: Use Sample Dataset

If Kusto connection is unavailable, we can analyze the 5-6 incidents already retrieved as a proof of concept.

```python
sample_ids = [
    51000000879655,
    51000000879746,
    51000000879362,
    741203392,
    51000000878019,
    51000000877201
]
```
