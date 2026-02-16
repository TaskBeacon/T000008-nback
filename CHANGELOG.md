# CHANGELOG

All notable development changes for T000008-nback are documented here.

## [1.1.0] - 2026-02-17

### Added
- Added mode-aware main.py flow for human, qa, and sim modes.
- Added split runtime configs: config/config.yaml, config/config_qa.yaml, config/config_scripted_sim.yaml, and config/config_sampler_sim.yaml.
- Added task-local responder scaffold in esponders/task_sampler.py.
- Added outputs/.gitkeep and standardized output folders for human/qa/sim runs.

### Changed
- Aligned trigger config to structured schema (	riggers.map, 	riggers.driver, 	riggers.policy, 	riggers.timing).
- Aligned src/run_trial.py to set responder trial context via set_trial_context(...) at response windows.
- Added/updated 	askbeacon.yaml with contracts.psyflow_taps: v0.1.0.
- Updated .gitignore to match standardized task artifacts and output handling.

### Verified
- psyflow-validate <task> passes all contract checks (including artifacts).
- psyflow-qa <task> --config config/config_qa.yaml --no-maturity-update passes.
- python main.py sim --config config/config_scripted_sim.yaml runs successfully and writes sim outputs.
