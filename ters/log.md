## [2026-05-27] analyze | Session 016 blink near 65.11-65.40 s

- Re-ran blink refinement from raw `Data_016.csv` and `Data_Raman016.csv`.
- Applied independent boundary refinement for conductance and Raman.
- Stored lag as local tendency with explicit synchronization uncertainty fields.
- Added event packet and analysis page under `events/`.
- Updated `AGENTS.md`, `CURRENT_STATE.md`, and `event.schema.json` to encode synchronization philosophy.

## [2026-05-27] update | Calibration module and skill-routing policy

- Added `ters_calibration.py` to store conductance fitting and Raman pixel-to-wavenumber fitting logic.
- Locked default Raman calibration to current project setting `633nm_2200`.
- Added explicit Skill Evolution Policy and Skill Routing Philosophy to `AGENTS.md`.
