# Task Logic Audit

## 1. Paradigm Intent

- Task: N-back working-memory task with blockwise 1-back and 2-back conditions.
- Primary construct: Updating and maintenance under varying working-memory load.
- Manipulated factors:
  - Memory load (`n_back` = 1 or 2)
  - Probe type (`match` vs `nomatch`)
- Dependent measures:
  - Probe response accuracy and RT
  - Omission rate
  - Trigger-aligned EEG events
- Key citations:
  - W2165702601
  - W1966476842
  - W2035978932

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 2 (human profile), each mapped to one load level by block order.
- Trials per block: 20.
- Randomization/counterbalancing:
  - Within block: pseudo-random condition generation with match ratio constraints.
  - Across block: deterministic order (1-back first, then 2-back).
- Condition weight policy:
  - `task.condition_weights` is not used.
  - `TaskSettings.resolve_condition_weights()` is not used.
  - Condition balance is controlled by custom generator `generate_nback_conditions(...)`.
- Condition generation method:
  - Custom generator is used because trial labels must carry per-trial digit content (`match_<digit>`, `nomatch_<digit>`), not only simple condition IDs.
  - Generated condition data shape passed into `run_trial.py`: single string token `<label>_<digit>`.
- Runtime-generated trial values (if any):
  - Probe text (`digit`) is decoded from condition token and injected via `stim_bank.rebuild(...)`.
  - Generator accepts optional seed; deterministic behavior can be enforced by runtime seed policy.

### Trial State Machine

1. State name: `nback_probe_response`
   - Onset trigger: `match_onset` or `nomatch_onset` plus load pad (`+10` for 1-back, `+20` for 2-back)
   - Stimuli shown: center digit (`stim_digit`)
   - Valid keys: `task.key_list` (`space`, `up`)
   - Timeout behavior: after `timing.probe_duration`, emit `no_response` (+pad) when no response
   - Next state: `inter_trial_interval`
2. State name: `inter_trial_interval`
   - Onset trigger: none
   - Stimuli shown: blank ITI (`stim_iti`)
   - Valid keys: `task.key_list` (ignored for scoring)
   - Timeout behavior: auto-advance after `timing.iti_duration`
   - Next state: next trial or block end

## 3. Condition Semantics

For condition tokens in runtime:

- Condition ID: `match_<digit>`
- Participant-facing meaning: current digit matches N-back reference digit.
- Concrete stimulus realization: probe digit text in `stim_digit`.
- Outcome rules: correct response is `task.match_key`.

- Condition ID: `nomatch_<digit>`
- Participant-facing meaning: current digit does not match N-back reference digit.
- Concrete stimulus realization: probe digit text in `stim_digit`.
- Outcome rules: correct response is `task.nomatch_key`.

Participant-facing text/stimuli source:

- Participant-facing text source: `config/*.yaml` stimuli (`instruction_*`, `block_break`, `good_bye`, `stim_digit`).
- Why this source is appropriate for auditability: localized wording and key mapping stay in config without runtime code edits.
- Localization strategy: swap config text/font per language while preserving `run_trial.py` orchestration logic.

## 4. Response and Scoring Rules

- Response mapping:
  - `space` = match
  - `up` = non-match
- Response key source: `task.match_key`, `task.nomatch_key`, and `task.key_list` in config.
- If code-defined, why config-driven mapping is not sufficient: not applicable.
- Missing-response policy: emit timeout trigger and mark trial as miss.
- Correctness logic: probe response correctness is computed by `StimUnit.capture_response(...)` against `correct_keys`.
- Reward/penalty updates: none.
- Running metrics: block break reports match-trial accuracy (`nback_probe_hit` on match trials).

## 5. Stimulus Layout Plan

- Screen name: `nback_probe_response`
- Stimulus IDs shown together: `stim_digit`
- Layout anchors (`pos`): default center
- Size/spacing (`height`, width, wrap): text defaults from config; single stimulus
- Readability/overlap checks: no overlap risk in single-stimulus frame
- Rationale: isolate probe processing and response timing

- Screen name: `inter_trial_interval`
- Stimulus IDs shown together: `stim_iti`
- Layout anchors (`pos`): default center
- Size/spacing (`height`, width, wrap): blank text
- Readability/overlap checks: no overlap risk
- Rationale: temporal reset between probes

## 6. Trigger Plan

- `exp_onset` (`98`): experiment start.
- `block_onset` (`100`): block start.
- `match_onset` (`2`) + pad:
  - 1-back: `12`
  - 2-back: `22`
- `nomatch_onset` (`3`) + pad:
  - 1-back: `13`
  - 2-back: `23`
- `key_press` (`4`) + pad:
  - 1-back: `14`
  - 2-back: `24`
- `no_response` (`5`) + pad:
  - 1-back: `15`
  - 2-back: `25`
- `block_end` (`101`): block end.
- `exp_end` (`99`): experiment end.

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: single auditable mode-aware flow for `human|qa|sim`.
- `utils.py` used?: yes.
- If yes, exact purpose: task-specific condition generator (`generate_nback_conditions`) for load-constrained sequence generation.
- Custom controller used?: no.
- If yes, why PsyFlow-native path is insufficient: not applicable.
- Legacy/backward-compatibility fallback logic required?: no.

## 8. Inference Log

- Decision: Use 20 trials per block in baseline profile.
- Why inference was required: selected papers support working-memory load manipulation but do not prescribe one universal trial count for this implementation profile.
- Citation-supported rationale: W2165702601 and W1966476842 focus on load-dependent EEG signatures requiring repeated probes.

- Decision: Keep fixed probe/ITI durations (0.8s, 1.2s).
- Why inference was required: exact durations vary by protocol; this repo profile prioritizes stable trigger timing and QA reproducibility.
- Citation-supported rationale: W2035978932 supports structured temporal windows for load-dependent oscillatory analysis.
