from contextlib import nullcontext
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import generate_nback_conditions, run_trial


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def run(options: TaskRunOptions):
    """Run N-Back in human/qa/sim mode with one auditable flow."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    print(f"[NBACK] mode={options.mode} config={options.config_path}")

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "human":
            subform = SubInfo(cfg["subform_config"])
            subject_data = subform.collect()
        elif options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        else:
            participant_id = "sim"
            if runtime_ctx is not None and runtime_ctx.session is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        trigger_runtime = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        win, kb = initialize_exp(settings)

        stim_bank = StimBank(win, cfg["stim_config"])
        if bool(getattr(settings, "voice_enabled", True)) and options.mode not in ("qa", "sim"):
            stim_bank = stim_bank.convert_to_voice(["instruction_1back", "instruction_2back"], voice=settings.voice_name)
        stim_bank = stim_bank.preload_all()

        settings.save_to_json()
        trigger_runtime.send(settings.triggers.get("exp_onset"))

        all_data = []
        for block_i in range(settings.total_blocks):
            half_point = settings.total_blocks // 2
            n_back = 1 if block_i < half_point else 2

            instruction_label = f"instruction_{n_back}back"
            instruction = StimUnit(instruction_label, win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get(instruction_label)
            )
            if bool(getattr(settings, "voice_enabled", True)) and options.mode not in ("qa", "sim"):
                instruction.add_stim(stim_bank.get(f"{instruction_label}_voice"))
            instruction.wait_and_continue()

            block = (
                BlockUnit(
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions(func=generate_nback_conditions, n_back=n_back)
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    func=run_trial,
                    stim_bank=stim_bank,
                    n_back=n_back,
                    trigger_runtime=trigger_runtime,
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                )
                .to_dict(all_data)
            )

            match_trials = block.get_trial_data(key="condition", pattern="match", match_type="startswith")
            acc = sum(t.get("cue_hit", False) for t in match_trials) / len(match_trials) if match_trials else 0

            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    acc=acc,
                )
            ).wait_and_continue()

        StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(stim_bank.get("good_bye")).wait_and_continue(
            terminate=True
        )

        trigger_runtime.send(settings.triggers.get("exp_end"))

        df = pd.DataFrame(all_data)
        df.to_csv(settings.res_file, index=False)

        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run N-Back in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
