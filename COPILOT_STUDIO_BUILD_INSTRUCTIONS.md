# 🤖 Building PHEPy Agent in Copilot Studio

**You're here:** Empty agent created in CxESharedServicesAI-Prod environment
**Goal:** Configure it with all your PHEPy capabilities

---

## 📝 Step 1: Configure Agent Instructions (5 min)

### In Copilot Studio:
1. Open your **PHEPy Orchestrator** agent
2. Go to **Settings** → **Generative AI** → **Instructions**
3. Paste this as the **System Prompt**:

```
You are the PHEPy Orchestrator - a specialized support engineering assistant for Microsoft Purview.

# Core Identity
You help Microsoft support engineers analyze product health, track escalations, and resolve customer issues for Purview/Information Protection products including DLP, MIP, eDiscovery, and related services.

# Core Capabilities
- 🎫 **ICM Management**: Query incidents, escalations, customer impact analysis
- 🐛 **ADO Integration**: Bug tracking, P0/P1 priority bugs, feature requests  
- 📊 **Kusto Analytics**: Telemetry analysis, diagnostic queries, trend analysis
- 💼 **Case Management**: Support case lifecycle, customer context, case history
- 📚 **Knowledge Base**: TSG lookup, troubleshooting guidance, best practices

# Available Data Sources
You have access to:
- ICM incident database (IcM IDs like 728221759)
- Azure DevOps projects: o365exchange, ASIM-Security (Bug IDs like 3563451)
- Kusto clusters for telemetry and diagnostics
- Support case system (Case IDs like 118, 131)
- Internal documentation and TSGs

# Key Products You Support
- **Data Loss Prevention (DLP)**: Policies, rules, incidents, false positives
- **Microsoft Information Protection (MIP)**: Sensitivity labels, encryption, auto-labeling
- **eDiscovery**: Search, holds, exports, compliance boundaries
- **Insider Risk Management (IRM)**: Risk detection, alerts, investigations
- **Communication Compliance**: Policy violations, escalations
- **Purview Auditing**: Audit logs, search, retention
- **Content Search**: Cross-workload search capabilities

# Response Guidelines

## When Analyzing Incidents
- Check severity (Sev 0/1 = critical, customer down)
- Identify owning team and escalation path
- Look for related bugs in ADO
- Check customer impact metrics
- Provide mitigation steps if available

## When Investigating Bugs
- Focus on P0/P1 bugs for critical issues
- Check bug state: Active, Resolved, Closed
- Look for linked ICM incidents
- Review root cause analysis if available
- Note any customer-impacting bugs

## When Querying Telemetry
- Use Kusto for aggregations and trends
- Look for error patterns across customers
- Identify spike in failures or latency
- Correlate with deployment timelines
- Provide actionable insights

## When Managing Cases
- Check case priority and SLA status
- Review case history for context
- Identify escalation triggers (SLA breach, escalations)
- Look for related cases from same customer
- Note any special handling requirements

# Escalation Awareness
- **Sev 0/1**: Immediate attention, customer outage
- **Sev 2**: High priority, degraded service
- **P0 Bugs**: Customer-impacting, needs immediate fix
- **P1 Bugs**: High priority feature/fix
- **LQE (Live Quality Escalation)**: Customer unhappy, needs PM attention

# Response Style
- Be precise and technical - this is for engineers
- Always include IDs when referencing work items (ICM, ADO, Cases)
- Provide actionable next steps
- Use data to support recommendations
- Link to relevant documentation when available
- Format responses clearly with bullet points for readability

# Common Queries You'll Handle
- "What are current critical incidents?"
- "Show me P0 bugs related to DLP"
- "Analyze case trends for customer XYZ"
- "Query telemetry for label application errors"
- "What's the status of ICM incident 728221759?"
- "Find bugs linked to this customer's issue"
- "Show recent escalations for eDiscovery"

# When You Don't Have Data
- Clearly state what data you don't have access to
- Suggest manual investigation steps
- Provide links to internal tools (ICM portal, ADO, Kusto Explorer)
- Recommend contacting specific teams if needed

# Safety & Privacy
- Never expose customer PII or sensitive data
- Redact confidential information in responses
- Follow Microsoft data handling policies
- Use aggregated data for trends, not individual records

Remember: Your goal is to help engineers work efficiently, reduce mean-time-to-resolution, and improve customer satisfaction by providing fast access to critical product health and escalation data.
```

4. Click **Save**

---

## 📚 Step 2: Add Knowledge Sources (10 min)

### Upload Your Documentation:

1. Go to **Knowledge** → **Add Knowledge**
2. Select **Upload files**

Upload these key files from your workspace:

```powershell
# From PHEPy root:
- GETTING_STARTED.md
- CAPABILITY_MATRIX.md  
- ADVANCED_CAPABILITIES.md
- QUICK_REFERENCE.md

# From docs/:
- docs/QUERY_CHEAT_SHEET.md
- docs/AGENT_BEST_PRACTICES.md
- docs/MCP_SERVER_BEST_PRACTICES.md

# From tsg_system/:
- tsg_system/wiki_tsg_baseline_report.md
```

3. **Alternative**: Add SharePoint/OneDrive link
   - If your PHEPy folder is in OneDrive, add it as a SharePoint knowledge source
   - Go to **Knowledge** → **SharePoint**
   - Add your OneDrive PHEPy folder URL

---

## 🔌 Step 3: Connect Data Sources via Actions (20 min)

### Option A: Use Built-in Connectors (Easiest)

#### Azure DevOps Connector
1. Go to **Actions** tab
2. Click **+ Add an action**
3. Search for **"Azure DevOps"**
4. Select **Azure DevOps** connector
5. Click **Add**
6. Configure connection:
   - **Organization**: `microsoft`  
   - **Project**: `o365exchange`
   - Authenticate with your Microsoft account
7. Enable these actions:
   - **Get work item**
   - **Query work items** (WIQL)
   - **List work items**
8. Repeat for `ASIM-Security` project

#### Azure Data Explorer (Kusto)
1. **Actions** → **+ Add an action**
2. Search for **"Azure Data Explorer"**
3. Configure:
   - **Cluster URL**: Your Kusto cluster
   - Authenticate
4. Enable:
   - **Execute query**
   - **List databases**

### Option B: Create Custom HTTP Actions (For ICM & OAP)

#### ICM Connector
1. **Actions** → **+ Add an action** → **Create a custom action**
2. Configure:
   - **Name**: ICM Incident Management
   - **Base URL**: `https://icm-mcp-prod.azure-api.net/v1/`
   - **Authentication**: Microsoft Entra ID
   - **Resource**: `api://icm-mcp/.default`

3. Add operations:
   ```
   GET /incidents/{incidentId}
   Description: Get incident details
   
   POST /incidents/search
   Description: Search incidents
   Body: {"query": "string", "filters": {}}
   
   GET /incidents/{incidentId}/impact
   Description: Get customer impact
   ```

4. Test the connection

#### OAP/Case Management Connector
1. **Actions** → **+ Add an action** → **Create a custom action**
2. Configure:
   - **Name**: Support Case Management
   - **Base URL**: `https://oap.microsoft.com/api/v1/`
   - **Authentication**: Microsoft Entra ID

3. Add operations:
   ```
   GET /cases/{caseId}
   POST /cases/search
   GET /cases/{caseId}/history
   ```

---

## 💬 Step 4: Add Conversation Starters (3 min)

1. Go to **Topics** → **Conversation starters**
2. Click **+ Add**
3. Add these prompts:

```
1. "What are the current Sev 0/1 ICM incidents?"
2. "Show me recent P0 bugs from ADO"
3. "Analyze support case trends for last week"
4. "Help me write a Kusto query for DLP telemetry"
5. "Show critical escalations for my team"
6. "Find bugs related to label visibility issues"
7. "What's the status of ICM 728221759?"
8. "Query telemetry for auto-labeling errors"
9. "Show eDiscovery holds failing today"
10. "Analyze DLP policy performance issues"
```

---

## ⚙️ Step 5: Configure Generative AI Settings (3 min)

1. Go to **Settings** → **Generative AI**

2. **Content Moderation**: 
   - Set to **Medium** (allows technical discussions)

3. **How should your copilot interact**:
   - Select **Informational** and **Professional**
   - Tone: Technical, precise, actionable

4. **Generative answers**:
   - Enable **Generate answers from:** Knowledge sources, Actions
   - Response length: **Long** (detailed technical responses)

5. **AI Model**:
   - Use **GPT-4** or **GPT-4 Turbo** for best results

---

## 🧪 Step 6: Test Your Agent (10 min)

1. Click **Test** button (top right)

2. Try these test queries:

```
Test 1: Knowledge Check
"What capabilities does PHEPy have?"
→ Should reference your uploaded docs

Test 2: ADO Integration
"Search for P0 bugs in o365exchange project"
→ Should use Azure DevOps connector

Test 3: ICM Query (if configured)
"Get details for incident 728221759"
→ Should use ICM connector

Test 4: General Support
"How do I troubleshoot label visibility issues?"
→ Should reference TSG documentation

Test 5: Kusto Help
"Help me write a query to find DLP policy evaluation failures"
→ Should provide KQL query structure
```

3. **Check the trace**:
   - Expand each response
   - Verify which knowledge sources were used
   - Check if actions were called correctly
   - Note any errors

---

## 📱 Step 7: Publish Your Agent (5 min)

### Publish to Teams
1. Click **Publish** button
2. Select **Microsoft Teams**
3. Choose channels/teams:
   - Your support team channel
   - PHE program channel
   - Testing channel first (recommended)
4. Click **Publish**

### Publish to Web
1. **Publish** → **Demo website**
2. Copy the URL
3. Share with your team

---

## 🔄 Step 8: Iterate and Improve

### Monitor Usage
- Go to **Analytics** tab
- Check:
  - Total sessions
  - Resolution rate
  - Top topics
  - Action success rates

### Refine Based on Feedback
- Add more conversation starters for common queries
- Expand knowledge base with more documentation
- Fine-tune instructions based on response quality
- Add more custom actions as needed

---

## 🚀 Quick Wins for Your Team

### Immediate Value
Once configured, your team can:
1. **Ask natural language questions** about incidents, bugs, cases
2. **Get instant status** on critical escalations
3. **Query telemetry** without opening Kusto Explorer
4. **Find documentation** quickly via chat
5. **Track trends** across products and customers

### Time Savings
- **Before**: 5-10 min to open ICM, find incident, check impact
- **After**: 30 seconds to ask "What's the status of ICM 728221759?"

- **Before**: 10-15 min to write Kusto query, run, analyze
- **After**: 2 minutes to ask "Show me DLP errors from last 24 hours"

---

## 📞 Need Help?

### Common Issues

**Actions not connecting?**
- Verify authentication permissions
- Check firewall/network access
- Ensure APIs are accessible from your tenant

**Knowledge sources not working?**
- Confirm files uploaded successfully
- Check file format (Markdown, PDF, DOCX supported)
- Re-index if needed

**Agent responses not accurate?**
- Refine system instructions
- Add more specific examples
- Expand knowledge base

### Resources
- Copilot Studio Docs: https://learn.microsoft.com/microsoft-copilot-studio/
- Your PHEPy docs: See README.md
- MCP Server config: mcp.json

---

## ✅ Success Checklist

Mark off as you complete:

- [ ] Agent instructions configured
- [ ] Knowledge sources uploaded (at least 3 docs)
- [ ] Azure DevOps connector added and tested
- [ ] Kusto connector added (or documented as manual)
- [ ] ICM connector added (or documented as manual)
- [ ] OAP/Case connector added (or documented as manual)
- [ ] 10 conversation starters added
- [ ] Generative AI settings configured
- [ ] Test queries all pass
- [ ] Published to test channel in Teams
- [ ] Team trained on basic usage
- [ ] Analytics dashboard bookmarked

---

**Estimated Total Time**: 60-90 minutes for full setup
**Minimum Viable**: 20 minutes (instructions + knowledge + 1 connector + test)

🎉 Once complete, you'll have a powerful AI assistant that understands your Purview support operations and can help your team work more efficiently!
