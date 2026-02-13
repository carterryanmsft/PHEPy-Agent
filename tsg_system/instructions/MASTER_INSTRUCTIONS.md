# TSG System Master Instructions

## Purpose
This system automatically reviews support escalations, analyzes existing TSGs (Trouble Shooting Guides), identifies gaps, and recommends updates to ensure comprehensive coverage of common and critical issues.

## System Overview

### Core Capabilities
1. **Escalation Analysis**: Parse and analyze support cases to identify patterns, recurring issues, and resolution paths
2. **TSG Gap Detection**: Compare escalation patterns against existing TSG library to find coverage gaps
3. **Update Recommendations**: Suggest improvements to existing TSGs based on recent learnings
4. **Automated TSG Generation**: Create new TSGs from successful escalation resolutions
5. **Quality Assurance**: Validate TSG completeness, accuracy, and usability

---

## Workflow Process

### Phase 1: Data Collection
**Input Sources:**
- Support case data from Kusto queries
- ICM incidents and escalations
- Existing TSG repository
- Customer feedback and CSAT data

**Actions:**
1. Execute Kusto queries to extract recent escalations (last 30-90 days)
2. Filter for:
   - High-severity cases (Sev 1-2)
   - Cases with multiple ownership transfers (>3)
   - Cases with long resolution times (>7 days)
   - Recurring issue patterns (same product/error appearing >3x)
   - Cases with ICM escalations
3. Export data to `/escalations/` folder with timestamp

**Query Criteria:**
```kql
// Key filters for escalation analysis
- ProductName == "Microsoft Purview Compliance"
- ServiceRequestCurrentSeverity in ("1", "2", "A", "B")
- DaysToResolve > 7 OR OwnershipCount > 3
- Group by: DerivedProductName, ErrorCode, SymptomKeywords
```

### Phase 2: Escalation Pattern Analysis
**Objective:** Identify common themes and resolution patterns

**Process:**
1. **Cluster Analysis**:
   - Group cases by product area (e.g., DLP, eDiscovery, Audit, Retention)
   - Identify symptom patterns (error messages, behaviors)
   - Track resolution methods used

2. **Pattern Recognition**:
   - **Frequency**: How often does this issue occur? (>5 cases = high priority)
   - **Impact**: Average severity and customer impact (TPID, Program: IC/MCS)
   - **Complexity**: Average resolution time and ownership transfers
   - **Knowledge Gaps**: Cases requiring SME escalation or extended research

3. **Categorization**:
   - **Category A**: Critical recurring issues (high frequency + high severity)
   - **Category B**: Complex issues (low frequency + high resolution time)
   - **Category C**: Common quick-fix issues (high frequency + low complexity)
   - **Category D**: New/emerging issues (recent spike in cases)

**Output:** Pattern analysis report in `/gap_analysis/patterns_[date].md`

### Phase 3: TSG Coverage Assessment
**Objective:** Map escalation patterns to existing TSGs

**Process:**
1. **Inventory Existing TSGs**:
   - List all TSGs in `/existing_tsgs/`
   - Extract metadata: Title, Product Area, Symptoms, Resolution Steps, Last Updated
   - Create TSG index with searchable fields

2. **Gap Identification**:
   - For each escalation pattern, search TSG index for coverage
   - **Full Coverage**: TSG exists with complete resolution steps
   - **Partial Coverage**: TSG exists but missing recent learnings/steps
   - **No Coverage**: No TSG addresses this pattern
   - **Outdated**: TSG exists but references deprecated processes/tools

3. **Priority Scoring**:
   ```
   Gap Priority Score = (Frequency × 3) + (Avg_Severity × 2) + (Avg_Resolution_Days × 1)
   
   Priority Levels:
   - Critical: Score > 50, affects IC/MCS customers
   - High: Score 30-50, recurring issue
   - Medium: Score 15-30, moderate impact
   - Low: Score < 15, edge cases
   ```

**Output:** Gap analysis report in `/gap_analysis/gap_report_[date].md`

### Phase 4: Recommendation Generation
**Objective:** Create actionable TSG update recommendations

**Types of Recommendations:**

#### 4A: New TSG Creation
**Criteria:** No coverage exists for pattern with Priority Score > 20

**Recommendation Format:**
```markdown
## New TSG Recommendation: [Title]

**Priority:** Critical/High/Medium
**Product Area:** [e.g., DLP, eDiscovery]
**Pattern ID:** [Reference to escalation pattern]

**Justification:**
- Frequency: [X] cases in last [Y] days
- Average Severity: [Sev level]
- Average Resolution Time: [Days]
- Customer Impact: [IC/MCS programs, TPIDs]

**Proposed Content:**
1. Symptom Description: [Common error messages, behaviors]
2. Root Cause: [Technical explanation]
3. Diagnostic Steps: [How to confirm issue]
4. Resolution Steps: [Detailed walkthrough]
5. Prevention: [How to avoid issue]
6. Related Issues: [Links to similar TSGs]

**Source Cases:** [List of case numbers used for analysis]
```

#### 4B: TSG Update Recommendations
**Criteria:** Partial coverage exists but requires enhancement

**Recommendation Format:**
```markdown
## TSG Update: [Existing TSG Title]

**Current TSG:** [Path/Link to existing TSG]
**Last Updated:** [Date]
**Priority:** Critical/High/Medium

**Gap Identified:**
[Description of what's missing or outdated]

**Recommended Updates:**

### Section to Add/Modify: [Section name]
**Current Content:**
[Existing content or "Not present"]

**Recommended Content:**
[New/updated content with specific steps]

**Rationale:**
- Based on [X] recent cases
- New resolution method proven effective in [Y] days vs previous [Z] days
- Addresses edge case found in [specific cases]

**Source Cases:** [List of case numbers]
```

#### 4C: TSG Deprecation
**Criteria:** TSG addresses issue no longer occurring (0 cases in 6+ months)

**Recommendation Format:**
```markdown
## TSG Deprecation: [TSG Title]

**Current TSG:** [Path/Link]
**Reason:** No cases matching this pattern in past 6 months
**Action:** Archive to `/existing_tsgs/archived/` with deprecation note
```

### Phase 5: Quality Validation
**Objective:** Ensure recommendations are accurate and complete

**Validation Checklist:**
- [ ] Recommendation references at least 3 source cases (unless Sev 1)
- [ ] Resolution steps are clear and actionable
- [ ] Prerequisites and tools are listed
- [ ] Expected outcomes are defined
- [ ] Troubleshooting alternatives included
- [ ] Links to related documentation provided
- [ ] Reviewed by subject matter expert (if applicable)

**Output:** Validated recommendations in `/recommended_updates/recommendations_[date].md`

---

## Automation Guidelines

### Scheduled Runs
- **Weekly**: Quick scan for critical gaps (Sev 1-2, IC/MCS cases)
- **Bi-weekly**: Full analysis including pattern clustering
- **Monthly**: Comprehensive review including TSG deprecation check

### Trigger Conditions for Immediate Analysis
- ICM escalation created
- Sev 1 case open > 24 hours
- >5 cases with same error code within 7 days
- PHE/CLE requests analysis

### AI Agent Integration
This system can be operated by AI agents with the following permissions:
- **Read**: Access to case data, existing TSGs
- **Analyze**: Run pattern analysis and gap detection
- **Recommend**: Generate TSG recommendations
- **Create** (with approval): Generate new TSG drafts from templates

---

## Data Sources and Queries

### Primary Kusto Tables
- `GetSCIMIncidentV2` - Support case data
- `ICMIncidentV2` - ICM escalations
- `CaseTransferHistory` - Ownership and transfer data
- `CustomerSatisfactionData` - CSAT and feedback

### Key Query Patterns
See `/queries/` folder for:
- `escalation_patterns.kql` - Identify recurring issues
- `resolution_analysis.kql` - Analyze successful resolutions
- `tsg_coverage_check.kql` - Match cases to TSG topics
- `priority_scoring.kql` - Calculate gap priority scores

---

## Output Formats

### Gap Analysis Report Structure
```markdown
# TSG Gap Analysis Report - [Date]

## Executive Summary
- Total escalations analyzed: [X]
- TSGs reviewed: [Y]
- Gaps identified: [Z]
- Critical gaps: [A]
- Recommendations generated: [B]

## Critical Gaps (Immediate Action Required)
[Table with: Issue, Frequency, Severity, Customer Impact, Priority Score]

## High Priority Gaps
[Table format]

## TSG Update Recommendations
[Table with: TSG Title, Issue, Recommended Action]

## Detailed Analysis
[For each gap: Full details with source cases]

## Appendix
- Source query results
- Pattern clustering details
- TSG inventory snapshot
```

### Recommendation Tracking
Maintain `/gap_analysis/recommendation_tracker.csv`:
```csv
Recommendation_ID,Date_Created,Priority,Type,Status,Assigned_To,Date_Completed,TSG_Link
```

---

## Best Practices

### For TSG Creation
1. **Start with the symptom, not the solution** - Users need to find TSGs by what they observe
2. **Include real-world examples** - Use anonymized case details
3. **Provide diagnostic steps** - Help users confirm they have the right TSG
4. **Offer alternatives** - Include fallback options if primary resolution fails
5. **Link related content** - Connect to other TSGs, documentation, tools

### For Gap Analysis
1. **Use sufficient sample size** - Analyze at least 30 days of data, minimum 3 cases for pattern
2. **Consider customer impact** - Prioritize IC/MCS customers and high TPIDs
3. **Validate with SMEs** - Have product experts review complex recommendations
4. **Track outcomes** - Monitor if new/updated TSGs reduce case resolution time

### For Automation
1. **Version control** - Track all TSG changes with dates and reasons
2. **Approval workflows** - Require SME review for critical TSGs
3. **Feedback loops** - Collect engineer feedback on TSG usefulness
4. **Metrics tracking** - Measure TSG usage, effectiveness, and case deflection

---

## Metrics and Success Criteria

### Key Performance Indicators
- **Coverage Rate**: % of escalation patterns with adequate TSGs
- **Resolution Time Impact**: Avg days reduced after TSG implementation
- **Case Deflection**: Cases resolved at L1/L2 instead of escalation
- **TSG Usage**: View count and engineer feedback scores
- **Update Frequency**: TSGs updated within 30 days of gap identification

### Target Goals
- Coverage Rate: >85% for all patterns, 100% for Sev 1-2
- Resolution Time: 20% reduction for covered issues
- Critical Gap Response: New TSG within 7 days
- High Priority Gap Response: Update within 14 days

---

## Contact and Support

### System Owners
- **PHE Team**: Product Health Engineers for product-specific TSGs
- **CLE Team**: Customer-facing escalation patterns
- **Knowledge Management**: TSG repository maintenance

### Escalation Path
1. Automated system generates recommendations
2. PHE/CLE reviews and validates
3. SME approves content accuracy
4. Knowledge team publishes to TSG library
5. Metrics team tracks effectiveness

---

## Appendix: Common Pitfalls to Avoid

1. **Over-generalization**: Don't create TSGs too broad - be specific to symptoms
2. **Under-documentation**: Include all prerequisites, permissions, tools needed
3. **Stale content**: TSGs must be updated when product features change
4. **Missing context**: Always explain WHY a step is needed, not just WHAT to do
5. **No validation**: Test all steps before publishing
6. **Ignoring feedback**: Monitor TSG usage and update based on engineer input
7. **Analysis paralysis**: Better to have 80% solution published than 100% solution delayed

---

**Last Updated:** February 4, 2026
**Version:** 1.0
**Next Review:** March 4, 2026
