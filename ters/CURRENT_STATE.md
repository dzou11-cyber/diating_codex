# CURRENT STATE OF THE TERS BLINK PROJECT

This document summarizes the current understanding,
design philosophy, unresolved questions,
and intended workflows of the project.

The purpose is to update the long-term AI memory system
and refine the scientific reasoning architecture.

---

## Core Scientific Goal

The goal is NOT simply to detect blinks.

The goal is to:

- organize correlated Raman-conductance events
- identify latent molecular junction states
- distinguish physical states from artifacts
- maintain an evolving scientific memory system
- allow hypotheses and taxonomy to evolve over time

The system should support scientific reasoning,
not just threshold-based classification.

---

## Experimental Structure

Each experimental folder corresponds to one large experiment.

Each folder contains many session pairs:

- one conductance file
- one Raman file

Each session pair corresponds to one manual start/stop acquisition.

Multiple blink events may exist inside one session pair.

---

## Conductance File Structure

Columns:

1. time
2. raw current signal
3. bias voltage
4. piezo voltage

The raw current signal may later be converted
to physical current and conductance using amplifier-specific fitting functions.

However:

initial blink boundary refinement should NOT depend on conductance fitting.

Temporal structure can first be analyzed directly
from raw current traces.

---

## Raman File Structure

Each row:

- first value = time
- remaining 1024 values = CCD pixel intensities

Pixel indices may later be converted to Raman shift
using laser- and spectrometer-specific fitting functions.

However:

initial blink boundary refinement should NOT require Raman fitting.

Temporal evolution can first be analyzed directly
from raw intensity behavior.

---

## Important Insight

Conductance and Raman are NOT strictly synchronized systems.

The two systems:

- have different sampling rates
- may have time offset drift
- may not align frame-to-frame

Therefore:

the system should NOT assume exact pointwise synchronization.

Instead:

the system should identify event boundaries independently
in conductance and Raman domains,
then estimate lead/lag relationships.

Absolute onset/offset deltas should be treated as approximate
because inter-system offset stability may be unknown.
Small timing differences should not be over-interpreted.

---

## Current Blink Taxonomy

Current working categories:

- true_blink
- plateau_only
- raman_only
- noisy_state
- artifact
- uncertain

These categories are provisional and expected to evolve.

---

## Important Physical Insights

### 1. Conductance plateau does NOT guarantee Raman enhancement

A stable conductance plateau may occur without visible Raman enhancement.

Possible explanations include:

- weak hotspot overlap
- dark transport states
- off-hotspot molecule position
- electronic stabilization without strong optical coupling

Therefore:

plateau-only events should NOT automatically be classified as artifacts.

### 2. Raman enhancement without conductance stabilization may occur

Possible causes:

- off-junction SERS
- plasmonic fluctuation
- hotspot instability

Therefore:

Raman-only events are physically meaningful
and should be retained.

### 3. Delayed Raman onset may be physically real

Some events show:

- conductance rising slightly before Raman enhancement

Observed lag scale:

~0.01–0.03 s

Possible interpretations:

- hotspot stabilization delay
- molecular orientation evolution
- delayed optical coupling

This lag should be measured,
not forced to zero.

### 4. Blink tails / shoulders are important

Some events contain:

- small sub-plateaus
- shoulders
- partial decay regions

These should NOT automatically be split into separate events.

If no full reset to baseline occurs,
the event should initially remain a single blink
with internal structure.

Suggested fields:

- core_window
- tail_window
- shoulder_flag
- split_suggestion

---

## Event Philosophy

The system should preserve uncertainty.

The AI should avoid prematurely collapsing ambiguous events
into rigid labels.

The system should preserve:

- edge cases
- contradictions
- unresolved interpretations
- alternative explanations

Scientific ambiguity is valuable.

---

## Desired AI Behavior

The AI should:

- refine coarse windows
- detect lead/lag
- identify shoulders/substates
- compare against historical cases
- propose interpretations
- criticize weak human labels
- preserve uncertainty

The AI should NOT blindly agree with human labels.

The AI should explicitly critique:

- weak evidence
- contradictory classifications
- over-interpretation
- ambiguous boundaries

---

## Knowledge Architecture

The system contains two distinct layers.

### JSON Layer

Structured factual memory.

Each blink event should eventually become
a structured JSON event packet.

JSON stores:

- boundaries
- labels
- timing
- lag estimates
- flags
- evidence
- uncertainty

JSON should remain machine-readable and relatively stable.

### Markdown Layer

Scientific reasoning layer.

Markdown notes contain:

- evolving interpretations
- taxonomy
- hypotheses
- contradictions
- unresolved questions
- cross-links between concepts

Markdown notes are expected to evolve continuously.

---

## Important Design Principle

The AI should NOT overwrite old interpretations.

Instead:

new observations should be appended historically.

Scientific evolution should remain visible.

Example:

Earlier interpretations may later become partially incorrect.
These revisions should be preserved chronologically.

---

## Current Workflow Vision

Human provides:

- coarse blink windows
- initial labels

AI performs:

- boundary refinement
- event packaging
- retrieval
- comparison
- criticism
- interpretation
- note suggestions

Human then reviews:

- refined windows
- labels
- interpretations
- criticisms

Corrected event packets are then fed back
into the long-term memory system.

---

## Long-Term Vision

The long-term goal is to build an evolving,
persistent scientific cognition system capable of:

- organizing all historical blink events
- discovering latent junction-state families
- maintaining scientific memory
- evolving taxonomy over time
- assisting hypothesis generation
- identifying recurring physical patterns
- supporting human scientific reasoning

This is NOT intended to be a simple chatbot or classifier.

The system should function as an evolving
AI-assisted scientific memory and reasoning architecture.
