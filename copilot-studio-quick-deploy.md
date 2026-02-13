# 🚀 PHEPy Copilot Studio - Quick Deploy Guide

## ✅ Files Ready
- `copilot-studio-manifest.json` - Your agent configuration
- All MCP servers configured in `mcp.json`

## 📝 5-Minute Portal Deployment

### Step 1: Create Copilot (2 min)

**Portal:** https://copilotstudio.microsoft.com

1. Click **"Create"** button
2. Select **"New Copilot"** or **"Agent"**
3. Choose **"Declarative agent"** or **"Start with a description"**
4. Upload `copilot-studio-manifest.json` OR manually enter:
   - **Name:** PHEPy Orchestrator
   - **Description:** Purview Product Health & Escalation assistant
   - **Instructions:** Paste from manifest file

### Step 2: Add Conversation Starters (1 min)

Add these prompts in the "Topics" or "Conversation starters" section:

```
1. "What are the current Sev 0/1 ICM incidents?"
2. "Show me recent P0 bugs from ADO"
3. "Analyze support case trends for last week"
4. "Help me write a Kusto query for DLP telemetry"
```

### Step 3: Connect Data Sources (2 min)

#### Option A: Use Copilot Studio Built-in Connectors

**For Azure DevOps:**
1. Go to **Settings** → **Generative AI** → **Knowledge sources**
2. Add **Azure DevOps** connector
3. Select organizations: `o365exchange`, `ASIM-Security`
4. Grant consent

**For Azure Data Explorer (Kusto):**
1. Add **Azure Data Explorer** connector
2. Configure cluster connections
3. Test query execution

#### Option B: Create Custom Actions (Advanced)

For ICM and OAP (requires admin permissions):

1. Go to **Actions** tab
2. Click **"Add an action"** → **"Create a connector"**
3. Configure:
   - **ICM:** Base URL: `https://icm-mcp-prod.azure-api.net/v1/`
   - **OAP:** Base URL: `https://oap.microsoft.com/api/v1/`
4. Set authentication to **Microsoft Entra ID**

### Step 4: Test (30 sec)

1. Click **"Test"** button (top right)
2. Try: `"Show me critical incidents"`
3. Verify responses are working

### Step 5: Publish (30 sec)

1. Click **"Publish"**
2. Select channel: **Microsoft Teams**
3. Choose: Your team or organization

---

## 🎯 Quick Links

- **Portal:** https://copilotstudio.microsoft.com
- **Full Guide:** [COPILOT_STUDIO_DEPLOYMENT.md](COPILOT_STUDIO_DEPLOYMENT.md)
- **Manifest:** [copilot-studio-manifest.json](copilot-studio-manifest.json)
- **MCP Config:** [mcp.json](mcp.json)

## 💡 Tips

### If You Get Stuck

**Can't find "Declarative Agent" option?**
- Look for "New Copilot" → "Create from scratch"
- Or "Agent" → "Create new agent"
- Different tenants have different UI versions

**Data sources not connecting?**
- Verify you have permissions to the data sources
- Check if your org allows custom connectors
- Try built-in connectors first (ADO, Azure Data Explorer)

**Want to skip connectors for now?**
- The agent will work as a conversational interface
- Add data sources later incrementally
- Start with just the instructions and conversation starters

### Simplest Path

If you just want to test the concept:

1. **Create new copilot** with name "PHEPy Orchestrator"
2. **Paste instructions** from manifest
3. **Add conversation starters**
4. **Test without data connections** first
5. **Add connectors** one at a time later

This gives you a working copilot that can have conversations about Purview support, even before connecting live data.

## 🔄 Alternative: Teams Only (No Portal Login)

### Direct Teams Integration

1. Open **Microsoft Teams**
2. Go to **Apps** → **Copilot Studio**
3. Click **"Create a copilot"**
4. Follow the same steps in Teams interface

## 📊 After Deployment

### Monitor Usage
- Check **Analytics** tab for usage stats
- Review conversation logs
- Collect feedback from team

### Iterate
- Add more conversation starters based on common queries
- Refine instructions based on responses
- Connect additional data sources as needed

---

**Ready?** Portal is open → Start at "Create" button! 🚀
