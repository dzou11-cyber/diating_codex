# System Architecture

## Goal

Build an AI-assisted scientific memory and reasoning system for correlated Raman-conductance molecular junction experiments.

The system should:

- Store all blink events
- Maintain long-term scientific memory
- Organize evolving hypotheses
- Compare new events against historical cases
- Assist with discovering latent junction states

---

## Data Structure

### Raw Sources

Raw experimental files are immutable.

Each session contains:

- One conductance file
- One Raman file

A folder may contain many sessions.

### Event Units

The basic unit of analysis is a blink event.

Each event contains:

- Folder name
- Session number
- Coarse time window
- Refined time window
- Conductance segment
- Raman segment
- Metadata
- Human label

---

## Blink Taxonomy

Current categories include:

- `true_blink`
- `plateau_only`
- `raman_only`
- `noisy_state`
- `artifact`
- `uncertain`

This taxonomy is expected to evolve over time.

---

## AI Responsibilities

The AI should:

- Analyze blink events
- Compare against historical cases
- Suggest possible physical interpretations
- Detect similarities and contradictions
- Maintain cross-references between notes
- Propose updates to taxonomy

The AI should **not** overwrite existing scientific conclusions without human confirmation.

---

## Scientific Priorities

The system should prioritize:

- Correlated Raman-conductance behavior
- Junction-state evolution
- Spectral synchronization
- Possible conformational switching
- Hotspot stability
- Distinguishing artifacts from physical states

---

## Long-Term Vision

The long-term goal is to build a persistent, evolving scientific memory system capable of:

- Organizing all historical blink events
- Identifying latent junction-state families
- Discovering recurring physical patterns
- Assisting with hypothesis generation
