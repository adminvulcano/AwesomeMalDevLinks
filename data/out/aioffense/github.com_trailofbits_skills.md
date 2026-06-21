# https://github.com/trailofbits/skills/

[Skip to content](https://github.com/trailofbits/skills#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/trailofbits/skills) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/trailofbits/skills) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/trailofbits/skills) to refresh your session.Dismiss alert

{{ message }}

[trailofbits](https://github.com/trailofbits)/ **[skills](https://github.com/trailofbits/skills)** Public

- [Notifications](https://github.com/login?return_to=%2Ftrailofbits%2Fskills) You must be signed in to change notification settings
- [Fork\\
509](https://github.com/login?return_to=%2Ftrailofbits%2Fskills)
- [Star\\
5.8k](https://github.com/login?return_to=%2Ftrailofbits%2Fskills)


main

[**18** Branches](https://github.com/trailofbits/skills/branches) [**0** Tags](https://github.com/trailofbits/skills/tags)

[Go to Branches page](https://github.com/trailofbits/skills/branches)[Go to Tags page](https://github.com/trailofbits/skills/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![jonathanreedmevs](https://avatars.githubusercontent.com/u/25496287?v=4&size=40)![dguido](https://avatars.githubusercontent.com/u/294844?v=4&size=40)![claude](https://avatars.githubusercontent.com/u/81847?v=4&size=40)<br>3 people<br>[fix(fp-check): use correct JSON response format in stop hooks (](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e) [#129](https://github.com/trailofbits/skills/pull/129) [)](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e)<br>Open commit detailssuccess<br>2 weeks agoJun 10, 2026<br>[c070b9b](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e) · 2 weeks agoJun 10, 2026<br>## History<br>[121 Commits](https://github.com/trailofbits/skills/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/trailofbits/skills/commits/main/) 121 Commits |
| [.claude-plugin](https://github.com/trailofbits/skills/tree/main/.claude-plugin ".claude-plugin") | [.claude-plugin](https://github.com/trailofbits/skills/tree/main/.claude-plugin ".claude-plugin") | [fix(fp-check): use correct JSON response format in stop hooks (](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e "fix(fp-check): use correct JSON response format in stop hooks (#129)  * fix(fp-check): use correct JSON response format in stop hooks  Prompt-type stop hooks must respond with JSON. The previous prompts instructed Claude to return plain text ('block' or 'approve'), causing 'Stop hook error: JSON validation failed' on every session end.  Updated both Stop and SubagentStop hook prompts to respond with: - {\"decision\": \"block\", \"reason\": \"...\"} to prevent stopping - {} to allow stopping (omitting decision field per Claude Code docs)  Bug discovered by Claude while debugging the JSON validation error during active use of the fp-check skill.  * fix: use documented ok/reason schema for prompt hooks, bump to 1.0.2  Per https://code.claude.com/docs/en/hooks.md (Prompt-based hooks > Response schema), prompt hooks must respond {\"ok\": true} to allow or {\"ok\": false, \"reason\": \"...\"} to block — not {\"decision\": \"block\"} or {}. Also bump to 1.0.2 since main already shipped 1.0.1 without this fix; clients only update when the version increases.  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Fable 5 <noreply@anthropic.com>") [#129](https://github.com/trailofbits/skills/pull/129) [)](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e "fix(fp-check): use correct JSON response format in stop hooks (#129)  * fix(fp-check): use correct JSON response format in stop hooks  Prompt-type stop hooks must respond with JSON. The previous prompts instructed Claude to return plain text ('block' or 'approve'), causing 'Stop hook error: JSON validation failed' on every session end.  Updated both Stop and SubagentStop hook prompts to respond with: - {\"decision\": \"block\", \"reason\": \"...\"} to prevent stopping - {} to allow stopping (omitting decision field per Claude Code docs)  Bug discovered by Claude while debugging the JSON validation error during active use of the fp-check skill.  * fix: use documented ok/reason schema for prompt hooks, bump to 1.0.2  Per https://code.claude.com/docs/en/hooks.md (Prompt-based hooks > Response schema), prompt hooks must respond {\"ok\": true} to allow or {\"ok\": false, \"reason\": \"...\"} to block — not {\"decision\": \"block\"} or {}. Also bump to 1.0.2 since main already shipped 1.0.1 without this fix; clients only update when the version increases.  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Fable 5 <noreply@anthropic.com>") | 2 weeks agoJun 10, 2026 |
| [.github](https://github.com/trailofbits/skills/tree/main/.github ".github") | [.github](https://github.com/trailofbits/skills/tree/main/.github ".github") | [Bump actions/checkout from 6.0.2 to 6.0.3 in the all group (](https://github.com/trailofbits/skills/commit/c910ecf7390a741b727210c03d230f34fb0bc62b "Bump actions/checkout from 6.0.2 to 6.0.3 in the all group (#182)  Bumps the all group with 1 update: [actions/checkout](https://github.com/actions/checkout).   Updates `actions/checkout` from 6.0.2 to 6.0.3 - [Release notes](https://github.com/actions/checkout/releases) - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) - [Commits](https://github.com/actions/checkout/compare/de0fac2e4500dabe0009e67214ff5f5447ce83dd...df4cb1c069e1874edd31b4311f1884172cec0e10)  --- updated-dependencies: - dependency-name: actions/checkout   dependency-version: 6.0.3   dependency-type: direct:production   update-type: version-update:semver-patch   dependency-group: all ...  Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>") [#182](https://github.com/trailofbits/skills/pull/182) [)](https://github.com/trailofbits/skills/commit/c910ecf7390a741b727210c03d230f34fb0bc62b "Bump actions/checkout from 6.0.2 to 6.0.3 in the all group (#182)  Bumps the all group with 1 update: [actions/checkout](https://github.com/actions/checkout).   Updates `actions/checkout` from 6.0.2 to 6.0.3 - [Release notes](https://github.com/actions/checkout/releases) - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) - [Commits](https://github.com/actions/checkout/compare/de0fac2e4500dabe0009e67214ff5f5447ce83dd...df4cb1c069e1874edd31b4311f1884172cec0e10)  --- updated-dependencies: - dependency-name: actions/checkout   dependency-version: 6.0.3   dependency-type: direct:production   update-type: version-update:semver-patch   dependency-group: all ...  Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>") | 2 weeks agoJun 10, 2026 |
| [plugins](https://github.com/trailofbits/skills/tree/main/plugins "plugins") | [plugins](https://github.com/trailofbits/skills/tree/main/plugins "plugins") | [fix(fp-check): use correct JSON response format in stop hooks (](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e "fix(fp-check): use correct JSON response format in stop hooks (#129)  * fix(fp-check): use correct JSON response format in stop hooks  Prompt-type stop hooks must respond with JSON. The previous prompts instructed Claude to return plain text ('block' or 'approve'), causing 'Stop hook error: JSON validation failed' on every session end.  Updated both Stop and SubagentStop hook prompts to respond with: - {\"decision\": \"block\", \"reason\": \"...\"} to prevent stopping - {} to allow stopping (omitting decision field per Claude Code docs)  Bug discovered by Claude while debugging the JSON validation error during active use of the fp-check skill.  * fix: use documented ok/reason schema for prompt hooks, bump to 1.0.2  Per https://code.claude.com/docs/en/hooks.md (Prompt-based hooks > Response schema), prompt hooks must respond {\"ok\": true} to allow or {\"ok\": false, \"reason\": \"...\"} to block — not {\"decision\": \"block\"} or {}. Also bump to 1.0.2 since main already shipped 1.0.1 without this fix; clients only update when the version increases.  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Fable 5 <noreply@anthropic.com>") [#129](https://github.com/trailofbits/skills/pull/129) [)](https://github.com/trailofbits/skills/commit/c070b9b5881183ea5f6e320ff06c46688becb13e "fix(fp-check): use correct JSON response format in stop hooks (#129)  * fix(fp-check): use correct JSON response format in stop hooks  Prompt-type stop hooks must respond with JSON. The previous prompts instructed Claude to return plain text ('block' or 'approve'), causing 'Stop hook error: JSON validation failed' on every session end.  Updated both Stop and SubagentStop hook prompts to respond with: - {\"decision\": \"block\", \"reason\": \"...\"} to prevent stopping - {} to allow stopping (omitting decision field per Claude Code docs)  Bug discovered by Claude while debugging the JSON validation error during active use of the fp-check skill.  * fix: use documented ok/reason schema for prompt hooks, bump to 1.0.2  Per https://code.claude.com/docs/en/hooks.md (Prompt-based hooks > Response schema), prompt hooks must respond {\"ok\": true} to allow or {\"ok\": false, \"reason\": \"...\"} to block — not {\"decision\": \"block\"} or {}. Also bump to 1.0.2 since main already shipped 1.0.1 without this fix; clients only update when the version increases.  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Fable 5 <noreply@anthropic.com>") | 2 weeks agoJun 10, 2026 |
| [.gitignore](https://github.com/trailofbits/skills/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/trailofbits/skills/blob/main/.gitignore ".gitignore") | [gh-cli: Replace skill with hooks-only enforcement (](https://github.com/trailofbits/skills/commit/00c013dba72e9d86841bad9173d88883de8c9def "gh-cli: Replace skill with hooks-only enforcement (#114)  * Add hooks to block gh api contents fallback and enforce session-scoped clone paths  Add two new PreToolUse hooks: - intercept-gh-api-contents: blocks `gh api repos/.../contents/... | base64 -d`   and suggests cloning instead - intercept-gh-clone-path: denies `gh repo clone` to non-session-scoped temp   paths, enforcing the `$TMPDIR/gh-clones-$CLAUDE_SESSION_ID/` convention  Update existing fetch/curl hooks to warn against the `gh api` contents anti-pattern in their denial messages. Update skill docs and references to discourage base64-decoding file contents via the API.  Bump version 1.3.0 → 1.6.0.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Replace regex-based PreToolUse hooks with a gh PATH shim  Swap intercept-gh-api-contents.sh and intercept-gh-clone-path.sh (regex-matched PreToolUse hooks) for a single shims/gh wrapper prepended to PATH via a SessionStart hook. The shim receives properly tokenized $@ args, eliminating the class of regex bypass bugs identified in PR review (subshell, @base64d, compound command gaps). All /contents/ API access is now blocked unconditionally.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix gh shim clone bypass, exec error handling, and docs accuracy  - Replace hardcoded $4 clone target with arg iteration to prevent   flag-based bypass (e.g., -u upstream owner/repo /tmp/bad-path) - Handle exec failure on real gh binary with error message and exit 126 - Add diagnostic message when gh not found on PATH in setup-shims.sh - Add error handling for CLAUDE_ENV_FILE write failure - Replace blocked gh api contents example in SKILL.md Quick Start - Fix incorrect --branch <sha> docs (git clone --branch requires a   branch/tag name, not a commit SHA) - Rename misleading \"exits silently\" test names to \"exits gracefully\" - Add test for clone bypass with flags before target path  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix review findings: dead exec handler, inaccurate docs, add tests  Remove unreachable || block after exec in the gh shim (dead code since exec replaces the process). Fix shallow clone + SHA checkout guidance to note --depth 1 must be omitted. Qualify README passthrough list to account for shim interceptions. Improve anti-pattern docs and api.md Headers section. Add 4 tests: bare gh passthrough, tmp substring path, session-scoped /var/folders/, missing shims dir.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Address PR review: shim executable check, tests, comment/doc accuracy  - Validate shims/gh is executable in setup-shims.sh before writing PATH - Add tests: API contents with query params, long-form flags before clone   target, non-executable shim file - Fix README \"silently pass through\" wording - Clarify shim comment on flag-value scanning behavior - Rename test for clarity on flag-preceding-target behavior  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Remove using-gh-cli skill, keep hooks-only enforcement  The skill rarely triggered (~0-11% recall across eval runs) because Claude's system prompt already includes gh CLI instructions. The hooks (WebFetch/curl interception, gh shim, clone cleanup) enforce the critical behaviors regardless of skill triggering, making the skill redundant.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix CI: marketplace description mismatch, shellcheck, bats test  - Sync marketplace.json description with plugin.json - Add shellcheck disable directives for bats subshell warnings - Use absolute bash path in setup-shims test to handle PATH filtering  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Remove skill reference from gh-cli README  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix curl hook circular suggestion, shim false positives, and session ID diagnostic  - Curl hook: add api.github.com/repos/.../contents/ branch before   generic catch-all so it suggests clone instead of gh api (which the   shim would then block) - Shim: anchor /contents/ regex to ^repos/ and skip flags so jq filter   values don't cause false positives - Shim: emit specific diagnostic when CLAUDE_SESSION_ID is unset   instead of a self-contradicting suggestion - Curl hook: remove redundant gh/git early exits so compound commands   like \"curl github.com/... && gh version\" are correctly denied - Tests: add coverage for all three fixes  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Add error handling for shim exec failure and session ID persistence  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix review issues: exec dead code, leading-slash bypass, exit codes, fetch contents gap  - Fix exec failure handler in gh shim: disable set -e around exec so   the error message is actually reachable, use resolved path consistently - Handle leading-slash API endpoints (gh api /repos/.../contents/...)   by changing regex from ^repos/ to ^/?repos/ - Exit 1 (not 0) when CLAUDE_ENV_FILE is missing in setup-shims.sh,   since this is a runtime contract violation, not graceful degradation - Add /contents/ branch to fetch hook for api.github.com URLs so   WebFetch to api.github.com/repos/.../contents/ gets the clone   suggestion instead of the generic gh api suggestion - Add tests for all fixes (leading slash, /private/tmp session path,   CLAUDE_ENV_FILE exit code, fetch contents endpoint)  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com> Co-authored-by: Dan Guido <dan@trailofbits.com>") [#114](https://github.com/trailofbits/skills/pull/114) [)](https://github.com/trailofbits/skills/commit/00c013dba72e9d86841bad9173d88883de8c9def "gh-cli: Replace skill with hooks-only enforcement (#114)  * Add hooks to block gh api contents fallback and enforce session-scoped clone paths  Add two new PreToolUse hooks: - intercept-gh-api-contents: blocks `gh api repos/.../contents/... | base64 -d`   and suggests cloning instead - intercept-gh-clone-path: denies `gh repo clone` to non-session-scoped temp   paths, enforcing the `$TMPDIR/gh-clones-$CLAUDE_SESSION_ID/` convention  Update existing fetch/curl hooks to warn against the `gh api` contents anti-pattern in their denial messages. Update skill docs and references to discourage base64-decoding file contents via the API.  Bump version 1.3.0 → 1.6.0.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Replace regex-based PreToolUse hooks with a gh PATH shim  Swap intercept-gh-api-contents.sh and intercept-gh-clone-path.sh (regex-matched PreToolUse hooks) for a single shims/gh wrapper prepended to PATH via a SessionStart hook. The shim receives properly tokenized $@ args, eliminating the class of regex bypass bugs identified in PR review (subshell, @base64d, compound command gaps). All /contents/ API access is now blocked unconditionally.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix gh shim clone bypass, exec error handling, and docs accuracy  - Replace hardcoded $4 clone target with arg iteration to prevent   flag-based bypass (e.g., -u upstream owner/repo /tmp/bad-path) - Handle exec failure on real gh binary with error message and exit 126 - Add diagnostic message when gh not found on PATH in setup-shims.sh - Add error handling for CLAUDE_ENV_FILE write failure - Replace blocked gh api contents example in SKILL.md Quick Start - Fix incorrect --branch <sha> docs (git clone --branch requires a   branch/tag name, not a commit SHA) - Rename misleading \"exits silently\" test names to \"exits gracefully\" - Add test for clone bypass with flags before target path  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix review findings: dead exec handler, inaccurate docs, add tests  Remove unreachable || block after exec in the gh shim (dead code since exec replaces the process). Fix shallow clone + SHA checkout guidance to note --depth 1 must be omitted. Qualify README passthrough list to account for shim interceptions. Improve anti-pattern docs and api.md Headers section. Add 4 tests: bare gh passthrough, tmp substring path, session-scoped /var/folders/, missing shims dir.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Address PR review: shim executable check, tests, comment/doc accuracy  - Validate shims/gh is executable in setup-shims.sh before writing PATH - Add tests: API contents with query params, long-form flags before clone   target, non-executable shim file - Fix README \"silently pass through\" wording - Clarify shim comment on flag-value scanning behavior - Rename test for clarity on flag-preceding-target behavior  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Remove using-gh-cli skill, keep hooks-only enforcement  The skill rarely triggered (~0-11% recall across eval runs) because Claude's system prompt already includes gh CLI instructions. The hooks (WebFetch/curl interception, gh shim, clone cleanup) enforce the critical behaviors regardless of skill triggering, making the skill redundant.  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix CI: marketplace description mismatch, shellcheck, bats test  - Sync marketplace.json description with plugin.json - Add shellcheck disable directives for bats subshell warnings - Use absolute bash path in setup-shims test to handle PATH filtering  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Remove skill reference from gh-cli README  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix curl hook circular suggestion, shim false positives, and session ID diagnostic  - Curl hook: add api.github.com/repos/.../contents/ branch before   generic catch-all so it suggests clone instead of gh api (which the   shim would then block) - Shim: anchor /contents/ regex to ^repos/ and skip flags so jq filter   values don't cause false positives - Shim: emit specific diagnostic when CLAUDE_SESSION_ID is unset   instead of a self-contradicting suggestion - Curl hook: remove redundant gh/git early exits so compound commands   like \"curl github.com/... && gh version\" are correctly denied - Tests: add coverage for all three fixes  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Add error handling for shim exec failure and session ID persistence  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>  * Fix review issues: exec dead code, leading-slash bypass, exit codes, fetch contents gap  - Fix exec failure handler in gh shim: disable set -e around exec so   the error message is actually reachable, use resolved path consistently - Handle leading-slash API endpoints (gh api /repos/.../contents/...)   by changing regex from ^repos/ to ^/?repos/ - Exit 1 (not 0) when CLAUDE_ENV_FILE is missing in setup-shims.sh,   since this is a runtime contract violation, not graceful degradation - Add /contents/ branch to fetch hook for api.github.com URLs so   WebFetch to api.github.com/repos/.../contents/ gets the clone   suggestion instead of the generic gh api suggestion - Add tests for all fixes (leading slash, /private/tmp session path,   CLAUDE_ENV_FILE exit code, fetch contents endpoint)  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com> Co-authored-by: Dan Guido <dan@trailofbits.com>") | 3 months agoMar 3, 2026 |
| [.pre-commit-config.yaml](https://github.com/trailofbits/skills/blob/main/.pre-commit-config.yaml ".pre-commit-config.yaml") | [.pre-commit-config.yaml](https://github.com/trailofbits/skills/blob/main/.pre-commit-config.yaml ".pre-commit-config.yaml") | [Add --write flag to shfmt pre-commit hook (](https://github.com/trailofbits/skills/commit/39dd47e05bf924fac54ccb424f1a28550e3a2a74 "Add --write flag to shfmt pre-commit hook (#44)  Custom args in .pre-commit-config.yaml replace default args rather than extend them. The shfmt hook's default args include --write, but our custom args (-i 2 -ci) were missing it. Without --write, shfmt outputs to stdout and exits 0 regardless of formatting issues.  Co-authored-by: Claude Opus 4.5 <noreply@anthropic.com>") [#44](https://github.com/trailofbits/skills/pull/44) [)](https://github.com/trailofbits/skills/commit/39dd47e05bf924fac54ccb424f1a28550e3a2a74 "Add --write flag to shfmt pre-commit hook (#44)  Custom args in .pre-commit-config.yaml replace default args rather than extend them. The shfmt hook's default args include --write, but our custom args (-i 2 -ci) were missing it. Without --write, shfmt outputs to stdout and exits 0 regardless of formatting issues.  Co-authored-by: Claude Opus 4.5 <noreply@anthropic.com>") | 5 months agoJan 26, 2026 |
| [AGENTS.md](https://github.com/trailofbits/skills/blob/main/AGENTS.md "AGENTS.md") | [AGENTS.md](https://github.com/trailofbits/skills/blob/main/AGENTS.md "AGENTS.md") | [Remove legacy codex compatiblity scripts/shims. (](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#173](https://github.com/trailofbits/skills/pull/173) [)](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 5, 2026 |
| [CLAUDE.md](https://github.com/trailofbits/skills/blob/main/CLAUDE.md "CLAUDE.md") | [CLAUDE.md](https://github.com/trailofbits/skills/blob/main/CLAUDE.md "CLAUDE.md") | [Remove legacy codex compatiblity scripts/shims. (](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#173](https://github.com/trailofbits/skills/pull/173) [)](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 5, 2026 |
| [CODEOWNERS](https://github.com/trailofbits/skills/blob/main/CODEOWNERS "CODEOWNERS") | [CODEOWNERS](https://github.com/trailofbits/skills/blob/main/CODEOWNERS "CODEOWNERS") | [C review (](https://github.com/trailofbits/skills/commit/870955f1af03acfec736f77c287219bc01af11e9 "C review (#156)  * init c review  * lsp  * agents -> prompts  * wip  * add windows, update judges  * improve  * upgrade  * size update  * rm toon format, improve workflow, cluster agents/prompts by issue type, improve prompt cache  * improve general workflow, fix bugs  * sarif via script, cluster manifest  * fix bugs  * fix workflow2  * workflow updates  * more fixes  * more fixes  * improvements  * update readme  * update codeowners  * update codeowners2  * fix small inconsistencies  * Address review feedback on c-review plugin  Critical: - Move SKILL.md into named skill subdirectory (plugins/c-review/skills/c-review/)   so plugin discovery and the Codex validator find it; add .codex/skills/c-review   symlink. - Convert allowed-tools in SKILL.md from YAML list to space-delimited string   (spec compliance per #139). - Fix parse_scalar in generate_sarif.py to respect quoted strings when splitting   inline lists; [\"a,b\", c] no longer corrupts to ['\"a', 'b\"', 'c']. - Fix location_parts trailing-colon handling so 'src/foo.c:' resolves to   ('src/foo.c', 1) instead of keeping the colon in the filename.  Important: - Convert agent tools: from YAML list to comma-separated string in worker,   dedup-judge, fp-judge. - Refactor build_run_plan.py main() (131 → 77 lines) by extracting   _validate_run_inputs / _render_workers / _print_summary helpers. - Fix ty possibly-missing-attribute warning by typing workers list explicitly. - Add PEP 723 inline metadata + plugins/c-review/scripts/pyproject.toml. - Rewrite SKILL.md description as scenario-based; add When to Use /   When NOT to Use section headers. - Add Usage section to README. - Resolve Tier 2 contradiction in dedup-judge: unparseable/multi findings   now skip Tier 2 and go straight to Tier 3. - Standardize placeholder convention in fp-judge ({var} not <var>). - Fix \"Widthness Overflows\" → \"Width Truncation\" in integer-overflow-finder. - Standardize \"Bug Patterns to Find\" heading in signal-handler and   thread-safety finders. - Replace ls -1 glob in worker shard-write with find for shell portability. - Bump version 1.1.0 → 1.1.1 in plugin.json + marketplace.json.  Verification: codex validator passes (73 plugin skills); ruff + ty clean; main() 77 lines (limit 100); SARIF generator runtime tests pass; end-to-end build_run_plan.py produces all 11 clusters with cache primer.  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>  * Address claude[bot] review feedback on c-review  - Phase 1 is_posix/is_windows probes in SKILL.md now include C++ extensions   (.cpp, .cxx, .cc, .hpp, .hh) in their --include lists. A pure C++ POSIX   daemon was silently dropping ~17 POSIX-gated passes plus all is_windows   clusters because pthread.h / windows.h includes only in .cpp/.hpp files   failed both --include='*.c' --include='*.h' filters. - generate_sarif.py informationUri points at trailofbits/skills (the actual   repo) instead of trailofbits/tob-skills (404). - CODEOWNERS: add @dguido co-owner to /plugins/c-review/ and move it to the   top of the c* alphabetical group (- < l < o < u under ASCII collation). - README.md: move c-review row after burpsuite-project-parser (b < c). - Bump version 1.1.1 → 1.1.2.  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>") [#156](https://github.com/trailofbits/skills/pull/156) [)](https://github.com/trailofbits/skills/commit/870955f1af03acfec736f77c287219bc01af11e9 "C review (#156)  * init c review  * lsp  * agents -> prompts  * wip  * add windows, update judges  * improve  * upgrade  * size update  * rm toon format, improve workflow, cluster agents/prompts by issue type, improve prompt cache  * improve general workflow, fix bugs  * sarif via script, cluster manifest  * fix bugs  * fix workflow2  * workflow updates  * more fixes  * more fixes  * improvements  * update readme  * update codeowners  * update codeowners2  * fix small inconsistencies  * Address review feedback on c-review plugin  Critical: - Move SKILL.md into named skill subdirectory (plugins/c-review/skills/c-review/)   so plugin discovery and the Codex validator find it; add .codex/skills/c-review   symlink. - Convert allowed-tools in SKILL.md from YAML list to space-delimited string   (spec compliance per #139). - Fix parse_scalar in generate_sarif.py to respect quoted strings when splitting   inline lists; [\"a,b\", c] no longer corrupts to ['\"a', 'b\"', 'c']. - Fix location_parts trailing-colon handling so 'src/foo.c:' resolves to   ('src/foo.c', 1) instead of keeping the colon in the filename.  Important: - Convert agent tools: from YAML list to comma-separated string in worker,   dedup-judge, fp-judge. - Refactor build_run_plan.py main() (131 → 77 lines) by extracting   _validate_run_inputs / _render_workers / _print_summary helpers. - Fix ty possibly-missing-attribute warning by typing workers list explicitly. - Add PEP 723 inline metadata + plugins/c-review/scripts/pyproject.toml. - Rewrite SKILL.md description as scenario-based; add When to Use /   When NOT to Use section headers. - Add Usage section to README. - Resolve Tier 2 contradiction in dedup-judge: unparseable/multi findings   now skip Tier 2 and go straight to Tier 3. - Standardize placeholder convention in fp-judge ({var} not <var>). - Fix \"Widthness Overflows\" → \"Width Truncation\" in integer-overflow-finder. - Standardize \"Bug Patterns to Find\" heading in signal-handler and   thread-safety finders. - Replace ls -1 glob in worker shard-write with find for shell portability. - Bump version 1.1.0 → 1.1.1 in plugin.json + marketplace.json.  Verification: codex validator passes (73 plugin skills); ruff + ty clean; main() 77 lines (limit 100); SARIF generator runtime tests pass; end-to-end build_run_plan.py produces all 11 clusters with cache primer.  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>  * Address claude[bot] review feedback on c-review  - Phase 1 is_posix/is_windows probes in SKILL.md now include C++ extensions   (.cpp, .cxx, .cc, .hpp, .hh) in their --include lists. A pure C++ POSIX   daemon was silently dropping ~17 POSIX-gated passes plus all is_windows   clusters because pthread.h / windows.h includes only in .cpp/.hpp files   failed both --include='*.c' --include='*.h' filters. - generate_sarif.py informationUri points at trailofbits/skills (the actual   repo) instead of trailofbits/tob-skills (404). - CODEOWNERS: add @dguido co-owner to /plugins/c-review/ and move it to the   top of the c* alphabetical group (- < l < o < u under ASCII collation). - README.md: move c-review row after burpsuite-project-parser (b < c). - Bump version 1.1.1 → 1.1.2.  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>") | last monthMay 3, 2026 |
| [LICENSE](https://github.com/trailofbits/skills/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/trailofbits/skills/blob/main/LICENSE "LICENSE") | [Initial release of Trail of Bits Skills Marketplace](https://github.com/trailofbits/skills/commit/695119c312e0eadbd953c30b9e051b7dfa4163dd "Initial release of Trail of Bits Skills Marketplace  16 plugins for security analysis, smart contract auditing, and verification:  Smart Contract Security: - building-secure-contracts - entry-point-analyzer  Code Auditing: - audit-context-building - burpsuite-project-parser - differential-review - semgrep-rule-creator - sharp-edges - testing-handbook-skills - variant-analysis  Verification: - constant-time-analysis - property-based-testing - spec-to-code-compliance  Audit Lifecycle: - fix-review  Reverse Engineering: - dwarf-expert  Development: - ask-questions-if-underspecified  Team Management: - culture-index  Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>") | 5 months agoJan 14, 2026 |
| [README.md](https://github.com/trailofbits/skills/blob/main/README.md "README.md") | [README.md](https://github.com/trailofbits/skills/blob/main/README.md "README.md") | [Remove legacy codex compatiblity scripts/shims. (](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#173](https://github.com/trailofbits/skills/pull/173) [)](https://github.com/trailofbits/skills/commit/f09e5c729a297834680d0fbff675743ca23bf4a6 "Remove legacy codex compatiblity scripts/shims. (#173)  * Remove legacy codex compatiblity scripts/shims.  Codex supports claude plugins so this shouldn't be necessary. Add a script to test the plugin loadablility in both claude and codex  * fix: resolve code review findings for PR #173  Review findings addressed (4 reviewers: pr-review-toolkit agents, Codex gpt-5.3-codex, direct diff review):  P2 fixed: - Bump versions for the 5 substantively changed plugins in both   plugin.json and marketplace.json (gh-cli 1.5.0 new skill,   claude-in-chrome-troubleshooting 1.1.0 skill rename,   modern-python 1.5.1 / skill-improver 1.0.3 hooks change,   zeroize-audit 0.1.1 MCP config relocation) so clients pick up   the changes - README Codex install: replace unpasteable /plugins slash-command   block with verified CLI syntax (codex plugin marketplace add) - check_claude_loadability: parse_json_output now fails fast with   command context on empty CLI output instead of returning None - check_codex_loadability: surface skipped RPC error messages in   timeout failures instead of a bare TimeoutError  P3 fixed: - Both checkers: error out when marketplace.json lists no plugins   instead of passing vacuously  Dismissed: - @latest CLI installs in validate.yml: deliberate; the check   validates against the clients users actually run - select.select portability: CI-only script on ubuntu-latest - Divergent mcpServers validation between checkers: intentional;   the Codex checker enforces the repo's .mcp.json convention  Verified: ruff, prek, validate_plugin_metadata.py, and both loadability checks pass end-to-end (39 plugins, 74 skills, 2 MCP servers load in Claude Code and Codex)  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 5, 2026 |
| [ruff.toml](https://github.com/trailofbits/skills/blob/main/ruff.toml "ruff.toml") | [ruff.toml](https://github.com/trailofbits/skills/blob/main/ruff.toml "ruff.toml") | [Add hook for gh-cli (](https://github.com/trailofbits/skills/commit/dca4d846ada14b48447ce36a1ecaebe269bfaa3a "Add hook for gh-cli (#78)  * Add hook for gh-cli  This should prevent claude code from wasting cycles trying to fetch from Github which will not work 90% of the time.  * Add guidance for claude for updating CODEOWNERS  * update codeowners  * fix: resolve code review findings for PR #78  - Add actions and gist endpoint handling to curl hook (parity with fetch hook) - Skip non-repo github.com paths (settings, notifications, login) in fetch hook - Move gh-cli entry to correct alphabetical position in marketplace.json - Fix stale \"prefer-gh-cli\" name in test_helper.bash comment - Remove unused Grep from SKILL.md allowed-tools  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  * fix: improve agent self-correction suggestions for PR #78  Add specific pattern matching for github.com PR, issue, release-download, and tree URLs so the deny message suggests the exact correct gh command (e.g., `gh pr view 78 --repo owner/repo`) instead of the generic `gh repo view owner/repo` catch-all. Also add releases/download pattern to the curl hook.  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>") [#78](https://github.com/trailofbits/skills/pull/78) [)](https://github.com/trailofbits/skills/commit/dca4d846ada14b48447ce36a1ecaebe269bfaa3a "Add hook for gh-cli (#78)  * Add hook for gh-cli  This should prevent claude code from wasting cycles trying to fetch from Github which will not work 90% of the time.  * Add guidance for claude for updating CODEOWNERS  * update codeowners  * fix: resolve code review findings for PR #78  - Add actions and gist endpoint handling to curl hook (parity with fetch hook) - Skip non-repo github.com paths (settings, notifications, login) in fetch hook - Move gh-cli entry to correct alphabetical position in marketplace.json - Fix stale \"prefer-gh-cli\" name in test_helper.bash comment - Remove unused Grep from SKILL.md allowed-tools  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  * fix: improve agent self-correction suggestions for PR #78  Add specific pattern matching for github.com PR, issue, release-download, and tree URLs so the deny message suggests the exact correct gh command (e.g., `gh pr view 78 --repo owner/repo`) instead of the generic `gh repo view owner/repo` catch-all. Also add releases/download pattern to the curl hook.  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Dan Guido <dan@trailofbits.com> Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>") | 4 months agoFeb 11, 2026 |
| View all files |

## Repository files navigation

# Trail of Bits Skills Marketplace

[Permalink: Trail of Bits Skills Marketplace](https://github.com/trailofbits/skills#trail-of-bits-skills-marketplace)

A Claude Code plugin marketplace from Trail of Bits providing skills to enhance AI-assisted security analysis, testing, and development workflows. Codex can load this marketplace through its Claude marketplace compatibility.

> Also see: [claude-code-config](https://github.com/trailofbits/claude-code-config) · [skills-curated](https://github.com/trailofbits/skills-curated) · [claude-code-devcontainer](https://github.com/trailofbits/claude-code-devcontainer) · [dropkit](https://github.com/trailofbits/dropkit)

## Installation

[Permalink: Installation](https://github.com/trailofbits/skills#installation)

### Claude Code Marketplace

[Permalink: Claude Code Marketplace](https://github.com/trailofbits/skills#claude-code-marketplace)

```
/plugin marketplace add trailofbits/skills
```

### Browse and Install Plugins

[Permalink: Browse and Install Plugins](https://github.com/trailofbits/skills#browse-and-install-plugins)

```
/plugin menu
```

### Codex

[Permalink: Codex](https://github.com/trailofbits/skills#codex)

Codex supports Claude plugin marketplaces directly, so this repository does not need Codex-specific sidecar metadata.

Install the marketplace with:

```
codex plugin marketplace add trailofbits/skills
codex plugin list
codex plugin add <plugin-name>@trailofbits
```

### Local Development

[Permalink: Local Development](https://github.com/trailofbits/skills#local-development)

To add the marketplace locally (e.g., for testing or development), navigate to the **parent directory** of this repository:

```
cd /path/to/parent  # e.g., if repo is at ~/projects/skills, be in ~/projects
/plugins marketplace add ./skills
```

## Available Plugins

[Permalink: Available Plugins](https://github.com/trailofbits/skills#available-plugins)

### Smart Contract Security

[Permalink: Smart Contract Security](https://github.com/trailofbits/skills#smart-contract-security)

| Plugin | Description |
| --- | --- |
| [building-secure-contracts](https://github.com/trailofbits/skills/blob/main/plugins/building-secure-contracts) | Smart contract security toolkit with vulnerability scanners for 6 blockchains |
| [entry-point-analyzer](https://github.com/trailofbits/skills/blob/main/plugins/entry-point-analyzer) | Identify state-changing entry points in smart contracts for security auditing |

### Code Auditing

[Permalink: Code Auditing](https://github.com/trailofbits/skills#code-auditing)

| Plugin | Description |
| --- | --- |
| [agentic-actions-auditor](https://github.com/trailofbits/skills/blob/main/plugins/agentic-actions-auditor) | Audit GitHub Actions workflows for AI agent security vulnerabilities |
| [audit-context-building](https://github.com/trailofbits/skills/blob/main/plugins/audit-context-building) | Build deep architectural context through ultra-granular code analysis |
| [burpsuite-project-parser](https://github.com/trailofbits/skills/blob/main/plugins/burpsuite-project-parser) | Search and extract data from Burp Suite project files |
| [c-review](https://github.com/trailofbits/skills/blob/main/plugins/c-review) | Comprehensive C/C++ security review with clustered parallel workers and SARIF output |
| [differential-review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review) | Security-focused differential review of code changes with git history analysis |
| [dimensional-analysis](https://github.com/trailofbits/skills/blob/main/plugins/dimensional-analysis) | Annotate codebases with dimensional analysis comments to detect unit mismatches and formula bugs |
| [fp-check](https://github.com/trailofbits/skills/blob/main/plugins/fp-check) | Systematic false positive verification for security bug analysis with mandatory gate reviews |
| [insecure-defaults](https://github.com/trailofbits/skills/blob/main/plugins/insecure-defaults) | Detect insecure default configurations, hardcoded credentials, and fail-open security patterns |
| [semgrep-rule-creator](https://github.com/trailofbits/skills/blob/main/plugins/semgrep-rule-creator) | Create and refine Semgrep rules for custom vulnerability detection |
| [semgrep-rule-variant-creator](https://github.com/trailofbits/skills/blob/main/plugins/semgrep-rule-variant-creator) | Port existing Semgrep rules to new target languages with test-driven validation |
| [sharp-edges](https://github.com/trailofbits/skills/blob/main/plugins/sharp-edges) | Identify error-prone APIs, dangerous configurations, and footgun designs |
| [static-analysis](https://github.com/trailofbits/skills/blob/main/plugins/static-analysis) | Static analysis toolkit with CodeQL, Semgrep, and SARIF parsing |
| [supply-chain-risk-auditor](https://github.com/trailofbits/skills/blob/main/plugins/supply-chain-risk-auditor) | Audit supply-chain threat landscape of project dependencies |
| [testing-handbook-skills](https://github.com/trailofbits/skills/blob/main/plugins/testing-handbook-skills) | Skills from the [Testing Handbook](https://appsec.guide/): fuzzers, static analysis, sanitizers, coverage |
| [trailmark](https://github.com/trailofbits/skills/blob/main/plugins/trailmark) | Code graph analysis, Mermaid diagrams, mutation testing triage, and protocol verification |
| [variant-analysis](https://github.com/trailofbits/skills/blob/main/plugins/variant-analysis) | Find similar vulnerabilities across codebases using pattern-based analysis |

### Malware Analysis

[Permalink: Malware Analysis](https://github.com/trailofbits/skills#malware-analysis)

| Plugin | Description |
| --- | --- |
| [yara-authoring](https://github.com/trailofbits/skills/blob/main/plugins/yara-authoring) | YARA detection rule authoring with linting, atom analysis, and best practices |

### Verification

[Permalink: Verification](https://github.com/trailofbits/skills#verification)

| Plugin | Description |
| --- | --- |
| [constant-time-analysis](https://github.com/trailofbits/skills/blob/main/plugins/constant-time-analysis) | Detect compiler-induced timing side-channels in cryptographic code |
| [mutation-testing](https://github.com/trailofbits/skills/blob/main/plugins/mutation-testing) | Configure mewt/muton mutation testing campaigns — scope targets, tune timeouts, optimize long runs |
| [property-based-testing](https://github.com/trailofbits/skills/blob/main/plugins/property-based-testing) | Property-based testing guidance for multiple languages and smart contracts |
| [spec-to-code-compliance](https://github.com/trailofbits/skills/blob/main/plugins/spec-to-code-compliance) | Specification-to-code compliance checker for blockchain audits |
| [zeroize-audit](https://github.com/trailofbits/skills/blob/main/plugins/zeroize-audit) | Detect missing or compiler-eliminated zeroization of secrets in C/C++ and Rust |

### Reverse Engineering

[Permalink: Reverse Engineering](https://github.com/trailofbits/skills#reverse-engineering)

| Plugin | Description |
| --- | --- |
| [dwarf-expert](https://github.com/trailofbits/skills/blob/main/plugins/dwarf-expert) | Interact with and understand the DWARF debugging format |

### Mobile Security

[Permalink: Mobile Security](https://github.com/trailofbits/skills#mobile-security)

| Plugin | Description |
| --- | --- |
| [firebase-apk-scanner](https://github.com/trailofbits/skills/blob/main/plugins/firebase-apk-scanner) | Scan Android APKs for Firebase security misconfigurations |

### Development

[Permalink: Development](https://github.com/trailofbits/skills#development)

| Plugin | Description |
| --- | --- |
| [ask-questions-if-underspecified](https://github.com/trailofbits/skills/blob/main/plugins/ask-questions-if-underspecified) | Clarify requirements before implementing |
| [devcontainer-setup](https://github.com/trailofbits/skills/blob/main/plugins/devcontainer-setup) | Create pre-configured devcontainers with Claude Code and language-specific tooling |
| [gh-cli](https://github.com/trailofbits/skills/blob/main/plugins/gh-cli) | Intercept GitHub URL fetches and redirect to the authenticated `gh` CLI |
| [git-cleanup](https://github.com/trailofbits/skills/blob/main/plugins/git-cleanup) | Safely clean up git worktrees and local branches with gated confirmation workflow |
| [let-fate-decide](https://github.com/trailofbits/skills/blob/main/plugins/let-fate-decide) | Draw Tarot cards using cryptographic randomness to add entropy to vague planning |
| [modern-python](https://github.com/trailofbits/skills/blob/main/plugins/modern-python) | Modern Python tooling and best practices with uv, ruff, and pytest |
| [seatbelt-sandboxer](https://github.com/trailofbits/skills/blob/main/plugins/seatbelt-sandboxer) | Generate minimal macOS Seatbelt sandbox configurations |
| [second-opinion](https://github.com/trailofbits/skills/blob/main/plugins/second-opinion) | Run code reviews using external LLM CLIs (OpenAI Codex, Google Gemini) on changes, diffs, or commits. Bundles Codex's built-in MCP server. |
| [skill-improver](https://github.com/trailofbits/skills/blob/main/plugins/skill-improver) | Iterative skill refinement loop using automated fix-review cycles |
| [workflow-skill-design](https://github.com/trailofbits/skills/blob/main/plugins/workflow-skill-design) | Design patterns for workflow-based Claude Code skills with review agent |

### Team Management

[Permalink: Team Management](https://github.com/trailofbits/skills#team-management)

| Plugin | Description |
| --- | --- |
| [culture-index](https://github.com/trailofbits/skills/blob/main/plugins/culture-index) | Interpret Culture Index survey results for individuals and teams |

### Tooling

[Permalink: Tooling](https://github.com/trailofbits/skills#tooling)

| Plugin | Description |
| --- | --- |
| [claude-in-chrome-troubleshooting](https://github.com/trailofbits/skills/blob/main/plugins/claude-in-chrome-troubleshooting) | Diagnose and fix Claude in Chrome MCP extension connectivity issues |

### Infrastructure

[Permalink: Infrastructure](https://github.com/trailofbits/skills#infrastructure)

| Plugin | Description |
| --- | --- |
| [debug-buttercup](https://github.com/trailofbits/skills/blob/main/plugins/debug-buttercup) | Debug [Buttercup](https://github.com/trailofbits/buttercup) Kubernetes deployments |

## Trophy Case

[Permalink: Trophy Case](https://github.com/trailofbits/skills#trophy-case)

Bugs discovered using Trail of Bits Skills. Found something? [Let us know!](https://github.com/trailofbits/skills/issues/new?template=trophy-case.yml)

When reporting bugs you've found, feel free to mention:

> Found using [Trail of Bits Skills](https://github.com/trailofbits/skills)

| Skill | Bug |
| --- | --- |
| constant-time-analysis | [Timing side-channel in ML-DSA signing](https://github.com/RustCrypto/signatures/pull/1144) |

## Contributing

[Permalink: Contributing](https://github.com/trailofbits/skills#contributing)

We welcome contributions! Please see [CLAUDE.md](https://github.com/trailofbits/skills/blob/main/CLAUDE.md) for skill authoring guidelines.

## License

[Permalink: License](https://github.com/trailofbits/skills#license)

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). Made by [Trail of Bits](https://www.trailofbits.com/).

## About

Trail of Bits Claude Code skills for security research, vulnerability detection, and audit workflows


### Topics

[agent-skills](https://github.com/topics/agent-skills "Topic: agent-skills")

### Resources

[Readme](https://github.com/trailofbits/skills#readme-ov-file)

### License

[CC-BY-SA-4.0 license](https://github.com/trailofbits/skills#CC-BY-SA-4.0-1-ov-file)

### Security policy

[Security policy](https://github.com/trailofbits/skills#security-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/trailofbits/skills).

[Activity](https://github.com/trailofbits/skills/activity)

[Custom properties](https://github.com/trailofbits/skills/custom-properties)

### Stars

[**5.8k**\\
stars](https://github.com/trailofbits/skills/stargazers)

### Watchers

[**63**\\
watching](https://github.com/trailofbits/skills/watchers)

### Forks

[**509**\\
forks](https://github.com/trailofbits/skills/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Ftrailofbits%2Fskills&report=trailofbits+%28user%29)

## [Releases](https://github.com/trailofbits/skills/releases)

No releases published

## [Packages\  0](https://github.com/orgs/trailofbits/packages?repo_name=skills)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/trailofbits/skills).

## [Contributors\  37](https://github.com/trailofbits/skills/graphs/contributors)

- [![@claude](https://avatars.githubusercontent.com/u/81847?s=64&v=4)](https://github.com/claude)
- [![@dguido](https://avatars.githubusercontent.com/u/294844?s=64&v=4)](https://github.com/dguido)
- [![@Ninja3047](https://avatars.githubusercontent.com/u/1284324?s=64&v=4)](https://github.com/Ninja3047)
- [![@ahpaleus](https://avatars.githubusercontent.com/u/38883201?s=64&v=4)](https://github.com/ahpaleus)
- [![@GrosQuildu](https://avatars.githubusercontent.com/u/6371919?s=64&v=4)](https://github.com/GrosQuildu)
- [![@tob-scott-a](https://avatars.githubusercontent.com/u/147527775?s=64&v=4)](https://github.com/tob-scott-a)
- [![@dependabot[bot]](https://avatars.githubusercontent.com/in/29110?s=64&v=4)](https://github.com/apps/dependabot)
- [![@DarkaMaul](https://avatars.githubusercontent.com/u/8711456?s=64&v=4)](https://github.com/DarkaMaul)
- [![@bsamuels453](https://avatars.githubusercontent.com/u/1222451?s=64&v=4)](https://github.com/bsamuels453)
- [![@tob-joe](https://avatars.githubusercontent.com/u/118293845?s=64&v=4)](https://github.com/tob-joe)
- [![@hbrodin](https://avatars.githubusercontent.com/u/90325907?s=64&v=4)](https://github.com/hbrodin)
- [![@lightcap](https://avatars.githubusercontent.com/u/12123?s=64&v=4)](https://github.com/lightcap)
- [![@computerality](https://avatars.githubusercontent.com/u/464609?s=64&v=4)](https://github.com/computerality)
- [![@jonathanhefner](https://avatars.githubusercontent.com/u/771968?s=64&v=4)](https://github.com/jonathanhefner)

[\+ 23 contributors](https://github.com/trailofbits/skills/graphs/contributors)

## Languages

- [Python66.8%](https://github.com/trailofbits/skills/search?l=python)
- [Shell23.0%](https://github.com/trailofbits/skills/search?l=shell)
- [YARA2.5%](https://github.com/trailofbits/skills/search?l=yara)
- [CodeQL1.3%](https://github.com/trailofbits/skills/search?l=codeql)
- [C0.9%](https://github.com/trailofbits/skills/search?l=c)
- [Swift0.6%](https://github.com/trailofbits/skills/search?l=swift)
- Other4.9%

You can’t perform that action at this time.