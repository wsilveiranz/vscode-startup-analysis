# Logic Apps Standard VS Code startup analysis

This workspace is configured for Copilot-assisted investigation of Visual
Studio Code startup and extension activation performance for Azure Logic Apps
Standard.

The authoritative workflow is the installed Copilot skill:

`.github/skills/logic-apps-vscode-startup-analyzer/SKILL.md`

Source captures belong in `performance-files/`. Generated parser output,
comparisons, and Markdown findings should be written to `analysis-output/`.

## Using the workspace

Open this folder in VS Code or start Copilot CLI from this directory. Ask
Copilot to analyze one or more captures, identify each capture as a baseline,
customer, or single-machine run, and state the user-visible readiness milestone
when it is known.

The current captures are not directly equivalent: one reports an initial
startup and the other a reopened window. They can be inspected for observations
and experiment design, but they should not be presented as a controlled
machine-to-machine regression comparison.

For repeatable evidence collection, follow:

`.github/skills/logic-apps-vscode-startup-analyzer/references/collection-protocol.md`
