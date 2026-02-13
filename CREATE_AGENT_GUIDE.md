# Create PHEPy Agent in Azure AI Studio - Step by Step

**Current Status:** ✅ GPT-4o model deployed, but agent not yet created

---

## 🎯 Create Agent in Portal (3 minutes)

### Step 1: Navigate to Your Project
1. Go to: **https://ai.azure.com**
2. Find and click: **"phepy-resource"** workspace
3. Click on: **"phepy"** project (or create if it doesn't exist)

### Step 2: Create Agent
1. In the left sidebar, click: **"Agents"** or **"Playground"**
2. Click: **"+ Create"** or **"+ New agent"**

### Step 3: Configure Agent
Fill in these details:

**Basic Settings:**
- **Name:** `PHEPy Orchestrator`
- **Description:** `Comprehensive Purview Product Health & Escalation Orchestrator Agent`

**Model Configuration:**
- **Deployment:** Select `phepy-gpt4o` ✅ (should appear in dropdown)
- **Temperature:** `0.3`
- **Max tokens:** `4096` (or leave default)
- **Top P:** `0.95` (or leave default)

### Step 4: Add System Instructions

Click **"System message"** or **"Instructions"** and paste:

```
Run this command to copy instructions:
```

```powershell
Get-Content "system-instructions.txt" | Set-Clipboard
```

Then **Ctrl+V** in the portal.

### Step 5: Add Knowledge (Optional but Recommended)

1. Click **"+ Add your data"** or **"Knowledge"**
2. Choose **"Upload files"** or **"GitHub"**
3. If GitHub:
   - Repository: `https://github.com/carterryanmsft/PHEPy-Agent`
   - Files to add:
     - `GETTING_STARTED.md`
     - `CAPABILITY_MATRIX.md`
     - `ADVANCED_CAPABILITIES.md`
     - `QUICK_REFERENCE.md`

### Step 6: Save Agent
1. Click **"Save"** or **"Create"**
2. Wait 10-30 seconds for agent to be created

### Step 7: Test Agent
In the chat interface, try:
```
What capabilities does PHEPy have?
```

### Step 8: Deploy (Optional)
Once tested:
1. Click **"Deploy"**
2. Choose channel: **Web app** / **API** / **Teams**

---

## 🔧 Alternative: Create via Azure OpenAI Studio

If the above doesn't work, try:

1. Go to: **https://oai.azure.com**
2. Click **"Chat playground"**
3. Under **"Setup"**:
   - Deployment: Select **phepy-gpt4o**
   - System message: Paste from system-instructions.txt
4. Click **"Deploy to"** → **"A new web app"**

---

## ⚠️ Troubleshooting

### If "phepy-gpt4o" doesn't appear:
```powershell
# Verify deployment
az cognitiveservices account deployment show --name phepy-resource --resource-group rg-PHEPy --deployment-name phepy-gpt4o
```

### If project "phepy" doesn't exist:
1. In Azure AI Studio, click **"+ New project"**
2. Name: `phepy`
3. Select workspace: `phepy-resource`
4. Click **Create**
5. Then follow steps above

### Check project exists:
```powershell
az rest --method GET --url "https://phepy-resource.services.ai.azure.com/api/projects" 2>&1
```

---

## ✅ Success Indicators

You'll know it's working when:
- Agent appears in the Agents list
- You can chat with it in Playground
- It responds using the system instructions
- The URL https://phepy-resource.services.ai.azure.com/api/projects/phepy/agents shows your agent

---

**Need help?** The portal is the easiest way. Let me know if you get stuck on any step!
