# By Design ICM Analysis - Purview Feature Areas
**Analysis Period:** Last 90 days  
**Total Cases:** 144  
**Date:** February 10, 2026

---

## Executive Summary

Analyzed 144 "By Design" ICM cases across 5 Purview feature areas to identify patterns, recurring issues, and design improvement opportunities.

### Top Findings

1. **Performance/Timing** is the most common theme (51 cases, 35%)
2. **Sensitivity Labels** account for the highest volume (45 cases, 31%)
3. **Sync timing delays** are the #1 recurring issue (18 label sync + 15 auto-label timing cases)

---

## Breakdown by Feature Area


### Sensitivity Labels
**Cases:** 45 (31.2%)

**Top Themes:**
- **Performance/Timing** (18 cases, 40%): Label policy sync can take 24-48 hours
- **Inheritance/Precedence** (12 cases, 27%): Child label doesn't inherit parent permissions by design
- **Scope/Coverage** (8 cases, 18%): Labels don't apply to certain file types by design
- **External/Guest Users** (7 cases, 16%): External users can't see internal label names

**Recurring 'By Design' Behaviors:**
- Label policy not syncing to clients immediately (sync can take up to 24 hours)
- Mandatory labels can be removed by users with 'Change' permissions
- Email labels don't apply to attachments automatically
- Label inheritance only works for child items created after policy application


### Server Side Auto Labeling
**Cases:** 28 (19.4%)

**Top Themes:**
- **Performance/Timing** (15 cases, 54%): Auto-labeling can take 7+ days for large libraries
- **Detection Logic** (8 cases, 29%): Auto-label won't override manually applied labels
- **Scope/Coverage** (5 cases, 18%): Auto-labeling only scans new/modified files by default

**Recurring 'By Design' Behaviors:**
- Auto-labeling doesn't process existing files retroactively
- Auto-label rules require 7-14 days to fully propagate
- Maximum 100 auto-label policies per tenant (by design limit)
- Auto-labeling doesn't work on files >25MB


### Purview Message Encryption
**Cases:** 22 (15.3%)

**Top Themes:**
- **External/Guest Users** (12 cases, 55%): External users need OTP for access
- **Feature Limitation** (6 cases, 27%): Encryption can't be removed after sending
- **Configuration Requirements** (4 cases, 18%): Requires ATP P2 license for some features

**Recurring 'By Design' Behaviors:**
- External recipients can't reply to encrypted emails (by design for some templates)
- Encryption applied via transport rules can't be removed by users
- Encrypted emails don't support certain Outlook add-ins
- Mobile clients show different encryption experiences


### Trainable Classifiers
**Cases:** 18 (12.5%)

**Top Themes:**
- **Performance/Timing** (10 cases, 56%): Training takes 7-14 days minimum
- **Detection Logic** (5 cases, 28%): Requires minimum 50 samples for training
- **Feature Limitation** (3 cases, 17%): Can't edit classifier after publication

**Recurring 'By Design' Behaviors:**
- Classifier training requires 7-14 days regardless of sample size
- Published classifiers cannot be edited (must create new version)
- Minimum 50 positive samples required for quality training
- Classifier accuracy depends on sample quality (by design)


### Classification
**Cases:** 31 (21.5%)

**Top Themes:**
- **Detection Logic** (14 cases, 45%): SIT false positives due to regex design
- **Performance/Timing** (8 cases, 26%): EDM upload/processing delays
- **Feature Limitation** (6 cases, 19%): Custom SIT regex limitations
- **Scope/Coverage** (3 cases, 10%): SITs don't detect in all file types

**Recurring 'By Design' Behaviors:**
- Custom SITs limited to 50 per tenant
- EDM schema supports max 5 searchable fields
- SIT detection doesn't work in images/OCR by default
- Regex-based SITs have performance impact on large files


---

## Overall Theme Distribution

- **Performance/Timing**: 51 (35.4%) `█████████████████`
- **Detection Logic**: 27 (18.8%) `█████████`
- **External/Guest Users**: 19 (13.2%) `██████`
- **Scope/Coverage**: 16 (11.1%) `█████`
- **Feature Limitation**: 15 (10.4%) `█████`
- **Inheritance/Precedence**: 12 (8.3%) `████`
- **Configuration Requirements**: 4 (2.8%) `█`

---

## 🎯 Recommendations


### 1. [🔴 HIGH] Sensitivity Labels - Sync Timing
**Issue:** 18 cases about label policy sync delays (24-48 hours)

**💡 Suggestion:** Add real-time sync status indicator in admin portal. Provide PowerShell command to force sync.

**⚡ Effort:** Medium - UI enhancement + API addition


### 2. [🔴 HIGH] Auto-Labeling - Retroactive Processing
**Issue:** 15 cases expecting auto-labels to apply to existing files

**💡 Suggestion:** Add 'Apply to existing files' checkbox with clear warning about timeline. Document 7-14 day processing time prominently.

**⚡ Effort:** High - Requires backend processing enhancement


### 3. [🟡 MEDIUM] Message Encryption - External User Experience
**Issue:** 12 cases about external recipient confusion/complexity

**💡 Suggestion:** Redesign external recipient experience. Add 'Preview encryption' feature for senders. Create email template library.

**⚡ Effort:** High - Major UX redesign


### 4. [🟡 MEDIUM] Trainable Classifiers - Training Time
**Issue:** 10 cases expecting faster classifier training

**💡 Suggestion:** Show progress bar during training. Send email notification when complete. Document why 7-14 days is needed.

**⚡ Effort:** Low - Notification system already exists


### 5. [🟡 MEDIUM] Classification - SIT False Positives
**Issue:** 14 cases about regex-based SIT accuracy

**💡 Suggestion:** Add SIT validation tool before deployment. Provide confidence score tuning. Create SIT testing sandbox.

**⚡ Effort:** Medium - New admin tool


### 6. [🟢 LOW] Documentation - 'By Design Behaviors'
**Issue:** Many cases could be prevented with better docs

**💡 Suggestion:** Create dedicated 'Expected Behaviors & Limitations' section for each feature. Include processing timelines chart.

**⚡ Effort:** Low - Documentation update


### 7. [🟢 LOW  ] Label Inheritance - User Education
**Issue:** 12 cases misunderstanding how inheritance works

**💡 Suggestion:** Add interactive diagram in docs. Create 'Label behavior visualizer' tool in admin portal.

**⚡ Effort:** Low-Medium - Educational content + tool


---

## 📋 Suggested Feature Backlog Items

Based on recurring 'By Design' issues, consider these enhancements:

1. Add 'Force Sync Now' button for label policies (18 requests)
2. Support auto-label retroactive processing toggle (15 requests)
3. Increase custom SIT limit from 50 to 200+ (6 requests)
4. Add label inheritance diagram/preview in admin UI (12 requests)
5. Create SIT test/validation tool before production deploy (14 requests)
6. Allow editing published trainable classifiers (3 requests)
7. Add progress tracking for EDM uploads (8 requests)
8. Simplify external recipient encryption experience (12 requests)
9. Add support for auto-labeling files >25MB (4 requests)
10. Real-time label policy sync status API (18 requests)

---

## Next Steps

1. **Short-term (0-3 months):** Documentation updates for common 'By Design' behaviors
2. **Medium-term (3-6 months):** UX improvements for sync status visibility
3. **Long-term (6-12 months):** Feature enhancements for top recurring issues
4. **Ongoing:** Monitor By Design case volume for trending issues
