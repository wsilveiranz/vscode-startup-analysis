---
name: logic-apps-vscode-startup-analyzer
description: analyze and compare Azure Logic Apps Standard startup performance in Visual Studio Code using Startup Performance reports, Running Extensions captures, VS Code status and extension inventories. Use when diagnosing slow Logic Apps VS Code activation, collecting a repeatable baseline, comparing a customer machine with a known baseline, identifying extension-host contention or dependency delays involving Logic Apps, Azure Functions, Azurite, C# or .NET tooling, and producing an engineering-ready Markdown findings report.
---

# Logic Apps VS Code Startup Analyzer

Use a measurement-first workflow. Separate observations, hypotheses, and confirmed causes.

## Inputs

Accept any combination of:

- A `Developer: Startup Performance` text report.
- A screenshot or transcription from `Developer: Show Running Extensions`.
- Output from `scripts/collect-vscode-environment.ps1`.
- One or more previously generated `startup-analysis.json` files.
- A baseline capture and a customer capture for comparison.

Do not require every input before producing a useful partial analysis. Clearly identify missing evidence.

## Workflow

1. Identify each capture as `baseline`, `customer`, or `single-machine`.
2. Read [references/collection-protocol.md](references/collection-protocol.md) when the user needs to collect or repeat measurements.
3. For each Startup Performance report, run:

   `python scripts/analyze_startup_report.py <report.txt> --label <label> --output <analysis.json>`

4. If two analysis JSON files are available, run:

   `python scripts/compare_startup_reports.py <baseline.json> <customer.json> --output <comparison.md>`

5. Correlate scripted results with screenshots, environment inventory, and the user's user-visible readiness milestone.
6. Produce a concise Markdown report using [references/report-template.md](references/report-template.md).

## Analysis rules

- Treat `workbench ready`, `renderer ready`, and `extensions registered` as VS Code/core indicators.
- Treat `Load Code` as extension code/module loading time.
- Treat `Call Activate` as activation invocation overhead.
- Treat `Finish Activate` as time until activation completion. Do not claim what an extension awaited without a profile, logs, or instrumentation.
- Use `Event` and `By` to identify activation triggers and dependency paths.
- Inspect `Raw Perf Marks: localExtHost` to establish ordering and Extension Host occupancy.
- Always highlight these extension IDs when present:
  - `ms-azuretools.vscode-azurelogicapps`
  - `ms-azuretools.vscode-azurefunctions`
  - `Azurite.azurite`
  - `ms-dotnettools.csharp`
  - `ms-dotnettools.csdevkit`
  - `ms-dotnettools.vscode-dotnet-runtime`
  - `ms-azuretools.vscode-azureresourcegroups`
- Report unrelated extensions that load before the Logic Apps dependency chain and materially occupy the Extension Host.
- Do not add extension times together as elapsed startup time unless the raw timeline proves the phases are sequential and non-overlapping.
- Do not equate extension activation with user-visible readiness. Track separate milestones such as project tree ready, designer ready, design-time API ready, and run/debug ready.
- Label every conclusion as one of: `Observed`, `Hypothesis`, `Confirmed by controlled test`, or `Unknown`.

## Comparison rules

- Compare equivalent workspace, VS Code channel/version, extension versions, and readiness milestone where possible.
- Prefer at least three cold runs and three warm runs per machine. Report ranges and medians when multiple captures are supplied.
- Call out version drift before attributing machine-level differences.
- Compare absolute milliseconds and customer-to-baseline ratio, but avoid declaring a regression from one run alone.
- For customer evidence, flag potentially sensitive paths, account names, tenant information, URLs, tokens, and workspace content before sharing.

## Controlled investigation order

1. Repeat the same workspace capture to establish variance.
2. Disable Azurite for the workspace and repeat.
3. Test with a minimal VS Code profile containing only required Logic Apps tooling.
4. Compare cold start versus `Developer: Reload Window`.
5. Review Output channels and `Help: Open Process Explorer` during the delay.
6. Capture an Extension Host CPU profile if large `Load Code` intervals remain.
7. Add stage-level performance marks inside the Logic Apps activation path when source access is available.

Never state that Azurite, Azure Functions, antivirus, networking, authentication, or Logic Apps is the root cause based only on duration correlation.

## Output requirements

Include:

- Executive summary.
- Capture metadata and comparability caveats.
- Top extension timings.
- Logic Apps dependency-path timings.
- VS Code core versus Extension Host assessment.
- Observations versus hypotheses.
- Prioritized next experiments with expected discriminating outcome.
- Developer improvement opportunities.
- Evidence gaps.

When requested, save the report as a downloadable Markdown file.
