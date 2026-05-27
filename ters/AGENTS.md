# AGENT RULES

## Core Workflow

When a new blink event is added:

1. read the event JSON
2. inspect raw conductance and Raman data
3. refine blink boundaries
4. compare against historical events
5. identify similarities and contradictions
6. suggest possible physical interpretations
7. propose updates to markdown notes

---

## Event Refinement Rules

The AI should:

- refine coarse windows into more precise boundaries
- detect conductance lead/lag relative to Raman
- identify shoulders, tails, substates
- distinguish single events from split events

The AI should preserve uncertainty when evidence is weak.

---

## Synchronization Rules

Conductance and Raman acquisition are independent systems.

The AI should assume:

- different sampling rates
- unstable inter-system offsets
- potential drift over time
- possible Raman timestamp discontinuities

Therefore:

- refine current and Raman boundaries independently first
- treat lag as local tendency, not absolute physical truth
- avoid over-interpreting small onset/offset differences
- store uncertainty explicitly in event JSON

Suggested lag fields:

- observed_local_lag_s
- absolute_lag_uncertain
- offset_stability_unknown

---

## Critic Mode

The AI should not blindly agree with human labels.

The AI should explicitly flag:

- contradictory labels
- weak evidence
- ambiguous boundaries
- possible artifacts
- possible over-interpretation

---

## Knowledge Maintenance

When new evidence changes an interpretation:

- append new observations
- preserve historical interpretations
- avoid destructive overwrites

---

## Repository Persistence

Treat GitHub as the durable source of truth for this project.

Use the local workspace as a working copy for reading, analysis,
validation, and temporary edits.

When a completed task changes project files:

- commit the durable changes back to GitHub by default
- group related edits into a coherent commit
- do not wait for a final computer-switching handoff unless the user asks
- keep exploratory scratch work local unless it becomes part of the project record

---

## Wiki Operations

When maintaining the markdown wiki, follow three operations:

1. ingest
2. query
3. lint

Ingest:

- summarize new source pages
- update relevant entity/concept/event pages
- update index.md
- append one entry to log.md

Query:

- answer from wiki pages first
- cite the pages used
- file high-value answers back into wiki as new pages when useful

Lint:

- flag contradictions
- flag stale claims
- find orphan pages
- suggest missing cross-links and missing concept pages

---

## Retrieval Behavior

Before analyzing a blink event:

1. read SYSTEM_ARCHITECTURE.md
2. read CURRENT_STATE.md
3. read index.md
4. retrieve relevant markdown notes
5. retrieve similar historical events
6. check recent log.md entries
7. synthesize reasoning

---

## Trigger Conditions and Priority

For this project, prefer explicit triggers over implicit guessing.

Priority order:

1. Safety and non-destructive history rules.
2. Retrieval behavior (architecture + current state + index + log).
3. Synchronization rules (independent boundary refinement first).
4. Event refinement and critic mode outputs.
5. Wiki maintenance updates (index/log/page edits).

Trigger rules:

- If user provides a new event window or event files:
  run full event analysis workflow and produce/update event JSON + analysis markdown.
- If user asks to ingest a new source:
  run ingest workflow and update index/log.
- If user asks a scientific question:
  run query workflow from wiki first, then optional raw-source drilldown.
- If user asks for consistency check:
  run lint workflow and append findings to log.

When instructions conflict:

- follow explicit user instruction first
- preserve uncertainty rather than forcing precision
- never overwrite historical conclusions silently

---

## Skill Evolution Policy

Avoid uncontrolled proliferation of new skills.

Prefer integrating new observations into:

- existing skills
- existing taxonomy notes
- existing mechanism notes

Only create a new skill when a fundamentally new capability is required.

High-level skill examples:

- transport_raman_analysis
- artifact_detection
- retrieval_and_memory
- junction_state_transition_analysis

Keep mechanism-level concepts as notes, not standalone skills:

- weak_hotspot_overlap
- delayed_raman_onset
- shoulder_states
- dark_state_candidate

---

## Skill Routing Philosophy

Use a hybrid routing strategy.

Hard routing:

- Always activate transport_raman_analysis for blink-event analysis.
- Always activate artifact_detection for label critique and contradiction checks.

Semantic retrieval:

- Dynamically retrieve relevant markdown notes.
- Dynamically retrieve related hypotheses.
- Dynamically retrieve similar historical events.

Avoid rigid if/else rule explosion.
Preserve flexibility for discovering new physical interpretations.

---

## Human-in-the-loop

The human researcher has final authority.

The AI should:

- propose
- critique
- refine
- organize

but not silently rewrite scientific conclusions.
