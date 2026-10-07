# VS Code startup comparison

Baseline: `baseline-cold-vscode-1.141`  
Customer: `customer-cold-vscode-1.140`

| Extension | Baseline load code | Customer load code | Ratio |
|---|---:|---:|---:|
| Azurite.azurite | 12268 ms | 27071 ms | 2.21x |
| ms-dotnettools.csharp | 6035 ms | 3717 ms | 0.62x |
| ms-azuretools.vscode-azureresourcegroups | 644 ms | 3239 ms | 5.03x |
| ms-azuretools.vscode-azurefunctions | 5323 ms | 3049 ms | 0.57x |
| ms-azuretools.logicapps-migration-agent | n/a ms | 2563 ms | n/a |
| ms-vscode-remote.remote-containers | n/a ms | 1205 ms | n/a |
| ms-windows-ai-studio.windows-ai-studio | n/a ms | 953 ms | n/a |
| ms-azuretools.vscode-azurelogicapps | 1298 ms | 781 ms | 0.60x |
| GitHub.copilot-chat | 736 ms | 691 ms | 0.94x |
| ms-dotnettools.csdevkit | 374 ms | 333 ms | 0.89x |
| vscode.markdown-language-features | 273 ms | 227 ms | 0.83x |
| ms-dotnettools.vscode-dotnet-runtime | 274 ms | 139 ms | 0.51x |
| humao.rest-client | 3183 ms | 86 ms | 0.03x |
| vscode.json-language-features | 197 ms | 66 ms | 0.34x |
| vscode.typescript-language-features | 51 ms | 55 ms | 1.08x |
| vscode.git | 52 ms | 45 ms | 0.87x |
| vscode.microsoft-authentication | 55 ms | 44 ms | 0.80x |
| vscode.terminal-suggest | n/a ms | 41 ms | n/a |
| vscode.github-authentication | 42 ms | 33 ms | 0.79x |
| ms-azuretools.vscode-azure-mcp-server | n/a ms | 32 ms | n/a |
| vscode.emmet | 38 ms | 27 ms | 0.71x |
| vscode.markdown-math | 14 ms | 27 ms | 1.93x |
| vscode.npm | 48 ms | 20 ms | 0.42x |
| vscode.extension-editing | 33 ms | 14 ms | 0.42x |
| vscode.merge-conflict | 19 ms | 14 ms | 0.74x |
| vscode.github | 14 ms | 12 ms | 0.86x |
| vscode.configuration-editing | 28 ms | 9 ms | 0.32x |
| vscode.git-base | 11 ms | 8 ms | 0.73x |
| vscode.debug-auto-launch | 9 ms | 7 ms | 0.78x |
| vscode.mermaid-markdown-features | 13 ms | 7 ms | 0.54x |
| MAI-EngineeringSystems.mai-ai-telemetry | 3178 ms | n/a ms | n/a |
| RobBos.ai-engineering-fluency | 2555 ms | n/a ms | n/a |
| Microsoft.agency | 2253 ms | n/a ms | n/a |
| MermaidChart.vscode-mermaid-chart | 541 ms | n/a ms | n/a |
| yzhang.markdown-all-in-one | 279 ms | n/a ms | n/a |
| ms-vscode.vscode-chat-customizations-evaluations | 319 ms | n/a ms | n/a |
| mechatroner.rainbow-csv | 12 ms | n/a ms | n/a |

## Interpretation guardrails

- Verify VS Code and extension version comparability.
- Treat ratios as observations, not root-cause proof.
- Use controlled tests and profiles to validate the critical path.
