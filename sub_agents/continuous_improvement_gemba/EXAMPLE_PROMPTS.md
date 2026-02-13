# CI/Gemba Walker - Example Prompts

**Agent:** Continuous Improvement & Gemba Walker  
**Last Updated:** February 4, 2026

---

## 🎯 Gemba Walk Prompts

### General Process Observation
```
Conduct a gemba walk of the [support case / escalation / onboarding] process
```

```
Observe how [process X] actually works using the last [30/60/90] days of data
```

```
Show me what really happens in [process] vs what's documented
```

### Specific Process Areas
```
Walk through the lifecycle of a typical support case
```

```
Observe how P1 escalations flow through ICM
```

```
Show me the actual onboarding process for MCS customers
```

---

## 🗑️ Waste Identification Prompts

### General Waste Hunting
```
What wastes exist in the [process name]?
```

```
Where is time being wasted in [workflow]?
```

```
Identify the 8 wastes in our support process
```

### Specific Waste Types
```
Where are cases waiting the longest? (Waiting waste)
```

```
How often are cases reopened or misrouted? (Defect waste)
```

```
How many handoffs occur per case? (Transportation waste)
```

```
What work are we doing that doesn't add value? (Overproduction)
```

```
Where do we have backlogs and pile-ups? (Inventory waste)
```

```
How much context switching occurs? (Motion waste)
```

```
What steps are redundant or duplicated? (Extra Processing)
```

```
Are people's skills being used effectively? (Non-Utilized Talent)
```

---

## 🔍 Root Cause Analysis Prompts

### 5-Whys
```
Why is [problem X] happening? (use 5-Whys)
```

```
What's the root cause of [high reopen rate / slow resolution / escalations]?
```

```
Drill down to the fundamental cause of [issue]
```

### Fishbone/Ishikawa
```
What factors contribute to [problem]? (use fishbone)
```

```
Analyze [issue] using the 6Ms framework
```

```
What are all the possible causes of [performance problem]?
```

### Pattern Analysis
```
What patterns exist across [cases / incidents / escalations]?
```

```
What do all [reopened cases / delayed escalations] have in common?
```

```
Find common factors in [problem category]
```

---

## 📊 Value Stream Mapping Prompts

### Current State
```
Create a value stream map for [process]
```

```
Map the current state of [case resolution / escalation / onboarding]
```

```
Show me the end-to-end flow of [process] with cycle times
```

```
What's the process efficiency of [workflow]?
```

### Metrics & Analysis
```
Calculate cycle time for each step in [process]
```

```
Where does [process] spend the most time?
```

```
What's the ratio of value-add to non-value-add time?
```

```
How much time is spent waiting vs. working?
```

### Future State
```
Design an improved [process] with waste eliminated
```

```
What would an optimized [workflow] look like?
```

```
How can we reduce [process] cycle time by 50%?
```

---

## 💡 Improvement Recommendation Prompts

### Quick Wins
```
What quick wins can improve [process]?
```

```
What low-effort, high-impact changes can we make?
```

```
What can we fix in the next 2 weeks?
```

### Strategic Improvements
```
What major changes would transform [process]?
```

```
What strategic improvements should we prioritize?
```

```
How can we fundamentally improve [workflow]?
```

### Impact Estimation
```
If we [change X], what's the impact?
```

```
Estimate the ROI of [improvement idea]
```

```
How much time would we save by [eliminating handoffs / automating X]?
```

---

## 🎭 DIVE Framework Prompts

### Full DIVE Analysis
```
Use DIVE to analyze [problem]
```

```
Apply the DIVE framework to improve [process]
```

```
Guide me through DIVE for [issue]
```

### By Phase
```
Help me define the problem with [issue] (DIVE: Define)
```

```
Investigate root causes of [problem] (DIVE: Investigate)
```

```
Verify that [solution] will work (DIVE: Verify)
```

```
Execute improvement plan for [process] (DIVE: Execute)
```

---

## 📈 Metrics & Measurement Prompts

### Baseline Metrics
```
What are the baseline metrics for [process]?
```

```
Measure current performance of [workflow]
```

```
What's our starting point for [improvement initiative]?
```

### Before/After Comparison
```
Compare [metric] before and after [improvement]
```

```
Has [improvement] been effective?
```

```
Show me the impact of [change] on [process]
```

### Benchmarking
```
How does our [metric] compare to best practices?
```

```
What's world-class performance for [process efficiency]?
```

```
Are we meeting industry standards?
```

---

## 🎯 Prioritization Prompts

### Effort vs Impact
```
Prioritize improvements by effort vs impact
```

```
What should we tackle first?
```

```
Rank these improvements: [list]
```

### Resource Allocation
```
Where should we focus improvement efforts?
```

```
What will give us the biggest bang for our buck?
```

```
What's the highest leverage improvement?
```

---

## 🔄 Kaizen Event Prompts

### Event Planning
```
Plan a kaizen event for [process]
```

```
Design a 1-week improvement sprint for [workflow]
```

```
What should we include in a kaizen for [issue]?
```

### Event Execution
```
We're in Day 2 of kaizen. What should we investigate?
```

```
Help us prioritize kaizen findings
```

```
Create action items from our kaizen event
```

---

## 🎭 Complex Multi-Agent Scenarios

### Gemba + Health Monitoring
```
Conduct a gemba of support process and check if improvements are working
```
*Routes to: CI/Gemba → Support Case Manager → Tenant Health Monitor*

---

### Root Cause + Product Issues
```
Why are cases taking longer? Is it a product issue or process issue?
```
*Routes to: CI/Gemba → Support Case Manager → Purview Product Expert*

---

### Improvement + Escalation
```
Analyze escalation process waste and recommend improvements
```
*Routes to: CI/Gemba → Escalation Manager → Kusto Expert*

---

### VSM + Multiple Data Sources
```
Create value stream map using case data, ICM data, and ADO data
```
*Routes to: CI/Gemba → Jacques → Support Case Manager → Escalation Manager*

---

## 💡 Pro Tips

### Be Specific About Process
❌ "Improve efficiency"  
✅ "Conduct gemba walk of case resolution process from open to close"

### Include Time Range
❌ "Show me waste"  
✅ "Identify waste in the last 30 days of support cases"

### Specify Desired Output
❌ "Analyze this"  
✅ "Create value stream map with cycle times and wait times for escalation process"

### Ask for Quantification
❌ "What's wrong?"  
✅ "Quantify the impact of excessive handoffs on case resolution time"

---

## 📚 Related Agents

- **Kusto Expert (Jacques)** - Provides metrics and telemetry for analysis
- **Support Case Manager** - Case lifecycle data for gemba walks
- **Escalation Manager** - ICM process data
- **Tenant Health Monitor** - Before/after improvement validation
- **Work Item Manager** - Development process analysis

---

## 🆘 Need Help?

### Understanding Concepts
```
Explain the 8 wastes with examples from PHE
```

```
What is value stream mapping?
```

```
How does the DIVE framework work?
```

### Getting Started
```
I want to improve [process]. Where do I start?
```

```
What data do I need for a gemba walk?
```

```
How do I calculate process efficiency?
```

---

## 📋 Common Workflows

### Weekly Process Review
1. "Conduct gemba walk of last week's support cases"
2. "Identify top 3 wastes"
3. "Recommend 2 quick wins"

### Monthly Improvement Initiative
1. "Use DIVE to analyze [chronic problem]"
2. "Create value stream map of [process]"
3. "Design future state with improvements"
4. "Estimate ROI and create implementation plan"

### Quarterly Kaizen Event
1. "Plan kaizen event for [process improvement]"
2. "Execute gemba walks and root cause analysis"
3. "Prioritize improvements by impact"
4. "Track metrics for 90 days post-implementation"
