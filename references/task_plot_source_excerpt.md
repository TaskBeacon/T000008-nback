# 源码摘录（N-Back Task）

## 输入文件
- `README.md`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\README.md`
- `config.yaml`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\config\config.yaml`
- `run_trial.py`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\src\run_trial.py`

## 选定条件
- `match`（代表性时间线，`nomatch` 作为等价变体折叠）

## 关键试次流程证据
- `Probe`：`probe_unit = make_unit(unit_label="nback_probe").add_stim(stim_bank.rebuild("stim_digit", text=_digit))`。随后 `set_trial_context(... phase="nback_probe_response", deadline_s=settings.probe_duration, ... stim_id="stim_digit")`，再调用 `capture_response(..., duration=settings.probe_duration, terminate_on_response=True)`，对应 800 ms 的数字呈现与反应窗。
- `ITI`：`iti_unit = make_unit(unit_label="iti").add_stim(stim_bank.get("stim_iti"))`。随后 `set_trial_context(... phase="inter_trial_interval", deadline_s=settings.iti_duration, ... stim_id="stim_iti")`，最后 `iti_unit.show(settings.iti_duration)`，对应 1200 ms 的空屏。

## 备注
- README 中的 `Block-Level Flow` 说明了 1-back / 2-back 的块级组织；试次级流程以 `run_trial.py` 为准。
- 本次绘图只保留一个代表性时间线，因为 `match` 与 `nomatch` 的阶段顺序与时序一致。
- 图中 `Probe` 使用示例数字 `5` 表示参与者看到的数字刺激；`ITI` 使用不可见占位图元表示空屏，避免渲染成 `[text]` 占位。
