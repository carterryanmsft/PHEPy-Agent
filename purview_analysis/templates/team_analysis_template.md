# [Team Name] ICM Analysis Report

**Analysis Date**: [YYYY-MM-DD]  
**Analyst**: [Your Name]  
**Time Period**: [Start Date] to [End Date] (X months)  
**Team**: PURVIEW\[TeamName]

---

## 📊 Executive Summary

### Analysis Scope
- **Total Incidents Analyzed**: [XXX]
- **"By Design" Incidents**: [XXX] ([X]%)
- **DCR Requests**: [XXX] ([X]%)
- **Both (By Design + DCR)**: [XXX] ([X]%)
- **Unique Customers Affected**: [XXX]
- **Date Range**: [Start] - [End]

### Key Findings
1. **[Theme 1]**: [Brief one-sentence description of primary issue]
2. **[Theme 2]**: [Brief one-sentence description]
3. **[Theme 3]**: [Brief one-sentence description]
4. **[Theme 4]**: [Brief one-sentence description]
5. **[Theme 5]**: [Brief one-sentence description]

### Critical Recommendations (P0)
1. 🔴 **[Action Item]**: [What needs to be done]
2. 🔴 **[Action Item]**: [What needs to be done]
3. 🔴 **[Action Item]**: [What needs to be done]

### Success Metrics
- **Target Incident Reduction**: [X]% decrease in By Design incidents within [X] months
- **Documentation Improvement**: [X]% increase in self-service resolution
- **Feature Adoption**: [X]% of customers using new workaround/feature
- **Customer Satisfaction**: Improve CSAT from [X] to [X]

---

## 🎯 Theme Deep-Dives

### Theme 1: [Theme Name]

**Priority**: 🔴 P0 / 🟡 P1 / 🟠 P2 / 🟢 P3

**Customer Pain Point**:
[Describe what customers are trying to do and what's preventing them. Use customer language.]

**Incident Volume**:
- Total Incidents: [XXX]
- By Design: [XXX]
- DCR: [XXX]
- Unique Customers: [XX]
- Date Range: [First] - [Last]

**Example Incidents**:
1. **IcM [IncidentID]**: "[Incident Title]"
   - Customer Impact: [Description]
   - Current Resolution: [What was told to customer]
   
2. **IcM [IncidentID]**: "[Incident Title]"
   - Customer Impact: [Description]
   - Current Resolution: [What was told to customer]

3. **IcM [IncidentID]**: "[Incident Title]"
   - Customer Impact: [Description]
   - Current Resolution: [What was told to customer]

**Root Cause Analysis**:
[Explain WHY customers are hitting this issue. Is it a feature gap? Unclear docs? Unexpected behavior?]

**Improvement Recommendations**:

#### 📚 Documentation
- **Issue**: [What's missing or unclear in current docs]
- **Action**: [Specific doc improvement needed]
- **Priority**: [P0/P1/P2/P3]
- **Owner**: [Team/Individual]
- **ETA**: [Timeline]

#### 🔧 Product
- **Issue**: [Feature gap or product limitation]
- **Action**: [Feature request or bug fix needed]
- **Priority**: [P0/P1/P2/P3]
- **Owner**: [Team/Individual]
- **ETA**: [Timeline]

#### 🎨 UX
- **Issue**: [Confusing interface or workflow]
- **Action**: [UX improvement needed]
- **Priority**: [P0/P1/P2/P3]
- **Owner**: [Team/Individual]
- **ETA**: [Timeline]

---

### Theme 2: [Theme Name]

**Priority**: 🔴 P0 / 🟡 P1 / 🟠 P2 / 🟢 P3

**Customer Pain Point**:
[Repeat structure from Theme 1]

[Continue for all themes...]

---

## 📋 Actionable Recommendations Summary

### Documentation Improvements (Priority Order)

| Priority | Action Item | Estimated Effort | Owner | Status |
|----------|-------------|------------------|-------|--------|
| 🔴 P0    | [Action]    | [X days/hours]   | [Team]| Not Started |
| 🔴 P0    | [Action]    | [X days/hours]   | [Team]| Not Started |
| 🟡 P1    | [Action]    | [X days/hours]   | [Team]| Not Started |
| 🟠 P2    | [Action]    | [X days/hours]   | [Team]| Not Started |

### Product Feature Requests (Priority Order)

| Priority | Feature Request | Engineering Effort | Owner | Roadmap Status |
|----------|----------------|-------------------|-------|----------------|
| 🔴 P0    | [Feature]      | [X sprints]       | [PM]  | Not Planned    |
| 🟡 P1    | [Feature]      | [X sprints]       | [PM]  | Under Review   |
| 🟠 P2    | [Feature]      | [X sprints]       | [PM]  | Backlog        |

### UX Enhancements (Priority Order)

| Priority | UX Change | Design Effort | Owner | Status |
|----------|-----------|--------------|-------|--------|
| 🔴 P0    | [Change]  | [X days]     | [UX]  | Not Started |
| 🟡 P1    | [Change]  | [X days]     | [UX]  | Not Started |

---

## 📈 Success Metrics & Tracking

### Baseline Metrics (Current State)
- **Incident Volume**: [XXX] incidents/month average
- **"By Design" Rate**: [X]%
- **DCR Rate**: [X]%
- **Customer Escalations**: [XX] per month
- **Documentation Page Views**: [XXX] views/month
- **Self-Service Resolution**: [X]%

### Target Metrics (6 Months)
- **Incident Volume**: Reduce to [XXX] incidents/month ([X]% reduction)
- **"By Design" Rate**: Reduce to [X]% ([X]% improvement)
- **DCR Rate**: [X]% (feature requests addressed)
- **Customer Escalations**: Reduce to [XX] per month
- **Documentation Page Views**: Increase to [XXX] views/month
- **Self-Service Resolution**: Increase to [X]%

### Tracking Plan
1. **Monthly Reviews**: Re-run analysis queries to track incident trends
2. **Documentation Analytics**: Monitor Learn.microsoft.com page views and feedback
3. **Feature Adoption**: Track usage telemetry for new features
4. **Customer Feedback**: Quarterly CSAT surveys for affected customers
5. **ICM Trend Analysis**: Compare incident volume month-over-month

---

## 🔍 Methodology

### Data Sources
- **Kusto Cluster**: https://icmcluster.kusto.windows.net/IcmDataWarehouse
- **Query Used**: [Link to .kql file or paste query]
- **ICM Portal**: https://portal.microsofticm.com
- **Time Range**: [Start Date] - [End Date] ([X] days)

### Analysis Process
1. **Incident Retrieval**: Queried IcmDataWarehouse.Incidents table for team-specific incidents
2. **Filtering**: Applied "By Design" OR "DCR in title" filter
3. **Pattern Identification**: Grouped incidents by title keywords
4. **Theme Extraction**: Identified [X] major themes from [XXX] unique titles
5. **Sample Analysis**: Retrieved full context for top [XX] incidents
6. **Impact Assessment**: Evaluated customer impact, frequency, severity
7. **Recommendation Development**: Categorized improvements (Docs/Product/UX)

### Classification Framework
- **P0 (Critical)**: >50 incidents, blocks customers, security/compliance impact
- **P1 (High)**: 20-50 incidents, significant pain, workaround exists
- **P2 (Medium)**: 5-20 incidents, quality-of-life improvement
- **P3 (Low)**: <5 incidents, nice-to-have enhancement

---

## 📎 Appendices

### Appendix A: Complete Incident List
[Attach CSV/Excel file with full incident details]

**Filename**: `[TeamName]_incidents_[YYYY-MM-DD].csv`

**Columns**:
- IncidentId
- Title
- CreateDate
- HowFixed
- Severity
- Status
- CustomerName
- Description (truncated)

### Appendix B: Query Used
```kusto
[Paste the complete Kusto query used for this analysis]
```

### Appendix C: Related Resources
- **Team Wiki**: [Link to internal team wiki]
- **Product Documentation**: [Link to Learn.microsoft.com docs]
- **Feature Backlog**: [Link to ADO/GitHub backlog]
- **Previous Analyses**: [Links to prior reports]

### Appendix D: Contact Information
- **Report Owner**: [Name] - [Email]
- **Team PM**: [Name] - [Email]
- **Engineering Lead**: [Name] - [Email]
- **Documentation Contact**: [Name] - [Email]

---

## 🔄 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| [Date] | 1.0 | Initial analysis | [Name] |
| [Date] | 1.1 | Updated metrics | [Name] |

---

**Next Review Date**: [YYYY-MM-DD]  
**Report Status**: Draft / In Review / Final  
**Approvals Needed**: PM, Engineering Lead, Documentation Lead
