# Collection protocol

## Preparation

- Use the same representative Logic Apps Standard workspace on each machine when permitted.
- Record the user-visible milestone being measured.
- Close all VS Code windows for a cold run.
- Avoid installing or updating extensions between comparison runs.
- Record whether endpoint security, remote filesystem, VPN, proxy, or roaming profile conditions differ. Treat these as context, not causes.

## Collect environment inventory

Run in PowerShell:

```powershell
./scripts/collect-vscode-environment.ps1 -OutputDirectory ./vscode-startup-evidence
```

Review the output before sharing externally. The collector intentionally avoids workspace file contents, environment variables, tokens, and account details.

## Collect Startup Performance

1. Open the representative Logic Apps Standard workspace.
2. Wait for the chosen readiness milestone.
3. Open the Command Palette with `Ctrl+Shift+P`.
4. Run `Developer: Startup Performance`.
5. Save the report as text using a run-specific name such as `baseline-cold-01.txt`.

## Collect Running Extensions

1. Run `Developer: Show Running Extensions` in the same session.
2. Capture the complete visible ranked list or at least the top entries and Logic Apps entry.

## Test matrix

Capture at least:

- Normal cold start, three runs.
- Normal warm reload, three runs.
- Azurite disabled for the workspace, three runs.
- Minimal extension profile, three runs.

Do not use a customer's production workspace if a sanitized representative workspace reproduces the issue.
