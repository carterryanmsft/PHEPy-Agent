# PHEPy Agent - Foundry Deployment Details

**Deployment Date:** February 13, 2026  
**Status:** ✅ Successfully Deployed

---

## 🚀 Deployment Information

### Azure Resources
- **Resource Name:** phepy-resource
- **Resource Group:** rg-PHEPy
- **Location:** East US 2
- **Subscription:** Visual Studio Enterprise

### AI Model Deployment
- **Deployment Name:** phepy-gpt4o
- **Model:** GPT-4o (OpenAI format)
- **Version:** 2024-08-06
- **Capacity:** 10 (Standard)

### Endpoints
- **AI Services Endpoint:** https://phepy-resource.cognitiveservices.azure.com/
- **Azure AI Studio Project:** https://phepy-resource.services.ai.azure.com
- **Portal Access:** https://ai.azure.com

### Source Code
- **GitHub Repository:** https://github.com/carterryanmsft/PHEPy-Agent
- **Branch:** master
- **Remote:** origin

---

## 🔐 Environment Variables

```bash
# Azure AI Configuration
AZURE_AI_ENDPOINT=https://phepy-resource.cognitiveservices.azure.com/
AZURE_AI_KEY=<retrieve from Azure Portal>
DEPLOYMENT_NAME=phepy-gpt4o
API_VERSION=2024-08-01-preview

# GitHub Integration
GITHUB_REPO=https://github.com/carterryanmsft/PHEPy-Agent
GITHUB_BRANCH=master
```

---

## 🌐 Access Methods

### 1. Azure AI Studio Portal
```
https://ai.azure.com
→ Navigate to "PHEPy" project
→ Go to Playground → Chat/Agents
```

### 2. REST API
```bash
curl -X POST "https://phepy-resource.cognitiveservices.azure.com/openai/deployments/phepy-gpt4o/chat/completions?api-version=2024-08-01-preview" \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are PHEPy Orchestrator Agent..."},
      {"role": "user", "content": "What capabilities do you have?"}
    ],
    "temperature": 0.3
  }'
```

### 3. Python SDK
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://phepy-resource.cognitiveservices.azure.com/",
    api_key="YOUR_API_KEY",
    api_version="2024-08-01-preview"
)

response = client.chat.completions.create(
    model="phepy-gpt4o",
    messages=[
        {"role": "system", "content": "You are PHEPy Orchestrator Agent..."},
        {"role": "user", "content": "Show me incident investigation examples"}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)
```

---

## 📋 Portal Configuration Checklist

Complete these steps in Azure AI Studio:

- [x] GPT-4o model deployed
- [x] GitHub repository connected
- [ ] Agent created in Playground
- [ ] System instructions configured
- [ ] Knowledge base files added:
  - [ ] GETTING_STARTED.md
  - [ ] CAPABILITY_MATRIX.md
  - [ ] ADVANCED_CAPABILITIES.md
  - [ ] QUICK_REFERENCE.md
  - [ ] INDEX.md
- [ ] Agent tested with sample prompts
- [ ] Agent deployed (Web/API/Teams)

---

## 🔄 Update Workflow

### To update the agent:

1. **Make local changes:**
   ```powershell
   # Edit files in VS Code
   git add .
   git commit -m "Updated agent capabilities"
   git push origin master
   ```

2. **Azure AI Studio automatically syncs** from GitHub

3. **Test changes** in Playground before deploying

---

## 🧪 Test Prompts

Once configured in the portal, test with:

```
What capabilities does PHEPy have?
```

```
List all available MCP agents and their functions
```

```
Show me example prompts for incident investigation
```

```
Get full details for ICM 21000000887894 including timeline and customer impact
```

---

## 📚 Documentation Files

All documentation is in the GitHub repo and available in the workspace:

- **Getting Started:** GETTING_STARTED.md
- **Capabilities:** CAPABILITY_MATRIX.md
- **Advanced Features:** ADVANCED_CAPABILITIES.md
- **Quick Reference:** QUICK_REFERENCE.md
- **Complete Index:** INDEX.md

---

## 🔧 Management Commands

### List deployments:
```powershell
az cognitiveservices account deployment list --name phepy-resource --resource-group rg-PHEPy -o table
```

### Get deployment details:
```powershell
az cognitiveservices account deployment show --name phepy-resource --resource-group rg-PHEPy --deployment-name phepy-gpt4o
```

### Get API keys:
```powershell
az cognitiveservices account keys list --name phepy-resource --resource-group rg-PHEPy
```

### Redeploy:
```powershell
.\push-to-foundry.ps1
```

---

## 🎯 Next Steps

1. **Open Azure AI Studio:** https://ai.azure.com
2. **Navigate to PHEPy project**
3. **Go to Playground → Agents**
4. **Create agent** with:
   - Name: PHEPy Orchestrator
   - Deployment: phepy-gpt4o
   - System message: Use system-instructions.txt (already in clipboard!)
5. **Add knowledge base** from GitHub
6. **Test** with sample prompts
7. **Deploy** to your preferred channel

---

## ✅ Deployment Status

- ✅ Azure resources created
- ✅ Git repository initialized and pushed
- ✅ GPT-4o model deployed
- ✅ Endpoint configured
- ✅ API keys generated
- 🔄 **Awaiting portal configuration** (5-10 minutes to complete)

---

**Last Updated:** February 13, 2026  
**Deployed By:** carterryan22@outlook.com  
**Deployment Script:** push-to-foundry.ps1
