# VS Code startup performance analysis

This workspace is dedicated to investigating Visual Studio Code startup and
activation performance for Azure Logic Apps Standard.

## Authoritative analysis method

For every Logic Apps Standard VS Code startup investigation, use the
`logic-apps-vscode-startup-analyzer` skill in
`.github/skills/logic-apps-vscode-startup-analyzer/`.

Treat that skill's `SKILL.md`, scripts, collection protocol, terminology,
guardrails, and report template as authoritative. Do not replace its
measurement-first workflow with an ad hoc analysis.

## Workspace conventions

- Treat files in `performance-files/` as immutable source evidence.
- Write generated JSON, comparisons, and reports under `analysis-output/`.
- Keep baseline, customer, cold, warm, and single-machine labels explicit in
  artifact names and reports.
- Do not compare captures as equivalent when startup type, workspace, VS Code
  version, extension versions, or user-visible readiness milestone differ.
- Separate `Observed`, `Hypothesis`, `Confirmed by controlled test`, and
  `Unknown` conclusions.
- Never infer root cause from duration correlation alone.
- Flag potentially sensitive paths, identities, tenant details, URLs, tokens,
  and workspace content before evidence is shared.

## Expected outcome

Analysis should identify the Logic Apps dependency path, distinguish VS Code
core time from Extension Host activity, expose evidence gaps, and prioritize
controlled experiments and actionable developer improvements.
