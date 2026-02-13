# 📋 Friday Night LQE - Complete Documentation Index

**Quick Navigation Guide for Friday Night Low Quality Escalation Analysis**

---

## 🚀 Getting Started

**New to Friday LQE?** Start here:

1. **[DELIVERABLE_SUMMARY.md](DELIVERABLE_SUMMARY.md)** ⭐ START HERE
   - Complete overview of what was built
   - Success criteria checklist
   - Production readiness status

2. **[FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md)** 🎯 QUICK REFERENCE
   - 3-step workflow
   - Command cheat sheet
   - Common troubleshooting

3. **[FRIDAY_WORKFLOW_VISUAL.md](FRIDAY_WORKFLOW_VISUAL.md)** 📊 VISUAL GUIDE
   - Flowchart of entire process
   - Data organization structure
   - Command reference

---

## 📚 Detailed Documentation

### Core Documentation
- **[FRIDAY_LQ_README.md](FRIDAY_LQ_README.md)** - Complete technical documentation
- **[FRIDAY_IMPLEMENTATION_SUMMARY.md](FRIDAY_IMPLEMENTATION_SUMMARY.md)** - Implementation details

### General LQE Agent
- **[LQ_ESCALATION_README.md](LQ_ESCALATION_README.md)** - Main LQE agent documentation
- **[lq_escalation_config.json](lq_escalation_config.json)** - Reviewer configuration

---

## 🔧 Code Files

### Python Scripts
| File | Purpose | When to Use |
|------|---------|-------------|
| **[run_friday_lq_analysis.py](run_friday_lq_analysis.py)** | Main Friday runner | Every Friday run |
| **[low_quality_escalation_agent.py](low_quality_escalation_agent.py)** | Core agent logic | Enhanced with region/feature methods |
| **[test_friday_analysis.py](test_friday_analysis.py)** | Test with sample data | Testing & validation |

### Query Files
| File | Purpose | When to Use |
|------|---------|-------------|
| **[queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql)** | Kusto query | Run in Kusto Explorer |

---

## 📂 Directory Structure

```
sub_agents/
├── 📄 Documentation (You Are Here!)
│   ├── DELIVERABLE_SUMMARY.md          ⭐ Overview & success criteria
│   ├── FRIDAY_QUICK_START.md           🎯 3-step quick guide
│   ├── FRIDAY_WORKFLOW_VISUAL.md       📊 Visual flowchart
│   ├── FRIDAY_LQ_README.md             📚 Complete documentation
│   ├── FRIDAY_IMPLEMENTATION_SUMMARY   🔧 Technical details
│   ├── FRIDAY_INDEX.md                 📋 This file
│   └── LQ_ESCALATION_README.md         📖 General LQE docs
│
├── 🐍 Python Scripts
│   ├── run_friday_lq_analysis.py       🚀 Main runner
│   ├── low_quality_escalation_agent.py 🤖 Core logic
│   └── test_friday_analysis.py         🧪 Test script
│
├── 📁 queries/
│   └── friday_lq_unassigned.kql        🔍 The query
│
├── 📁 data/
│   └── friday_lq_*.json                💾 Query results
│
└── 📁 friday_reports/
    ├── friday_lq_report_*.json         📊 JSON reports
    └── friday_lq_report_*.csv          📈 CSV exports
```

---

## 🎯 Use Case Guide

### I Want To...

#### Run Friday Analysis for First Time
1. Read: [DELIVERABLE_SUMMARY.md](DELIVERABLE_SUMMARY.md)
2. Follow: [FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md)
3. Execute: `python run_friday_lq_analysis.py`

#### Test Before Production
1. Run: `python test_friday_analysis.py`
2. Review: Generated reports in `friday_reports/`
3. Verify: Data organization is correct

#### Schedule Automatic Runs
1. Read: [FRIDAY_LQ_README.md](FRIDAY_LQ_README.md) - Scheduling section
2. Create: Windows Task Scheduler job
3. Test: Scheduled execution

#### Understand the Query
1. Open: [queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql)
2. Read: [FRIDAY_IMPLEMENTATION_SUMMARY.md](FRIDAY_IMPLEMENTATION_SUMMARY.md) - Query Logic section
3. Review: Filter criteria

#### Customize Region Mapping
1. Edit: [queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql)
2. Modify: `OriginRegion` case statement
3. Test: `python test_friday_analysis.py`

#### Customize Feature Areas
1. Edit: [queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql)
2. Modify: `FeatureAreaCategory` case statement
3. Test: `python test_friday_analysis.py`

#### Add/Remove Reviewers
1. Edit: [lq_escalation_config.json](lq_escalation_config.json)
2. Update: `reviewers` array
3. No restart needed

#### Troubleshoot Issues
1. Check: [FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md) - Troubleshooting section
2. Review: Console output for errors
3. Test: With sample data first

#### Understand Report Structure
1. Read: [FRIDAY_IMPLEMENTATION_SUMMARY.md](FRIDAY_IMPLEMENTATION_SUMMARY.md) - Report Output section
2. View: Sample report in `friday_reports/`
3. Reference: [FRIDAY_WORKFLOW_VISUAL.md](FRIDAY_WORKFLOW_VISUAL.md)

---

## 📊 Quick Command Reference

```powershell
# Navigate to directory
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"

# Show query (first time)
python run_friday_lq_analysis.py

# Run with data file
python run_friday_lq_analysis.py --data-file data/friday_lq_20260207.json

# Test with sample data
python test_friday_analysis.py

# View latest report
code friday_reports/friday_lq_report_*.json

# Open CSV
start friday_reports/friday_lq_report_*.csv
```

---

## 🎓 Learning Path

### Level 1: Beginner
1. Read [DELIVERABLE_SUMMARY.md](DELIVERABLE_SUMMARY.md)
2. Follow [FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md)
3. Run `python test_friday_analysis.py`

### Level 2: Regular User
1. Read [FRIDAY_LQ_README.md](FRIDAY_LQ_README.md)
2. Review [queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql)
3. Run weekly: `python run_friday_lq_analysis.py --data-file ...`

### Level 3: Advanced User
1. Read [FRIDAY_IMPLEMENTATION_SUMMARY.md](FRIDAY_IMPLEMENTATION_SUMMARY.md)
2. Review [low_quality_escalation_agent.py](low_quality_escalation_agent.py)
3. Customize queries and mappings
4. Set up automation

---

## 🔍 Document Quick Comparison

| Document | Length | Detail Level | Best For |
|----------|--------|--------------|----------|
| DELIVERABLE_SUMMARY | Long | High | Understanding scope & deliverables |
| FRIDAY_QUICK_START | Short | Low | Quick daily reference |
| FRIDAY_WORKFLOW_VISUAL | Medium | Visual | Understanding process flow |
| FRIDAY_LQ_README | Long | High | Complete how-to guide |
| FRIDAY_IMPLEMENTATION_SUMMARY | Long | Technical | Understanding code & architecture |

---

## 📧 Contact & Support

**Created By**: Carter Ryan  
**Created On**: February 5, 2026  
**Status**: ✅ Production Ready

**For Issues**:
1. Check [FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md) troubleshooting
2. Review error messages in console output
3. Test with sample data: `python test_friday_analysis.py`

---

## 🎉 Quick Win Checklist

- [ ] Read [DELIVERABLE_SUMMARY.md](DELIVERABLE_SUMMARY.md)
- [ ] Run `python test_friday_analysis.py`
- [ ] Review generated test reports
- [ ] Execute Kusto query for real data
- [ ] Run with real data file
- [ ] Review output report structure
- [ ] Set up Task Scheduler (optional)
- [ ] Distribute first report to reviewers

---

## 📚 Related Systems

This Friday LQE workflow is part of the larger **PHEPy Sub-Agent System**:

- **Main README**: [sub_agents/README.md](README.md)
- **LQE Agent**: [low_quality_escalation_agent.py](low_quality_escalation_agent.py)
- **Kusto Expert (Jacques)**: [kusto_expert/](kusto_expert/)
- **Escalation Manager**: [escalation_manager/](escalation_manager/)

---

## 🆕 What's New

**February 5, 2026** - Initial Release
- ✅ Friday night workflow created
- ✅ Region & feature area organization
- ✅ Unassigned escalation focus
- ✅ Comprehensive documentation
- ✅ Test script with sample data
- ✅ Production ready

---

## 🔮 Future Enhancements

Potential improvements for consideration:

- 📧 Automated email distribution
- 📊 Week-over-week trend analysis
- 🎨 HTML report generation
- 🔔 Slack/Teams notifications
- 📈 Dashboard integration
- 🤖 Auto-reviewer assignment suggestions
- 📉 Quality improvement tracking

---

**End of Index**

*Last Updated: February 5, 2026*  
*Version: 1.0*  
*Status: Complete & Production Ready* ✅
