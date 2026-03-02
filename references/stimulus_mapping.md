# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `match` | `nback_probe_response` | `stim_digit` | Single digit (1-9) at center; participant judges whether it matches N-back target and responds via key mapping. | `W2165702601` | Working-memory load indexed through active probe comparison under controlled timing. | `psychopy_builtin` | `config/config*.yaml -> stimuli.stim_digit` | Runtime token is `match_<digit>` and is parsed in `run_trial.py`. |
| `nomatch` | `nback_probe_response` | `stim_digit` | Single digit (1-9) at center; participant judges non-match against N-back target and responds. | `W2165702601` | Non-match probe trials complement match trials for working-memory discrimination. | `psychopy_builtin` | `config/config*.yaml -> stimuli.stim_digit` | Runtime token is `nomatch_<digit>` and is parsed in `run_trial.py`. |
| `match` | `inter_trial_interval` | `stim_iti` | Blank ITI screen between probe trials. | `W1966476842` | EEG working-memory paradigms include inter-stimulus spacing for temporal separation. | `psychopy_builtin` | `config/config*.yaml -> stimuli.stim_iti` | ITI is condition-invariant. |
| `nomatch` | `inter_trial_interval` | `stim_iti` | Blank ITI screen between probe trials. | `W1966476842` | EEG working-memory paradigms include inter-stimulus spacing for temporal separation. | `psychopy_builtin` | `config/config*.yaml -> stimuli.stim_iti` | ITI is condition-invariant. |
