"""
Enhanced By Design Analysis with Real ICM IDs and Customer Names
"""

import pandas as pd
from collections import defaultdict, Counter
import re

def load_case_data():
    """Load production case data with ICM IDs"""
    df = pd.read_csv('data/production_full_cases.csv')
    return df

def extract_icm_ids(icm_string):
    """Extract individual ICM IDs from comma-separated string"""
    if pd.isna(icm_string) or icm_string == '':
        return []
    return [icm.strip() for icm in str(icm_string).split(',')]

def categorize_by_feature(summary_text, sap_path, queue_name):
    """Categorize case by feature area - using SAP Path for accurate categorization"""
    # SAP Path has the actual feature path like "Security/Microsoft Purview Compliance/Data loss prevention (DLP)/DLP Alerts"
    combined_text = f"{summary_text} {sap_path} {queue_name}".lower()
    path_lower = sap_path.lower() if sap_path else ""
    
    # Priority order matters - check most specific first using SAP Path
    if 'retention label' in path_lower or 'label analytics' in path_lower or 'activity explorer' in path_lower:
        return "Sensitivity Labels"
    elif 'sensitivity' in combined_text or 'mip label' in combined_text or 'aip label' in combined_text or 'label policy' in combined_text:
        return "Sensitivity Labels"
    elif 'auto label' in combined_text or 'auto-label' in combined_text or 'autolabel' in combined_text:
        return "Server Side Auto Labeling"
    elif any(kw in combined_text for kw in ['message encryption', 'messaging encryption', 'ome', 'purview message encryption']):
        return "Purview Message Encryption"
    elif 'encryption' in path_lower:
        return "Purview Message Encryption"
    elif any(kw in combined_text for kw in ['trainable classifier', 'custom classifier', 'classifier training']):
        return "Trainable Classifiers"
    elif 'exact data match' in combined_text or 'edm' in path_lower:
        return "Classification"
    elif 'sensitive information type' in combined_text or 'document fingerprint' in combined_text:
        return "Classification"
    elif 'data classification' in path_lower or '/classification' in path_lower:
        return "Classification"
    elif any(kw in combined_text for kw in ['dlp', 'data loss prevention']) or 'dlp' in path_lower:
        return "DLP"
    elif any(kw in combined_text for kw in ['retention', 'data lifecycle', 'dlm']) or 'lifecycle' in path_lower:
        return "Data Lifecycle Management"
    elif 'ediscovery' in combined_text or 'e-discovery' in combined_text or 'ediscovery' in path_lower:
        return "eDiscovery"
    elif 'communication compliance' in combined_text or 'comm compliance' in combined_text:
        return "Communication Compliance"
    elif 'audit' in path_lower:
        return "Auditing"
    else:
        return "Other"

def analyze_real_data():
    """Analyze real case data with ICM IDs"""
    
    print("=" * 80)
    print("BY DESIGN ICM ANALYSIS - REAL DATA")
    print("IC/MCS Cases with ICM References")
    print("=" * 80)
    print()
    
    # Load data
    df = load_case_data()
    df_with_icms = df[df['HasICM'] == 'Yes'].copy()
    
    print(f"📊 Total IC/MCS Cases: {len(df)}")
    print(f"📋 Cases with ICMs: {len(df_with_icms)} ({len(df_with_icms)/len(df)*100:.1f}%)")
    print()
    
    # Extract all ICM IDs with case context
    icm_data = []
    feature_debug = defaultdict(list)  # Debug: track sample queues per feature
    
    for _, row in df_with_icms.iterrows():
        icm_ids = extract_icm_ids(row['RelatedICM_Id'])
        feature = categorize_by_feature(row['Summary'], row['SAPPath'], row['QueueName'])
        
        # Debug: collect sample queue names
        if len(feature_debug[feature]) < 3:
            feature_debug[feature].append(row['SAPPath'])
        
        for icm_id in icm_ids:
            icm_data.append({
                'ICM_ID': icm_id,
                'Customer': row['TopParentName'],
                'TPID': row['TPID'],
                'CaseNumber': row['ServiceRequestNumber'],
                'DaysOpen': row['DaysOpen'],
                'Feature': feature,
                'Summary': row['Summary'],
                'Queue': row['QueueName'],
                'PHE': row['PHE'],
                'Status': row['ServiceRequestStatus'],
                'RiskScore': row['RiskScore']
            })
    
    icm_df = pd.DataFrame(icm_data)
    
    print(f"🔍 Unique ICMs Found: {icm_df['ICM_ID'].nunique()}")
    print(f"🏢 Unique Customers: {icm_df['Customer'].nunique()}")
    print()
    
    # Debug: Show sample queue names per feature
    print("🔧 Feature Categorization Samples (from SAP Path):")
    for feature in sorted(feature_debug.keys()):
        print(f"\n  {feature}:")
        for path in feature_debug[feature][:2]:
            print(f"    - {path}")
    print()
    
    # Feature area breakdown
    print("=" * 80)
    print("ICM DISTRIBUTION BY FEATURE AREA")
    print("=" * 80)
    feature_counts = icm_df.groupby('Feature').agg({
        'ICM_ID': 'nunique',
        'Customer': 'nunique',
        'CaseNumber': 'nunique'
    }).sort_values('ICM_ID', ascending=False)
    
    print(f"\n{'Feature Area':<35} {'ICMs':>8} {'Customers':>10} {'Cases':>7}")
    print("-" * 80)
    for feature, row in feature_counts.iterrows():
        if feature in ['Sensitivity Labels', 'Server Side Auto Labeling', 'Purview Message Encryption', 
                       'Trainable Classifiers', 'Classification']:
            marker = "🎯"
        else:
            marker = "  "
        print(f"{marker} {feature:<33} {row['ICM_ID']:>8} {row['Customer']:>10} {row['CaseNumber']:>7}")
    
    # Top customers by ICM count
    print("\n" + "=" * 80)
    print("TOP CUSTOMERS BY ICM COUNT (Priority Areas)")
    print("=" * 80)
    
    priority_features = ['Sensitivity Labels', 'Server Side Auto Labeling', 
                        'Purview Message Encryption', 'Trainable Classifiers', 'Classification']
    priority_icms = icm_df[icm_df['Feature'].isin(priority_features)]
    
    customer_icms = priority_icms.groupby('Customer').agg({
        'ICM_ID': 'nunique',
        'CaseNumber': 'nunique',
        'Feature': lambda x: ', '.join(x.value_counts().head(2).index.tolist())
    }).sort_values('ICM_ID', ascending=False).head(10)
    
    print(f"\n{'Customer':<25} {'ICMs':>6} {'Cases':>7} {'Top Features'}")
    print("-" * 80)
    for customer, row in customer_icms.iterrows():
        print(f"{customer:<25} {row['ICM_ID']:>6} {row['CaseNumber']:>7} {row['Feature']}")
    
    # Detailed analysis by feature
    print("\n\n" + "=" * 80)
    print("DETAILED ANALYSIS BY FEATURE AREA")
    print("=" * 80)
    
    for feature in priority_features:
        feature_data = icm_df[icm_df['Feature'] == feature]
        if len(feature_data) == 0:
            continue
        
        print(f"\n{'─' * 80}")
        print(f"🔹 {feature}")
        print(f"{'─' * 80}")
        print(f"Total ICMs: {feature_data['ICM_ID'].nunique()}")
        print(f"Affected Customers: {feature_data['Customer'].nunique()}")
        print(f"Related Cases: {feature_data['CaseNumber'].nunique()}")
        print()
        
        # Top ICMs by case frequency
        top_icms = feature_data['ICM_ID'].value_counts().head(5)
        print(f"  📍 Most Referenced ICMs:")
        for icm_id, count in top_icms.items():
            # Get customer examples for this ICM
            icm_cases = feature_data[feature_data['ICM_ID'] == icm_id]
            customers = icm_cases['Customer'].unique()[:3]
            customer_str = ", ".join(customers)
            if len(customers) > 2:
                customer_str += "..."
            print(f"    • ICM {icm_id}: {count} cases ({customer_str})")
        
        # Customers affected
        print(f"\n  🏢 Affected Customers:")
        cust_counts = feature_data.groupby('Customer').agg({
            'ICM_ID': 'nunique',
            'CaseNumber': 'count'
        }).sort_values('ICM_ID', ascending=False).head(5)
        
        for customer, row in cust_counts.iterrows():
            # Get sample ICMs for this customer
            cust_icms = feature_data[feature_data['Customer'] == customer]['ICM_ID'].unique()[:2]
            icm_str = ", ".join([str(i) for i in cust_icms])
            print(f"    • {customer}: {row['ICM_ID']} ICMs, {row['CaseNumber']} cases (e.g., {icm_str})")
        
        # Sample case summaries mentioning typical By Design patterns
        print(f"\n  🔄 Common Patterns (from case summaries):")
        sample_summaries = feature_data['Summary'].head(3)
        for i, summary in enumerate(sample_summaries, 1):
            summary_short = summary[:100] + "..." if len(summary) > 100 else summary
            print(f"    {i}. {summary_short}")
    
    # Generate comprehensive report
    print("\n\n" + "=" * 80)
    print("COMPREHENSIVE ICM-CUSTOMER MAPPING")
    print("=" * 80)
    
    # Create detailed mapping
    mapping_data = []
    for feature in priority_features:
        feature_data = icm_df[icm_df['Feature'] == feature]
        if len(feature_data) == 0:
            continue
        
        # Group by ICM and get all customers
        icm_groups = feature_data.groupby('ICM_ID').agg({
            'Customer': lambda x: list(x.unique()),
            'CaseNumber': lambda x: list(x.unique()),
            'DaysOpen': 'mean',
            'RiskScore': 'mean'
        }).sort_values('RiskScore', ascending=False)
        
        for icm_id, row in icm_groups.iterrows():
            mapping_data.append({
                'Feature': feature,
                'ICM_ID': icm_id,
                'Customers': ', '.join(row['Customer'][:3]) + ("..." if len(row['Customer']) > 3 else ""),
                'Cases': len(row['CaseNumber']),
                'AvgAge': f"{row['DaysOpen']:.0f}",
                'AvgRisk': f"{row['RiskScore']:.0f}"
            })
    
    mapping_df = pd.DataFrame(mapping_data)
    
    # Export to Excel
    output_file = "icm_by_design_analysis_with_customers.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Full ICM mapping
        mapping_df.to_excel(writer, sheet_name='ICM-Customer Mapping', index=False)
        
        # Feature summary
        feature_summary = icm_df.groupby('Feature').agg({
            'ICM_ID': 'nunique',
            'Customer': 'nunique',
            'CaseNumber': 'nunique',
            'DaysOpen': 'mean',
            'RiskScore': 'mean'
        }).round(1)
        feature_summary.to_excel(writer, sheet_name='Feature Summary')
        
        # Customer summary
        customer_summary = priority_icms.groupby('Customer').agg({
            'ICM_ID': 'nunique',
            'CaseNumber': 'nunique',
            'Feature': lambda x: ', '.join(x.unique()[:3])
        }).sort_values('ICM_ID', ascending=False)
        customer_summary.to_excel(writer, sheet_name='Customer Summary')
        
        # Raw data
        icm_df.to_excel(writer, sheet_name='All ICM Data', index=False)
    
    print(f"\n✅ Detailed Excel report saved: {output_file}")
    
    # Generate markdown report with real data
    generate_markdown_with_real_data(icm_df, feature_counts, mapping_df, priority_icms)
    
    print(f"\n✅ Updated markdown report: by_design_analysis_real_data.md")

def generate_markdown_with_real_data(icm_df, feature_counts, mapping_df, priority_icms):
    """Generate markdown report with real ICM IDs and customers"""
    
    priority_features = ['Sensitivity Labels', 'Server Side Auto Labeling', 
                        'Purview Message Encryption', 'Trainable Classifiers', 'Classification']
    
    report = f"""# By Design ICM Analysis - Real Data with ICM IDs & Customers
**Data Source:** IC/MCS Production Cases  
**Total ICMs Analyzed:** {icm_df['ICM_ID'].nunique()}  
**Affected Customers:** {icm_df['Customer'].nunique()}  
**Date:** February 10, 2026

---

## Executive Summary

Analyzed {icm_df['ICM_ID'].nunique()} unique ICMs across {icm_df['CaseNumber'].nunique()} IC/MCS cases affecting {icm_df['Customer'].nunique()} strategic customers. Focus on 5 priority Purview feature areas commonly associated with "By Design" resolutions.

### Key Findings

1. **DLP** has highest ICM volume ({icm_df[icm_df['Feature']=='DLP']['ICM_ID'].nunique()} ICMs) but focus is on core Info Protection features
2. Priority features represent **{len(priority_icms)}** ICMs across **{priority_icms['Customer'].nunique()}** customers
3. Top customer: **{priority_icms.groupby('Customer')['ICM_ID'].nunique().idxmax()}** ({priority_icms.groupby('Customer')['ICM_ID'].nunique().max()} ICMs)

---

## Feature Area Analysis with ICM IDs

"""
    
    for feature in priority_features:
        feature_data = icm_df[icm_df['Feature'] == feature]
        if len(feature_data) == 0:
            continue
        
        report += f"\n### {'🎯 ' + feature}\n\n"
        report += f"**Total ICMs:** {feature_data['ICM_ID'].nunique()}  \n"
        report += f"**Customers:** {feature_data['Customer'].nunique()}  \n"
        report += f"**Cases:** {feature_data['CaseNumber'].nunique()}  \n\n"
        
        # Top ICMs
        report += "**Most Referenced ICMs:**\n\n"
        top_icms = feature_data['ICM_ID'].value_counts().head(5)
        for icm_id, count in top_icms.items():
            icm_cases = feature_data[feature_data['ICM_ID'] == icm_id]
            customers = icm_cases['Customer'].unique()[:2]
            customer_str = ", ".join(customers)
            case_nums = [str(c) for c in icm_cases['CaseNumber'].unique()[:2].tolist()]
            report += f"- **ICM {icm_id}**: {count} cases\n"
            report += f"  - Customers: {customer_str}\n"
            report += f"  - Case #: {', '.join(case_nums)}\n"
        
        report += "\n**Affected Customers:**\n\n"
        cust_counts = feature_data.groupby('Customer').agg({
            'ICM_ID': lambda x: list(x.unique()),
            'CaseNumber': 'count'
        }).sort_values('CaseNumber', ascending=False).head(5)
        
        for customer, row in cust_counts.iterrows():
            icm_list = [str(i) for i in row['ICM_ID'][:3]]
            report += f"- **{customer}**: {len(row['ICM_ID'])} ICMs, {row['CaseNumber']} cases\n"
            report += f"  - ICMs: {', '.join(icm_list)}{'...' if len(row['ICM_ID']) > 3 else ''}\n"
        
        report += "\n"
    
    # Top customers table
    report += "\n---\n\n## Top 10 Customers by ICM Count\n\n"
    report += "| Customer | ICMs | Cases | Top Features |\n"
    report += "|----------|------|-------|-------------|\n"
    
    customer_icms = priority_icms.groupby('Customer').agg({
        'ICM_ID': 'nunique',
        'CaseNumber': 'nunique',
        'Feature': lambda x: ', '.join(x.value_counts().head(2).index.tolist())
    }).sort_values('ICM_ID', ascending=False).head(10)
    
    for customer, row in customer_icms.iterrows():
        report += f"| {customer} | {row['ICM_ID']} | {row['CaseNumber']} | {row['Feature']} |\n"
    
    # Recommendations section
    report += "\n---\n\n## 🎯 Recommendations\n\n"
    report += """Based on real ICM data patterns:

### 1. 🔴 HIGH: Create ICM-Specific "By Design" Documentation

**Action:** For top 20 recurring ICMs, create dedicated KB articles
- Include ICM ID, customer names (if applicable), and clear "By Design" explanation
- Add to public docs with "Expected Behavior" tag
- **Priority ICMs to document first:** Top 5 from each feature area (see above)

### 2. 🔴 HIGH: Customer-Specific Playbooks

**Target customers:** Top 10 (see table above)
- Create custom runbook for each customer's specific ICM patterns
- Include PHE/CSA contact info
- Proactive communication strategy

### 3. 🟡 MEDIUM: ICM Pattern Analysis

**Action:** Deep dive into recurring ICM IDs
- Why do same ICMs appear across multiple customers?
- Are these genuine "By Design" or needing feature improvements?
- Prioritize by customer impact (IC vs MCS)

### 4. 🟢 LOW: Self-Service ICM Lookup

**Action:** Create internal tool
- Input ICM ID → Get "By Design" status + explanation
- Link to KB articles automatically
- Reduce support ticket volume

---

## Next Steps

1. **Week 1:** Review top 10 ICMs per feature for "By Design" status validation
2. **Week 2:** Create KB articles for confirmed "By Design" ICMs
3. **Week 3:** Share with PHEs for top 10 customers
4. **Ongoing:** Monitor new ICM patterns monthly

---

## Data Files

- **Excel**: `icm_by_design_analysis_with_customers.xlsx`
  - Full ICM-Customer mapping
  - Feature summaries
  - Customer breakdowns
  - Raw data for analysis

"""
    
    with open("by_design_analysis_real_data.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    analyze_real_data()
