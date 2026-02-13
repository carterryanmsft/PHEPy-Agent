# PHEPy Project - Foundry Deployment Preparation Plan

**Date:** February 11, 2026  
**Purpose:** Prepare PHEPy Orchestrator Agent for Foundry publication  
**Status:** Ready for Implementation

---

## 📊 Executive Summary

### Current State
- **202+ Python files** across workspace
- **50+ root-level scripts** (many one-off analyses)
- **Extensive documentation** (~30 markdown files in root)
- **5 MCP server integrations** configured
- **8 sub-agent systems** with complete instructions

### Target State for Foundry
- **Clean agent structure** with essential components only
- **Core sub-agents** (8 folders with AGENT_INSTRUCTIONS.md)
- **Organized documentation** in proper hierarchy
- **MCP configuration** ready for deployment
- **No sensitive data or generated artifacts**

### Impact
- **Space Reduction:** ~80% cleaner workspace
- **Clarity:** Clear separation of agent vs analysis scripts
- **Security:** No PII, credentials, or customer data
- **Maintainability:** Easy to understand and extend

---

## 🎯 Phase 1: Identify Core Agent Components (KEEP)

### Essential for Agent Deployment ✅

#### Root Configuration Files
```
✅ mcp.json                    # MCP server configuration
✅ requirements.txt            # Python dependencies
✅ .gitignore                  # Security protections
✅ README.md                   # Main entry point
✅ INDEX.md                    # Navigation hub
✅ GETTING_STARTED.md          # Quick start guide
```

#### Core Documentation (Root)
```
✅ CAPABILITY_MATRIX.md        # Feature reference
✅ ADVANCED_CAPABILITIES.md    # Power user guide
✅ QUICK_REFERENCE.md          # Quick reference
✅ GRAPH_API_SETUP.md          # Setup instructions
```

#### Essential Folders
```
✅ agent_memory/               # Persistent memory system
   ├── README.md
   ├── QUICK_SETUP.md
   ├── bootstrap.py
   ├── cli.py
   ├── session_manager.py
   └── src/

✅ sub_agents/                 # 8 sub-agent systems
   ├── icm_agent/
   ├── kusto_expert/
   ├── support_case_manager/
   ├── work_item_manager/
   ├── tenant_health_monitor/
   ├── purview_product_expert/
   ├── program_onboarding_manager/
   ├── escalation_manager/
   └── contacts_escalation_finder/

✅ docs/                       # Organized documentation
   ├── project/                # Project documentation
   ├── CONTINUOUS_IMPROVEMENT_WEEKLY.md
   ├── AGENT_BEST_PRACTICES.md
   ├── MCP_SERVER_BEST_PRACTICES.md
   └── QUERY_CHEAT_SHEET.md

✅ grounding_docs/             # Domain knowledge files

✅ purview_analysis/           # ICM analysis framework
   ├── queries/                # Kusto templates
   ├── templates/              # Report templates
   └── documentation/

✅ tsg_system/                 # Troubleshooting system

✅ risk_reports/               # Risk report system
   ├── scripts/                # Core scripts only
   ├── templates/              # Report templates
   └── documentation/
```

---

## 🗑️ Phase 2: Archive/Remove Non-Agent Files (CLEANUP)

### A. Root Directory - One-Off Analysis Scripts (MOVE TO archive/)

**Problem:** 40+ single-purpose analysis scripts clutter root directory

#### Bug/ICM Analysis Scripts (16 files)
```
❌ analyze_bug_linkage.py
❌ analyze_by_design_icms.py
❌ analyze_by_design_real_icms.py
❌ analyze_by_design_report.py
❌ analyze_icm_owners.py
❌ analyze_ic_mcs_bugs_from_icm.py
❌ analyze_ic_mcs_tenants_bugs.py
❌ analyze_ic_risk_report.py
❌ comprehensive_icm_bug_analysis.py
❌ parse_icm_bug_mentions.py
❌ extract_bugs_for_fetch.py
❌ extract_icm_from_ado_bugs.py
❌ extract_icm_ids_for_ado.py
❌ fetch_icm_hyperlinks.py
❌ process_ado_search_results.py
❌ process_ic_filtered.py
```

**Action:** Move to `archive/one_off_analyses/bug_icm_analysis/`

#### Validation Scripts (6 files)
```
❌ validate_90day_threshold.py
❌ validate_bug_summary.py
❌ validate_critical_table.py
❌ validate_final_report.py
❌ validate_unassigned_flag.py
❌ final_validation.py
```

**Action:** Move to `archive/one_off_analyses/validation/`

#### Data Checking Scripts (5 files)
```
❌ check_active_unassigned.py
❌ check_bug_data.py
❌ check_icm_data.py
❌ check_scim_cases.py
❌ filter_scim_cases.py
```

**Action:** Move to `archive/one_off_analyses/data_checking/`

#### Customer Report Generators (4 files)
```
❌ generate_cibc_report.py
❌ generate_ge_report.py
❌ generate_santander_zurich_report.py
❌ show_barclays_details.py
```

**Action:** Move to `archive/customer_specific_reports/`

#### Mapping/Matching Scripts (5 files)
```
❌ map_ado_bugs_to_ic_mcs.py
❌ map_ic_mcs_bugs_to_customers.py
❌ match_bugs_to_customers.py
❌ match_bugs_to_customers_final.py
❌ final_bug_linkage_analysis.py
```

**Action:** Move to `archive/one_off_analyses/mapping/`

#### Miscellaneous Utilities (5 files)
```
❌ config_email_credentials.py  # One-time setup
❌ convert_timeline_to_pptx.py  # Specific use case
❌ create_icm_owner_query.py    # Query builder
❌ display_bug_matches_table.py # Display utility
❌ fix_ic_csv.py                # Data fix script
❌ find_unassigned_case.py      # Finder utility
❌ SOLUTION_STEPS.py            # Just steps, not script
```

**Action:** Move to `archive/utilities/`

### B. Root Directory - Analysis Reports (MOVE TO archive/)

#### Analysis Markdown Files
```
❌ by_design_analysis_real_data.md
❌ by_design_analysis_report.md
❌ COMPREHENSIVE_BUG_LINKAGE_REPORT.md
❌ GEMBA_ANALYSIS_2512120040008759_Desjardins.md
❌ INCIDENT_TIMELINE_2512120040008759_Desjardins.md
❌ INCIDENT_TIMELINE_2512120040008759_Desjardins_Full.md
❌ IC_REPORT_UPDATES_2026-02-09.md
```

**Action:** Move to `archive/analysis_reports/`

### C. Root Directory - Implementation Documentation (MOVE TO docs/)

```
❌ CLEANUP_PLAN.md
❌ CLEANUP_QUICK_REFERENCE.md
❌ DOCUMENTATION_MAP.md
❌ OPTIMIZATION_GUIDE.md
❌ WHATS_NEW.md
❌ WORKSPACE_ORGANIZATION.md
❌ WORKSPACE_REVIEW_SUMMARY.md
```

**Action:** Move to `docs/project/workspace/`

### D. Root Directory - Data Files (REMOVE - Gitignored Anyway)

```
❌ export (9).csv
❌ DSCGP Squad Map.csv          → Move to docs/reference/
❌ icm_by_design_analysis_with_customers.xlsx → Move to archive/
❌ Desjardins_Incident_Timeline.pptx → Move to archive/
```

### E. Folders to Archive/Remove Entirely

```
❌ archive/                    # Already archived, can remove from deployment
❌ Copilot/                    # Temp/scratch workspace
❌ --output/                   # Output folder (empty or temp data)
❌ __pycache__/                # Python cache
❌ .venv/                      # Virtual environment (never deploy)
❌ .vscode/                    # Editor settings (optional, can keep)
```

---

## 🔧 Phase 3: Organize Remaining Structure

### Final Directory Structure for Foundry

```
PHEPy/
│
├── 📄 mcp.json                          # MCP server config
├── 📄 requirements.txt                  # Dependencies
├── 📄 .gitignore                        # Security
├── 📄 README.md                         # Main entry
├── 📄 INDEX.md                          # Navigation
├── 📄 GETTING_STARTED.md                # Quick start
├── 📄 CAPABILITY_MATRIX.md              # Features
├── 📄 ADVANCED_CAPABILITIES.md          # Advanced guide
├── 📄 QUICK_REFERENCE.md                # Reference
├── 📄 GRAPH_API_SETUP.md                # Setup
├── 📄 TODO.md                           # Tracking (optional)
│
├── 📁 agent_memory/                     # Persistent memory
│   ├── README.md
│   ├── QUICK_SETUP.md
│   ├── bootstrap.py
│   ├── cli.py
│   ├── session_manager.py
│   └── src/
│
├── 📁 sub_agents/                       # 8 sub-agents
│   ├── icm_agent/
│   │   ├── AGENT_INSTRUCTIONS.md
│   │   ├── README.md
│   │   └── [agent files]
│   ├── kusto_expert/
│   ├── support_case_manager/
│   ├── work_item_manager/
│   ├── tenant_health_monitor/
│   ├── purview_product_expert/
│   ├── program_onboarding_manager/
│   ├── escalation_manager/
│   └── contacts_escalation_finder/
│
├── 📁 docs/                             # Documentation
│   ├── project/                         # Project docs
│   │   ├── AGENT_INSTRUCTIONS.md
│   │   ├── ARCHITECTURE_DIAGRAM.md
│   │   ├── COMPLETION_SUMMARY.md
│   │   ├── EXECUTIVE_BRIEFING.md
│   │   ├── FOLDER_STRUCTURE.md
│   │   ├── PROJECT_SUMMARY.md
│   │   ├── QUICK_START.md
│   │   └── workspace/                   # Workspace docs
│   │       ├── CLEANUP_PLAN.md
│   │       ├── OPTIMIZATION_GUIDE.md
│   │       └── WORKSPACE_ORGANIZATION.md
│   ├── AGENT_BEST_PRACTICES.md
│   ├── MCP_SERVER_BEST_PRACTICES.md
│   ├── CONTINUOUS_IMPROVEMENT_WEEKLY.md
│   ├── QUERY_CHEAT_SHEET.md
│   └── reference/                       # Reference materials
│       └── DSCGP_Squad_Map.csv
│
├── 📁 grounding_docs/                   # Domain knowledge
│   └── [grounding documents]
│
├── 📁 purview_analysis/                 # Analysis framework
│   ├── README.md
│   ├── SYSTEM_SUMMARY.md
│   ├── queries/                         # Kusto queries
│   ├── templates/                       # Report templates
│   └── documentation/
│
├── 📁 tsg_system/                       # TSG system
│   └── [tsg files]
│
├── 📁 risk_reports/                     # Risk reports
│   ├── README.md
│   ├── templates/                       # Templates only
│   ├── scripts/                         # Core scripts
│   │   ├── ic_mcs_risk_report_generator.py
│   │   ├── generate_production_report.py
│   │   └── run_full_report.py
│   └── documentation/
│
├── 📁 data/                             # Data folder (gitignored)
│   └── .gitkeep                         # Keep folder structure
│
└── 📁 output/                           # Output folder (gitignored)
    └── .gitkeep                         # Keep folder structure
```

---

## ✅ Phase 4: Execution Checklist

### Step 1: Backup Everything
```powershell
# Create backup
$backupDate = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "c:\Users\carterryan\OneDrive - Microsoft\PHEPy" -Destination "c:\Users\carterryan\OneDrive - Microsoft\PHEPy_BACKUP_$backupDate" -Recurse
```

### Step 2: Archive Root Scripts
```powershell
# Create archive structure
New-Item -ItemType Directory -Path "archive/one_off_analyses/bug_icm_analysis" -Force
New-Item -ItemType Directory -Path "archive/one_off_analyses/validation" -Force
New-Item -ItemType Directory -Path "archive/one_off_analyses/data_checking" -Force
New-Item -ItemType Directory -Path "archive/one_off_analyses/mapping" -Force
New-Item -ItemType Directory -Path "archive/customer_specific_reports" -Force
New-Item -ItemType Directory -Path "archive/utilities" -Force
New-Item -ItemType Directory -Path "archive/analysis_reports" -Force

# Move bug/ICM analysis scripts
$bugAnalysisFiles = @(
    "analyze_bug_linkage.py",
    "analyze_by_design_icms.py",
    "analyze_by_design_real_icms.py",
    "analyze_by_design_report.py",
    "analyze_icm_owners.py",
    "analyze_ic_mcs_bugs_from_icm.py",
    "analyze_ic_mcs_tenants_bugs.py",
    "analyze_ic_risk_report.py",
    "comprehensive_icm_bug_analysis.py",
    "parse_icm_bug_mentions.py",
    "extract_bugs_for_fetch.py",
    "extract_icm_from_ado_bugs.py",
    "extract_icm_ids_for_ado.py",
    "fetch_icm_hyperlinks.py",
    "process_ado_search_results.py",
    "process_ic_filtered.py"
)
$bugAnalysisFiles | ForEach-Object { Move-Item $_ -Destination "archive/one_off_analyses/bug_icm_analysis/" -ErrorAction SilentlyContinue }

# Move validation scripts
$validationFiles = @(
    "validate_90day_threshold.py",
    "validate_bug_summary.py",
    "validate_critical_table.py",
    "validate_final_report.py",
    "validate_unassigned_flag.py",
    "final_validation.py"
)
$validationFiles | ForEach-Object { Move-Item $_ -Destination "archive/one_off_analyses/validation/" -ErrorAction SilentlyContinue }

# Move data checking scripts
$dataCheckFiles = @(
    "check_active_unassigned.py",
    "check_bug_data.py",
    "check_icm_data.py",
    "check_scim_cases.py",
    "filter_scim_cases.py"
)
$dataCheckFiles | ForEach-Object { Move-Item $_ -Destination "archive/one_off_analyses/data_checking/" -ErrorAction SilentlyContinue }

# Move customer report generators
$customerReports = @(
    "generate_cibc_report.py",
    "generate_ge_report.py",
    "generate_santander_zurich_report.py",
    "show_barclays_details.py"
)
$customerReports | ForEach-Object { Move-Item $_ -Destination "archive/customer_specific_reports/" -ErrorAction SilentlyContinue }

# Move mapping scripts
$mappingFiles = @(
    "map_ado_bugs_to_ic_mcs.py",
    "map_ic_mcs_bugs_to_customers.py",
    "match_bugs_to_customers.py",
    "match_bugs_to_customers_final.py",
    "final_bug_linkage_analysis.py"
)
$mappingFiles | ForEach-Object { Move-Item $_ -Destination "archive/one_off_analyses/mapping/" -ErrorAction SilentlyContinue }

# Move utilities
$utilityFiles = @(
    "config_email_credentials.py",
    "convert_timeline_to_pptx.py",
    "create_icm_owner_query.py",
    "display_bug_matches_table.py",
    "fix_ic_csv.py",
    "find_unassigned_case.py",
    "SOLUTION_STEPS.py"
)
$utilityFiles | ForEach-Object { Move-Item $_ -Destination "archive/utilities/" -ErrorAction SilentlyContinue }

# Move analysis reports
$analysisReports = @(
    "by_design_analysis_real_data.md",
    "by_design_analysis_report.md",
    "COMPREHENSIVE_BUG_LINKAGE_REPORT.md",
    "GEMBA_ANALYSIS_2512120040008759_Desjardins.md",
    "INCIDENT_TIMELINE_2512120040008759_Desjardins.md",
    "INCIDENT_TIMELINE_2512120040008759_Desjardins_Full.md",
    "IC_REPORT_UPDATES_2026-02-09.md"
)
$analysisReports | ForEach-Object { Move-Item $_ -Destination "archive/analysis_reports/" -ErrorAction SilentlyContinue }
```

### Step 3: Organize Documentation
```powershell
# Create workspace docs folder
New-Item -ItemType Directory -Path "docs/project/workspace" -Force
New-Item -ItemType Directory -Path "docs/reference" -Force

# Move workspace documentation
$workspaceDocs = @(
    "CLEANUP_PLAN.md",
    "CLEANUP_QUICK_REFERENCE.md",
    "DOCUMENTATION_MAP.md",
    "OPTIMIZATION_GUIDE.md",
    "WHATS_NEW.md",
    "WORKSPACE_ORGANIZATION.md",
    "WORKSPACE_REVIEW_SUMMARY.md"
)
$workspaceDocs | ForEach-Object { Move-Item $_ -Destination "docs/project/workspace/" -ErrorAction SilentlyContinue }

# Move reference materials
Move-Item "DSCGP Squad Map.csv" -Destination "docs/reference/" -ErrorAction SilentlyContinue
Move-Item "icm_by_design_analysis_with_customers.xlsx" -Destination "archive/" -ErrorAction SilentlyContinue
Move-Item "Desjardins_Incident_Timeline.pptx" -Destination "archive/" -ErrorAction SilentlyContinue
```

### Step 4: Clean Up Temp Files
```powershell
# Remove temp data files (already gitignored)
Remove-Item "export (9).csv" -ErrorAction SilentlyContinue

# Remove Copilot scratch workspace
Remove-Item "Copilot" -Recurse -Force -ErrorAction SilentlyContinue

# Create .gitkeep files for empty directories
"" | Out-File "data/.gitkeep"
"" | Out-File "output/.gitkeep"
```

### Step 5: Update Documentation Links
```powershell
# Update links in README.md, INDEX.md, etc. to point to new locations
# This step requires manual review of:
# - README.md
# - INDEX.md
# - TODO.md (update paths to archived scripts)
```

### Step 6: Verify Structure
```powershell
# List root directory to verify clean structure
Get-ChildItem "c:\Users\carterryan\OneDrive - Microsoft\PHEPy" -File | Select-Object Name

# Verify essential folders exist
$essentialFolders = @(
    "agent_memory",
    "sub_agents",
    "docs",
    "grounding_docs",
    "purview_analysis",
    "tsg_system",
    "risk_reports",
    "data",
    "output"
)
$essentialFolders | ForEach-Object { 
    if (Test-Path $_) { 
        Write-Host "✅ $_" -ForegroundColor Green 
    } else { 
        Write-Host "❌ $_ MISSING" -ForegroundColor Red 
    }
}
```

---

## 🚀 Phase 5: Foundry Deployment Preparation

### Pre-Deployment Checklist

#### Security & Compliance
- [ ] Verify no PII in any file (customer names, emails, tenant IDs)
- [ ] Verify no credentials or API keys
- [ ] Verify .gitignore covers all sensitive files
- [ ] Review all markdown files for sensitive content
- [ ] Ensure agent_memory/memory.db is in .gitignore

#### Documentation
- [ ] Update README.md with Foundry deployment instructions
- [ ] Verify all links work after reorganization
- [ ] Ensure GETTING_STARTED.md is clear and concise
- [ ] Verify CAPABILITY_MATRIX.md lists all features
- [ ] Review all sub-agent AGENT_INSTRUCTIONS.md files

#### Configuration
- [ ] Verify mcp.json has correct server configurations
- [ ] Verify requirements.txt lists all dependencies
- [ ] Test agent_memory bootstrap.py works
- [ ] Verify sub-agent folder structure is complete

#### Testing (if possible before deployment)
- [ ] Test agent can read sub-agent instructions
- [ ] Test MCP server connections
- [ ] Test agent memory system initialization
- [ ] Verify grounding docs are accessible

### Foundry Deployment Package Structure

```
PHEPy-Agent-v1.0/
├── README.md                    # Quick start for Foundry users
├── INDEX.md                     # Navigation
├── mcp.json                     # MCP configuration
├── requirements.txt             # Dependencies
├── .gitignore                   # Security
├── agent_memory/                # Memory system
├── sub_agents/                  # 8 sub agent systems
├── docs/                        # Documentation
├── grounding_docs/              # Domain knowledge
├── purview_analysis/            # Analysis framework
├── tsg_system/                  # TSG system
├── risk_reports/templates/      # Templates only
└── [Core helper scripts if needed]
```

---

## 📊 Expected Outcomes

### Before Cleanup
```
📂 PHEPy (Original)
├── 202 Python files
├── 50+ root scripts
├── 30+ root markdown files
├── Mixed organization
└── ~500+ MB with data files
```

### After Cleanup
```
📂 PHEPy (Foundry-Ready)
├── ~50 essential Python files
├── 10 root configuration/documentation files
├── Organized folder structure
├── Clear agent architecture
└── ~50 MB without data files
```

### Benefits
- ✅ **80% reduction** in file clutter
- ✅ **Clear agent structure** for Foundry
- ✅ **Security compliant** (no PII/credentials)
- ✅ **Easy to understand** and extend
- ✅ **Production ready** for deployment

---

## 🏁 Success Criteria

### Must Have (Blocking)
- ✅ No PII, credentials, or sensitive data
- ✅ Clean root directory (< 15 files)
- ✅ All 8 sub-agents have AGENT_INSTRUCTIONS.md
- ✅ MCP configuration validated
- ✅ Documentation updated with new paths
- ✅ .gitignore covers all sensitive files

### Should Have (Important)
- ✅ Agent memory system tested
- ✅ All links in documentation work
- ✅ Grounding docs organized
- ✅ Templates separated from generated reports
- ✅ Archive folder excluded from deployment

### Nice to Have (Optional)
- ✅ Continuous improvement tracker works
- ✅ Risk report scripts consolidated
- ✅ Version tagging for deployment
- ✅ Deployment automation script

---

## 📝 Notes

### What NOT to Include in Foundry Deployment
- ❌ `archive/` folder - already archived old scripts
- ❌ `.venv/` - virtual environment
- ❌ `__pycache__/` - Python cache
- ❌ `Copilot/` - scratch workspace
- ❌ Data files (*.csv, *.json) - gitignored
- ❌ Generated reports (*.htm) - gitignored
- ❌ One-off analysis scripts - moved to archive
- ❌ Customer-specific reports - moved to archive
- ❌ Agent memory database (memory.db) - user-specific

### What Makes This Agent Valuable for Foundry
- ✅ Multi-agent orchestration architecture
- ✅ 5 MCP server integrations (ICM, ADO, Kusto, DFM, SharePoint)
- ✅ 8 specialized sub-agents with detailed instructions
- ✅ Persistent memory system
- ✅ Comprehensive documentation
- ✅ Query templates and workflows
- ✅ Grounding documents for domain knowledge
- ✅ TSG and analysis frameworks

---

**Ready for Implementation:** Yes  
**Estimated Time:** 2-3 hours  
**Risk Level:** Low (backup created first)  
**Reversible:** Yes (backup available)
