# PHEPy Workspace - Optimized Structure

**Optimization Date**: February 4, 2026  
**Status**: ✅ Cleaned and Organized

---

## 📁 Folder Organization

### Root Level (Clean)
```
PHEPy/
├── INDEX.md                    # Main navigation/entry point
├── README.md                   # Workspace overview
├── TODO.md                     # Task tracking
├── mcp.json                    # MCP server configuration
└── (Folders organized below)
```

---

## 📚 Documentation (`docs/`)

### `docs/project/` - Project Documentation
- **AGENT_INSTRUCTIONS.md** - Agent behavior guidelines
- **ARCHITECTURE_DIAGRAM.md** - System architecture
- **COMPLETION_SUMMARY.md** - Project milestones
- **EXECUTIVE_BRIEFING.md** - Leadership summary
- **FOLDER_STRUCTURE.md** - Workspace layout
- **PROJECT_SUMMARY.md** - Project overview
- **QUICK_START.md** - Getting started guide

**Total**: 7 documentation files (moved from root for cleanliness)

---

## 🔍 Purview Analysis System (`purview_analysis/`)

**Purpose**: ICM incident analysis framework for Purview teams

### Structure:
```
purview_analysis/
├── INDEX.md                    # Navigation hub
├── README.md                   # Master instructions
├── SYSTEM_SUMMARY.md           # Complete overview
├── WORKFLOW_GUIDE.md           # Step-by-step guide
│
├── queries/                    # 14 Kusto query templates
│   ├── all_teams_summary.kql
│   ├── team_template.kql
│   ├── by_design_analysis.kql
│   ├── dcr_analysis.kql
│   └── [10 team-specific].kql
│
├── templates/                  # 3 report templates
│   ├── team_analysis_template.md
│   ├── improvement_tracker.md
│   └── executive_summary_template.md
│
├── reports/                    # Generated analysis reports
├── team_analyses/              # Completed analyses
└── data/                       # Raw data exports
```

**Total**: 21 files - Complete, production-ready system

---

## 📊 Risk Reports System (`risk_reports/`)

**Purpose**: IC/MCS case risk assessment and reporting

### Optimized Structure:

#### `scripts/` - Automation Scripts
**Python Scripts**:
- `ic_mcs_risk_report_generator.py` - Main report generator
- `generate_production_report.py` - Production report automation
- `generate_production_report_auto.py` - Auto-generation
- `generate_production_report_quick.py` - Quick reports
- `generate_production_report_from_json.ps1` - JSON-based
- `auto_report.py` - Automated reporting
- `generate_report_auto.py` - Report automation
- `run_full_report.py` - Full report runner
- `save_kusto_data.py` - Kusto data saver
- `save_kusto_result.py` - Result saver
- `save_query_result.py` - Query result handler
- `write_kusto_data.py` - Data writer
- `prepare_csv_writer.py` - CSV preparation
- `kusto_to_csv_and_report.py` - Combined processor
- `convert_kusto_to_csv.py` - Format converter
- `convert_results.py` - Result converter

**PowerShell Scripts**:
- `generate_full_report.ps1` - Full report generation
- `generate_production_report.ps1` - Production automation
- `Run-ProductionReport.ps1` - Report runner
- `convert_to_csv.ps1` - CSV converter

**Total**: ~20 scripts (organized from root)

#### `data/` - Data Files
- `production_cases_131.json` - Current production cases
- `production_cases_131_sample.json` - Sample data
- `production_cases_131_temp.json` - Temporary data
- `production_cases.json` - Production cases
- `production_cases_sample.csv` - CSV sample
- `production_full_cases.csv` - Full case list
- `CaseRiskReport - 2026-02-03.csv` - Latest risk report
- `icm.csv` - ICM data
- `test_cases.csv` - Test data
- `test_output_cases.csv` - Test output
- `sample_risk_data.csv` - Sample risk data

**Total**: ~12 data files (CSV/JSON)

#### `output/` - Production Reports
- `IC_MCS_Production_Report_131.htm` - Latest production (current)
- `IC_MCS_Production_Report.htm` - Production report
- `IC_MCS_Production_Risk_Report.htm` - Risk assessment
- `IC_MCS_Report_ActiveFirst.htm` - Active-first view
- `IC_MCS_Risk_Report.htm` - Risk summary

**Total**: 5 current production reports

#### `archive/` - Historical Reports
- `IC_MCS_Test_Report.htm` - Test reports
- `IC_MCS_Test_Report_Debug.htm` - Debug versions
- `IC_MCS_Test_Report_Debug2.htm`
- `IC_MCS_Test_Report_Debug3.htm`
- `IC_MCS_Test_Report_FINAL.htm` - Final test
- `IC_MCS_Test_Report_Fixed.htm` - Fixed version
- `IC_MCS_Test_Report_v2.htm` - Version 2
- `IC_MCS_Final_Test_Report.htm`
- `IC_MCS_Final_Test_Report_v2.htm`
- `IC_MCS_Enhanced_Report.htm`
- `test_report_final.html`

**Total**: ~11 archived test/debug reports

#### Existing Folders (Unchanged)
- `queries/` - Kusto query definitions
- `templates/` - Report templates
- `documentation/` - System documentation

---

## 📖 Reference Documents (`grounding_docs/`)

### Organized by Topic:

#### `contacts_access/`
- CLE and PHE contact information
- IC and MCS team rosters (CSV)

#### `continuous_improvement/`
- Continuous improvement methodologies
- Gemba process documentation
- Problem-solving frameworks
- Value stream & Kaizen guides
- README with process overview

#### `customer_tenant_data/`
- Customer-specific information (placeholder)

#### `phe_program_operations/`
- CEM Product Engineer priorities
- Customer Reliability Engineering grounding
- FY26 PHEP Core Priorities
- Kusto queries reference
- Operational rhythms & governance
- SHI v2 (Support Health Index) documentation

#### `purview_product/`
- Purview product documentation (placeholder)

#### `support_escalation/`
- Escalation procedures (placeholder)

**Purpose**: Knowledge base for agent grounding and context

---

## 🤖 Sub-Agents (`sub_agents/`)

### Agent Definitions:
Each sub-agent has its own folder with instructions:
- `access_role_manager/` - Access & permissions management
- `contacts_escalation_finder/` - Contact lookup & escalation paths
- `escalation_manager/` - Escalation handling
- `gemba_analysis_ford_case_2505160040006784.md` - Case analysis example
- `kusto_expert/` - Kusto query assistance
- `program_onboarding_manager/` - Onboarding automation
- `purview_product_expert/` - Purview product knowledge
- `support_case_manager/` - Case management
- `tenant_health_monitor/` - Health monitoring
- `work_item_manager/` - Work item tracking

**Purpose**: Specialized agent capabilities for specific tasks

---

## 📝 Generated Content (`Copilot/Created/`)

### Analysis Reports:
- `Sensitivity_Labels_Analysis_Report.md` - Complete Sensitivity Labels analysis (717 incidents)
- `Purview_DCR_ByDesign_Analysis_Report.md` - Purview DCR/By Design analysis

**Purpose**: Copilot-generated analysis outputs and reports

---

## 🔧 Configuration Files

### Root Level:
- **mcp.json** - MCP server configuration
  - Defines available MCP servers
  - Connection settings
  - Authentication configuration

### Hidden Folders:
- `.vscode/` - VS Code workspace settings

---

## 📂 Other Folders

### `Custom Office Templates/`
- Custom Office document templates

### `OneNote Notebooks/`
- OneNote notebook shortcuts (.url files)
- The Coaching Habit notebooks
- Purview Care Team notes

### `tsg_system/`
- Troubleshooting guides system (details not listed)

---

## 🎯 Optimization Benefits

### Before Cleanup:
- ❌ 7 documentation files cluttering root
- ❌ 20+ scripts scattered in risk_reports root
- ❌ 12 data files mixed with reports
- ❌ 11 old test reports mixed with production
- ❌ Hard to find current vs. archived reports

### After Optimization:
- ✅ Clean root with only 4 essential files
- ✅ Scripts organized in `risk_reports/scripts/`
- ✅ Data files in `risk_reports/data/`
- ✅ Production reports in `risk_reports/output/`
- ✅ Old reports archived in `risk_reports/archive/`
- ✅ Project docs in `docs/project/`
- ✅ Clear separation of concerns

---

## 🔍 Quick Navigation

### Need to...

**→ View current production report**
```
risk_reports/output/IC_MCS_Production_Report_131.htm
```

**→ Run report generation**
```
risk_reports/scripts/generate_production_report.py
```

**→ Analyze Purview ICMs**
```
purview_analysis/WORKFLOW_GUIDE.md
```

**→ Find project documentation**
```
docs/project/
```

**→ Access grounding documents**
```
grounding_docs/[topic]/
```

**→ Work with sub-agents**
```
sub_agents/[agent_name]/
```

---

## 📊 File Statistics

| Category | Count | Location |
|----------|-------|----------|
| Root files | 4 | INDEX.md, README.md, TODO.md, mcp.json |
| Project docs | 7 | docs/project/ |
| Purview analysis | 21 | purview_analysis/ |
| Risk report scripts | 20 | risk_reports/scripts/ |
| Risk report data | 12 | risk_reports/data/ |
| Production reports | 5 | risk_reports/output/ |
| Archived reports | 11 | risk_reports/archive/ |
| Grounding docs | ~30 | grounding_docs/ |
| Sub-agents | 10 | sub_agents/ |
| Generated reports | 2 | Copilot/Created/ |

**Total Files**: ~122 organized files

---

## ✅ Maintenance Guidelines

### Keep Root Clean:
- Only INDEX.md, README.md, TODO.md, mcp.json
- All other files go in organized folders

### Risk Reports:
- **New scripts** → `scripts/`
- **New data** → `data/`
- **New production reports** → `output/`
- **Old reports** → `archive/` (after 30 days)

### Documentation:
- **Project docs** → `docs/project/`
- **Technical docs** → relevant system folder

### Generated Content:
- **Copilot outputs** → `Copilot/Created/`
- **Analysis reports** → `purview_analysis/reports/` or `team_analyses/`

---

## 🎉 Optimization Complete!

**Status**: ✅ Workspace fully optimized and organized  
**Benefit**: Easy navigation, clear structure, maintainable  
**Next**: Follow folder conventions for new files

---

**Last Updated**: February 4, 2026  
**Maintained By**: Product Health Engineering Team
