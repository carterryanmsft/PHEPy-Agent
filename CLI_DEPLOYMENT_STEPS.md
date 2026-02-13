# 🎯 PHEPy CLI Deployment - Step by Step

## ✅ Files Ready for Deployment

Your configuration files have been created:
- `system-instructions.txt` - Agent system prompt
- `endpoint.yml` - Endpoint configuration  
- `deployment.yml` - Deployment settings
- `deploy-foundry-cli.ps1` - Automated deployment script

---

## 🚀 RECOMMENDED: Hybrid CLI + Portal Approach

Since AI Foundry is still evolving, the fastest path is CLI prep + Portal completion:

### Step 1: Complete Azure Authentication (In Progress)

```powershell
# If authentication window appeared, complete sign-in
# Then verify:
az account show
```

### Step 2: Find Your Workspace

```powershell
# After auth completes, list workspaces:
cd "C:\Users\carterryan\OneDrive - Microsoft\PHEPy"
.\deploy-foundry-cli.ps1 -ListWorkspaces

# You should see a table of workspaces you have access to
```

### Step 3: Deploy to Correct Workspace

```powershell
# Once you see the workspace name, deploy:
.\deploy-foundry-cli.ps1 -WorkspaceName "<actual-workspace-name>"

# For example, if it's named differently:
.\deploy-foundry-cli.ps1 -WorkspaceName "CxESharedServicesAI"
```

---

## 🎯 FASTEST: Direct Portal Setup (10 min)

If CLI is having issues, skip to portal (already open at https://ai.azure.com):

### Portal Steps:

1. **Find your workspace:**
   - Look for anything with "CxE", "Shared", or "AI" in the name
   - Or create a new workspace if you have permissions

2. **Create project:**
   - Click "+ New project"
   - Name: PHEPy-Orchestrator
   - Click Create

3. **Go to Playground → Chat**

4. **Copy/paste system instructions:**
   - Click "System message" 
   - Open: `system-instructions.txt`
   - Copy entire content and paste

5. **Upload documentation:**
   - Go to Data → Upload files
   - Upload:
     - GETTING_STARTED.md
     - CAPABILITY_MATRIX.md
     - ADVANCED_CAPABILITIES.md
     - QUICK_REFERENCE.md

6. **Test:**
   - In chat, ask: "What capabilities does PHEPy have?"
   - Verify it cites your uploaded docs

7. **Deploy:**
   - Click "Deploy" button
   - Choose your target (API endpoint, Teams, etc.)

---

## 📝 What to Do After Authentication Completes

Run these commands in order:

```powershell
# 1. Verify you're logged in
az account show

# 2. List available workspaces
cd "C:\Users\carterryan\OneDrive - Microsoft\PHEPy"
az ml workspace list -o table

# 3. If you see your workspace, deploy:
.\deploy-foundry-cli.ps1 -WorkspaceName "<workspace-name-from-step-2>"

# 4. If no workspace exists, you can either:
#    a) Use portal to create one (recommended)
#    b) Create via CLI (if you have permissions):
az ml workspace create --name PHEPy-Workspace --resource-group <your-rg>
```

---

##  Alternative: Simpler API-Only Deployment

If you just want to get it working quickly without full Foundry setup:

```powershell
# Use Azure OpenAI directly (if you have access)
az cognitiveservices account list --query "[?kind=='OpenAI']" -o table

# Deploy as simple chat completion with your instructions
# This doesn't need AI Foundry workspace
```

---

## 🔍 Troubleshooting

**"Account has previously been signed out"**
→ Authentication window should have opened - complete sign-in there
→ If stuck, run: `az logout` then `az login` again

**"Workspace not found"**
→ Either workspace doesn't exist or is in different subscription
→ Run: `.\deploy-foundry-cli.ps1 -ListWorkspaces` to see what's available
→ Or check in portal: https://portal.azure.com → Search "machine learning"

**"No permission to create"**
→ Ask your admin for "Contributor" role on the workspace/resource group
→ Or have them create the project for you

**CLI seems broken**
→ Portal approach works just as well and is actually faster
→ Use portal for initial setup, CLI for updates later

---

## ✅ Success Criteria

You'll know it's working when:
- [ ] You can access a workspace in portal or CLI
- [ ] Project "PHEPy-Orchestrator" is created
- [ ] System instructions are configured
- [ ] At least 2-3 docs are uploaded
- [ ] Test query returns relevant answer
- [ ] Agent is deployed to an endpoint or Teams

---

## 💡 Current Status

✅ Configuration files created
✅ System instructions written
✅ Portal opened (https://ai.azure.com)
⏳ Waiting for authentication to complete
⏳ Need to identify correct workspace

**Next action:** Complete authentication in browser, then run the workspace list command above.

---

## 🆘 Need Help?

**Fastest path right now:**
1. Complete authentication in the browser window
2. Go to portal: https://ai.azure.com
3. Click around to find your workspace
4. Create project directly in portal
5. Follow portal steps above

The portal is actually faster than CLI for initial setup anyway! 😊
