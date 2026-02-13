# Weekly "Try It" - Continuous Improvement Activities

**Purpose:** Lightweight, actionable micro-practices to build continuous improvement into daily workflows. Each activity takes 5-15 minutes and can be applied to recurring work.

**Instructions for Agent:** When users ask for continuous improvement suggestions, weekly practices, or ways to improve their workflow, recommend activities from this list based on their context and recent work patterns. Suggest one activity per week and help track their progress.

---

## How to Use This Document

**As an Agent:**
1. When asked about improvements, suggest relevant activities from the categories below
2. Consider the user's recent work context to recommend the most relevant activity
3. Help users log completed activities using: `python continuous_improvement_tracker.py log --week X --notes "notes"`
4. Periodically suggest checking progress: `python continuous_improvement_tracker.py status`
5. Link improvements to their actual work (e.g., "I noticed you worked on ICM incidents this week - Week 2's root cause analysis might help")

**Activity Selection Tips:**
- **New to CI:** Start with Week 1 (5-Minute Reflection) or Week 13 (Celebrate a Win)
- **Documentation gaps:** Weeks 3, 11, 16, 18, 26
- **Process friction:** Weeks 4, 7, 9, 10, 20, 22
- **Experimentation:** Weeks 5, 12, 14, 19, 25
- **Team collaboration:** Weeks 8, 13, 15, 21, 24
- **Reflection & analysis:** Weeks 1, 2, 6, 17, 23, 27

---

## Activities by Category

### 🔍 Reflection & Learning

**Week 1: The 5-Minute Reflection**
- **Activity:** At the end of your day, jot down one thing that went well and one thing you'd improve tomorrow
- **Why:** Small improvements lead to big changes
- **Time:** 5 minutes
- **Prompt for agent:** "Help me do a 5-minute reflection on today's work"

**Week 2: Ask "Why?" Five Times**
- **Activity:** Pick a recurring issue and dig into its root cause using the 5 Whys technique
- **Why:** Surface hidden root causes beyond surface symptoms
- **Time:** 10-15 minutes
- **Prompt for agent:** "Guide me through a 5 Whys analysis on [recurring issue]"

**Week 6: Try a 10-Minute Retrospective**
- **Activity:** Reflect on a recent project or task. What went well? What could improve?
- **Why:** Learn from recent experiences while they're fresh
- **Time:** 10 minutes
- **Prompt for agent:** "Help me do a quick retrospective on [project/task]"

**Week 17: Revisit a Past Mistake**
- **Activity:** Reflect on a past misstep and identify what you learned from it
- **Why:** Turn failures into learning opportunities
- **Time:** 10 minutes
- **Prompt for agent:** "Help me reflect on [past incident/mistake] and extract lessons"

**Week 23: Use a Feedback Grid**
- **Activity:** Try "Start, Stop, Continue" to reflect on a recent effort
- **Why:** Structured reflection reveals actionable insights
- **Time:** 10 minutes
- **Prompt for agent:** "Create a Start/Stop/Continue grid for [recent work]"

**Week 27: End the Week with a Win**
- **Activity:** On Friday, write down one improvement you made this week
- **Why:** Celebrate progress and build momentum
- **Time:** 5 minutes
- **Prompt for agent:** "Help me identify my improvement wins from this week"

---

### 📋 Process Documentation

**Week 3: Document One Process**
- **Activity:** Choose a task you do often and write down the steps. Share it with a teammate
- **Why:** Explicit knowledge beats tribal knowledge
- **Time:** 15 minutes
- **Prompt for agent:** "Help me document the process for [recurring task]"

**Week 11: Use a Checklist**
- **Activity:** Create a checklist for a recurring task to reduce errors and save time
- **Why:** Checklists prevent mistakes and reduce cognitive load
- **Time:** 10 minutes
- **Prompt for agent:** "Create a checklist for [task]"

**Week 16: Create a "How-To" Snippet**
- **Activity:** Write a short tip or trick and share it with your team
- **Why:** Scale knowledge across the team
- **Time:** 5 minutes
- **Prompt for agent:** "Help me write a quick how-to for [tip/trick]"

**Week 18: Visualize a Process**
- **Activity:** Sketch out a workflow or decision tree to spot inefficiencies
- **Why:** Visual representation reveals hidden complexity
- **Time:** 15 minutes
- **Prompt for agent:** "Help me create a flowchart for [process]"

**Week 26: Do a "Walkthrough"**
- **Activity:** Explain a process to someone new and note where they get confused
- **Why:** Fresh eyes reveal unclear steps
- **Time:** 15 minutes
- **Prompt for agent:** "Help me create an onboarding walkthrough for [process]"

---

### ⚙️ Process Optimization

**Week 4: Declutter One Process**
- **Activity:** Choose a workflow you use regularly. Eliminate one unnecessary step or simplify one part of it
- **Why:** Less complexity = less friction
- **Time:** 10 minutes
- **Prompt for agent:** "Analyze [workflow] and suggest simplifications"

**Week 7: Eliminate One Friction Point**
- **Activity:** Identify a small annoyance in your workflow and fix or simplify it
- **Why:** Death by a thousand paper cuts—fix one cut at a time
- **Time:** 10 minutes
- **Prompt for agent:** "Help me identify and eliminate friction in [workflow]"

**Week 9: Automate One Repetitive Task**
- **Activity:** Use a rule, template, or shortcut to save time on a recurring task
- **Why:** Manual repetition is waste
- **Time:** 15 minutes
- **Prompt for agent:** "Help me automate [repetitive task]"

**Week 10: Create a "Stop Doing" List**
- **Activity:** Identify one habit or task that no longer adds value and stop doing it
- **Why:** Saying no is as important as saying yes
- **Time:** 5 minutes
- **Prompt for agent:** "Help me identify non-value-add activities in my workflow"

**Week 20: Update a Template**
- **Activity:** Improve a document or deck template you use often
- **Why:** Better inputs create better outputs
- **Time:** 10 minutes
- **Prompt for agent:** "Help me improve [template/document]"

**Week 22: Try a "Before & After"**
- **Activity:** Improve a small process and compare the results
- **Why:** Evidence beats opinion
- **Time:** 15 minutes
- **Prompt for agent:** "Help me measure the before/after of [process improvement]"

---

### 🧪 Experimentation

**Week 5: One Small Experiment**
- **Activity:** Hypothesize a new way of doing a routine task then try it out. Track what changes—time saved, fewer errors, better results?
- **Why:** Learning by doing beats analysis paralysis
- **Time:** Variable
- **Prompt for agent:** "Help me design an experiment to improve [routine task]"

**Week 12: Try a New Tool or Feature**
- **Activity:** Explore a feature in a tool you use daily that you've never tried before
- **Why:** You're probably only using 20% of your tools' capabilities
- **Time:** 10 minutes
- **Prompt for agent:** "Suggest underutilized features in [tool] for my workflows"

**Week 14: Ask "What If?"**
- **Activity:** Identify a current pain point or opportunity and ask "How might we do this differently?"
- **Why:** Questions unlock innovation
- **Time:** 10 minutes
- **Prompt for agent:** "Help me brainstorm alternatives for [pain point]"

**Week 19: Try a "Silent Brainstorm"**
- **Activity:** Generate ideas individually before discussing as a group
- **Why:** Avoid groupthink and amplify quiet voices
- **Time:** 10 minutes
- **Prompt for agent:** "Guide me through a structured brainstorm for [problem]"

**Week 25: Try a "One-Minute Fix"**
- **Activity:** Spend 60 seconds improving something small but annoying
- **Why:** Momentum breeds momentum
- **Time:** 1 minute
- **Prompt for agent:** "What's a quick 1-minute improvement I can make right now?"

---

### 🤝 Collaboration & Feedback

**Week 8: Ask for Feedback**
- **Activity:** Request quick feedback from a peer on something you're working on
- **Why:** Outside perspective reveals blind spots
- **Time:** 10 minutes
- **Prompt for agent:** "Help me draft a feedback request for [work item]"

**Week 13: Celebrate a Small Win**
- **Activity:** Acknowledge a recent improvement or success, no matter how small
- **Why:** Positive reinforcement drives behavior
- **Time:** 5 minutes
- **Prompt for agent:** "Help me identify and celebrate recent wins"

**Week 15: Shadow a Colleague**
- **Activity:** Spend 15 minutes learning how someone else approaches a shared task
- **Why:** Different approaches teach new tricks
- **Time:** 15 minutes
- **Prompt for agent:** "Create a shadowing plan for learning [skill/process] from a colleague"

**Week 21: Ask "What's the Value?"**
- **Activity:** For one task, identify who your customer is and ask "What do they value?"
- **Why:** Customer focus prevents busywork
- **Time:** 10 minutes
- **Prompt for agent:** "Help me analyze the customer value of [task]"

**Week 24: Create a Quick Survey**
- **Activity:** Ask your team one question to gather improvement ideas
- **Why:** Crowdsource insights
- **Time:** 5 minutes
- **Prompt for agent:** "Help me draft a team survey question about [topic]"

---

## Agent Response Templates

### When suggesting an activity:
```
I noticed you're working on [context]. This might be a good time to try:

**Week [X]: [Activity Title]**
🎯 Activity: [Description]
⏱️ Time: [Duration]
💡 Why: [Benefit]

Would you like me to guide you through this? When you're done, you can log it:
`python continuous_improvement_tracker.py log --week X --notes "Your reflection"`
```

### When checking on progress:
```
Let's see your continuous improvement progress:
`python continuous_improvement_tracker.py status`

Would you like a suggestion for this week's activity?
```

### When helping reflection:
```
Great! Let's reflect on [topic]. I'll ask you a few questions:
1. [Relevant question based on activity]
2. [Follow-up question]
3. [Action-oriented question]

Based on your answers, here's what I'm capturing:
[Summary and insights]

Ready to log this? Use:
`python continuous_improvement_tracker.py log --week X --notes "[summary]" --impact "[measured outcome]"`
```

---

## Integration with Daily Work

**Context-Aware Suggestions:**
- Working on ICMs all day → Suggest Week 2 (5 Whys) or Week 6 (Retrospective)
- Managing support cases → Suggest Week 3 (Document Process) or Week 11 (Checklist)
- Friday afternoon → Suggest Week 27 (End with a Win)
- Frustrated with tools → Suggest Week 7 (Eliminate Friction) or Week 12 (Try New Feature)
- Team meeting scheduled → Suggest Week 15 (Shadow Colleague) or Week 24 (Quick Survey)
- Building reports → Suggest Week 20 (Update Template) or Week 4 (Declutter Process)

**Tracking Milestones:**
- After 5 activities: "You're building momentum! 🎯"
- After 10 activities: "Halfway there! Notice any patterns in what's working?"
- After 20 activities: "You're a continuous improvement champion! 🏆"
- After 27 activities: "All activities completed! Time to repeat your favorites or create custom ones."

---

## Success Metrics

Track these outcomes over time:
- ✅ Number of processes documented
- ⏱️ Time saved through automation  
- 🔧 Friction points eliminated
- 🧪 Experiments conducted
- 🔄 Feedback loops established
- 📚 Knowledge shared with team

---

**For full details, see:** `docs/CONTINUOUS_IMPROVEMENT_WEEKLY.md`  
**Tracking tool:** `continuous_improvement_tracker.py`  
**Last Updated:** February 11, 2026
