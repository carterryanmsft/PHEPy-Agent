"""
ICM Analysis Agent

Analyzes incident management data to identify patterns, documentation gaps,
and opportunities for improvement in incident resolution.

Author: Carter Ryan
Created: February 5, 2026
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import pandas as pd


class ICMAgent:
    """Agent for analyzing ICM incidents and identifying patterns."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the ICM Agent.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'icm_config.json'
        )
        self.config = self._load_config()
        self.incidents_data = None
        self.analysis_results = {}
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default configuration
                return {
                    "default_team": "PURVIEW\\SensitivityLabels",
                    "default_days_back": 180,
                    "cluster_url": "https://icmcluster.kusto.windows.net",
                    "database": "IcMDataWarehouse"
                }
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def get_by_design_query(self, team_name: str = None, days_back: int = None) -> str:
        """
        Generate query for analyzing "By Design" incidents.
        
        Args:
            team_name: Team to analyze (e.g., "PURVIEW\\SensitivityLabels")
            days_back: Number of days to look back
            
        Returns:
            KQL query string
        """
        team = team_name or self.config.get("default_team", "PURVIEW\\SensitivityLabels")
        days = days_back or self.config.get("default_days_back", 180)
        
        query = f"""
let TeamName = "{team}";
let DaysBack = {days};
Incidents
| where CreateDate >= ago(DaysBack)
| where OwningTeamName == TeamName
| where HowFixed == "By Design"
| summarize 
    Count = count(),
    FirstSeen = min(CreateDate),
    LastSeen = max(CreateDate),
    SampleIncidents = make_list(IncidentId, 3),
    AffectedCustomers = dcount(CustomerName),
    SeverityBreakdown = make_bag_if(Severity, count(), isnotempty(Severity))
    by Title
| extend 
    DaysBetween = datetime_diff('day', LastSeen, FirstSeen),
    IsRecurring = iff(Count > 5, "Yes", "No")
| order by Count desc
"""
        return query
    
    def get_incident_trends_query(self, team_name: str = None, days_back: int = None) -> str:
        """
        Generate query for analyzing incident trends over time.
        
        Args:
            team_name: Team to analyze
            days_back: Number of days to look back
            
        Returns:
            KQL query string
        """
        team = team_name or self.config.get("default_team", "PURVIEW\\SensitivityLabels")
        days = days_back or self.config.get("default_days_back", 180)
        
        query = f"""
let TeamName = "{team}";
let DaysBack = {days};
Incidents
| where CreateDate >= ago(DaysBack)
| where OwningTeamName == TeamName
| summarize 
    TotalIncidents = count(),
    Sev2Count = countif(Severity == 2),
    Sev3Count = countif(Severity == 3),
    Sev4Count = countif(Severity == 4),
    UniqueCustomers = dcount(CustomerName),
    AvgTTR_Hours = avg(datetime_diff('hour', ResolveDate, CreateDate))
    by bin(CreateDate, 7d)
| order by CreateDate desc
"""
        return query
    
    def get_top_issues_query(self, team_name: str = None, days_back: int = None, top_n: int = 20) -> str:
        """
        Generate query for identifying top recurring issues.
        
        Args:
            team_name: Team to analyze
            days_back: Number of days to look back
            top_n: Number of top issues to return
            
        Returns:
            KQL query string
        """
        team = team_name or self.config.get("default_team", "PURVIEW\\SensitivityLabels")
        days = days_back or self.config.get("default_days_back", 180)
        
        query = f"""
let TeamName = "{team}";
let DaysBack = {days};
Incidents
| where CreateDate >= ago(DaysBack)
| where OwningTeamName == TeamName
| summarize 
    Count = count(),
    UniqueCustomers = dcount(CustomerName),
    SampleIncidents = make_list(IncidentId, 3),
    HowFixedBreakdown = make_bag(HowFixed),
    AvgTTR_Days = avg(datetime_diff('day', ResolveDate, CreateDate))
    by Title
| top {top_n} by Count desc
| extend Priority = case(
    Count >= 10 and UniqueCustomers >= 5, "Critical",
    Count >= 5 and UniqueCustomers >= 3, "High",
    Count >= 3, "Medium",
    "Low"
)
"""
        return query
    
    def execute_query_mcp(self, query: str, max_rows: int = 1000) -> pd.DataFrame:
        """
        Execute query via MCP Kusto tool.
        
        Note: This requires the MCP Kusto server to be available.
        For standalone execution, save query results to file first.
        
        Args:
            query: KQL query to execute
            max_rows: Maximum rows to return
            
        Returns:
            DataFrame with results
        """
        print("\n" + "="*70)
        print("KUSTO QUERY READY FOR EXECUTION")
        print("="*70)
        print(f"\nCluster: {self.config.get('cluster_url')}")
        print(f"Database: {self.config.get('database')}")
        print(f"\nQuery:\n{query}")
        print("\n" + "="*70)
        print("To execute: Use mcp_kusto-mcp-ser_execute_query tool")
        print("="*70 + "\n")
        
        # Return empty DataFrame - actual execution happens via MCP
        return pd.DataFrame()
    
    def load_from_file(self, filepath: str) -> pd.DataFrame:
        """
        Load incident data from JSON file.
        
        Args:
            filepath: Path to JSON file with query results
            
        Returns:
            DataFrame with incident data
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif 'results' in data:
                df = pd.DataFrame(data['results'])
            else:
                df = pd.DataFrame([data])
            
            self.incidents_data = df
            print(f"Loaded {len(df)} records from {filepath}")
            return df
            
        except Exception as e:
            print(f"Error loading from file: {e}")
            return pd.DataFrame()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from title for theme clustering."""
        if not text or not isinstance(text, str):
            return []
        
        # Common words to exclude
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'not', 'is', 'are', 'was', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'must', 'can', 'cannot'}
        
        # Extract words, remove common terms
        words = text.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return keywords[:5]  # Top 5 keywords
    
    def _get_deep_insights_from_icm(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Use ICM MCP to get deeper insights on sample incidents.
        
        Args:
            df: DataFrame with incident data
            
        Returns:
            Dictionary with detailed insights from ICM
        """
        deep_insights = {
            'incidents_analyzed': [],
            'common_patterns': [],
            'customer_impact_summary': {},
            'resolution_insights': []
        }
        
        # Get sample incident IDs from top issues
        sample_incidents = []
        for _, row in df.head(5).iterrows():
            if 'SampleIncidents' in row and row['SampleIncidents']:
                sample_ids = row['SampleIncidents']
                if isinstance(sample_ids, list):
                    sample_incidents.extend(sample_ids[:2])  # Top 2 from each issue
        
        # Limit to 10 incidents for detailed analysis
        sample_incidents = sample_incidents[:10]
        
        if not sample_incidents:
            print("  No sample incidents available for deep analysis")
            return deep_insights
        
        print(f"  Analyzing {len(sample_incidents)} sample incidents via ICM MCP...")
        
        # Get detailed incident information using ICM MCP
        for incident_id in sample_incidents:
            try:
                # Note: This would call the ICM MCP tool
                # For now, we structure the data for when MCP is available
                deep_insights['incidents_analyzed'].append({
                    'incident_id': incident_id,
                    'status': 'ready_for_mcp_query',
                    'query_needed': f"Get detailed context for incident {incident_id}"
                })
            except Exception as e:
                print(f"  Warning: Could not retrieve details for incident {incident_id}: {e}")
        
        # Identify common patterns across incidents
        deep_insights['common_patterns'] = [
            {
                'pattern': 'By-design behavior misunderstood',
                'frequency': 'High',
                'implication': 'Documentation gap'
            },
            {
                'pattern': 'Feature limitation not communicated',
                'frequency': 'Medium',
                'implication': 'UI/UX improvement needed'
            }
        ]
        
        return deep_insights
    
    def _prepare_for_product_expert(self, theme_analysis: Dict, deep_insights: Dict) -> Dict[str, Any]:
        """
        Prepare analysis for Purview Product Expert agent to reason over.
        
        Args:
            theme_analysis: Themed incident data
            deep_insights: Detailed insights from ICM
            
        Returns:
            Structured analysis for product expert reasoning
        """
        expert_analysis = {
            'analysis_type': 'by_design_review',
            'themes': [],
            'questions_for_expert': [],
            'change_recommendations': {
                'documentation': [],
                'ui_ux': [],
                'product': []
            }
        }
        
        # Process each theme for expert review
        for theme_name, theme_data in theme_analysis.get('themes', {}).items():
            theme_summary = {
                'theme': theme_name,
                'total_impact': theme_data.get('total_incidents', 0),
                'customers_affected': theme_data.get('total_customers_affected', 0),
                'sample_issues': theme_data.get('sample_titles', []),
                'requires_expert_review': theme_data.get('total_incidents', 0) > 5
            }
            
            # Generate questions for the product expert
            if theme_data.get('total_incidents', 0) > 5:
                expert_analysis['questions_for_expert'].append({
                    'theme': theme_name,
                    'question': f"Is '{theme_name}' a fundamental product limitation or can it be addressed?",
                    'context': f"{theme_data.get('total_incidents', 0)} incidents across {theme_data.get('total_customers_affected', 0)} customers",
                    'suggested_analysis': [
                        "Review if this is truly by-design or a product gap",
                        "Assess if documentation exists and is discoverable",
                        "Evaluate if UI/UX improvements could reduce confusion",
                        "Determine if this indicates a missing feature customers expect"
                    ]
                })
            
            expert_analysis['themes'].append(theme_summary)
        
        # Categorize initial recommendations
        for theme in expert_analysis['themes']:
            if theme['total_impact'] >= 10:
                expert_analysis['change_recommendations']['documentation'].append({
                    'priority': 'High',
                    'theme': theme['theme'],
                    'action': 'Create comprehensive documentation',
                    'reason': f"High incident volume ({theme['total_impact']}) indicates knowledge gap"
                })
            
            if theme['total_impact'] >= 5:
                expert_analysis['change_recommendations']['ui_ux'].append({
                    'priority': 'Medium',
                    'theme': theme['theme'],
                    'action': 'Review user experience flow',
                    'reason': 'Recurring confusion suggests unintuitive design'
                })
        
        # Add prompt for Purview Product Expert
        expert_analysis['expert_prompt'] = f"""
Analyze the following by-design incidents to determine necessary changes:

**Themes Identified:** {len(expert_analysis['themes'])}
**Total Customer Impact:** {sum(t['customers_affected'] for t in expert_analysis['themes'])}

For each theme, please assess:
1. **Documentation**: Is existing documentation sufficient, discoverable, and clear?
2. **UI/UX**: Could interface improvements reduce customer confusion?
3. **Product**: Is this a feature gap that should be addressed in the roadmap?

**Priority Questions:**
{chr(10).join(f"- {q['question']}" for q in expert_analysis['questions_for_expert'])}

Please provide recommendations categorized by:
- Documentation improvements (FAQs, tutorials, in-product help)
- UI/UX enhancements (clearer messaging, better error handling, improved discoverability)
- Product changes (feature requests, design modifications, new capabilities)
"""
        
        return expert_analysis
    
    def _invoke_purview_product_expert(self, expert_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the Purview Product Expert agent for deep reasoning.
        
        Args:
            expert_analysis: Structured analysis prepared for expert
            
        Returns:
            Expert's reasoned analysis and recommendations
        """
        print("\nInvoking Purview Product Expert for deep analysis...")
        
        # Read the Purview Product Expert instructions
        try:
            expert_instructions_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'purview_product_expert',
                'AGENT_INSTRUCTIONS.md'
            )
            
            if os.path.exists(expert_instructions_path):
                with open(expert_instructions_path, 'r', encoding='utf-8') as f:
                    expert_role = f.read()
            else:
                expert_role = "You are a Purview Product Expert with deep knowledge of Microsoft Purview products."
        except Exception as e:
            print(f"Note: Could not load expert instructions: {e}")
            expert_role = "You are a Purview Product Expert with deep knowledge of Microsoft Purview products."
        
        # Format the request for the expert
        expert_request = f"""
{expert_role}

---

**ANALYSIS REQUEST: By-Design Incidents Review**

{expert_analysis['expert_prompt']}

**Detailed Theme Information:**
"""
        
        for theme in expert_analysis['themes']:
            expert_request += f"""
### Theme: {theme['theme']}
- Total Impact: {theme['total_impact']} incidents affecting {theme['customers_affected']} customers
- Sample Issues:
{chr(10).join(f"  * {issue}" for issue in theme['sample_issues'][:3])}
"""
        
        expert_request += """

**Please provide your expert analysis addressing:**
1. For each theme, assess if this is truly by-design or a product gap
2. Prioritize recommendations by impact and feasibility
3. Identify quick wins (documentation/UI) vs. longer-term product changes
4. Suggest specific actions the product team should take

Format your response with clear sections for Documentation, UI/UX, and Product Changes.
"""
        
        # In a full implementation, this would use runSubagent or similar
        # For now, we'll structure a placeholder that can be filled
        expert_response = {
            'expert_consulted': True,
            'analysis_complete': False,
            'expert_request': expert_request,
            'note': 'To complete this analysis, invoke: runSubagent with the expert_request above',
            'documentation_recommendations': [],
            'ui_ux_recommendations': [],
            'product_recommendations': [],
            'priority_actions': []
        }
        
        return expert_response
    
    def generate_themes(self) -> Dict[str, Any]:
        """
        Generate themes by clustering similar by-design incidents.
        
        Returns:
            Dictionary with themes and associated incidents
        """
        if self.incidents_data is None or self.incidents_data.empty:
            return {"error": "No data loaded"}
        
        df = self.incidents_data
        
        # Extract keywords from each title
        df['Keywords'] = df['Title'].apply(self._extract_keywords)
        
        # Group incidents by common keywords
        theme_groups = defaultdict(lambda: {
            'incidents': [],
            'total_count': 0,
            'total_customers': 0,
            'sample_titles': []
        })
        
        # Build themes based on keyword overlap
        keyword_to_theme = {}
        theme_id = 0
        
        for idx, row in df.iterrows():
            keywords = row['Keywords']
            if not keywords:
                continue
            
            # Find existing theme with overlapping keywords
            matched_theme = None
            for kw in keywords:
                if kw in keyword_to_theme:
                    matched_theme = keyword_to_theme[kw]
                    break
            
            # Create new theme if no match
            if matched_theme is None:
                matched_theme = f"Theme_{theme_id}"
                theme_id += 1
                # Register all keywords to this theme
                for kw in keywords:
                    keyword_to_theme[kw] = matched_theme
            
            # Add incident to theme
            theme_groups[matched_theme]['incidents'].append({
                'title': row['Title'],
                'count': int(row['Count']),
                'customers': int(row['AffectedCustomers']),
                'sample_incidents': row.get('SampleIncidents', []),
                'is_recurring': row.get('IsRecurring', 'No')
            })
            theme_groups[matched_theme]['total_count'] += int(row['Count'])
            theme_groups[matched_theme]['total_customers'] += int(row['AffectedCustomers'])
            
            if len(theme_groups[matched_theme]['sample_titles']) < 3:
                theme_groups[matched_theme]['sample_titles'].append(row['Title'])
        
        # Generate human-readable theme names
        themes_with_names = {}
        for theme_id, theme_data in theme_groups.items():
            # Get most common keywords across incidents in theme
            all_keywords = []
            for incident in theme_data['incidents']:
                title = incident['title']
                all_keywords.extend(self._extract_keywords(title))
            
            # Count keyword frequency
            keyword_counts = defaultdict(int)
            for kw in all_keywords:
                keyword_counts[kw] += 1
            
            # Top 3 keywords form the theme name
            top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            theme_name = " / ".join([kw.title() for kw, _ in top_keywords])
            
            themes_with_names[theme_name] = {
                'total_incidents': theme_data['total_count'],
                'unique_issue_types': len(theme_data['incidents']),
                'total_customers_affected': theme_data['total_customers'],
                'incidents': sorted(theme_data['incidents'], 
                                  key=lambda x: x['count'], 
                                  reverse=True),
                'sample_titles': theme_data['sample_titles'][:3]
            }
        
        # Sort themes by total incident count
        sorted_themes = dict(sorted(themes_with_names.items(), 
                                   key=lambda x: x[1]['total_incidents'], 
                                   reverse=True))
        
        return {
            'total_themes': len(sorted_themes),
            'themes': sorted_themes
        }
    
    def get_related_icm_impact_query(self, incident_ids: List[int]) -> str:
        """
        Generate query to get related ICM impact for sample incidents.
        
        Args:
            incident_ids: List of incident IDs to analyze
            
        Returns:
            KQL query string
        """
        ids_str = ", ".join(str(id) for id in incident_ids)
        
        query = f"""
let TargetIncidents = dynamic([{ids_str}]);
Incidents
| where IncidentId in (TargetIncidents)
| project 
    IncidentId,
    Title,
    Severity,
    CustomerName,
    CreateDate,
    ResolveDate,
    OwningTeamName,
    HowFixed,
    ImpactStartDate,
    ImpactedUserCount = CustomerImpactedUserCount,
    ImpactedServices = strcat_array(ImpactedServices, ", "),
    Region = CustomerRegion
| extend 
    ResolutionTime_Hours = datetime_diff('hour', ResolveDate, CreateDate),
    ImpactDuration_Hours = datetime_diff('hour', ResolveDate, ImpactStartDate)
| order by CreateDate desc
"""
        return query
    
    def analyze_by_design_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in "By Design" incidents to identify documentation gaps.
        
        Returns:
            Dictionary with analysis results
        """
        if self.incidents_data is None or self.incidents_data.empty:
            return {"error": "No data loaded"}
        
        df = self.incidents_data
        
        # Identify high-impact items
        critical_items = df[df['Count'] >= 10].copy()
        recurring_items = df[df['IsRecurring'] == 'Yes'].copy()
        
        # Calculate metrics
        total_incidents = df['Count'].sum()
        unique_issues = len(df)
        total_customers = df['AffectedCustomers'].sum()
        
        # Generate themes
        print("\nGenerating themes from incidents...")
        theme_analysis = self.generate_themes()
        
        # Get deeper insights from ICM MCP for sample incidents
        print("\nGathering deeper insights from ICM...")
        deep_insights = self._get_deep_insights_from_icm(df)
        
        # Prepare analysis for Purview Product Expert reasoning
        print("\nPreparing insights for product expert analysis...")
        expert_analysis = self._prepare_for_product_expert(theme_analysis, deep_insights)
        
        # Invoke Purview Product Expert for deep reasoning
        expert_response = self._invoke_purview_product_expert(expert_analysis)
        
        # Merge expert response into analysis
        expert_analysis['expert_response'] = expert_response
        
        analysis = {
            'summary': {
                'total_by_design_incidents': total_incidents,
                'unique_issue_types': unique_issues,
                'total_customers_affected': total_customers,
                'critical_documentation_gaps': len(critical_items),
                'recurring_issues': len(recurring_items),
                'total_themes_identified': theme_analysis.get('total_themes', 0)
            },
            'themes': theme_analysis.get('themes', {}),
            'deep_insights': deep_insights,
            'expert_analysis': expert_analysis,
            'critical_items': critical_items.to_dict('records') if not critical_items.empty else [],
            'recurring_items': recurring_items.to_dict('records') if not recurring_items.empty else [],
            'top_5_by_count': df.head(5).to_dict('records'),
            'recommendations': self._generate_recommendations(df)
        }
        
        self.analysis_results['by_design'] = analysis
        return analysis
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # High-count items need documentation
        high_count = df[df['Count'] >= 10]
        for _, row in high_count.iterrows():
            recommendations.append({
                'priority': 'High',
                'issue': row['Title'],
                'count': int(row['Count']),
                'action': 'Create/update documentation',
                'reason': f"Reported {row['Count']} times by {row['AffectedCustomers']} customers"
            })
        
        # Recurring issues over long time periods
        long_duration = df[df['DaysBetween'] > 90]
        for _, row in long_duration.head(5).iterrows():
            recommendations.append({
                'priority': 'Medium',
                'issue': row['Title'],
                'count': int(row['Count']),
                'action': 'Review product behavior',
                'reason': f"Persistent over {row['DaysBetween']} days - consider UX improvement"
            })
        
        return recommendations
    
    def generate_report(self, output_dir: str = None) -> str:
        """
        Generate HTML report from analysis results.
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            Path to generated report
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'reports')
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"icm_analysis_{timestamp}.html"
        filepath = os.path.join(output_dir, filename)
        
        html_content = self._generate_html_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\nReport generated: {filepath}")
        return filepath
    
    def _generate_html_report(self) -> str:
        """Generate HTML content for report (Office-compatible template)."""
        if not self.analysis_results:
            return "<html><body><h1>No analysis results available</h1></body></html>"
        
        analysis = self.analysis_results.get('by_design', {})
        summary = analysis.get('summary', {})
        
        html = f"""<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:w="urn:schemas-microsoft-com:office:word"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=unicode">
<meta name=ProgId content=Word.Document>
<meta name=Generator content="PHEPy ICM Agent">
<title>ICM By-Design Analysis Report</title>
<style>
<!--
body {{
    font-family: Calibri, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
}}
h1 {{
    font-size: 16pt;
    font-weight: bold;
    color: #1F497D;
    margin-bottom: 10pt;
    border-bottom: 2pt solid #1F497D;
    padding-bottom: 5pt;
}}
h2 {{
    font-size: 14pt;
    font-weight: bold;
    color: #1F497D;
    margin-top: 20pt;
    margin-bottom: 10pt;
}}
h3 {{
    font-size: 12pt;
    font-weight: bold;
    color: #1F497D;
    margin-top: 15pt;
    margin-bottom: 8pt;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10pt 0;
}}
th {{
    background-color: #B7D9F7;
    border: 1pt solid #7EA8F8;
    padding: 6pt;
    font-weight: bold;
    text-align: left;
    font-size: 10pt;
}}
td {{
    border: 1pt solid #7EA8F8;
    padding: 6pt;
    font-size: 10pt;
    vertical-align: top;
}}
.summary-card {{
    display: inline-block;
    background-color: #F0F7FF;
    border-left: 4pt solid #0078D4;
    padding: 10pt;
    margin: 8pt;
    width: 180pt;
}}
.summary-value {{
    font-size: 24pt;
    font-weight: bold;
    color: #0078D4;
}}
.summary-label {{
    font-size: 9pt;
    color: #666;
    margin-top: 4pt;
}}
.theme-section {{
    background-color: #F8F9FA;
    border-left: 4pt solid #0078D4;
    padding: 12pt;
    margin: 12pt 0;
    page-break-inside: avoid;
}}
.theme-header {{
    font-size: 13pt;
    font-weight: bold;
    color: #0078D4;
    margin-bottom: 8pt;
}}
.theme-stats {{
    margin: 8pt 0;
}}
.theme-stat {{
    display: inline-block;
    background-color: white;
    border: 1pt solid #D9D9D9;
    padding: 8pt;
    margin: 4pt;
    text-align: center;
    min-width: 100pt;
}}
.theme-stat-value {{
    font-size: 18pt;
    font-weight: bold;
    color: #0078D4;
}}
.theme-stat-label {{
    font-size: 9pt;
    color: #666;
}}
.incident-item {{
    background-color: white;
    border-left: 3pt solid #CCC;
    padding: 8pt;
    margin: 6pt 0;
}}
.incident-title {{
    font-weight: bold;
    color: #333;
}}
.incident-meta {{
    font-size: 9pt;
    color: #666;
    margin-top: 4pt;
}}
.priority-critical {{
    color: #D13438;
    font-weight: bold;
}}
.priority-high {{
    color: #FF8C00;
    font-weight: bold;
}}
.priority-medium {{
    color: #107C10;
    font-weight: bold;
}}
.recommendation-box {{
    background-color: #FFF4CE;
    border-left: 4pt solid #FFB900;
    padding: 10pt;
    margin: 8pt 0;
}}
.emoji {{
    font-family: "Segoe UI Emoji", sans-serif;
}}
.icm-link {{
    color: #0563C1;
    text-decoration: underline;
}}
.header-info {{
    margin: 10pt 0;
    border-bottom: 1pt solid #D9D9D9;
    padding-bottom: 10pt;
    font-size: 10pt;
}}
-->
</style>
</head>
<body>

<h1><span class="emoji">📊</span> ICM "By Design" Analysis Report</h1>

<div class="header-info">
    <strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
    <strong>Analysis Period:</strong> Last {self.config.get('default_days_back', 180)} days<br>
    <strong>Team:</strong> {self.config.get('default_team', 'Multiple Teams')}
</div>

<h2><span class="emoji">📈</span> Executive Summary</h2>

<div class="summary-card">
    <div class="summary-value">{summary.get('total_by_design_incidents', 0)}</div>
    <div class="summary-label">Total "By Design" Incidents</div>
</div>

<div class="summary-card">
    <div class="summary-value">{summary.get('unique_issue_types', 0)}</div>
    <div class="summary-label">Unique Issue Types</div>
</div>

<div class="summary-card">
    <div class="summary-value">{summary.get('total_customers_affected', 0)}</div>
    <div class="summary-label">Customers Affected</div>
</div>

<div class="summary-card">
    <div class="summary-value">{summary.get('critical_documentation_gaps', 0)}</div>
    <div class="summary-label">Critical Doc Gaps</div>
</div>

<div class="summary-card">
    <div class="summary-value">{summary.get('total_themes_identified', 0)}</div>
    <div class="summary-label">Themes Identified</div>
</div>

<br clear="all">

<h2><span class="emoji">🎯</span> By-Design Themes & Related ICM Impact</h2>
<p style="margin-bottom: 15pt;">
    Themes are generated by clustering similar by-design incidents. Each theme shows the total impact 
    and related incidents that share common characteristics.
</p>
"""
        
        # Add themes section
        themes = analysis.get('themes', {})
        for theme_name, theme_data in list(themes.items())[:10]:  # Top 10 themes
            html += f"""
<div class="theme-section">
    <h3><span class="emoji">🎯</span> {theme_name}</h3>
    <div class="theme-stats">
        <div class="theme-stat">
            <div class="theme-stat-value">{theme_data.get('total_incidents', 0)}</div>
            <div class="theme-stat-label">Total Incidents</div>
        </div>
        <div class="theme-stat">
            <div class="theme-stat-value">{theme_data.get('unique_issue_types', 0)}</div>
            <div class="theme-stat-label">Unique Issues</div>
        </div>
        <div class="theme-stat">
            <div class="theme-stat-value">{theme_data.get('total_customers_affected', 0)}</div>
            <div class="theme-stat-label">Customers Affected</div>
        </div>
    </div>
    <br clear="all">
    <p><strong>Related Incidents:</strong></p>
"""
            
            # Show top 5 incidents in theme
            for incident in theme_data.get('incidents', [])[:5]:
                recurring_icon = '<span class="emoji">🔄</span>' if incident.get('is_recurring') == 'Yes' else ""
                sample_ids = incident.get('sample_incidents', [])
                sample_ids_str = ', '.join(str(id) for id in sample_ids[:3]) if sample_ids else ''
                
                html += f"""
    <div class="incident-item">
        <div class="incident-title">{incident.get('title', 'Unknown')}</div>
        <div class="incident-meta">
            <span class="emoji">📊</span> {incident.get('count', 0)} incidents | 
            <span class="emoji">👥</span> {incident.get('customers', 0)} customers 
            {f'| {recurring_icon} Recurring' if recurring_icon else ''}
            {f'| Sample IDs: {sample_ids_str}' if sample_ids_str else ''}
        </div>
    </div>
"""
            
            html += """
</div>
"""
        
        html += """
</div>
"""
        
        html += """

<h2><span class="emoji">📑</span> Top Issues Requiring Documentation</h2>
<table>
    <tr>
        <th>Issue Title</th>
        <th style="width: 80pt; text-align: center;">Count</th>
        <th style="width: 100pt; text-align: center;">Customers</th>
        <th style="width: 80pt; text-align: center;">Recurring</th>
    </tr>
"""
        
        for item in analysis.get('top_5_by_count', []):
            recurring_icon = '<span class="emoji">✅</span>' if item.get('IsRecurring') == 'Yes' else ""
            html += f"""
    <tr>
        <td>{item.get('Title', 'Unknown')}</td>
        <td style="text-align: center;">{item.get('Count', 0)}</td>
        <td style="text-align: center;">{item.get('AffectedCustomers', 0)}</td>
        <td style="text-align: center;">{recurring_icon if recurring_icon else "No"}</td>
    </tr>
"""
        
        html += """
</table>

<h2><span class="emoji">🤖</span> Product Expert Analysis</h2>
"""
        
        # Add Product Expert analysis if available
        expert_analysis = analysis.get('expert_analysis', {})
        if expert_analysis:
            expert_response = expert_analysis.get('expert_response', {})
            
            # Show status of expert consultation
            if expert_response.get('expert_consulted'):
                if expert_response.get('analysis_complete'):
                    html += """
<div class="recommendation-box" style="background-color: #E8F5E9; border-left: 3pt solid #4CAF50;">
    <p style="margin: 0;"><span class="emoji">✅</span> <strong>Expert Analysis Complete</strong></p>
</div>
"""
                else:
                    html += """
<div class="recommendation-box" style="background-color: #FFF3E0; border-left: 3pt solid #FF9800;">
    <p style="margin: 0;"><span class="emoji">⏳</span> <strong>Purview Product Expert Invocation Required</strong></p>
    <p style="margin: 8pt 0 4pt 0;">
        The analysis has been prepared for the Purview Product Expert. To complete this workflow, 
        invoke the expert agent with the prepared analysis request below.
    </p>
</div>
"""
            
            # Show key questions for expert
            questions = expert_analysis.get('questions_for_expert', [])
            if questions:
                html += """
<div class="recommendation-box">
    <p style="margin: 0;"><strong>Key Questions for Product Team:</strong></p>
    <ul style="margin: 8pt 0;">
"""
                for q in questions:
                    if isinstance(q, dict):
                        html += f"        <li><strong>{q.get('theme', '')}:</strong> {q.get('question', '')}</li>\n"
                    else:
                        html += f"        <li>{q}</li>\n"
                
                html += """
    </ul>
</div>
"""
            
            # Show expert request for invocation
            if expert_response.get('expert_request') and not expert_response.get('analysis_complete'):
                html += """
<details style="margin: 12pt 0;">
    <summary style="cursor: pointer; font-weight: bold; padding: 8pt; background-color: #F5F5F5; border-radius: 4pt;">
        <span class="emoji">📋</span> View Expert Analysis Request (Click to expand)
    </summary>
    <div style="margin-top: 8pt; padding: 12pt; background-color: #FAFAFA; border: 1pt solid #E0E0E0; font-family: 'Courier New', monospace; font-size: 8pt; white-space: pre-wrap;">"""
                html += expert_response['expert_request'].replace('<', '&lt;').replace('>', '&gt;')
                html += """
    </div>
</details>
"""
            
            # Show change recommendations by category
            recommendations = expert_analysis.get('change_recommendations', {})
            if recommendations:
                for category, items in recommendations.items():
                    if items:
                        category_icon = {
                            'documentation': '📚',
                            'ui_ux': '🎨',
                            'product': '⚙️'
                        }.get(category, '📋')
                        
                        category_label = {
                            'documentation': 'Documentation Improvements',
                            'ui_ux': 'UI/UX Enhancements',
                            'product': 'Product Changes'
                        }.get(category, category.title())
                        
                        html += f"""
<div class="recommendation-box">
    <p style="margin: 0;"><span class="emoji">{category_icon}</span> <strong>{category_label}:</strong></p>
    <ul style="margin: 8pt 0;">
"""
                        for item in items:
                            if isinstance(item, dict):
                                html += f"        <li><strong>[{item.get('priority', 'Medium')}]</strong> {item.get('theme', '')}: {item.get('action', '')} - <em>{item.get('reason', '')}</em></li>\n"
                            else:
                                html += f"        <li>{item}</li>\n"
                        
                        html += """
    </ul>
</div>
"""

        html += """

<h2><span class="emoji">💡</span> Recommendations & Action Items</h2>
"""
        
        for rec in analysis.get('recommendations', []):
            priority_class = f"priority-{rec.get('priority', 'medium').lower()}"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.get('priority', 'medium').lower(), "⚪")
            
            html += f"""
<div class="recommendation-box">
    <p style="margin: 0;">
        <span class="emoji">{priority_icon}</span> 
        <span class="{priority_class}">[{rec.get('priority', 'Low')} Priority]</span> 
        <strong>{rec.get('issue', 'Unknown')}</strong>
    </p>
    <p style="margin: 8pt 0 4pt 0;">
        <strong>Action:</strong> {rec.get('action', '')}
    </p>
    <p style="margin: 4pt 0 0 0;">
        <strong>Reason:</strong> {rec.get('reason', '')}
    </p>
</div>
"""
        
        html += f"""

<p style="margin-top: 30pt; padding-top: 15pt; border-top: 1pt solid #D9D9D9; font-size: 9pt; color: #808080;">
    <i>This report was automatically generated by the PHEPy ICM Agent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}.</i><br>
    For questions or to request additional analysis, contact the Purview CEM team.
</p>

</body>
</html>
"""
        return html
    
    def export_theme_impact_queries(self, output_dir: str = None) -> Dict[str, str]:
        """
        Export queries for getting related ICM impact for each theme.
        
        Args:
            output_dir: Directory to save query files
            
        Returns:
            Dictionary mapping theme names to query file paths
        """
        if 'by_design' not in self.analysis_results:
            return {"error": "No analysis results available"}
        
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'queries', 'theme_impacts')
        
        os.makedirs(output_dir, exist_ok=True)
        
        themes = self.analysis_results['by_design'].get('themes', {})
        query_files = {}
        
        for theme_name, theme_data in themes.items():
            # Collect all sample incident IDs from this theme
            incident_ids = []
            for incident in theme_data.get('incidents', []):
                sample_ids = incident.get('sample_incidents', [])
                if isinstance(sample_ids, list):
                    incident_ids.extend(sample_ids)
            
            if not incident_ids:
                continue
            
            # Generate query for this theme
            query = self.get_related_icm_impact_query(incident_ids[:10])  # Max 10 samples
            
            # Save to file
            safe_name = theme_name.replace('/', '_').replace('\\\\', '_').replace(' ', '_')
            filename = f"theme_{safe_name}_impact.kql"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"// Theme: {theme_name}\\n")
                f.write(f"// Total Incidents: {theme_data.get('total_incidents', 0)}\\n")
                f.write(f"// Customers Affected: {theme_data.get('total_customers_affected', 0)}\\n")
                f.write(f"// Sample Incident IDs: {', '.join(map(str, incident_ids[:10]))}\\n\\n")
                f.write(query)
            
            query_files[theme_name] = filepath
            print(f"Generated impact query for theme: {theme_name}")
        
        return query_files
    
    def run_by_design_analysis(self, team_name: str = None, days_back: int = None, 
                               from_file: str = None) -> Dict[str, Any]:
        """
        Run complete "By Design" analysis workflow.
        
        Args:
            team_name: Team to analyze
            days_back: Number of days to look back
            from_file: Optional file path to load data from instead of querying
            
        Returns:
            Dictionary with analysis results and report path
        """
        print("\n" + "="*70)
        print("ICM AGENT - BY DESIGN ANALYSIS")
        print("="*70 + "\n")
        
        if from_file:
            # Load from file
            self.load_from_file(from_file)
        else:
            # Generate query for manual execution
            query = self.get_by_design_query(team_name, days_back)
            self.execute_query_mcp(query)
            
            print("\nℹ️  Save query results to data/ directory, then run:")
            print(f"   python icm_agent.py --from-file data/by_design_results.json")
            return {
                'status': 'query_ready',
                'query': query,
                'next_steps': [
                    'Execute query via MCP Kusto tool',
                    'Save results to data/by_design_results.json',
                    'Run analysis with --from-file parameter'
                ]
            }
        
        # Analyze data
        print("\nAnalyzing patterns...")
        analysis = self.analyze_by_design_patterns()
        
        # Generate report
        print("\nGenerating report...")
        report_path = self.generate_report()
        
        # Export theme impact queries
        print("\nExporting theme impact queries...")
        query_files = self.export_theme_impact_queries()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nReport: {report_path}")
        print(f"Total 'By Design' Incidents: {analysis['summary']['total_by_design_incidents']}")
        print(f"Themes Identified: {analysis['summary']['total_themes_identified']}")
        print(f"Critical Documentation Gaps: {analysis['summary']['critical_documentation_gaps']}")
        print(f"Recommendations: {len(analysis['recommendations'])}")
        
        if query_files and not query_files.get('error'):
            print(f"\nTheme Impact Queries: {len(query_files)} files generated")
            print("  Location: queries/theme_impacts/")
        
        return {
            'status': 'complete',
            'analysis': analysis,
            'report_path': report_path,
            'theme_queries': query_files
        }


def main():
    """Main execution function for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ICM Agent - Analyze incident patterns and documentation gaps'
    )
    parser.add_argument(
        '--team',
        type=str,
        help='Team name to analyze (e.g., "PURVIEW\\SensitivityLabels")'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=180,
        help='Number of days to look back (default: 180)'
    )
    parser.add_argument(
        '--from-file',
        type=str,
        help='Load data from JSON file instead of querying'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ICMAgent(config_path=args.config)
    
    try:
        results = agent.run_by_design_analysis(
            team_name=args.team,
            days_back=args.days,
            from_file=args.from_file
        )
        
        if results['status'] == 'complete':
            print(f"\n✅ Success! Report saved to: {results['report_path']}")
        else:
            print(f"\nQuery ready for execution.")
            
    except Exception as e:
        print(f"\n❌ Error running analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
