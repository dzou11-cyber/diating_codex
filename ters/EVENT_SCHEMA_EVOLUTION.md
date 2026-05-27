# Event JSON Schema Evolution Guide

This document defines how the blink `event JSON` evolves from the current draft in safe, incremental steps.

Current baseline file:

- `event.schema.json`

---

## v0 Baseline (Done)

Goals:

- describe one blink event completely
- preserve uncertainty and critic outputs
- keep the format flexible for fast experimentation

Status:

- implemented
- `additionalProperties: true` is intentional at this stage

---

## v1 Normalization (Target: 1-2 weeks)

Goals:

- stabilize IDs and field conventions
- prepare for scalable querying and statistics

Changes:

1. add `schema_version` (example: `"v1"`)
2. split `event_id` into normalized parts
3. add `session_id` (example: `"016"`)
4. add `event_index` (example: `1`)
5. keep `event_id` for backward compatibility
6. standardize all windows as `[start_s, end_s]`
7. enforce `start_s < end_s` in pipeline validation

Acceptance:

1. all new events include `schema_version`
2. legacy data still parses correctly
3. queries support both `event_id` and `(session_id, event_index)`

---

## v2 Evidence Binding (Target: 2-3 weeks)

Goals:

- tie interpretations directly to observable signal evidence

Changes:

1. add `evidence` block
2. add `current_features` (step, plateau, shoulder, tail, reset)
3. add `raman_features` (peak rise, bandwidth change, baseline drift)
4. add `source_refs` (raw file path plus index/time ranges)
5. optionally add quality metrics: `snr_current`, `snr_raman`, `artifact_score`

Acceptance:

1. every interpretation points to raw data slices
2. reviewers can verify key evidence from JSON alone

---

## v3 Auditable Reasoning (Target: 2 weeks)

Goals:

- make AI decisions reviewable and critic-friendly

Changes:

1. replace single `confidence` with structured fields
2. add `label_confidence`
3. add `boundary_confidence`
4. add `interpretation_confidence`
5. extend `criticisms` with `severity` and `evidence_strength`
6. add `hypothesis_candidates` with support and contradiction notes

Acceptance:

1. high-risk conclusions are easy to locate
2. multiple interpretation paths can be preserved and compared

---

## v4 Scientific Memory Integration (Target: 3-4 weeks)

Goals:

- enable cross-event memory and latent state discovery

Changes:

1. add links: `similar_event_ids`, `contradictory_event_ids`
2. add state tags: `junction_state_candidate`, `conformation_candidate`, `hotspot_stability_tag`
3. add lineage links: `derived_from_notes`, `supersedes_interpretation_of`

Acceptance:

1. new events can link to historical analogs
2. state-family and contradiction graphs can be built from JSON

---

## Hard Rules During Evolution

1. Never overwrite historical interpretations destructively.
2. Append new evidence and log confidence changes.
3. Keep new fields optional before promoting to required.
4. Record every schema upgrade in a changelog entry.
5. Maintain backward compatibility for at least one full version cycle.

---

## Recommended Immediate Next Step

Apply the minimum v1 upgrade now:

1. add `schema_version`
2. add `session_id`
3. add `event_index`
4. keep `event_id` unchanged
