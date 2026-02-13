"""
Analyze "By Design" ICMs for Purview Feature Areas
Identifies themes, patterns, and potential design improvement opportunities
"""

import os
from datetime import datetime, timedelta
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd
from collections import Counter
import re

# Feature areas to analyze
FEATURE_AREAS = [
    "Sensitivity Labels",
    "Server Side Auto Labeling", 
    "Purview Message Encryption",
    "Trainable Classifiers",
    "Classification"
]

# Common keywords for theme bucketing
THEME_KEYWORDS = {
    "Performance/Scale": [
        "slow", "performance", "timeout", "delay", "latency", "scale",
        "large", "too long", "processing time", "batch", "throttle"
    ],
    "Configuration/Settings": [
        "configuration", "setting", "policy", "rule", "parameter", "option",
        "enabled", "disabled", "scope", "permission", "access"
    ],
    "User Experience": [
        "confusing", "unclear", "ux", "ui", "message", "error message",
        "notification", "display", "visible", "hidden", "user experience"
    ],
    "Integration/Compatibility": [
        "integration", "compatibility", "third party", "works with", "interop",
        "connector", "api", "powershell", "graph", "sdk"
    ],
    "Timing/Sync": [
        "sync", "propagation", "replication", "timing", "delay in", 
        "eventual consistency", "cache", "refresh", "update"
    ],
    "Detection/Accuracy": [
        "false positive", "false negative", "not detected", "missed",
        "accuracy", "precision", "confidence", "detection", "classifier"
    ],
    "Documentation Gap": [
        "not documented", "documentation", "unclear in docs", "expected behavior",
        "should be documented", "docs", "guidance"
    ],
    "Feature Limitation": [
        "limitation", "not supported", "cannot", "doesn't support",
        "by design", "working as designed", "current design", "future enhancement"
    ],
    "Encryption/Security": [
        "encryption", "decrypt", "rights", "rms", "protection", "external user",
        "recipient", "ome", "secure"
    ],
    "Auto-labeling Logic": [
        "auto label", "automatic", "shouldn't apply", "applied to wrong",
        "label condition", "senstivity label", "inheritance", "overwrite"
    ]
}

def get_kusto_client():
    """Initialize Kusto client for ICM cluster"""
    cluster = "https://icmcluster.kusto.windows.net"
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
    return KustoClient(kcsb)

def analyze_by_design_icms():
    """Query and analyze By Design ICMs"""
    
    client = get_kusto_client()
    
    # Calculate date range (90 days back)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    query = f"""
    let FeatureAreas = dynamic([
        "Sensitivity Labels",
        "Server Side Auto Labeling",
        "Purview Message Encryption", 
        "Trainable Classifiers",
        "Classification"
    ]);
    Incidents
    | where CreateDate >= datetime({start_date.strftime('%Y-%m-%d')})
    | where CreateDate <= datetime({end_date.strftime('%Y-%m-%d')})
    | where ServiceName == "Microsoft Purview" or ServiceName == "Office Substrate"
    | where HowFixed == "By Design" or HowFixed == "ByDesign"
    | where Status in ("RESOLVED", "CLOSED")
    | extend TitleLower = tolower(Title)
    | extend DescriptionLower = tolower(Description)
    | extend FeatureArea = case(
        TitleLower contains "sensitivity label" or DescriptionLower contains "sensitivity label", "Sensitivity Labels",
        TitleLower contains "auto label" or TitleLower contains "auto-label", "Server Side Auto Labeling",
        TitleLower contains "message encryption" or TitleLower contains "ome", "Purview Message Encryption",
        TitleLower contains "trainable classifier" or TitleLower contains "custom classifier", "Trainable Classifiers",
        TitleLower contains "classification" or TitleLower contains "sensitive info" or TitleLower contains "sit", "Classification",
        "Other")
    | where FeatureArea in (FeatureAreas)
    | project IncidentId, Title, Description, CreateDate, ResolvedDate, 
              FeatureArea, Severity, ImpactedServices, OwningTeamName,
              CustomerImpact = customDimensions.CustomerImpact,
              Resolution = Resolution
    | order by CreateDate desc
    """
    
    print("Querying ICM cluster for By Design incidents...")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    try:
        response = client.execute("IcmDataWarehouse", query)
        df = dataframe_from_result_table(response.primary_results[0])
        
        if len(df) == 0:
            print("No By Design ICMs found for these feature areas in the last 90 days.")
            return
        
        print(f"\n✅ Found {len(df)} By Design ICMs\n")
        
        # Analyze by feature area
        print("=" * 80)
        print("BREAKDOWN BY FEATURE AREA")
        print("=" * 80)
        feature_counts = df['FeatureArea'].value_counts()
        for area, count in feature_counts.items():
            pct = (count / len(df)) * 100
            print(f"{area:40s} {count:3d} ({pct:5.1f}%)")
        
        # Theme analysis
        print("\n" + "=" * 80)
        print("THEME ANALYSIS")
        print("=" * 80)
        
        themes_by_icm = {}
        for idx, row in df.iterrows():
            text = f"{row['Title']} {row['Description']}".lower()
            icm_themes = []
            
            for theme, keywords in THEME_KEYWORDS.items():
                if any(keyword in text for keyword in keywords):
                    icm_themes.append(theme)
            
            if not icm_themes:
                icm_themes = ["Uncategorized"]
            
            themes_by_icm[row['IncidentId']] = icm_themes
        
        # Count themes
        all_themes = []
        for themes in themes_by_icm.values():
            all_themes.extend(themes)
        
        theme_counts = Counter(all_themes)
        print(f"\nTop Themes (ICMs may have multiple themes):")
        for theme, count in theme_counts.most_common():
            pct = (count / len(df)) * 100
            print(f"  {theme:35s} {count:3d} ({pct:5.1f}%)")
        
        # Feature Area + Theme matrix
        print("\n" + "=" * 80)
        print("FEATURE AREA × THEME MATRIX")
        print("=" * 80)
        
        matrix_data = []
        for feature in feature_counts.index:
            feature_df = df[df['FeatureArea'] == feature]
            feature_themes = []
            for icm_id in feature_df['IncidentId']:
                feature_themes.extend(themes_by_icm.get(icm_id, []))
            
            theme_counter = Counter(feature_themes)
            for theme, count in theme_counter.most_common(3):  # Top 3 themes per feature
                matrix_data.append({
                    'Feature': feature,
                    'Theme': theme,
                    'Count': count
                })
        
        matrix_df = pd.DataFrame(matrix_data)
        for feature in feature_counts.index:
            print(f"\n{feature}:")
            feature_matrix = matrix_df[matrix_df['Feature'] == feature]
            for _, row in feature_matrix.iterrows():
                print(f"  → {row['Theme']:30s} ({row['Count']} ICMs)")
        
        # Severity breakdown
        print("\n" + "=" * 80)
        print("SEVERITY DISTRIBUTION")
        print("=" * 80)
        sev_counts = df['Severity'].value_counts()
        for sev, count in sev_counts.items():
            pct = (count / len(df)) * 100
            print(f"Severity {sev}: {count:3d} ({pct:5.1f}%)")
        
        # Time to resolution
        print("\n" + "=" * 80)
        print("TIME TO RESOLUTION (By Design)")
        print("=" * 80)
        df['ResolvedDate'] = pd.to_datetime(df['ResolvedDate'])
        df['CreateDate'] = pd.to_datetime(df['CreateDate'])
        df['ResolutionDays'] = (df['ResolvedDate'] - df['CreateDate']).dt.days
        
        avg_resolution = df['ResolutionDays'].mean()
        median_resolution = df['ResolutionDays'].median()
        print(f"Average: {avg_resolution:.1f} days")
        print(f"Median:  {median_resolution:.1f} days")
        print(f"Min:     {df['ResolutionDays'].min():.0f} days")
        print(f"Max:     {df['ResolutionDays'].max():.0f} days")
        
        # Top issues by frequency
        print("\n" + "=" * 80)
        print("TOP RECURRING ISSUES (Similar Titles)")
        print("=" * 80)
        
        # Extract common patterns from titles
        title_patterns = {}
        for title in df['Title']:
            # Remove specific case numbers, IDs, customer names
            normalized = re.sub(r'\d+', 'X', title)
            normalized = re.sub(r'SR\s*\d+|Case\s*\d+|ICM\s*\d+', '', normalized)
            normalized = normalized.strip()
            
            if len(normalized) > 20:  # Ignore very short titles
                title_patterns[normalized] = title_patterns.get(normalized, 0) + 1
        
        # Show patterns that appear 2+ times
        recurring = {k: v for k, v in title_patterns.items() if v >= 2}
        recurring_sorted = sorted(recurring.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for pattern, count in recurring_sorted:
            print(f"{count:2d}× {pattern[:100]}")
        
        # RECOMMENDATIONS
        print("\n" + "=" * 80)
        print("🎯 DESIGN IMPROVEMENT OPPORTUNITIES")
        print("=" * 80)
        
        recommendations = generate_recommendations(df, theme_counts, feature_counts, recurring_sorted)
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']}")
            print(f"   Priority: {rec['priority']}")
            print(f"   Impact: {rec['impact']}")
            print(f"   Suggestion: {rec['suggestion']}")
        
        # Export detailed data
        output_file = "by_design_icms_analysis.xlsx"
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All ICMs', index=False)
            
            # Summary sheet
            summary_df = pd.DataFrame({
                'Feature Area': feature_counts.index,
                'Count': feature_counts.values,
                'Percentage': (feature_counts.values / len(df) * 100).round(1)
            })
            summary_df.to_excel(writer, sheet_name='Feature Summary', index=False)
            
            # Theme summary
            theme_df = pd.DataFrame({
                'Theme': [k for k, v in theme_counts.most_common()],
                'Count': [v for k, v in theme_counts.most_common()],
                'Percentage': [(v / len(df) * 100) for k, v in theme_counts.most_common()]
            })
            theme_df.to_excel(writer, sheet_name='Theme Summary', index=False)
            
            # Matrix
            matrix_df.to_excel(writer, sheet_name='Feature x Theme Matrix', index=False)
        
        print(f"\n\n✅ Detailed analysis exported to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error querying ICM data: {e}")
        import traceback
        traceback.print_exc()

def generate_recommendations(df, theme_counts, feature_counts, recurring_issues):
    """Generate actionable recommendations based on analysis"""
    recs = []
    
    # Recommendation based on top theme
    top_theme = theme_counts.most_common(1)[0]
    if top_theme[0] == "Feature Limitation":
        recs.append({
            'title': f"Address Feature Limitations (Top Theme: {top_theme[1]} ICMs)",
            'priority': "HIGH",
            'impact': f"{(top_theme[1]/len(df)*100):.0f}% of By Design cases are feature limitations",
            'suggestion': "Consider adding most-requested features to roadmap. Create FAQ for common limitation questions."
        })
    
    if "Documentation Gap" in dict(theme_counts) and dict(theme_counts)["Documentation Gap"] > 5:
        count = dict(theme_counts)["Documentation Gap"]
        recs.append({
            'title': f"Close Documentation Gaps ({count} ICMs)",
            'priority': "MEDIUM",
            'impact': "Customers unclear on expected behavior",
            'suggestion': "Create comprehensive 'By Design Behaviors' doc section for each feature area. Add to public docs."
        })
    
    if "Performance/Scale" in dict(theme_counts):
        count = dict(theme_counts)["Performance/Scale"]
        recs.append({
            'title': f"Review Performance Expectations ({count} ICMs)",
            'priority': "MEDIUM",
            'impact': "Customer expectations misaligned with current performance",
            'suggestion': "Document SLAs and expected processing times. Consider performance improvements for large tenants."
        })
    
    # Feature-specific recommendations
    if "Sensitivity Labels" in feature_counts.index:
        count = feature_counts["Sensitivity Labels"]
        if count > len(df) * 0.3:  # If >30% of issues
            recs.append({
                'title': f"Sensitivity Labels High Volume ({count} ICMs, {count/len(df)*100:.0f}%)",
                'priority': "HIGH",
                'impact': "Most common By Design area",
                'suggestion': "Review label policy design, sync behavior, and inheritance rules. Consider UX improvements."
            })
    
    # Recurring issues
    if len(recurring_issues) > 0:
        recs.append({
            'title': f"Address Recurring Issues ({len(recurring_issues)} patterns found)",
            'priority': "HIGH", 
            'impact': "Same issues reported multiple times",
            'suggestion': "Create self-service tools or improved error messages for top recurring patterns."
        })
    
    # Timing/Sync issues
    if "Timing/Sync" in dict(theme_counts) and dict(theme_counts)["Timing/Sync"] > 3:
        count = dict(theme_counts)["Timing/Sync"]
        recs.append({
            'title': f"Improve Sync Transparency ({count} ICMs)",
            'priority': "MEDIUM",
            'impact': "Customers don't understand eventual consistency model",
            'suggestion': "Add progress indicators, improve admin notifications, document expected sync times."
        })
    
    return recs

if __name__ == "__main__":
    print("=" * 80)
    print("BY DESIGN ICM ANALYSIS - PURVIEW FEATURE AREAS")
    print("Last 90 Days")
    print("=" * 80)
    print()
    
    analyze_by_design_icms()
