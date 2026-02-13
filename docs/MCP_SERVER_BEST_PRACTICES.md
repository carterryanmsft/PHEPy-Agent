# MCP Server Configuration Best Practices

**For PHEPy Workspace - GitHub Copilot CLI Integration**

This guide covers Model Context Protocol (MCP) server configuration, optimization, and best practices for the PHEPy workspace.

---

## 📋 Overview

**What are MCP Servers?**  
MCP (Model Context Protocol) servers are plugins that give GitHub Copilot CLI access to external data sources and tools. They act as "senses" for your AI assistant, enabling it to query databases, manage work items, fetch incident data, and more.

**Current PHEPy Configuration:**  
The workspace has 5 configured MCP servers in [`mcp.json`](../mcp.json).

---

## 🔌 Configured MCP Servers

### 1. Azure DevOps (o365exchange)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["@azure-devops/mcp", "o365exchange"],
  "description": "ADO work items: bugs and features (DCRs)"
}
```

**Capabilities**:
- Query work items, bugs, features
- Create and update items
- Link artifacts (commits, PRs, builds)
- Manage pull requests and code reviews
- Wiki operations

**ID Format**: `3563451` (numeric ADO work item ID)

**Best Practices**:
- Use WIQL (Work Item Query Language) for complex queries
- Cache query results in `data/` folders for expensive queries
- Link ICMs to ADO bugs for traceability
- Use tags to organize work items by theme/project

### 2. Azure DevOps (ASIM-Security)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@azure-devops/mcp", "ASIM-Security"],
  "description": "ASIM Security work items and queries"
}
```

**Purpose**: Specialized ADO instance for security-related work items and repositories.

**Best Practices**:
- Use for security-specific queries and operations
- Keep separate from main o365exchange server to avoid confusion

### 3. ICM (Incident Management)
```json
{
  "type": "http",
  "url": "https://icm-mcp-prod.azure-api.net/v1/",
  "description": "ICM incidents and escalations"
}
```

**Capabilities**:
- Get incident details, timeline, customer impact
- Query on-call schedules
- Find incidents by customer, service, or pattern
- Retrieve AI-generated summaries
- Get contact information

**ID Format**: 
- ICM: `728221759` (9 digits)
- DFM: `51000000877262` (14 digits, starts with 5)
- SCIM: `21000000855343` (14 digits, starts with 2)

**Best Practices**:
- Always request customer impact for escalations
- Use AI summaries (`get_ai_summary`) for quick context
- Cache incident details locally to reduce API calls
- Check on-call schedules before escalating
- Link ICMs to ADO bugs for tracking

**Common Queries**:
```python
# Get incident details
mcp_icm_mcp_eng_get_incident(incidentId="728221759")

# Get AI summary
mcp_icm_mcp_eng_get_ai_summary(incidentId="728221759")

# Get customer impact
mcp_icm_mcp_eng_get_impacted_customers(incidentId="728221759")

# Get on-call schedule
mcp_icm_mcp_eng_get_team_oncall_schedule(teamPublicId="...")
```

### 4. Enterprise MCP (DFM Support Cases)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["@mcp-apps/enterprise-mcp-server@latest"],
  "description": "DFM support cases with SCIM access and PII guardrails"
}
```

**Capabilities**:
- Query DFM support cases
- SCIM case access
- PII-protected data retrieval

**ID Format**: Same as ICM (14 digits)

**Best Practices**:
- PII guardrails are enforced - request only necessary data
- Use for support case lifecycle tracking
- Link support cases to ICMs for full context

### 5. Kusto MCP (Query Engine)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["@mcp-apps/kusto-mcp@latest"],
  "description": "Kusto query engine for telemetry and analytics"
}
```

**Capabilities**:
- Execute KQL queries against Kusto clusters
- List databases and tables
- Get table schemas
- Support for multiple clusters

**Key Databases**:
- `IcMDataWarehouse` - ICM incident data
- `CXEDataPlatform` - Customer experience metrics
- Various telemetry and diagnostic databases

**Best Practices**:
- **Always specify maxRows** to prevent large result sets
- **Cache results** in `data/*.json` for expensive queries
- **Use query files** in `queries/` directories for reusability
- **Test queries in Kusto Explorer first** before running via MCP
- **Add time filters** to limit data volume
- **Use `take` and `limit`** in queries

**Query Template**:
```kql
cluster('icmcluster').database('IcMDataWarehouse').Incidents
| where CreateDate >= ago(90d)
| where OwningTeamName contains "PURVIEW"
| where Severity <= 2  // P0, P1, P2
| summarize Count=count() by OwningTeamName, Severity
| order by Count desc
| take 100  // Limit results
```

**Common Operations**:
```python
# List tables
mcp_kusto_execute_query(
    clusterUrl="https://icmcluster.kusto.windows.net",
    database="IcMDataWarehouse",
    query=".show tables",
    maxRows=100
)

# Get schema
mcp_kusto_execute_query(
    clusterUrl="https://icmcluster.kusto.windows.net",
    database="IcMDataWarehouse",
    query=".show table Incidents schema",
    maxRows=100
)

# Execute analysis query
mcp_kusto_execute_query(
    clusterUrl="https://icmcluster.kusto.windows.net",
    database="IcMDataWarehouse",
    query="<your KQL query>",
    maxRows=1000
)
```

---

## 🎯 Best Practices by Use Case

### ICM Analysis Workflows

**Pattern**: Query ICMs → Cache results → Analyze → Generate report

1. **Generate query** using sub-agent tools
2. **Execute via Kusto MCP** with maxRows limit
3. **Save results** to `data/<timestamp>.json`
4. **Process locally** using Python scripts
5. **Generate HTML report** with metrics and recommendations

**Example**:
```bash
# Generate query
cd sub_agents/icm_agent
python icm_agent.py --team "PURVIEW\\SensitivityLabels" --days 90

# Execute query via Copilot CLI (MCP)
# (Copy query output and ask Copilot to execute)

# Save results manually to data/by_design_results.json

# Process and generate report
python icm_agent.py --from-file data/by_design_results.json
```

### ADO Work Tracking

**Pattern**: Query ADO → Link to ICMs → Track progress

1. **Use WIQL** for complex work item queries
2. **Tag items** for easy filtering
3. **Link ICMs** to bugs using artifact links
4. **Track in ADO dashboards** for visibility

**Example WIQL**:
```sql
SELECT [System.Id], [System.Title], [System.State], [System.Tags]
FROM WorkItems
WHERE [System.Tags] CONTAINS 'SensitivityLabels'
  AND [System.State] <> 'Closed'
ORDER BY [System.ChangedDate] DESC
```

### Customer Health Monitoring

**Pattern**: Kusto telemetry → Aggregate metrics → Risk reports

1. **Query tenant-level metrics** from CXEDataPlatform
2. **Aggregate across IC/MCS customers**
3. **Flag high-risk tenants** (SLA breaches, high escalations)
4. **Generate HTML risk reports** with customer impact

### Report Generation

**Pattern**: Live data → HTML template → Stakeholder delivery

1. **Fetch live data** via MCP (ICM, ADO, Kusto)
2. **Apply business logic** (risk scoring, prioritization)
3. **Use HTML templates** with embedded CSS/JS for rich visualizations
4. **Include metadata** (generation time, data sources)
5. **Save with timestamps** for versioning

---

## ⚡ Performance Optimization

### Caching Strategy

**Why**: Reduce API calls, improve response time, enable offline work

**What to cache**:
- Kusto query results (`data/*.json`)
- ICM incident details (for bulk analysis)
- ADO work item snapshots (for trend analysis)
- On-call schedules (update weekly)

**Naming convention**:
```
data/<source>_<description>_<timestamp>.<ext>

Examples:
data/icm_by_design_sensitivity_labels_20260211.json
data/ado_bugs_ic_mcs_mapping.json
data/kusto_risk_report_ic_20260210.csv
```

### Query Optimization

**Kusto Queries**:
- Add time filters (`ago(90d)`)
- Use `where` before `summarize`
- Limit results with `take` or `limit`
- Use `project` to select only needed columns
- Test query performance in Kusto Explorer

**ADO Queries**:
- Use specific field filters
- Limit time ranges
- Use tags for categorization
- Cache results for dashboards

**ICM Queries**:
- Request only needed fields
- Batch incident details when possible
- Use AI summaries for quick overviews

### Parallel Execution

When possible, execute independent queries in parallel:

```python
# Instead of sequential:
icm_data = query_icm()
ado_data = query_ado()
kusto_data = query_kusto()

# Run in parallel (pseudo-code):
with ThreadPoolExecutor() as executor:
    icm_future = executor.submit(query_icm)
    ado_future = executor.submit(query_ado)
    kusto_future = executor.submit(query_kusto)
    
    icm_data = icm_future.result()
    ado_data = ado_future.result()
    kusto_data = kusto_future.result()
```

---

## 🔧 Configuration Management

### mcp.json Structure

```json
{
  "servers": {
    "<server-name>": {
      "type": "stdio" | "http",
      "command": "<executable>",  // For stdio
      "args": ["<arg1>", "<arg2>"],  // For stdio
      "url": "<endpoint>",  // For http
      "env": {},  // Optional environment variables
      "description": "<clear description for agent>"
    }
  },
  "inputs": []
}
```

### Adding a New MCP Server

1. **Install the server** (if stdio-based):
   ```bash
   npm install -g <mcp-package>
   ```

2. **Add to mcp.json**:
   ```json
   {
     "your-server": {
       "type": "stdio",
       "command": "npx",
       "args": ["<package-name>"],
       "description": "Clear description of what it does"
     }
   }
   ```

3. **Test the connection**:
   ```bash
   # In Copilot CLI
   "List available tools from your-server"
   ```

4. **Update documentation**:
   - Add to this file
   - Add to custom instructions
   - Add examples to GETTING_STARTED.md

### Environment Variables

Some MCP servers need configuration via environment variables:

```json
{
  "servers": {
    "your-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["<package>"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}",
        "ENDPOINT": "https://your-endpoint.com"
      }
    }
  }
}
```

---

## 🚨 Error Handling

### Common Issues

**"MCP server not responding"**:
1. Check if package is installed: `npm list -g | grep <package>`
2. Try running command manually: `npx <package>`
3. Check Windows Defender/firewall
4. Restart Copilot CLI

**"Rate limit exceeded"**:
1. Implement caching to reduce calls
2. Add delays between requests
3. Use batch operations when available

**"Query timeout"**:
1. Add `maxRows` parameter
2. Add time filters to query
3. Break into smaller queries

**"Authentication failed"**:
1. For Azure CLI-based servers: `az login`
2. Check token expiration
3. Verify permissions

### Fallback Strategies

If MCP server fails:
1. **Use cached data** if available
2. **Manual execution** (e.g., Kusto Explorer for queries)
3. **Alternative MCP server** (e.g., different ADO instance)
4. **Inform user** of limitation and suggest workaround

---

## 📊 Monitoring & Observability

### Track MCP Usage

Log MCP calls in agent memory for analysis:

```bash
# After a session with heavy MCP usage
python cli.py insight add -t pattern \
  --content "ICM queries taking 30+ seconds, consider adding more filters" \
  --tags "performance,icm,mcp"
```

### Performance Metrics

Track and optimize:
- Query execution time
- Result set sizes
- API call frequency
- Cache hit rates
- Error rates by server

### User Experience

Good indicators:
- ✅ Responses in < 10 seconds
- ✅ Accurate data (no stale cache issues)
- ✅ Clear error messages when MCP fails
- ✅ Automatic fallbacks

---

## 🎓 Learning Resources

### MCP Documentation
- [Model Context Protocol Spec](https://spec.modelcontextprotocol.io/)
- [GitHub MCP Servers](https://github.com/modelcontextprotocol/servers)

### Server-Specific Docs
- [Azure DevOps MCP](https://github.com/microsoft/azure-devops-mcp)
- [ICM MCP](https://icm-mcp-prod.azure-api.net/) (Internal)
- [Kusto MCP](https://github.com/mcp-apps/kusto-mcp)

### Kusto Query Language
- [KQL Quick Reference](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference)
- [KQL Tutorials](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/)

---

## 🔄 Maintenance & Updates

### Weekly
- Review MCP server performance
- Update cached data (on-call schedules)
- Check for package updates

### Monthly
- Update MCP server packages: `npm update -g`
- Review and archive old cached data
- Update query templates based on schema changes

### As Needed
- Add new MCP servers for new capabilities
- Remove unused servers
- Update descriptions in mcp.json
- Document new patterns and best practices

---

## ✅ Checklist: Adding a New Analysis Workflow

- [ ] Identify data sources needed
- [ ] Determine which MCP servers to use
- [ ] Create query templates in `queries/`
- [ ] Build caching strategy in `data/`
- [ ] Create processing scripts
- [ ] Add report generation
- [ ] Document in sub-agent README
- [ ] Add examples to GETTING_STARTED.md
- [ ] Test end-to-end workflow
- [ ] Log workflow pattern in agent memory

---

**Version**: 1.0.0  
**Last Updated**: February 11, 2026  
**Workspace**: PHEPy  
**Related**: [mcp.json](../mcp.json), [Custom Instructions](../../.copilot/copilot-instructions.md)
