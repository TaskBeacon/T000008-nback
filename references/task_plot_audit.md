# Task Plot 审计

- generated_at: 2026-03-23T23:15:43
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback

## 1. 输入与来源

- `README.md`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\README.md`
- `config.yaml`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\config\config.yaml`
- `run_trial.py`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\src\run_trial.py`

## 2. 从 README 提取的证据

- README 的任务流分为块级流程和试次级流程两层。
- 块级流程说明了 `1-back` 和 `2-back` 的块组织、块间休息以及结束页。
- 试次级流程只包含两步：数字呈现与 ITI 空屏。

## 3. 从 config/source 提取的证据

- `match`：`probe_unit = make_unit(unit_label="nback_probe").add_stim(stim_bank.rebuild("stim_digit", text=_digit))`，随后 `set_trial_context(... phase="nback_probe_response", deadline_s=settings.probe_duration, stim_id="stim_digit")`，再用 `capture_response(..., duration=settings.probe_duration, terminate_on_response=True)`；这是 800 ms 的数字呈现与反应窗。
- `nomatch`：与 `match` 使用同一套阶段顺序和时序，只是正确反应键由条件决定，因此在图中折叠为等价变体。
- `ITI`：`iti_unit = make_unit(unit_label="iti").add_stim(stim_bank.get("stim_iti"))`，随后 `set_trial_context(... phase="inter_trial_interval", deadline_s=settings.iti_duration, stim_id="stim_iti")`，最后 `iti_unit.show(settings.iti_duration)`；这是 1200 ms 的空屏。
- `Probe` 的实际运行内容不是配置里的 `*`，而是运行时重建后的数字字符串 `_digit`。

## 3b. 警告

- 无。`run_trial.py` 中这两个参与者可见阶段都带有 `set_trial_context(...)`。

## 4. 映射到 task_plot_spec

- `root_key`: `task_plot_spec`
- `spec_version`: `0.2`
- 采用“一条代表性时间线 + 等价变体注记”的集合式图形。
- 由于 `match` 与 `nomatch` 的阶段顺序和时序相同，图中保留 `Match` 作为代表性时间线，并把 `Nomatch` 作为等价变体折叠到同一行。
- `Probe` 的图示从配置占位 `*` 修正为示例数字 `5`，更贴近运行时实际看到的数字刺激。
- `ITI` 的图示改为不可见占位图元，用来表达空屏，避免渲染成 `[text]` 占位。

## 5. 样式决策与理由

- 继续使用 timeline collection，因为这是 task-plot 的固定图型。
- 这个任务没有独立的显性反馈阶段，最有信息量的内容就是试次里的 `Probe` 与 `ITI`。
- 只保留一条代表性时间线可以避免 `match/nomatch` 的重复展示，同时保留条件变体注记，便于审计。

## 6. 渲染参数与约束

- `output_file`: `task_flow.png`
- `dpi`: `300`
- `max_conditions`: `2`
- `screens_per_timeline`: `4`
- `screen_overlap_ratio`: `0.1`
- `screen_slope`: `0.08`
- `screen_slope_deg`: `25.0`
- `screen_aspect_ratio`: `1.4545454545454546`
- `left_margin`: `0.2`
- `right_margin`: `0.03`
- `top_margin`: `0.03`
- `bottom_margin`: `0.05`
- `qa_mode`: `local`
- `auto_layout_feedback`:
  - `layout pass 1: crop-only; left=0.052, right=0.053, blank=0.177`
- `auto_layout_feedback_records`:
  - `pass: 1`
    `metrics`: `{'left_ratio': 0.0522, 'right_ratio': 0.0532, 'blank_ratio': 0.177}`
- `validator_warnings`: 无

## 7. 输出文件与校验和

- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\references\task_plot_spec.yaml`: `sha256=3c1df511a2f95694988e01ecade094624283be5274d5bc952dc5ca881bc369d2`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\references\task_plot_spec.json`: `sha256=0a625dc0166fae89f534b99d0f2da465e3df89b588df5fb1056ed10a6265223a`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\references\task_plot_source_excerpt.md`: `sha256=fe7af28c67394f89adee7b993a1289e95f4ff37c946509af8e33bb63b17b88af`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000008-nback\task_flow.png`: `sha256=b3073db8c99025d9e8b30b60370ab10cb04e9055979e9f0279c17a171b7e6d6c`

## 8. 推断项与不确定项

- `match` 与 `nomatch` 在试次层面共享同一套阶段顺序和时序，因此图中折叠为代表性时间线。
- `Probe` 的实际刺激内容来自运行时重建后的 `_digit`，无法在静态代码中固定成唯一数字，所以图中只选了一个示例数字 `5`。
- `ITI` 是空屏阶段，图中使用不可见占位图元来表达，以避免把它画成带文字的占位屏幕。
