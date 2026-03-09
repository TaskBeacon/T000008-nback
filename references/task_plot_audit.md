# Task Plot Audit

- generated_at: 2026-03-10T00:17:30
- mode: existing
- task_path: E:\Taskbeacon\T000008-nback

## 1. Inputs and provenance

- E:\Taskbeacon\T000008-nback\README.md
- E:\Taskbeacon\T000008-nback\config\config.yaml
- E:\Taskbeacon\T000008-nback\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | 1. Digit Presentation | A digit is presented on the screen for the duration specified by `probe_duration`. The participant can respond during this time. |
- | 2. Inter-Trial Interval (ITI) | A blank screen is shown for the duration specified by `iti_duration`. |

## 3. Evidence extracted from config/source

- match: phase=nback probe response, deadline_expr=settings.probe_duration, response_expr=n/a, stim_expr='stim_digit'
- match: phase=inter trial interval, deadline_expr=settings.iti_duration, response_expr=n/a, stim_expr='stim_iti'
- nomatch: phase=nback probe response, deadline_expr=settings.probe_duration, response_expr=n/a, stim_expr='stim_digit'
- nomatch: phase=inter trial interval, deadline_expr=settings.iti_duration, response_expr=n/a, stim_expr='stim_iti'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.052, right=0.053, blank=0.185
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0522, 'right_ratio': 0.0532, 'blank_ratio': 0.1849}

## 7. Output files and checksums

- E:\Taskbeacon\T000008-nback\references\task_plot_spec.yaml: sha256=159d9a049b9feab39b11600572ff86b2ba7921c0679a2fc115af2a83ce81ba13
- E:\Taskbeacon\T000008-nback\references\task_plot_spec.json: sha256=f953273e331668b40794183feed4d13425ea7e66bb0a2c0a7aea0b51742f66f4
- E:\Taskbeacon\T000008-nback\references\task_plot_source_excerpt.md: sha256=eec4196b83da9a1841e1cd61de6081969e9c1933a39a9ec7d8195ca06372388a
- E:\Taskbeacon\T000008-nback\task_flow.png: sha256=a1b6c272d15d6c61936b3d91ffbed9acaf378017e746e6767ab8d0e525e28f9f

## 8. Inferred/uncertain items

- collapsed equivalent condition logic into representative timeline: match, nomatch
