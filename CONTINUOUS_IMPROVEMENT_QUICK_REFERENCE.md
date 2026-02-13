# 🔄 Continuous Improvement Quick Reference Card

**Use these prompts to activate continuous improvement coaching with your agent:**

---

## 🎯 Getting Started

```
"Show me my continuous improvement progress"
"Suggest a continuous improvement activity for this week"
"Help me build better work habits"
```

---

## 📊 Check Your Progress

```
python continuous_improvement_tracker.py status
python continuous_improvement_tracker.py suggest
python continuous_improvement_tracker.py list
```

---

## 💬 Context-Aware Prompts

**After finishing work:**
```
"I just finished [task/incident]. Any continuous improvement suggestions?"
"Help me reflect on what just happened"
"What's worth documenting from this?"
```

**When frustrated:**
```
"This workflow is annoying. Help me improve it"
"I do this task all the time. Can we simplify it?"
"What friction points can I eliminate?"
```

**For documentation:**
```
"Help me document [process]"
"Create a checklist for [recurring task]"
"Visualize the workflow for [process]"
```

**On Fridays:**
```
"What's my continuous improvement win this week?"
"Help me do a weekly reflection"
"End the week with a win"
```

---

## 🎓 Guided Activities

**Root Cause Analysis:**
```
"Guide me through a 5 Whys analysis on [issue]"
"Help me understand why [recurring problem] keeps happening"
```

**Process Optimization:**
```
"Analyze [workflow] and suggest simplifications"
"Help me automate [repetitive task]"
"What can I stop doing?"
```

**Team Collaboration:**
```
"Help me draft a feedback request for [work]"
"Create a quick survey for the team about [topic]"
"What value does [task] provide to customers?"
```

**Experimentation:**
```
"Design an experiment to improve [routine task]"
"What unexplored features in [tool] could help me?"
"Brainstorm alternatives for [pain point]"
```

---

## 📝 Logging Activities

```
python continuous_improvement_tracker.py log --week 1 --notes "Daily reflection: improved ICM response time"

python continuous_improvement_tracker.py log --week 9 --notes "Automated report generation" --impact "Saves 2 hours per week"
```

---

## 🎯 Weekly Activity Categories

**🔍 Reflection & Learning:** Weeks 1, 2, 6, 17, 23, 27  
**📋 Process Documentation:** Weeks 3, 11, 16, 18, 26  
**⚙️ Process Optimization:** Weeks 4, 7, 9, 10, 20, 22  
**🧪 Experimentation:** Weeks 5, 12, 14, 19, 25  
**🤝 Collaboration & Feedback:** Weeks 8, 13, 15, 21, 24  

---

## 💡 Pro Tips

**Let the agent be proactive:**
- The agent monitors your work patterns
- Suggestions come at natural break points
- Context-aware based on what you just did

**Make it a habit:**
- One activity per week is plenty
- Friday check-ins build momentum
- Track impact to see compound gains

**Integrate with work:**
- After incidents → Root cause analysis
- After projects → Retrospectives
- When stuck → Simplify processes
- With team → Collaboration activities

---

## 📚 Full Documentation

- **All activities:** [docs/CONTINUOUS_IMPROVEMENT_WEEKLY.md](../docs/CONTINUOUS_IMPROVEMENT_WEEKLY.md)
- **Agent instructions:** [grounding_docs/continuous_improvement/AGENT_PROMPT.md](grounding_docs/continuous_improvement/AGENT_PROMPT.md)
- **Activity details:** [grounding_docs/continuous_improvement/weekly_try_it_activities.md](grounding_docs/continuous_improvement/weekly_try_it_activities.md)

---

**Start now:** `"Suggest a continuous improvement activity for this week"`
