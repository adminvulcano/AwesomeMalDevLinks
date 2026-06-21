# https://github.com/evilsocket/audit

[Skip to content](https://github.com/evilsocket/audit#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/evilsocket/audit) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/evilsocket/audit) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/evilsocket/audit) to refresh your session.Dismiss alert

{{ message }}

[evilsocket](https://github.com/evilsocket)/ **[audit](https://github.com/evilsocket/audit)** Public

- [Notifications](https://github.com/login?return_to=%2Fevilsocket%2Faudit) You must be signed in to change notification settings
- [Fork\\
99](https://github.com/login?return_to=%2Fevilsocket%2Faudit)
- [Star\\
646](https://github.com/login?return_to=%2Fevilsocket%2Faudit)


main

[**1** Branch](https://github.com/evilsocket/audit/branches) [**0** Tags](https://github.com/evilsocket/audit/tags)

[Go to Branches page](https://github.com/evilsocket/audit/branches)[Go to Tags page](https://github.com/evilsocket/audit/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![evilsocket](https://avatars.githubusercontent.com/u/86922?v=4&size=40)](https://github.com/evilsocket)[evilsocket](https://github.com/evilsocket/audit/commits?author=evilsocket)<br>[Merge pull request](https://github.com/evilsocket/audit/commit/d6ee73035f47d9b6ff3353e6fe030395d85e6e08) [#5](https://github.com/evilsocket/audit/pull/5) [from aviat/fix/session-limit-resume-requeue](https://github.com/evilsocket/audit/commit/d6ee73035f47d9b6ff3353e6fe030395d85e6e08)<br>Open commit details<br>2 weeks agoJun 10, 2026<br>[d6ee730](https://github.com/evilsocket/audit/commit/d6ee73035f47d9b6ff3353e6fe030395d85e6e08) · 2 weeks agoJun 10, 2026<br>## History<br>[15 Commits](https://github.com/evilsocket/audit/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/evilsocket/audit/commits/main/) 15 Commits |
| [audit](https://github.com/evilsocket/audit/tree/main/audit "audit") | [audit](https://github.com/evilsocket/audit/tree/main/audit "audit") | [Merge pull request](https://github.com/evilsocket/audit/commit/d6ee73035f47d9b6ff3353e6fe030395d85e6e08 "Merge pull request #5 from aviat/fix/session-limit-resume-requeue  fix: treat \"session limit\" as quota-exhausted and re-queue interrupted tasks on resume") [#5](https://github.com/evilsocket/audit/pull/5) [from aviat/fix/session-limit-resume-requeue](https://github.com/evilsocket/audit/commit/d6ee73035f47d9b6ff3353e6fe030395d85e6e08 "Merge pull request #5 from aviat/fix/session-limit-resume-requeue  fix: treat \"session limit\" as quota-exhausted and re-queue interrupted tasks on resume") | 2 weeks agoJun 10, 2026 |
| [config](https://github.com/evilsocket/audit/tree/main/config "config") | [config](https://github.com/evilsocket/audit/tree/main/config "config") | [fix: handle SDK client initialization timeout and improve error resil…](https://github.com/evilsocket/audit/commit/c82705481cd9291e420368fc470b33c1b2ee79b3 "fix: handle SDK client initialization timeout and improve error resilience  - Restructure ClaudeSDKClient async context to catch initialization   timeouts as TransientAgentError instead of crashing the runner - Add catch-all error handler in hunt stage so a single task failure   doesn't abort the entire run - Add repair_attempts: 2 to gapfill and feedback stages - Fix priority field type in gapfill/feedback prompts (integer, not string)") | 3 weeks agoMay 29, 2026 |
| [docs](https://github.com/evilsocket/audit/tree/main/docs "docs") | [docs](https://github.com/evilsocket/audit/tree/main/docs "docs") | [things](https://github.com/evilsocket/audit/commit/80d746e4f74b93fc21c4e1c184c262edf730c7c9 "things") | last monthMay 18, 2026 |
| [prompts](https://github.com/evilsocket/audit/tree/main/prompts "prompts") | [prompts](https://github.com/evilsocket/audit/tree/main/prompts "prompts") | [fix: handle SDK client initialization timeout and improve error resil…](https://github.com/evilsocket/audit/commit/c82705481cd9291e420368fc470b33c1b2ee79b3 "fix: handle SDK client initialization timeout and improve error resilience  - Restructure ClaudeSDKClient async context to catch initialization   timeouts as TransientAgentError instead of crashing the runner - Add catch-all error handler in hunt stage so a single task failure   doesn't abort the entire run - Add repair_attempts: 2 to gapfill and feedback stages - Fix priority field type in gapfill/feedback prompts (integer, not string)") | 3 weeks agoMay 29, 2026 |
| [schemas](https://github.com/evilsocket/audit/tree/main/schemas "schemas") | [schemas](https://github.com/evilsocket/audit/tree/main/schemas "schemas") | [initial: 8-stage vulnerability discovery harness](https://github.com/evilsocket/audit/commit/d03e6b0360f0268b1ae20b5ee8e92392d0197e7c "initial: 8-stage vulnerability discovery harness") | last monthMay 18, 2026 |
| [tests](https://github.com/evilsocket/audit/tree/main/tests "tests") | [tests](https://github.com/evilsocket/audit/tree/main/tests "tests") | [fix: treat "session limit" as quota-exhausted and re-queue interrupte…](https://github.com/evilsocket/audit/commit/60fc8eed7b154b97bf70977b08e313cb82d38b35 "fix: treat \"session limit\" as quota-exhausted and re-queue interrupted tasks on resume  Subscription session-limit errors (\"You've hit your session limit · resets …\") were classified as unknown→transient, so the runner burned its backoff retries and then marked each hunt task permanently 'failed'. Because Hunt only dispatches 'pending' tasks and resume never re-queued 'failed'/'running' ones, an interrupted run could finish and report itself 'completed' on a fraction of its intended coverage.  - runner.py: add \"session limit\" to _QUOTA_MARKERS so these errors   classify as quota_exhausted (terminal) and abort into a resumable   state instead of retrying a cap that resets hours later. - hunt.py: catch QuotaExhaustedError explicitly — leave the task   'pending' (not 'failed') and re-raise so the pipeline aborts cleanly. - state.py: add reset_incomplete_tasks() to re-queue 'running'/'failed'   tasks to 'pending'. - orchestrator.py: call it on --resume so interrupted/failed work is   actually re-attempted. - tests: cover session-limit classification and the reset helper.  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 3 weeks agoJun 2, 2026 |
| [.env.example](https://github.com/evilsocket/audit/blob/main/.env.example ".env.example") | [.env.example](https://github.com/evilsocket/audit/blob/main/.env.example ".env.example") | [initial: 8-stage vulnerability discovery harness](https://github.com/evilsocket/audit/commit/d03e6b0360f0268b1ae20b5ee8e92392d0197e7c "initial: 8-stage vulnerability discovery harness") | last monthMay 18, 2026 |
| [.gitignore](https://github.com/evilsocket/audit/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/evilsocket/audit/blob/main/.gitignore ".gitignore") | [new: integrated stuff from my stuff](https://github.com/evilsocket/audit/commit/0f44307aee69a41938ea75028aebe7b974d23a74 "new: integrated stuff from my stuff") | last monthMay 19, 2026 |
| [LICENSE](https://github.com/evilsocket/audit/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/evilsocket/audit/blob/main/LICENSE "LICENSE") | [things](https://github.com/evilsocket/audit/commit/80d746e4f74b93fc21c4e1c184c262edf730c7c9 "things") | last monthMay 18, 2026 |
| [README.md](https://github.com/evilsocket/audit/blob/main/README.md "README.md") | [README.md](https://github.com/evilsocket/audit/blob/main/README.md "README.md") | [open auth](https://github.com/evilsocket/audit/commit/6dd18433d036a3d7c14aa6d78f64786b8e9262a4 "open auth") | last monthMay 19, 2026 |
| [pyproject.toml](https://github.com/evilsocket/audit/blob/main/pyproject.toml "pyproject.toml") | [pyproject.toml](https://github.com/evilsocket/audit/blob/main/pyproject.toml "pyproject.toml") | [things](https://github.com/evilsocket/audit/commit/80d746e4f74b93fc21c4e1c184c262edf730c7c9 "things") | last monthMay 18, 2026 |
| View all files |

## Repository files navigation

# audit

[Permalink: audit](https://github.com/evilsocket/audit#audit)

An 8-stage vulnerability-discovery agent, driven by your **Claude Pro / Max**
**subscription** through the official Claude Code Agent SDK. Many narrow agents,
deliberate disagreement, and an explicit reachability gate.

MIT-licensed. No API key needed if you already use `claude login`.

## Origin

[Permalink: Origin](https://github.com/evilsocket/audit#origin)

This project is a from-scratch reimplementation of the pipeline described in
Cloudflare's [Project Glasswing](https://blog.cloudflare.com/cyber-frontier-models/)
post, which tested Anthropic's Mythos preview LLM against Cloudflare's own
codebase. The blog argues that real-world vulnerability discovery does **not**
come from asking one big model "find bugs here" — it comes from:

1. **Many narrow agents** working in parallel on tightly-scoped questions
("Look for command injection in this specific function, with this trust
boundary above it") rather than one exhaustive agent.
2. **Deliberate disagreement** — a second agent, on a different model, that
tries to _disprove_ the first agent's findings.
3. **A reachability trace** as the gating step — most "is this code buggy?"
findings are noise unless an attacker-controlled input can actually reach
the sink from outside the system.
4. **A feedback loop** so reachable bugs in one place automatically seed
hunts for the same pattern elsewhere.

This repo packages that pipeline into a runnable agent. The Cloudflare post
showed the architecture; this codebase ships the prompts, schemas, state
store, and orchestrator.

## The 8 stages

[Permalink: The 8 stages](https://github.com/evilsocket/audit#the-8-stages)

![Vulnerability discovery harness — 8 stages](https://raw.githubusercontent.com/evilsocket/audit/main/docs/pipeline.png)

Diagram from Cloudflare's [Project Glasswing](https://blog.cloudflare.com/cyber-frontier-models/) post, reproduced here for reference.

| # | Stage | Default model | Purpose |
| --- | --- | --- | --- |
| 1 | Recon | Opus 4.7 | Map the repo, emit narrowly-scoped Hunt tasks |
| 2 | Hunt | Sonnet 4.6 | One attack class per agent; compile/run PoCs |
| 3 | Validate | Opus 4.7 | Adversarial re-read; tries to **disprove** (different model from Hunt) |
| 4 | Gapfill | Sonnet 4.6 | Re-queue under-covered areas |
| 5 | Dedupe | Sonnet 4.6 | Cluster findings by root cause |
| 6 | Trace | Opus 4.7 | Prove attacker-controlled input reaches the sink |
| 7 | Feedback | Sonnet 4.6 | Turn reachable traces into new Hunt tasks |
| 8 | Report | Sonnet 4.6 | Schema-validated structured report |

Each stage is one markdown prompt in `prompts/` \+ one JSON Schema in
`schemas/`. The orchestrator passes the schema into the system prompt so
every output is shape-stable on the first try.

## Quickstart

[Permalink: Quickstart](https://github.com/evilsocket/audit#quickstart)

```
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Auth (pick one)
#    (a) Already logged in via claude login? You're done.
#    (b) Or generate a 1-year OAuth token for CI / non-interactive use:
claude setup-token
echo "CLAUDE_CODE_OAUTH_TOKEN=<paste>" > .env

# 3. Verify
audit auth-check

# 4. Run
audit run --repo /path/to/target --run-id my-run
audit status --run-id my-run
audit report --run-id my-run --format md > report.md
```

By default the agent uses **subscription billing** via your Claude.ai
login — it does **not** call the metered Anthropic API. The on-disk auth
module scrubs `ANTHROPIC_API_KEY` from the environment so it can't
silently route around the OAuth flow.

## Using a different model / provider

[Permalink: Using a different model / provider](https://github.com/evilsocket/audit#using-a-different-model--provider)

The auth module picks one of three modes, in this order:

1. **LLM gateway** (OpenRouter, custom proxy, etc.) — when
`ANTHROPIC_BASE_URL` points away from `anthropic.com` AND
`ANTHROPIC_AUTH_TOKEN` is set. The gateway env is left intact;
only `ANTHROPIC_API_KEY` is scrubbed (it would otherwise outrank the
gateway token).
2. **Subscription OAuth (headless)** — `CLAUDE_CODE_OAUTH_TOKEN` from
`claude setup-token`. Best for CI.
3. **Subscription OAuth (interactive)** — `~/.claude/.credentials.json`
from `claude login`. Best for local dev.

### OpenRouter

[Permalink: OpenRouter](https://github.com/evilsocket/audit#openrouter)

OpenRouter exposes Claude-compatible Anthropic-API endpoints behind its
own credit system; that lets you spend OpenRouter credits instead of an
Anthropic subscription, and gives you access to Sonnet/Opus _and_ other
models through the same SDK path. See [OpenRouter's Agent SDK guide](https://openrouter.ai/docs/guides/community/anthropic-agent-sdk).

```
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""           # must be explicitly empty / unset
# optional: pick a non-Anthropic model
export ANTHROPIC_MODEL="anthropic/claude-sonnet-4-6"
# or e.g.: ANTHROPIC_MODEL="openai/gpt-5"
#         ANTHROPIC_MODEL="google/gemini-2.5-pro"
#         ANTHROPIC_MODEL="qwen/qwen3-coder-480b"

audit auth-check                       # confirms "using LLM gateway at https://openrouter.ai/api"
audit run --repo /path/to/target --run-id orun --max-cost-usd 30
```

Caveats:

- Per-stage model overrides in `config/stages.yaml` are model **names**
(e.g. `claude-opus-4-7`); OpenRouter accepts slash-prefixed forms like
`anthropic/claude-opus-4-7`. Edit the YAML if you want different
providers per stage. Otherwise `ANTHROPIC_MODEL` forces every stage
onto one model.
- Non-Claude models may not produce schema-compliant JSON as reliably.
The runner's schema-validation + repair turn still applies; quality
varies by model.
- Tool-use semantics (Read/Grep/Glob/Bash) are part of the Claude Code
CLI, not the model — they work as long as the gateway speaks the
Anthropic Messages API.

### Other gateways / cloud providers

[Permalink: Other gateways / cloud providers](https://github.com/evilsocket/audit#other-gateways--cloud-providers)

Same recipe — anything that exposes the Anthropic Messages API at a URL

- a bearer token works:

```
export ANTHROPIC_BASE_URL="https://your-proxy.example.com"
export ANTHROPIC_AUTH_TOKEN="$YOUR_TOKEN"
unset ANTHROPIC_API_KEY
```

For Amazon Bedrock / Google Vertex / Microsoft Foundry, Claude Code has
first-class env-var flags (`CLAUDE_CODE_USE_BEDROCK=1` etc.) that
outrank everything else. See the [Claude Code auth docs](https://code.claude.com/docs/en/authentication).

## Cost containment

[Permalink: Cost containment](https://github.com/evilsocket/audit#cost-containment)

A real production codebase can produce 15-50 Hunt tasks and 25+ findings to
validate. At default concurrency this gets expensive. Flags to keep it sane:

```
audit run --repo /path/to/target \
  --max-concurrency 1 \           # one claude subprocess at a time
  --max-recon-tasks 15 \          # cap initial Hunt fanout
  --max-cost-usd 30               # abort cleanly if exceeded
```

The budget guard fires between _and_ within stages — a per-task check in
Hunt cooperatively aborts rather than running 30 more tasks past the cap.

## Live-target reproduction (optional)

[Permalink: Live-target reproduction (optional)](https://github.com/evilsocket/audit#live-target-reproduction-optional)

If the target has a running deployment, point the agents at it. Hunt now
**reproduces** each finding against the live service instead of compiling
a local PoC, Validate **rejects** findings that don't reproduce, and Trace
**confirms** reachability with real HTTP round-trips. The static path
remains available — these flags are opt-in.

```
audit run --repo /path/to/target --run-id live \
  --max-concurrency 1 --max-cost-usd 30 \
  --target-url http://server.local:8888 \
  --target-creds email=admin@system.com \
  --target-creds password=changechangeme
```

Rules the agents follow when `--target-url` is set:

- Network egress is restricted to that host + `127.0.0.1`. No other external
hosts.
- A finding that doesn't reproduce against the live target is dropped or
rejected (depending on stage) — "no fabrication".
- Credentials flow into every relevant stage's user\_input as a dict.

## Scope notes (optional)

[Permalink: Scope notes (optional)](https://github.com/evilsocket/audit#scope-notes-optional)

Targets often have intentionally-loose-by-design surfaces that aren't bugs
(e.g. plaintext API keys when that's a feature, test-only Mailpit endpoints,
anonymous-analytics ingest). Drop them in a text file and pass it in — the
notes are appended verbatim to every stage's user\_input, and Recon / Hunt /
Validate honor exclusions you list.

```
audit run --repo /path/to/target --scope-notes target_scope.md
```

Example `target_scope.md`:

```
- Mailpit (port 1025) is test-only; ignore.
- Plaintext API keys in the database are a required feature.
- Don't flag rate-limit absence on anonymous /ping endpoints.
- Only consider critical/high severity.
```

## Recon mines git history

[Permalink: Recon mines git history](https://github.com/evilsocket/audit#recon-mines-git-history)

Recon greps the git history for past security patches
(`CVE`, `sec:`, `fix.*auth`, `sanitize`, …) — patched files are hardened,
but **sibling files with the same idiom often aren't**. Findings get seeded
against the unpatched copies. Adds zero cost on repos without that pattern;
catches real cross-component bugs on repos that have it.

## Logic chains

[Permalink: Logic chains](https://github.com/evilsocket/audit#logic-chains)

The pipeline's default is one-attack-class-per-task (the Cloudflare paper's
narrow-scope rule). Recon can also emit `logic_chain` tasks for high-impact
multi-component paths (auth-bypass + IDOR + path-traversal that compose into
RCE, etc.) — one chain per task, with the `scope_hint` naming the specific
chain. This is the one allowed exception to single-attack-class scoping.

## Layout

[Permalink: Layout](https://github.com/evilsocket/audit#layout)

```
prompts/        8 stage prompts (markdown, loaded as system prompts)
schemas/        9 JSON schemas — every agent output is validated
config/         stages.yaml — model + concurrency + tool allowlist per stage
audit/          Python package
  auth.py       OAuth check + ANTHROPIC_API_KEY scrubbing
  state.py      SQLite DAO (runs, tasks, findings, traces, dedupe, costs)
  runner.py     claude-agent-sdk wrapper with schema validation + repair turn
  orchestrator.py pipeline driver
  stages/       one module per stage
work/           per-Hunt-task scratch dirs (sandbox for PoC compile/run)
results/        JSONL artifacts per stage + final report.json
state.db        SQLite (gitignored)
```

## Safety

[Permalink: Safety](https://github.com/evilsocket/audit#safety)

Hunt agents have Bash and run inside per-task scratch dirs. They are **not**
sandboxed at the OS level. Run the audit inside a disposable VM or container
when you don't trust the target source — a target with malicious build
scripts could otherwise execute on your host during PoC compilation.

The agent reads everything you `--add-dir`, including any `.env` or
`secrets/` directories in the target. Outputs land in `results/<run-id>/`
which is `.gitignore`d but **not** scrubbed of those reads.

## License

[Permalink: License](https://github.com/evilsocket/audit#license)

[MIT](https://github.com/evilsocket/audit/blob/main/LICENSE). Reuse freely. No warranty.

## Acknowledgements

[Permalink: Acknowledgements](https://github.com/evilsocket/audit#acknowledgements)

- The pipeline design is from Cloudflare's [Project Glasswing](https://blog.cloudflare.com/cyber-frontier-models/)
blog post. The credit for the architecture goes there.
- Built on the official [Claude Code Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview).

## About

An 8-stage vulnerability-discovery agent.


### Resources

[Readme](https://github.com/evilsocket/audit#readme-ov-file)

### License

[MIT license](https://github.com/evilsocket/audit#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/evilsocket/audit).

[Activity](https://github.com/evilsocket/audit/activity)

### Stars

[**646**\\
stars](https://github.com/evilsocket/audit/stargazers)

### Watchers

[**1**\\
watching](https://github.com/evilsocket/audit/watchers)

### Forks

[**99**\\
forks](https://github.com/evilsocket/audit/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fevilsocket%2Faudit&report=evilsocket+%28user%29)

## [Releases](https://github.com/evilsocket/audit/releases)

No releases published

## [Packages\  0](https://github.com/users/evilsocket/packages?repo_name=audit)

No packages published

## [Contributors\  6](https://github.com/evilsocket/audit/graphs/contributors)

- [![@evilsocket](https://avatars.githubusercontent.com/u/86922?s=64&v=4)](https://github.com/evilsocket)
- [![@claude](https://avatars.githubusercontent.com/u/81847?s=64&v=4)](https://github.com/claude)
- [![@TheCjw](https://avatars.githubusercontent.com/u/2680302?s=64&v=4)](https://github.com/TheCjw)
- [![@aviat](https://avatars.githubusercontent.com/u/13485545?s=64&v=4)](https://github.com/aviat)
- [![@MarkAtwood](https://avatars.githubusercontent.com/u/34491708?s=64&v=4)](https://github.com/MarkAtwood)
- [![@5h4d0wr007](https://avatars.githubusercontent.com/u/51066119?s=64&v=4)](https://github.com/5h4d0wr007)

## Languages

- [Python100.0%](https://github.com/evilsocket/audit/search?l=python)

You can’t perform that action at this time.