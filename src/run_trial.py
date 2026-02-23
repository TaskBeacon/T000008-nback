from functools import partial

from psyflow import StimUnit, set_trial_context, next_trial_id

# trial stages use task-specific phase labels via set_trial_context(...)

def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    n_back,
    trigger_runtime=None,
    block_id=None,
    block_idx=None,
):
    """Run one n-back trial."""
    trial_id = next_trial_id()
    trial_data = {"condition": condition}

    _match = condition.split("_")[0]
    _digit = condition.split("_")[1]
    correct_key = settings.match_key if _match == "match" else settings.nomatch_key
    trigger_pad = 10 if n_back == 1 else 20

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: nback_probe_response
    # phase: nback_probe_response
    cue_unit = make_unit(unit_label="cue").add_stim(stim_bank.rebuild("stim_digit", text=_digit))
    set_trial_context(
        cue_unit,
        trial_id=trial_id,
        phase="nback_probe_response",
        deadline_s=settings.cue_duration,
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={"condition": str(condition), "stage": "nback_probe_response", "n_back": int(n_back), "digit": str(_digit), "block_idx": block_idx},
        stim_id="stim_digit",
    )
    cue_unit.capture_response(
        keys=settings.key_list,
        correct_keys=correct_key,
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get(f"{_match}_onset") + trigger_pad,
        response_trigger=settings.triggers.get("key_press") + trigger_pad,
        timeout_trigger=settings.triggers.get("no_response") + trigger_pad,
        terminate_on_response=True,
    ).to_dict(trial_data)

    # phase: inter_trial_interval
    iti_unit = make_unit(unit_label="iti").add_stim(stim_bank.get("stim_iti"))
    set_trial_context(
        iti_unit,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=settings.iti_duration,
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={"condition": str(condition), "stage": "inter_trial_interval", "n_back": int(n_back), "block_idx": block_idx},
        stim_id="stim_iti",
    )
    iti_unit.show(settings.iti_duration).to_dict(trial_data)

    # outcome display (n-back uses no explicit outcome screen)
    return trial_data
