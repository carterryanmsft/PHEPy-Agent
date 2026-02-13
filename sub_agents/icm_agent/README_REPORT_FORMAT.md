# Documentation Gap Analysis - Report Format (LOCKED)

## Approved Format
**Date Locked:** February 11, 2026  
**Version:** 1.0  
**Status:** ✅ APPROVED

## Report Structure

### 1. Header Section
- Title: "Documentation Gap Analysis"
- Subtitle: "Executive Summary - MIP/DLP 'By Design' Prevention Type: Public Documentation"
- Generation timestamp

### 2. Statistics Cards (4 cards)
- Total ICMs Analyzed
- Major Themes
- Specific Doc Gaps
- Doc Pages to Create/Update

### 3. Executive Summary Table
**Columns:**
- Theme (25%)
- Priority (15%) - Color coded: HIGH (red), MEDIUM (yellow), LOW (green)
- ICMs (10%) - Count
- What's Missing (50%)

### 4. Detailed Theme Sections
For each theme:

**A. Customer Confusion Examples Table**
- Columns: ICM ID (clickable link) | Issue Title | Customer Question/Confusion | Team
- Shows top 5 ICMs per theme

**B. Required Actions Section**
- Ordered list (numbered)
- Specific documentation pages to create/update
- Clear, actionable items

### 5. Implementation Roadmap Table
**Columns:**
- Phase (20%)
- Timeline (15%)
- Effort (15%)
- Deliverables (50%)

**Phases:**
1. Quick Wins (1-2 weeks, Low effort)
2. New Reference Pages (2-4 weeks, Medium effort)
3. Examples & Samples (1-2 months, Medium-High effort)
4. Product Enhancements (2-3 months, High effort)

### 6. Documentation Pages Summary Table
**Columns:**
- Documentation Page (40%)
- Action (15%) - CREATE NEW / UPDATE / ENHANCE
- Priority (15%) - Color coded
- Key Content (30%)

## Styling Rules

### Colors
- Primary Blue: `#0078d4`
- Secondary Blue: `#106ebe`
- High Priority: `#d13438` (Red background: `#fde7e9`)
- Medium Priority: `#8a5a00` (Yellow background: `#fff4ce`)
- Low Priority: `#107c10` (Green background: `#dff6dd`)
- Background: `#f5f5f5`

### Typography
- Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- H1: 2.5em
- H2: 1.8em (with bottom border)
- H3: 1.4em
- Body: 1.6 line-height

### Layout
- Max width: 1400px
- Padding: 20px
- Border radius: 8-10px for cards
- Box shadow: 0 2px 10px rgba(0,0,0,0.1)

### Tables
- Full width
- Header: Blue background (#0078d4), white text
- Row hover: #f9f9f9
- Border: 1px solid #e1e1e1

## Generation Script

**Primary Script:** `generate_executive_summary.py`

**Usage:**
```bash
cd sub_agents/icm_agent
python generate_executive_summary.py
```

**Output:** 
- `reports/executive_summary_YYYYMMDD_HHMMSS.html`
- Automatically opens in default browser

## Key Features

✅ **No emojis** - Professional, clean formatting  
✅ **All tables** - Easy to scan and follow  
✅ **Clickable links** - ICM portal links, documentation pages  
✅ **Color-coded priorities** - Visual indicators  
✅ **Specific actions** - Clear next steps per theme  
✅ **Responsive design** - Works on different screen sizes  

## Files

- **Template Script:** `generate_executive_summary.py`
- **Latest Report:** `FINAL_Executive_Summary_Documentation_Gaps.html`
- **Data Source:** `data/public_doc_icms/icm_details_with_themes.json`

## Notes

This format has been approved for:
- Executive presentations
- Documentation team reviews
- Stakeholder updates
- Project planning

Do not modify the core structure without approval.
