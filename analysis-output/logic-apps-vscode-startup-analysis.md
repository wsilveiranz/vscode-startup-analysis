# Logic Apps Standard VS Code Startup Analysis

## Executive summary

**Observed:** The baseline and customer captures are both initial startups,
making them more comparable than the previous warm baseline capture. VS Code
core readiness is nearly identical: workbench ready is 2.010 seconds for the
baseline and 1.939 seconds for the customer.

**Observed:** The long delay remains in the shared Extension Host rather than
VS Code core. The raw Logic Apps dependency-loading interval is approximately
27.2 seconds for the baseline and 38.3 seconds for the customer capture.

**Observed:** The component distribution differs substantially:

- Azurite loads in 12.268 seconds for the baseline and 27.071 seconds for the
  customer.
- Azure Resource Groups loads in 0.644 seconds and 3.239 seconds.
- Azure Functions loads in 5.323 seconds and 3.049 seconds.
- C# loads in 6.035 seconds and 3.717 seconds.
- Logic Apps finishes activation in 15.300 seconds and 4.212 seconds.

**Observed:** The customer dependency-loading interval is approximately
11.1 seconds longer than the baseline. Customer Azurite and Resource Groups
loads are substantially slower, outweighing the customer's faster Functions,
C#, and post-load activation stages.

**Unknown:** This is still not a controlled machine-to-machine benchmark.
The customer project is unavailable, the workspaces differ, the activation
events differ (`onLanguage:csharp` versus `onLanguage:json`), and VS Code
changed from 1.140.0 to 1.141.0. The results identify engineering hotspots but
cannot prove that either machine is intrinsically faster.

## Capture scope and metadata

| Attribute | Baseline cold capture | Customer cold capture |
|---|---|---|
| Role in this report | Baseline | Customer example |
| Startup | Initial startup | Initial startup |
| VS Code | 1.141.0 | 1.140.0 |
| OS | Windows 10.0.26300 | Windows 10.0.26300 |
| CPU | AMD Ryzen AI 7 PRO 350, 16 logical processors | Intel Core Ultra 7 155H, 22 logical processors |
| Memory | 31.28 GB, 6.71 GB free | 63.32 GB, 47.12 GB free |
| Workspace | Baseline Logic Apps workspace | Customer project; unavailable for reproduction |
| Logic Apps activation trigger | `onLanguage:json` | `onLanguage:csharp` |
| User-visible readiness milestone | Unknown | Unknown |
| Runs represented | One | One |

### Comparability assessment

| Factor | Status | Impact |
|---|---|---|
| Cold versus cold | Comparable | Removes the largest problem in the original report. |
| OS build | Comparable | Both report Windows 10.0.26300. |
| VS Code version | Not comparable | Baseline 1.141.0 versus customer 1.140.0 may alter startup and Extension Host behavior. |
| Workspace/project | Not comparable | Project shape, file count, settings, restored state, and language activation differ. |
| Activation trigger | Not comparable | C# versus JSON changes which built-in and third-party extensions load and when. |
| Extension versions | Unknown | Package/version drift may explain component differences. |
| Readiness milestone | Unknown | Extension activation cannot be equated with designer or project readiness. |
| Repeated runs | Missing | A single run cannot establish variance or regression. |

The cold captures are suitable for a **directional component comparison**, not
a machine performance verdict.

## VS Code core versus Extension Host

### Core startup

| Core milestone | Baseline | Customer | Customer / baseline |
|---|---:|---:|---:|
| Renderer ready | 1,419 ms | 1,357 ms | 0.96x |
| Workbench ready | 2,010 ms | 1,939 ms | 0.96x |
| Overall workbench load | 515 ms | 647 ms | 1.26x |
| Register extensions and spawn Extension Host | 2,381 ms | 1,088 ms | 0.46x |
| Extensions registered | 4,289 ms | 2,879 ms | 0.67x |

**Observed:** User-facing core readiness differs by only 71 milliseconds at
`workbench ready` and 62 milliseconds at `renderer ready`.

**Observed:** Extension registration is 1.410 seconds earlier for the customer
than the baseline, with most of the difference in `register extensions & spawn
extension host`. Core and registration metrics therefore do not explain the
customer's longer Logic Apps dependency path.

**Hypothesis:** The extension inventory, VS Code version, machine state,
available memory, or security/filesystem conditions may contribute to the
registration difference.

**Unknown:** The reports do not isolate which of those factors is responsible.

### Extension Host initialization

| Milestone | Baseline | Customer |
|---|---:|---:|
| Extension Host ready | 2,582 ms | 1,108 ms |
| Logic Apps dependency path starts | 4,256 ms | 2,081 ms |
| Time from host ready to dependency path | 1,674 ms | 973 ms |

**Observed:** The customer reaches Extension Host readiness and starts the
dependency path earlier than the baseline. The customer slowdown occurs inside
the dependency-loading path, not before it.

## Top Logic Apps dependency timings

| Extension | Baseline load | Customer load | Customer / baseline | Directional finding |
|---|---:|---:|---:|---|
| `Azurite.azurite` | 12,268 ms | 27,071 ms | 2.21x | Largest customer excess and largest single customer interval. |
| `ms-azuretools.vscode-azurefunctions` | 5,323 ms | 3,049 ms | 0.57x | Customer is faster. |
| `ms-dotnettools.csharp` | 6,035 ms | 3,717 ms | 0.62x | Customer is faster. |
| `ms-azuretools.vscode-azureresourcegroups` | 644 ms | 3,239 ms | 5.03x | Large customer excess. |
| `ms-azuretools.vscode-azurelogicapps` | 1,298 ms | 781 ms | 0.60x | Customer's own Logic Apps module load is faster. |
| `ms-dotnettools.csdevkit` | 374 ms | 333 ms | 0.89x | Similar module-load duration. |
| `ms-dotnettools.vscode-dotnet-runtime` | 274 ms | 139 ms | 0.51x | Customer is faster; small absolute interval. |

Ratios are observations only. Workspace, activation event, VS Code version,
extension versions, cache state, and machine environment are not controlled.

## Logic Apps dependency path

### Customer dependency path

The raw Extension Host timeline proves this serialized code-loading sequence:

1. Azure Resource Groups: 3.238 seconds.
2. Azurite: 27.071 seconds.
3. .NET runtime extension: 0.139 seconds.
4. Azure Functions: 3.049 seconds.
5. C#: 3.717 seconds.
6. C# Dev Kit: 0.333 seconds.

The customer path begins at approximately 2.081 seconds and C# Dev Kit finishes at
40.342 seconds: a **38.3-second wall-clock interval** containing approximately
37.5 seconds of directly measured dependency code loading.

**Observed:** Customer Azurite accounts for about 72% of the measured
dependency code-load duration and is 14.803 seconds slower than the baseline.

### Baseline dependency path

The raw Extension Host timeline establishes:

1. Azure Resource Groups: 0.643 seconds.
2. Azurite: 12.267 seconds.
3. .NET runtime extension: 0.273 seconds.
4. Copilot Chat loads between dependencies: 0.735 seconds.
5. Azure Functions: 5.323 seconds.
6. C#: 6.035 seconds.
7. C# Dev Kit: 0.373 seconds.

The baseline path begins at approximately 4.256 seconds and C# Dev Kit finishes at
31.429 seconds: a **27.2-second wall-clock interval** containing approximately
24.9 seconds of directly measured Logic Apps dependency code loading.

**Observed:** This baseline interval is approximately 11.1 seconds shorter
than the customer interval.

**Observed:** The Extension Host is serialized during the large Azurite,
Functions, and C# code-load intervals. These intervals can delay other work on
that host regardless of whether every dependency is required for the first
user-visible Logic Apps milestone.

### Before the baseline dependency path

Before Azure Resource Groups starts, the raw timeline records approximately
0.9 seconds of unrelated extension code loading, including Mermaid Chart,
JSON language features, NPM, Emmet, Rainbow CSV, and authentication support.
This is materially lower than the roughly 8.1 seconds seen in the previous
warm/reopened capture.

**Observed:** Restored editors and activation state strongly affected the warm
capture. The cold capture is a better representation of startup, but a neutral
initially visible file should still be standardized for future runs.

## Activation completion findings

| Extension | Baseline finish activation | Customer finish activation |
|---|---:|---:|
| Logic Apps | 15,300 ms | 4,212 ms |
| C# | 8,693 ms | 223 ms |
| C# Dev Kit | 16,707 ms | 3,633 ms |
| Azure Functions | 38 ms | 28 ms |
| Azure Resource Groups | 36 ms | 20 ms |
| Azurite | 0 ms | 0 ms |

**Observed:** The customer has shorter completion values for Logic Apps, C#,
and C# Dev Kit than the baseline. These metrics do not explain the customer's
longer dependency-loading interval.

**Unknown:** `Finish Activate` may include asynchronous work and overlapping
waits. These values must not be added together or treated as a wall-clock
critical path.

**Hypothesis:** The baseline workspace or environment triggers additional
post-load C#/C# Dev Kit/Logic Apps initialization, potentially including
project discovery, language service startup, runtime discovery, or design-time
services. This is a baseline optimization opportunity, not evidence of the
customer slowdown.

**Unknown:** The startup report does not identify the awaited stages. Logs,
profiles, and stage-level instrumentation are required.

## Findings from the previous warm capture

The previous baseline reopened-window capture remains useful as
single-machine evidence:

- Core workbench readiness was 563 milliseconds.
- Azurite code loading was 32.968 seconds, compared with 12.268 seconds in the
  new cold capture.
- Azure Functions code loading was 15.091 seconds, compared with 5.323 seconds.
- Approximately 8.1 seconds of unrelated code loading occurred before the
  Logic Apps dependency path, compared with approximately 0.9 seconds in the
  new cold capture.

**Observed:** Large run-to-run/state-dependent variation exists on the same
machine. A single capture is therefore insufficient for regression decisions.

**Hypothesis:** Cache state, restored editors, competing extensions, extension
updates, or machine load may explain the variation.

**Unknown:** Because VS Code and extension state may have changed, the two
baseline captures are not a controlled cold-versus-warm experiment.

## Prioritized investigations

| Priority | Investigation | Expected discriminating outcome |
|---|---|---|
| P0 | Collect three cold runs and three `Developer: Reload Window` runs on the baseline machine using the same workspace, initially visible file, VS Code version, and extension versions. | Establishes median/range and determines whether Azurite, Functions, C#, and activation tails are repeatable. |
| P0 | Define and time user-visible milestones: project tree ready, designer usable, design-time API ready, and run/debug ready. | Determines which measured dependency stages actually block users. |
| P0 | Repeat with Azurite disabled for the workspace. | Tests whether Azurite's 12-27 second module load lies on the required readiness path; does not assume root cause. |
| P0 | Repeat with a minimal profile containing only required Logic Apps tooling. | Quantifies unrelated Extension Host contention and inventory/registration cost. |
| P1 | Capture an Extension Host CPU profile spanning Azurite, Functions, and C# loads. | Distinguishes JavaScript execution, module resolution, synchronous filesystem work, native calls, and idle/wait time. |
| P1 | Capture exact extension versions and environment inventory using the skill collector. | Exposes version drift and allows future captures to be reproduced. |
| P1 | Add stage-level Logic Apps marks around dependency acquisition, project discovery, runtime resolution, design-time host initialization, tree registration, designer services, and command registration. | Separates customer module-loading delay from baseline post-load activation delay. |
| P1 | Review C# and C# Dev Kit logs and process activity during activation. | Explains why the baseline has longer completion intervals despite a shorter dependency-loading path. |
| P1 | Run a synthetic sanitized Logic Apps workspace on both machines. | Provides a common project without requiring access to the customer project. |
| P2 | With security-team approval, capture filesystem/process traces or run a narrowly scoped security-scanning experiment. | Confirms or rejects filesystem/security contribution to module loading. |

## Recommended common-workspace strategy

Lack of access to the customer project does not block useful investigation.
Create a sanitized synthetic benchmark workspace that both engineers can use:

1. Pin the same VS Code version and all relevant extension versions.
2. Include a representative Logic Apps Standard project with agreed workflow,
   connector, project-file, and artifact counts.
3. Use identical workspace settings and the same initially visible neutral
   file.
4. Avoid secrets, managed-connection credentials, tenant details, production
   URLs, and customer content.
5. Record the benchmark workspace revision or archive hash with every capture.
6. Collect at least three cold and three warm runs per machine.

This will not reproduce every characteristic of the customer project, but it will
separate machine/environment effects from workspace-specific effects more
reliably than comparing unrelated projects.

## Suggested developer actions

1. **Decouple optional dependencies from first readiness.** Review whether
   Azurite, Azure Functions, C#, C# Dev Kit, and .NET runtime must all load
   before project-tree or designer readiness. Defer run/debug-only capabilities
   where product behavior permits.
2. **Profile module-loading hotspots.** Prioritize Azurite because it remains
   the largest single load, then Functions and C#. Examine package file count,
   dependency duplication, eager imports, module resolution, bundling, and
   synchronous filesystem operations.
3. **Instrument activation stages.** The current aggregate Logic Apps, C#, and
   C# Dev Kit completion values are too coarse to guide fixes.
4. **Separate readiness contracts.** Publish explicit project-tree, designer,
   design-time API, and run/debug readiness events rather than using extension
   activation completion as a proxy.
5. **Add a repeatable performance benchmark.** Use the synthetic workspace,
   pinned toolchain, cold/warm classifications, multiple runs, and median/range
   thresholds in engineering validation.
6. **Record dependency attribution.** Log why each dependency activated,
   whether it blocks the current milestone, and its stage start/end.
7. **Keep Extension Host startup separate from the customer issue.** The
   baseline spends an additional 1.293 seconds spawning/registering the
   Extension Host, while the customer still has the longer dependency path.

## Evidence gaps and privacy review

Missing evidence:

- Exact extension versions for each capture.
- A shared workspace or synthetic benchmark workspace.
- Repeated runs and variance.
- User-visible readiness timestamps.
- Running Extensions captures.
- Extension Host CPU profiles.
- Logic Apps, Functions, Azurite, C#, and C# Dev Kit logs.
- Storage type, endpoint-security state, proxy/VPN state, and filesystem
  location.

Before sharing future evidence, review it for user paths, identities, tenant
information, URLs, tokens, connection details, and workspace content.

### Sanitization applied before sharing

- Replaced participant and machine-owner identifiers with `baseline` and
  `customer`.
- Replaced the Windows user-profile segment with `REDACTED_USER`.
- Redacted GitHub avatar account IDs.
- Redacted the environment-specific MCP server name.
- Converted the Logic Apps extension repository references from absolute local
  paths to repository-relative paths.
- Retained public VS Code extension IDs and public service endpoints because
  they are required to interpret activation and resource-timing evidence.
- No credentials, access tokens, API keys, connection strings, tenant IDs, or
  subscription IDs were detected in the shareable workspace files.

## Appendix A: Logic Apps extension dependency and activation review

### Summary

**Observed:** The dependency startup chain is configured by the Logic Apps
extension manifest. The production manifest lists Azure Functions, Azurite,
Azure Resource Groups, C#, and C# Dev Kit under `extensionDependencies`:

`LogicAppsUX\apps\vs-code-designer\src\package.json:1109-1115`

`extensionDependencies` expresses an extension runtime dependency, not only an
installation recommendation. This differs from `extensionPack`, which VS Code
documents as extensions that can be installed together. See the
[VS Code extension manifest reference](https://code.visualstudio.com/api/references/extension-manifest).

**Observed:** The performance reports corroborate the runtime relationship.
Azure Functions, Azurite, Azure Resource Groups, C#, C# Dev Kit, and the
transitive .NET runtime extension report:

`By = ms-azuretools.vscode-azurelogicapps`

This means that activating Logic Apps caused VS Code to activate or load those
dependencies in the measured sessions.

### Activation events amplify the dependency chain

**Observed:** The Logic Apps manifest contains these activation events:

- `onView:azureWorkspace`
- `onView:azureResourceGroups`
- `workspaceContains:host.json`
- `workspaceContains:*/host.json`
- `onDebugInitialConfigurations`
- `onStartupFinished`
- `onLanguage:csharp`
- `onLanguage:json`

Source:

`LogicAppsUX\apps\vs-code-designer\src\package.json:1116-1125`

**Observed:** The baseline capture activates Logic Apps through
`onLanguage:json`, while the customer capture activates it through
`onLanguage:csharp`. Once Logic Apps activates, its `extensionDependencies`
propagate that activation into the dependency chain.

**Hypothesis:** `onStartupFinished`, `onLanguage:json`, and
`onLanguage:csharp` are broader than required for the first Logic Apps
user-visible milestone. In particular, opening an ordinary JSON or C# file can
start the Logic Apps dependency chain even when the user is not opening the
designer or starting/debugging a workflow.

**Unknown:** Each activation event may support an existing behavior not
visible from the startup reports. Remove or narrow an event only after mapping
it to commands, views, debugging, project discovery, and backward-compatibility
requirements.

### Dependency-by-dependency source findings

| Dependency | Source observation | Engineering implication |
|---|---|---|
| Azurite | `executeOnAzuriteExt.ts:13-30` already locates Azurite and explicitly calls `activate()` only when an Azurite operation requires it. | Strong candidate to move from `extensionDependencies` to install-only packaging such as `extensionPack`. The existing feature-boundary activation can preserve debug behavior while avoiding unconditional startup activation. |
| Azure Functions | `executeOnFunctionsExt.ts:15-22` checks whether Functions is active and warns if it is not; it does not currently activate it. | If removed from `extensionDependencies`, update Functions-backed feature entry points to activate the extension on demand or return a clear unavailable/activation error. |
| Azure Resource Groups | `main.ts:196-207` awaits `getResourceGroupsApi()`, stores its tree API, registers the Logic Apps resolver, and obtains the Azure Resources v2 API during Logic Apps activation. | This is a genuine activation-time API dependency today. Removing it from `extensionDependencies` requires moving cloud-tree initialization behind the Azure view or cloud-command boundary. |
| C# | Listed in `extensionDependencies`; the targeted production search found no direct `extensions.getExtension('ms-dotnettools.csharp')` call. | It may be an installation/tooling prerequisite rather than an unconditional activation prerequisite. Validate codeless, codeful, designer, build, and debug behavior before changing it. |
| C# Dev Kit | Listed in `extensionDependencies`; E2E setup explicitly requires it because extension activation expects it. | Current tests encode mandatory activation. Refactoring requires changing both production readiness assumptions and E2E setup, especially for codeful projects. |
| .NET runtime | Not directly listed by Logic Apps; the E2E setup identifies it as a transitive dependency of C#/C# Dev Kit. | Its startup load should defer naturally if C# tooling is no longer activated for codeless or designer-only scenarios. |

Additional source references:

- Azurite feature-boundary activation:
  `LogicAppsUX\apps\vs-code-designer\src\app\azuriteExtension\executeOnAzuriteExt.ts:13-30`
- Functions active-state assumption:
  `LogicAppsUX\apps\vs-code-designer\src\app\functionsExtension\executeOnFunctionsExt.ts:15-22`
- Azure Resource Groups API initialization:
  `LogicAppsUX\apps\vs-code-designer\src\main.ts:196-207`
- E2E dependency assumptions and transitive .NET runtime handling:
  `LogicAppsUX\apps\vs-code-designer\src\test\ui\run-e2e.ts:684-709`

### Recommended dependency model

**Hypothesis:** A staged dependency model can preserve installation behavior
without forcing every installed extension onto the first-readiness path:

1. Use `extensionPack` for extensions that should be installed with Logic Apps
   but are not required for base activation.
2. Keep `extensionDependencies` only for extensions whose API must be available
   before Logic Apps can safely complete `activate()`.
3. Activate optional extensions at the command, view, designer, codeful, build,
   or debug feature boundary that requires them.
4. Report missing, disabled, or failed optional dependencies explicitly rather
   than silently degrading the requested feature.
5. Separate local project/designer readiness from Azure cloud-tree readiness.

### Candidate implementation order

| Priority | Candidate change | Reason |
|---|---|---|
| P0 | Add stage-level marks around dependency readiness and user-visible milestones before changing behavior. | Establishes which dependency actually blocks project-tree, designer, design-time API, and debug readiness. |
| P0 | Narrow or remove broad `onStartupFinished`, `onLanguage:json`, and `onLanguage:csharp` events where feature mapping permits. | Prevents unrelated editor activity from starting the full Logic Apps dependency chain. |
| P0 | Move Azurite to install-only/on-demand activation and retain the existing explicit activation at the debug boundary. | Azurite is the largest customer code-load interval, and the repository already contains an on-demand activation path. |
| P1 | Gate C# and C# Dev Kit activation on the presence or invocation of codeful functionality. | Codeless project-tree and designer scenarios may not require language tooling at first readiness. |
| P1 | Add explicit on-demand Azure Functions activation for Functions-backed commands, then remove it as an unconditional dependency if tests permit. | Preserves command behavior without requiring Functions for unrelated designer/project operations. |
| P1 | Lazily initialize Azure Resource Groups for Azure views and cloud operations. | It is currently awaited during activation even though local project/designer readiness may not require the cloud tree. |

### Required controlled validation

No dependency should be reclassified using timing correlation alone. Validate
each candidate change with:

1. At least three cold and three warm runs using a pinned VS Code and extension
   set.
2. Codeless and codeful Logic Apps projects.
3. Project-tree, designer, design-time API, build, run, and debug milestones.
4. Azure subscription/resource-tree operations.
5. Missing, disabled, activation-failure, and incompatible-version dependency
   cases.
6. A comparison of Extension Host ordering and user-visible readiness, not
   only aggregate `Finish Activate` values.

**Unknown:** Until those controlled tests are run, the repository review
establishes why dependencies enter the startup chain but does not prove that
each dependency can be safely deferred.
