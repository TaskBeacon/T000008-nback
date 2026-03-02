# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `total_blocks` | `task.total_blocks` | `2` (human), `1` (qa/sim) | `W2035978932` | Working-memory load manipulations are handled via blockwise task settings. | `inferred` | QA/sim uses 1 block for runtime efficiency. |
| `trial_per_block` | `task.trial_per_block` | `20` | `W1966476842` | Continuous working-memory probe streams require repeated probe sampling within each block. | `inferred` | Chosen to provide stable condition coverage. |
| `conditions` | `task.conditions` | `['match', 'nomatch']` | `W2165702601` | Probe classification follows match vs non-match memory comparison. | `reference_exact` | Runtime condition tokens are expanded to `match_<digit>`/`nomatch_<digit>`. |
| `key_list` | `task.key_list` | `['space', 'up']` | `W1966476842` | Probe-response phase requires active key responses under working-memory load. | `inferred` | Matches config-defined instruction mapping. |
| `match_key` | `task.match_key` | `space` | `W2165702601` | Match decision recorded with dedicated response key. | `inferred` | Localized in config for portability. |
| `nomatch_key` | `task.nomatch_key` | `up` | `W2165702601` | Non-match decision recorded with dedicated response key. | `inferred` | Avoids ambiguous single-key go/no-go interpretation. |
| `probe_duration` | `timing.probe_duration` | `0.8` | `W2035978932` | Probe display window supports load-sensitive response collection. | `inferred` | Retained across human/qa/sim profiles. |
| `iti_duration` | `timing.iti_duration` | `1.2` | `W1966476842` | Inter-trial blank interval separates probe events for EEG analysis. | `inferred` | Implemented as fixed duration in this baseline profile. |
| `match_onset` | `triggers.map.match_onset` | `2` (+block pad) | `W2165702601` | Probe onset markers support load-specific electrophysiological analysis. | `inferred` | Runtime adds `+10` for 1-back and `+20` for 2-back. |
| `nomatch_onset` | `triggers.map.nomatch_onset` | `3` (+block pad) | `W2165702601` | Non-match probe onset marker is separated from match onset code. | `inferred` | Runtime adds same block pad policy. |
| `key_press` | `triggers.map.key_press` | `4` (+block pad) | `W1966476842` | Response marker aligns behavioral timing with EEG samples. | `inferred` | Emitted on valid key response in probe window. |
| `no_response` | `triggers.map.no_response` | `5` (+block pad) | `W1966476842` | Timeout marker captures omission events for trial-level QC. | `inferred` | Emitted on missed probe window. |
