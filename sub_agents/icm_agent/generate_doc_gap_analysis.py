"""
Generate Documentation Gap Analysis for MIP/DLP

Reviews by-design themes and generates specific documentation gap
recommendations for Purview Product Expert evaluation.

Author: Carter Ryan  
Created: February 11, 2026
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def load_themes() -> Dict[str, Any]:
    """Load theme analysis results."""
    themes_file = Path(__file__).parent / "data" / "mip_dlp_themes.json"
    
    if not themes_file.exists():
        raise FileNotFoundError(
            f"Themes file not found: {themes_file}\n"
            "Please run: python analyze_mip_dlp_themes.py"
        )
    
    with open(themes_file, 'r') as f:
        return json.load(f)


def generate_expert_prompts(themes_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate prompts for Purview Product Expert to assess documentation gaps."""
    
    prompts = []
    
    # Handle themes as dict (theme_name -> theme_data)
    themes_items = []
    if isinstance(themes_data['themes'], dict):
        for theme_name, theme_info in themes_data['themes'].items():
            themes_items.append({
                'theme_name': theme_name,
                'total_incidents': theme_info['total_incidents'],
                'total_customers': theme_info['total_customers_affected'],
                'related_issues': theme_info.get('incidents', [])
            })
        # Sort by incidents descending
        themes_items.sort(key=lambda x: x['total_incidents'], reverse=True)
    else:
        themes_items = themes_data['themes']
    
    for i, theme in enumerate(themes_items, 1):
        # Extract key information
        theme_name = theme['theme_name']
        total_incidents = theme['total_incidents']
        total_customers = theme['total_customers']
        issues = theme.get('related_issues', [])[:5]  # Top 5 issues in theme
        
        # Build issue description
        issue_descriptions = []
        for issue in issues:
            issue_descriptions.append(
                f"  • \"{issue['title']}\" "
                f"({issue['count']} incidents, {issue['customers']} customers)"
            )
        
        issues_text = "\n".join(issue_descriptions)
        
        # Create expert prompt
        prompt = f"""
**Theme #{i}: {theme_name}**

**Impact:**
- {total_incidents} total by-design incidents
- {total_customers} unique customers affected
- {len(issues)} distinct issue patterns

**Common Issues:**
{issues_text}

**Analysis Request:**
As the Purview Product Expert, please review this theme and identify:

1. **Is this truly by-design or a product gap?**
   - If by-design: What's the intended behavior?
   - If product gap: What should be changed?

2. **Documentation assessment on learn.microsoft.com:**
   - Does clear documentation exist explaining this behavior?
   - If yes: Where is it? Is it discoverable?
   - If no: What documentation is missing?

3. **Content recommendations:**
   - What specific content should be created/updated?
   - Where should it be published? (conceptual docs, troubleshooting, known issues)
   - What key points must be covered?

4. **Customer guidance:**
   - What should customers be told when they encounter this?
   - Are there workarounds or alternative approaches?
   - Should this be included in release notes or service health advisories?

5. **Priority assessment:**
   - CRITICAL: Blocking customer deployments, security/compliance impact
   - HIGH: Frequent confusion, multiple customers affected
   - MEDIUM: Occasional questions, workarounds available
   - LOW: Edge case, minimal impact

Please provide specific, actionable recommendations with links to existing docs or proposals for new content.
"""
        
        prompts.append({
            'theme_number': i,
            'theme_name': theme_name,
            'impact_level': _calculate_impact_level(total_incidents, total_customers),
            'prompt': prompt.strip()
        })
    
    return prompts


def _calculate_impact_level(incidents: int, customers: int) -> str:
    """Calculate impact level based on incident and customer counts."""
    if incidents >= 10 and customers >= 5:
        return "CRITICAL"
    elif incidents >= 5 and customers >= 3:
        return "HIGH"
    elif incidents >= 3:
        return "MEDIUM"
    else:
        return "LOW"


def generate_report(themes_data: Dict[str, Any], prompts: List[Dict[str, str]]):
    """Generate comprehensive documentation gap analysis report."""
    
    # Create output directory
    output_dir = Path(__file__).parent / "reports"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = output_dir / f"mip_dlp_doc_gap_analysis_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"""# MIP/DLP Documentation Gap Analysis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Scope:** {themes_data['scope']}  
**Teams Analyzed:** {', '.join(themes_data['teams'])}

---

## Executive Summary

This report identifies documentation gaps in learn.microsoft.com content based on analysis of "by-design" ICM incidents in MIP/DLP areas.

**Key Findings:**
- **Total By-Design Incidents:** {themes_data['summary']['total_by_design_incidents']}
- **Unique Issue Types:** {themes_data['summary']['unique_issue_types']}
- **Themes Identified:** {themes_data['summary']['total_themes_identified']}
- **Customers Affected:** {themes_data['summary']['total_customers_affected']}

**Priority Distribution:**
""")
        
        # Calculate priority distribution
        priority_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for prompt in prompts:
            priority_counts[prompt['impact_level']] += 1
        
        for priority, count in priority_counts.items():
            if count > 0:
                f.write(f"- **{priority}:** {count} themes\n")
        
        f.write(f"""
---

## Purpose

These themes represent areas where customers are encountering by-design behavior that is causing confusion, leading to ICM incidents being filed. Each theme requires assessment by the **Purview Product Expert** to determine:

1. Whether the behavior is truly by-design or a product gap
2. If documentation exists to explain the behavior
3. What content needs to be created or improved on learn.microsoft.com
4. Customer communication strategy

---

## Purview Product Expert Review Instructions

For each theme below:

1. **Read the theme details and common issues**
2. **Answer the analysis questions** provided
3. **Provide specific, actionable recommendations** with:
   - Links to existing docs (if applicable)
   - Proposed new content (title, location, key points)
   - Priority level and rationale

4. **Document your findings** in a response file or directly in an issue tracker

---

## Themes for Review

""")
        
        # Write each theme prompt
        for prompt in prompts:
            f.write(f"\n{'='*70}\n")
            f.write(f"\n{prompt['prompt']}\n")
            f.write(f"\n**Impact Level:** {prompt['impact_level']}\n")
            f.write(f"\n{'='*70}\n")
        
        f.write(f"""

---

## Next Steps

### 1. Expert Review
- Share this report with **Purview Product Expert** for detailed assessment
- Request specific documentation recommendations for each theme

### 2. Content Creation
- Based on expert recommendations, create/update documentation on learn.microsoft.com
- Ensure content is discoverable via search and cross-linked

### 3. Customer Communication
- For CRITICAL/HIGH priority items, consider proactive communication:
  - Service health advisories
  - Release notes
  - Known issues updates
  - Customer-facing blog posts

### 4. Tracking
- Create work items in ADO for documentation tasks
- Track completion and measure impact (reduction in incidents)

### 5. Validation
- After documentation is published, monitor for trend changes
- Re-run this analysis in 90 days to measure effectiveness

---

## How to Use This Report

### For Product Experts
Review each theme and provide your assessment following the analysis questions.

### For Documentation Teams
Use expert recommendations to create/update content with specific focus on discoverability.

### For Engineering Managers
Use impact levels to prioritize documentation work alongside feature development.

### For Customer Success
Use this analysis to inform proactive customer education and support strategies.

---

## Data Sources

- **ICM Database:** IcMDataWarehouse (icmcluster.kusto.windows.net)
- **Analysis Period:** Last 90 days
- **Resolution Type:** By Design
- **Teams:**
""")
        
        for team in themes_data['teams']:
            f.write(f"  - PURVIEW\\{team}\n")
        
        f.write(f"""

---

## Contact

For questions about this analysis:
- **ICM Agent:** sub_agents/icm_agent/
- **Purview Product Expert:** sub_agents/purview_product_expert/
- **Analysis Scripts:** analyze_mip_dlp_by_design.py, analyze_mip_dlp_themes.py

---

*Report generated by PHEPy ICM Agent*
""")
    
    return report_file


def generate_expert_context_file(themes_data: Dict[str, Any], prompts: List[Dict[str, str]]):
    """Generate a context file for Purview Product Expert agent."""
    
    output_dir = Path(__file__).parent / "data"
    context_file = output_dir / "purview_expert_context.json"
    
    expert_context = {
        'task': 'documentation_gap_analysis',
        'scope': themes_data['scope'],
        'teams': themes_data['teams'],
        'analysis_date': themes_data['analysis_date'],
        'summary': themes_data['summary'],
        'themes_for_review': []
    }
    
    for prompt in prompts:
        expert_context['themes_for_review'].append({
            'theme_number': prompt['theme_number'],
            'theme_name': prompt['theme_name'],
            'impact_level': prompt['impact_level'],
            'prompt': prompt['prompt']
        })
    
    with open(context_file, 'w') as f:
        json.dump(expert_context, f, indent=2)
    
    return context_file


def main():
    print("="*70)
    print("MIP/DLP Documentation Gap Analysis")
    print("="*70)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Load themes
        print("📊 Loading theme analysis...")
        themes_data = load_themes()
        print(f"✓ Loaded {len(themes_data['themes'])} themes")
        
        # Generate expert prompts
        print("\n🔍 Generating Purview Product Expert analysis prompts...")
        prompts = generate_expert_prompts(themes_data)
        print(f"✓ Generated {len(prompts)} expert review requests")
        
        # Priority summary
        priority_dist = {}
        for p in prompts:
            level = p['impact_level']
            priority_dist[level] = priority_dist.get(level, 0) + 1
        
        print("\n📊 Impact Distribution:")
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if level in priority_dist:
                print(f"  {level}: {priority_dist[level]} themes")
        
        # Generate report
        print("\n📄 Generating documentation gap analysis report...")
        report_file = generate_report(themes_data, prompts)
        print(f"✓ Report generated: {report_file}")
        
        # Generate context file for expert
        print("\n💾 Generating Purview Product Expert context file...")
        context_file = generate_expert_context_file(themes_data, prompts)
        print(f"✓ Context saved: {context_file}")
        
        print("\n" + "="*70)
        print("✅ Documentation gap analysis complete!")
        print("="*70)
        print(f"""
Next Steps:
  
1. Review the generated report:
   {report_file}

2. Share with Purview Product Expert for detailed assessment
   
3. Or invoke Purview Product Expert agent directly with:
   "Please review the documentation gap analysis in 
    {context_file}
    and provide your assessment for each theme."

4. Create ADO work items for documentation tasks based on recommendations

5. Track and measure impact over subsequent 90-day periods
""")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease run the analysis steps in order:")
        print("  1. python analyze_mip_dlp_by_design.py")
        print("  2. Execute generated KQL queries")
        print("  3. python analyze_mip_dlp_themes.py")
        print("  4. python generate_doc_gap_analysis.py")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
