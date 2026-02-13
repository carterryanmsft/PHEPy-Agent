# Purview Product Expert Integration Guide

## Overview
The ICM Agent now features a multi-agent workflow that prepares analysis for the **Purview Product Expert** to provide deep reasoning on by-design incidents.

## Workflow Stages

### Stage 1: Kusto Query ✅ COMPLETE
- Queries ICM DataWarehouse for by-design incidents
- Retrieves incident patterns, counts, customer impact
- Status: **Working**

### Stage 2: ICM Deep Insights ✅ COMPLETE  
- Analyzes sample incidents for common patterns
- Structures data for detailed MCP queries
- Prepares customer impact and resolution insights
- Status: **Working** (structure ready for MCP tool integration)

### Stage 3: Product Expert Preparation ✅ COMPLETE
- Generates targeted questions for product team
- Categorizes preliminary recommendations (Doc/UI/Product)
- Creates expert analysis request with full context
- Status: **Working**

### Stage 4: Expert Invocation ⏳ READY TO IMPLEMENT
- Invokes Purview Product Expert agent
- Receives reasoned analysis back
- Integrates expert recommendations into report
- Status: **Structure complete, needs runSubagent call**

---

## Current Implementation

### What's Working
✅ **Analysis Report Generated**: [icm_analysis_20260205_142253.html](reports/icm_analysis_20260205_142253.html)
✅ **Expert Request Prepared**: Structured prompt with all context
✅ **Questions Generated**: Specific asks for product team
✅ **Recommendations Categorized**: Doc/UI-UX/Product buckets
✅ **Report Section Added**: "Product Expert Analysis" with expandable request

### What's in the Report
The generated report now includes:
1. **Product Expert Analysis Section** 🤖
   - Status indicator (⏳ Expert invocation required)
   - Key questions for product team
   - Expandable expert analysis request
   - Preliminary recommendations by category

2. **Expert Request Details** (click to expand in report)
   - Full Purview Product Expert role context
   - Detailed theme information
   - Specific questions to address
   - Expected output format

---

## How to Complete the Integration

### Option 1: Automatic Invocation (Recommended)
Update `_invoke_purview_product_expert()` method to use `runSubagent`:

```python
def _invoke_purview_product_expert(self, expert_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Invoke the Purview Product Expert agent for deep reasoning."""
    
    # Use runSubagent to invoke the expert
    from your_agent_framework import runSubagent
    
    expert_response = runSubagent(
        agent="purview_product_expert",
        prompt=expert_analysis['expert_prompt'],
        context={
            'themes': expert_analysis['themes'],
            'questions': expert_analysis['questions_for_expert']
        }
    )
    
    return {
        'expert_consulted': True,
        'analysis_complete': True,
        'documentation_recommendations': expert_response.get('doc_recs', []),
        'ui_ux_recommendations': expert_response.get('ui_recs', []),
        'product_recommendations': expert_response.get('product_recs', []),
        'priority_actions': expert_response.get('actions', [])
    }
```

### Option 2: Manual Invocation
1. Open the generated report
2. Expand "View Expert Analysis Request"
3. Copy the full request text
4. Invoke Purview Product Expert with: 
   ```
   Act as Purview Product Expert and [paste request]
   ```
5. Manually add expert response to report

### Option 3: External Integration
- Extract `expert_request` from the analysis JSON
- Send to external system (email, API, etc.)
- Human expert reviews and responds
- Response gets integrated into next report run

---

## Expert Request Structure

The prepared request includes:

### Context Section
- Purview Product Expert role definition (from AGENT_INSTRUCTIONS.md)
- Analysis request type: "By-Design Incidents Review"

### Analysis Details
- **Themes Identified**: Count and names
- **Customer Impact**: Total incidents and affected customers
- **Theme Breakdown**: For each theme:
  - Total impact (incident count)
  - Customers affected
  - Sample issue titles

### Questions for Expert
Generated dynamically based on theme volume:
- Is this truly by-design or a product gap?
- Can this be addressed through documentation/UI/product changes?
- What's the priority and feasibility?

### Expected Output
Requests expert to provide:
1. Assessment of whether issues are by-design or product gaps
2. Prioritized recommendations by impact and feasibility
3. Quick wins (doc/UI) vs. longer-term product changes
4. Specific actions for product team

---

## Report Viewing

### Opening the Report
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent"
start reports\icm_analysis_20260205_142253.html
```

### Report Sections
1. **Executive Summary**: Key metrics
2. **Themes**: Clustered incident patterns
3. **Top Issues**: High-volume documentation needs
4. **🤖 Product Expert Analysis**: 
   - Status indicator
   - Key questions
   - Expert request (expandable)
   - Preliminary recommendations
5. **Recommendations & Action Items**: Prioritized actions

---

## Example DLP Analysis Results

### Current Run Results
- **Total Incidents**: 9 by-design cases
- **Unique Issues**: 4 distinct patterns
- **Themes Identified**: 1 ("Issue / Policy / Applying")
- **Sample Issues**:
  - "Microsoft Purview: Issue with DLP policy not applying in real time"
  - "DLP Alert - Detection took a long time, alerts generated after many days"
  - "DLP Policy Tip is not visible in OWA"

### Expert Questions Generated
1. **Theme: Issue / Policy / Applying**
   - "Is 'Issue / Policy / Applying' a fundamental product limitation or can it be addressed?"
   - Context: 9 incidents across 0 customers
   - Suggested Analysis:
     - Review if truly by-design or product gap
     - Assess if documentation exists and is discoverable
     - Evaluate if UI/UX improvements could reduce confusion
     - Determine if this indicates missing feature customers expect

### Preliminary Recommendations
**📚 Documentation Improvements:**
- [High] Issue / Policy / Applying: Create comprehensive documentation
  - Reason: High incident volume (9) indicates knowledge gap

**🎨 UI/UX Enhancements:**
- [Medium] Issue / Policy / Applying: Review user experience flow
  - Reason: Recurring confusion suggests unintuitive design

---

## Next Steps

1. **Immediate**: Review generated report to validate analysis quality
2. **Short-term**: Choose integration approach (automatic/manual/external)
3. **Long-term**: Set up recurring runs with expert auto-invocation

### For Automatic Integration
- Implement runSubagent or equivalent agent invocation mechanism
- Update `_invoke_purview_product_expert()` method
- Test with small dataset first
- Validate expert responses are properly formatted

### For Production Use
- Schedule regular runs (weekly/monthly)
- Set up email delivery of reports
- Create dashboards tracking recommendations over time
- Link to ADO work items for tracking implementation

---

## File Locations

- **Main Agent**: `icm_agent.py`
- **Generated Reports**: `reports/icm_analysis_*.html`
- **Sample Data**: `data/dlp_by_design_results.json`
- **KQL Queries**: `queries/dlp_by_design_analysis.kql`
- **Theme Impact Queries**: `queries/theme_impacts/theme_*.kql`
- **Expert Instructions**: `../purview_product_expert/AGENT_INSTRUCTIONS.md`

---

## Questions?

- **How do I re-run the analysis?** `python run_dlp_report.py`
- **Where's the expert request?** Open the HTML report and expand the "View Expert Analysis Request" section
- **Can I customize the questions?** Yes, modify `_prepare_for_product_expert()` method
- **How do I add more themes?** Adjust theme clustering parameters in `generate_themes()` method

---

*Last Updated: February 5, 2026*
