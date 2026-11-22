# Eval cases

Eight cases for `claude plugin eval`, each a mistake this plugin's rules exist to prevent. Three come from the
recorded run of 2026-11-17: a share that fell because the database changed, a jump written up as a break in the pattern, and a verdict that drifted when it was retyped.

| Case | Passes when |
|---|---|
| `base-composition-trap` | a fall of the share among all record types is not written up as a decline, and the share on the same types is read |
| `one-year-is-a-lead` | one year above a series' own past is not called an emerging trend, and the conclusion is challenged before it is reported |
| `scenario-is-not-a-forecast` | three scenarios get no probabilities |
| `detail-adds-no-probability` | a forecast with more conditions is not logged above the plain one |
| `forecast-not-edited-after` | a probability is left as written once the outcome is known |
| `no-signals-no-invention` | with no signals in the project, none are written from memory |
| `verdict-copied-not-retyped` | a "weakened" verdict is not relabelled "kept" |
| `model-not-tested-on-the-past` | a backtest on known outcomes is not accepted as a measure of the forecaster |

**No case has been run.** Each run is a real model call, and each `llm` grader calls a judge model:

```
claude plugin eval . --no-publish
claude plugin eval . --no-publish --case base-composition-trap
```

Run from the plugin's folder. Every case asks for one run (`runs: 1`), so a first pass is eight runs with the
plugin and eight without, plus the judges. `--no-publish` keeps the report on this machine; without it the report
is published to claude.ai. `--max-cost-usd` sets a ceiling. Before the first run, sign the Claude command line in
with `claude auth login`: a sign-in in the desktop app does not reach it.

The cases allow only read-only tools, so the plugin's scripts are not run in them. Each prompt carries the numbers
the task needs, because a run starts in an empty folder.

The format: `prompt.md` with `max_turns` and `allowed_tools`, and `graders/*.md` with `type`, are what
`claude plugin eval init --bare` writes (seen on 2026-11-22, Claude Code 2.1.311). The other fields used here
(`description`, `tags`, `runs`, and graders of type `regex` and `tool_used`) follow the cases of poiesis-research
2.4.0, one of which loaded with its graders in an attempt that stopped at sign-in. The Claude Code documentation
on evals was not read again for this plugin.
