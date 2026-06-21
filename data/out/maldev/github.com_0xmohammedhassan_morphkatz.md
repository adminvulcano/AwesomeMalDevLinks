# https://github.com/0xMohammedHassan/morphkatz

[Skip to content](https://github.com/0xMohammedHassan/morphkatz#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xMohammedHassan/morphkatz) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xMohammedHassan/morphkatz) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xMohammedHassan/morphkatz) to refresh your session.Dismiss alert

{{ message }}

[0xMohammedHassan](https://github.com/0xMohammedHassan)/ **[morphkatz](https://github.com/0xMohammedHassan/morphkatz)** Public

- [Notifications](https://github.com/login?return_to=%2F0xMohammedHassan%2Fmorphkatz) You must be signed in to change notification settings
- [Fork\\
32](https://github.com/login?return_to=%2F0xMohammedHassan%2Fmorphkatz)
- [Star\\
186](https://github.com/login?return_to=%2F0xMohammedHassan%2Fmorphkatz)


main

[**1** Branch](https://github.com/0xMohammedHassan/morphkatz/branches) [**0** Tags](https://github.com/0xMohammedHassan/morphkatz/tags)

[Go to Branches page](https://github.com/0xMohammedHassan/morphkatz/branches)[Go to Tags page](https://github.com/0xMohammedHassan/morphkatz/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![author](https://github.githubassets.com/images/gravatars/gravatar-user-420.png?size=40)<br>Mohammed Abuhassan<br>[ci: gate every PR with the rules equivalence-proof harness](https://github.com/0xMohammedHassan/morphkatz/commit/d21ed4d9a4fefa808a55deef607efc029ac30e9e)<br>Open commit detailsfailure<br>2 weeks agoJun 6, 2026<br>[d21ed4d](https://github.com/0xMohammedHassan/morphkatz/commit/d21ed4d9a4fefa808a55deef607efc029ac30e9e) · 2 weeks agoJun 6, 2026<br>## History<br>[9 Commits](https://github.com/0xMohammedHassan/morphkatz/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xMohammedHassan/morphkatz/commits/main/) 9 Commits |
| [.github/workflows](https://github.com/0xMohammedHassan/morphkatz/tree/main/.github/workflows "This path skips through empty directories") | [.github/workflows](https://github.com/0xMohammedHassan/morphkatz/tree/main/.github/workflows "This path skips through empty directories") | [ci: gate every PR with the rules equivalence-proof harness](https://github.com/0xMohammedHassan/morphkatz/commit/d21ed4d9a4fefa808a55deef607efc029ac30e9e "ci: gate every PR with the rules equivalence-proof harness  Add a windows-latest job, `rules-equivalence-proof`, that on every pull request:    * configures the ninja-x64-release preset against the project's     vcpkg cache,   * builds only the morphkatz_tests target,   * runs ctest with `-L unit -R \"equivalence proof|YAML rule pack|     duplicate rule ids\"` and `--output-on-failure`.  The job is intentionally minimal (tests-only target, no installer, no samples) so it stays fast and never gates on unrelated build flakes. Wired last so the test labels and rule packs it points at already exist on `main`.") | 2 weeks agoJun 6, 2026 |
| [assets](https://github.com/0xMohammedHassan/morphkatz/tree/main/assets "assets") | [assets](https://github.com/0xMohammedHassan/morphkatz/tree/main/assets "assets") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [docs](https://github.com/0xMohammedHassan/morphkatz/tree/main/docs "docs") | [docs](https://github.com/0xMohammedHassan/morphkatz/tree/main/docs "docs") | [docs(rules): rewrite schema reference to match the loader grammar](https://github.com/0xMohammedHassan/morphkatz/commit/d46656d8f14259d2a9e53c5ee8374199cee00f7f "docs(rules): rewrite schema reference to match the loader grammar  The original schema doc drifted from the implementation. It used key names the loader has never accepted (`op_index`, `reg_class`, `imm_equals`) and omitted constraints rule authors actually need (`flags_value_differs_in`, the raw-pair `from`/`to` form, weight, size_delta).  This rewrite:   * Aligns every example with the real keys the loader parses:     `op`, `class`, `imm`, `register_blacklist`, `same_register`.   * Documents flag handling end-to-end: how `flags_effect` interacts     with the EFLAGS liveness pass, when to use     `equivalent_if_dead`, and the exact bit names accepted by     `flags_value_differs_in`.   * Documents the targeted raw-byte pack form (`raw: { from, to }`)     used by Sliver / Havoc / Meterpreter / UPX style packs.   * Adds a \"Not yet supported\" subsection enumerating grammar     extensions the loader does not yet implement (per-operand     imm_min/imm_max, size_bits override on copy_from) so authors     don't try them and silently get a no-op rule.  No code change.") | 2 weeks agoJun 6, 2026 |
| [fuzz](https://github.com/0xMohammedHassan/morphkatz/tree/main/fuzz "fuzz") | [fuzz](https://github.com/0xMohammedHassan/morphkatz/tree/main/fuzz "fuzz") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [include/morphkatz](https://github.com/0xMohammedHassan/morphkatz/tree/main/include/morphkatz "This path skips through empty directories") | [include/morphkatz](https://github.com/0xMohammedHassan/morphkatz/tree/main/include/morphkatz "This path skips through empty directories") | [refactor(verify): extract emulate\_block into a reusable public API](https://github.com/0xMohammedHassan/morphkatz/commit/83f56381073f652fba04a0fbe9d9d5cd1e032b55 "refactor(verify): extract emulate_block into a reusable public API  The Unicorn-backed block emulator was previously locked inside an anonymous namespace in unicorn_verify.cpp, only reachable through the patch-pair walker. The rule-pack expansion work needs to drive the same emulator with hand-rolled byte buffers and arbitrary initial states, so move the implementation into a dedicated header/source pair and expose:    morphkatz::verify::BlockEmuState        // GPRs + RFLAGS in/out   morphkatz::verify::BlockEmuResult       // ok + out state + error   morphkatz::verify::default_block_emu_state()   morphkatz::verify::emulate_block(code, va, in, timeout_ms)  `unicorn_verify` now consumes the same public API instead of holding a private copy. No behavioural change: the per-block sandbox layout (stack page, code page, GPR seeding, RFLAGS seeding, timeout) is preserved byte-for-byte, and unicorn_verify still uses default_block_emu_state() as its single seed.  Wiring: * CMakeLists.txt adds src/verify/block_emu.cpp to morphkatz_core.   * Same change ships a long-standing ASan/Catch2 mismatch fix:     vcpkg's Catch2 is built without container annotations, so     /fsanitize=address objects refused to link. Setting     _DISABLE_STRING_ANNOTATION + _DISABLE_VECTOR_ANNOTATION on the     ASan path keeps both vs2022-x64-asan and clang-cl-asan green.") | 2 weeks agoJun 6, 2026 |
| [packaging](https://github.com/0xMohammedHassan/morphkatz/tree/main/packaging "packaging") | [packaging](https://github.com/0xMohammedHassan/morphkatz/tree/main/packaging "packaging") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [rules](https://github.com/0xMohammedHassan/morphkatz/tree/main/rules "rules") | [rules](https://github.com/0xMohammedHassan/morphkatz/tree/main/rules "rules") | [rules(x64): add targeted byte packs (Sliver, Havoc, Meterpreter, UPX)](https://github.com/0xMohammedHassan/morphkatz/commit/f061a7d84666f0712d4b00348cb5cd4c4df9c568 "rules(x64): add targeted byte packs (Sliver, Havoc, Meterpreter, UPX)  Four new raw-byte rule packs that target signature atoms from high-profile public offensive tooling. Each pack is sourced from public upstream repos and is limited to short fixed byte windows that ship inside the stager / loader code paths, so the patches are safe to apply with the existing raw-pair matcher:  sliver.yaml              - Sliver implant stager byte pairs havoc.yaml               - Havoc demon byte pairs meterpreter_stager.yaml  - Metasploit reverse_tcp stager byte pairs upx_stub.yaml            - UPX packer-stub byte pairs (Defender's                            generic-packer atom)  The integration test table in targeted_byte_pairs_test.cpp grows one entry per pack, asserting each one loads, queues into the applied-patch list, and round-trips through Patcher::apply -> Patcher::rollback with identical post-rollback bytes.  These packs strictly add coverage; no existing rule, encoder, or matcher path is touched.") | 2 weeks agoJun 6, 2026 |
| [scripts](https://github.com/0xMohammedHassan/morphkatz/tree/main/scripts "scripts") | [scripts](https://github.com/0xMohammedHassan/morphkatz/tree/main/scripts "scripts") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [src](https://github.com/0xMohammedHassan/morphkatz/tree/main/src "src") | [src](https://github.com/0xMohammedHassan/morphkatz/tree/main/src "src") | [refactor(verify): extract emulate\_block into a reusable public API](https://github.com/0xMohammedHassan/morphkatz/commit/83f56381073f652fba04a0fbe9d9d5cd1e032b55 "refactor(verify): extract emulate_block into a reusable public API  The Unicorn-backed block emulator was previously locked inside an anonymous namespace in unicorn_verify.cpp, only reachable through the patch-pair walker. The rule-pack expansion work needs to drive the same emulator with hand-rolled byte buffers and arbitrary initial states, so move the implementation into a dedicated header/source pair and expose:    morphkatz::verify::BlockEmuState        // GPRs + RFLAGS in/out   morphkatz::verify::BlockEmuResult       // ok + out state + error   morphkatz::verify::default_block_emu_state()   morphkatz::verify::emulate_block(code, va, in, timeout_ms)  `unicorn_verify` now consumes the same public API instead of holding a private copy. No behavioural change: the per-block sandbox layout (stack page, code page, GPR seeding, RFLAGS seeding, timeout) is preserved byte-for-byte, and unicorn_verify still uses default_block_emu_state() as its single seed.  Wiring: * CMakeLists.txt adds src/verify/block_emu.cpp to morphkatz_core.   * Same change ships a long-standing ASan/Catch2 mismatch fix:     vcpkg's Catch2 is built without container annotations, so     /fsanitize=address objects refused to link. Setting     _DISABLE_STRING_ANNOTATION + _DISABLE_VECTOR_ANNOTATION on the     ASan path keeps both vs2022-x64-asan and clang-cl-asan green.") | 2 weeks agoJun 6, 2026 |
| [tests](https://github.com/0xMohammedHassan/morphkatz/tree/main/tests "tests") | [tests](https://github.com/0xMohammedHassan/morphkatz/tree/main/tests "tests") | [rules(x64): add targeted byte packs (Sliver, Havoc, Meterpreter, UPX)](https://github.com/0xMohammedHassan/morphkatz/commit/f061a7d84666f0712d4b00348cb5cd4c4df9c568 "rules(x64): add targeted byte packs (Sliver, Havoc, Meterpreter, UPX)  Four new raw-byte rule packs that target signature atoms from high-profile public offensive tooling. Each pack is sourced from public upstream repos and is limited to short fixed byte windows that ship inside the stager / loader code paths, so the patches are safe to apply with the existing raw-pair matcher:  sliver.yaml              - Sliver implant stager byte pairs havoc.yaml               - Havoc demon byte pairs meterpreter_stager.yaml  - Metasploit reverse_tcp stager byte pairs upx_stub.yaml            - UPX packer-stub byte pairs (Defender's                            generic-packer atom)  The integration test table in targeted_byte_pairs_test.cpp grows one entry per pack, asserting each one loads, queues into the applied-patch list, and round-trips through Patcher::apply -> Patcher::rollback with identical post-rollback bytes.  These packs strictly add coverage; no existing rule, encoder, or matcher path is touched.") | 2 weeks agoJun 6, 2026 |
| [.editorconfig](https://github.com/0xMohammedHassan/morphkatz/blob/main/.editorconfig ".editorconfig") | [.editorconfig](https://github.com/0xMohammedHassan/morphkatz/blob/main/.editorconfig ".editorconfig") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [.gitignore](https://github.com/0xMohammedHassan/morphkatz/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/0xMohammedHassan/morphkatz/blob/main/.gitignore ".gitignore") | [chore: anchor VS build-dir ignores so rule packs ship with the repo](https://github.com/0xMohammedHassan/morphkatz/commit/12eda12154a4e081e809d557fa95453d3c09d875 "chore: anchor VS build-dir ignores so rule packs ship with the repo  Gitignore patterns without a leading slash match at any depth, so the existing `x64/` line (intended for VS per-config output) was also silently matching `rules/x64/`. The result was that every YAML rule pack and the bundled YARA rule were tracked nowhere - the engine was shipping a v1.0 binary with no rules to load.  Anchor `/x64/`, `/x86/`, `/Debug/`, `/Release/` to repo root only. Nested build output is still covered by the existing `build/`, `out/`, `bin/`, `lib/`, `.vs/`, and `vcpkg_installed/` rules.  Also commit the previously-shadowed runtime assets:   - rules/x64/encoding/{alt_mov_89_8b,alt_nop_pool}.yaml   - rules/x64/equivalence/{add_sub_neg,mov_forms,push_pop_pairs,zero_register}.yaml   - rules/x64/targeted/{adaptix,cobaltstrike,donut,mimikatz}.yaml   - rules/yara/x64/mimikatz.yar") | 2 weeks agoJun 6, 2026 |
| [CMakeLists.txt](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeLists.txt "CMakeLists.txt") | [CMakeLists.txt](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeLists.txt "CMakeLists.txt") | [refactor(verify): extract emulate\_block into a reusable public API](https://github.com/0xMohammedHassan/morphkatz/commit/83f56381073f652fba04a0fbe9d9d5cd1e032b55 "refactor(verify): extract emulate_block into a reusable public API  The Unicorn-backed block emulator was previously locked inside an anonymous namespace in unicorn_verify.cpp, only reachable through the patch-pair walker. The rule-pack expansion work needs to drive the same emulator with hand-rolled byte buffers and arbitrary initial states, so move the implementation into a dedicated header/source pair and expose:    morphkatz::verify::BlockEmuState        // GPRs + RFLAGS in/out   morphkatz::verify::BlockEmuResult       // ok + out state + error   morphkatz::verify::default_block_emu_state()   morphkatz::verify::emulate_block(code, va, in, timeout_ms)  `unicorn_verify` now consumes the same public API instead of holding a private copy. No behavioural change: the per-block sandbox layout (stack page, code page, GPR seeding, RFLAGS seeding, timeout) is preserved byte-for-byte, and unicorn_verify still uses default_block_emu_state() as its single seed.  Wiring: * CMakeLists.txt adds src/verify/block_emu.cpp to morphkatz_core.   * Same change ships a long-standing ASan/Catch2 mismatch fix:     vcpkg's Catch2 is built without container annotations, so     /fsanitize=address objects refused to link. Setting     _DISABLE_STRING_ANNOTATION + _DISABLE_VECTOR_ANNOTATION on the     ASan path keeps both vs2022-x64-asan and clang-cl-asan green.") | 2 weeks agoJun 6, 2026 |
| [CMakePresets.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakePresets.json "CMakePresets.json") | [CMakePresets.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakePresets.json "CMakePresets.json") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [CMakeSettings.json.example](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeSettings.json.example "CMakeSettings.json.example") | [CMakeSettings.json.example](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeSettings.json.example "CMakeSettings.json.example") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [CMakeUserPresets.json.example](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeUserPresets.json.example "CMakeUserPresets.json.example") | [CMakeUserPresets.json.example](https://github.com/0xMohammedHassan/morphkatz/blob/main/CMakeUserPresets.json.example "CMakeUserPresets.json.example") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [CONTRIBUTING.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [CONTRIBUTING.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [LICENSE](https://github.com/0xMohammedHassan/morphkatz/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/0xMohammedHassan/morphkatz/blob/main/LICENSE "LICENSE") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [NOTICE](https://github.com/0xMohammedHassan/morphkatz/blob/main/NOTICE "NOTICE") | [NOTICE](https://github.com/0xMohammedHassan/morphkatz/blob/main/NOTICE "NOTICE") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [Open-in-VS.cmd](https://github.com/0xMohammedHassan/morphkatz/blob/main/Open-in-VS.cmd "Open-in-VS.cmd") | [Open-in-VS.cmd](https://github.com/0xMohammedHassan/morphkatz/blob/main/Open-in-VS.cmd "Open-in-VS.cmd") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [README.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/README.md "README.md") | [README.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/README.md "README.md") | [Update link to Beatrice.py repository](https://github.com/0xMohammedHassan/morphkatz/commit/df91c558f3881757843328f22b76b1c22b4c3ff9 "Update link to Beatrice.py repository") | last monthMay 9, 2026 |
| [RESPONSIBLE\_USE.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/RESPONSIBLE_USE.md "RESPONSIBLE_USE.md") | [RESPONSIBLE\_USE.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/RESPONSIBLE_USE.md "RESPONSIBLE_USE.md") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [SECURITY.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/SECURITY.md "SECURITY.md") | [SECURITY.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/SECURITY.md "SECURITY.md") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [TELEMETRY.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/TELEMETRY.md "TELEMETRY.md") | [TELEMETRY.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/TELEMETRY.md "TELEMETRY.md") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [TRADEMARK.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/TRADEMARK.md "TRADEMARK.md") | [TRADEMARK.md](https://github.com/0xMohammedHassan/morphkatz/blob/main/TRADEMARK.md "TRADEMARK.md") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [vcpkg-configuration.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/vcpkg-configuration.json "vcpkg-configuration.json") | [vcpkg-configuration.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/vcpkg-configuration.json "vcpkg-configuration.json") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| [vcpkg.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/vcpkg.json "vcpkg.json") | [vcpkg.json](https://github.com/0xMohammedHassan/morphkatz/blob/main/vcpkg.json "vcpkg.json") | [MorphKatz v1.0 - polymorphic PE rewriter for Windows x64](https://github.com/0xMohammedHassan/morphkatz/commit/2e0bcc8950ad60622151e3589aad34bf63b3ba46 "MorphKatz v1.0 - polymorphic PE rewriter for Windows x64") | last monthMay 4, 2026 |
| View all files |

## Repository files navigation

[![MorphKatz logo — three cat heads, one body](https://github.com/0xMohammedHassan/morphkatz/raw/main/assets/morphkatz-logo.png)](https://github.com/0xMohammedHassan/morphkatz/blob/main/assets/morphkatz-logo.png)

# MorphKatz

[Permalink: MorphKatz](https://github.com/0xMohammedHassan/morphkatz#morphkatz)

**Windows x64 polymorphic machine-code rewriter.**

_N faces, one body._ One static `morphkatz.exe` that rewrites
PE binaries into semantically identical but byte-different variants.

[Who it's for](https://github.com/0xMohammedHassan/morphkatz#who-its-for) ·
[Quick start](https://github.com/0xMohammedHassan/morphkatz#quick-start) ·
[Architecture](https://github.com/0xMohammedHassan/morphkatz#architecture--benchmarks) ·
[Rule schema](https://github.com/0xMohammedHassan/morphkatz#writing-your-own-rewrite-rules) ·
[Responsible use](https://github.com/0xMohammedHassan/morphkatz#responsible-use) ·
[Licensing](https://github.com/0xMohammedHassan/morphkatz#licensing)

[Contributing](https://github.com/0xMohammedHassan/morphkatz/blob/main/CONTRIBUTING.md) ·
[Security](https://github.com/0xMohammedHassan/morphkatz/blob/main/SECURITY.md) ·
[Zero telemetry](https://github.com/0xMohammedHassan/morphkatz/blob/main/TELEMETRY.md) ·
[Trademark](https://github.com/0xMohammedHassan/morphkatz/blob/main/TRADEMARK.md)

* * *

MorphKatz rewrites x86-64 machine code inside PE executables and raw shellcode
into **semantically identical but byte-different** equivalents. Same arithmetic,
same observable EFLAGS effects, same control-flow — different bytes. That
breaks byte-pattern detection (YARA rules, Defender signatures, Elastic rules,
Sigma detection content) without changing what the code actually does.

## Live Demo

[Permalink: Live Demo](https://github.com/0xMohammedHassan/morphkatz#live-demo)

[![MorphKatz live demo — scan detected, morph, scan clean, run works](https://github.com/0xMohammedHassan/morphkatz/raw/main/assets/MorphKatz_Test.gif)](https://github.com/0xMohammedHassan/morphkatz/blob/main/assets/MorphKatz_Test.gif)[![MorphKatz live demo — scan detected, morph, scan clean, run works](https://github.com/0xMohammedHassan/morphkatz/raw/main/assets/MorphKatz_Test.gif)](https://github.com/0xMohammedHassan/morphkatz/blob/main/assets/MorphKatz_Test.gif)[Open MorphKatz live demo — scan detected, morph, scan clean, run works in new window](https://github.com/0xMohammedHassan/morphkatz/blob/main/assets/MorphKatz_Test.gif)

> Scan → **detected** (`HackTool:Win32/AmDisable!MTB`) → morph with `--data-morph on` → scan again → **clean** → run → bypass still works at runtime.

## Who it's for

[Permalink: Who it's for](https://github.com/0xMohammedHassan/morphkatz#who-its-for)

MorphKatz is built for **two complementary audiences**, and we treat both as
first-class:

### 🛡️ Detection engineers / Blue team

[Permalink: 🛡️ Detection engineers / Blue team](https://github.com/0xMohammedHassan/morphkatz#%EF%B8%8F-detection-engineers--blue-team)

If your job is to write YARA rules, Defender custom indicators, Elastic
detection content, or Sigma rules, MorphKatz tells you **how durable each rule**
**actually is**. Pipe one of your malware samples through MorphKatz with
`--variants 50` and `--target your-yara/*.yar` and you get back, per rule, the
percentage of variants on which it still triggers. Rules that fall off a
cliff under polymorphic mutation are the ones an evolving threat actor will
silence first; you want to harden those before the actor does.

Specific Blue-team workflows:

- **Detection-engineering coverage testing** — quantify "what % of my rules
are one equivalent-swap away from silence?".
- **Signature triage** — see exactly which bytes in a PE drove a Defender
detection (`morphkatz scan --bisect`), and use that to harden or generalise
the rule.
- **Polymorphic-robust classifier training** — generate diverse but
semantically identical training data for ML malware classifiers.
- **Binary-similarity research** — generate evaluation corpora with known
ground truth (every variant shares the same source semantics).

### 🗡️ Red team / Authorised offensive research

[Permalink: 🗡️ Red team / Authorised offensive research](https://github.com/0xMohammedHassan/morphkatz#%EF%B8%8F-red-team--authorised-offensive-research)

If you're testing detection coverage from the offensive side under a clear
rules-of-engagement paper trail, MorphKatz turns "manually rewrite five
gadgets and recompile" into a rules-of-engagement-friendly automation:

- **Rules-of-engagement-friendly evasion** — every mutation is rule-cited from
the Intel SDM, every run is reproducible from `--seed`, every change lands
in a JSON / HTML diff report you can drop into the engagement deliverable.
- **Reproducibility for your write-up** — same seed, same input, byte-for-byte
identical output, on any machine.
- **Author-audited rules only** — MorphKatz refuses to ship pop-malware-of-
the-month rule packs. Every rule has a cited semantic-equivalence proof in
its YAML.

What MorphKatz is **not**:

- ❌ A live-malware obfuscator. We deliberately do not target the
pop-malware-of-the-month list — see [`RESPONSIBLE_USE.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/RESPONSIBLE_USE.md).
- ❌ A behavioural / ML-evasion tool. MorphKatz mutates _bytes_ with
preserved semantics; ML detections (anything ending in `!ml`) evaluate
global behaviour and won't budge — that class of evasion is out of
scope.
- ❌ A black box. Every rule's equivalence proof, every diff report's
metric, every byte changed is yours to audit.

## Features

[Permalink: Features](https://github.com/0xMohammedHassan/morphkatz#features)

- **CFG-aware disassembly** — Zydis-powered recursive descent with
jump-table recovery; data-in-code regions are never accidentally
decoded.
- **In-process encoding** — Zydis encoder generates patched
instructions in the same address space, zero IPC overhead.
- **YAML rule packs** — every rewrite rule lives under `rules/x64/`,
reviewable and hot-swappable. Add your own without recompiling.
- **Typed intermediate representation** — `ir::Instruction` carries
full Zydis operand metadata through the entire rewrite pipeline.
- **EFLAGS liveness** — full effect model (AF/CF/OF/PF/SF/ZF) with
per-basic-block dataflow so rewrites never corrupt flag state.
- **Seeded polymorphism** — `xoshiro256**` RNG; `--seed N` gives
byte-for-byte reproducible output on any machine.
- **Intel SDM NOP padding** — 1..9-byte multi-byte NOP rotation drawn
from the Intel Optimization Reference Manual.
- **Semantic verification** — re-disassembly check by default;
optional Unicorn basic-block emulation (`--verify unicorn`).
- **YARA-aware targeting** — `--target rules.yar` prioritises rewrites
that break specified signature atoms.
- **Defender feedback loop** — `--target-defender` runs MpCmdRun,
bisects anchors, and feeds them into the priority queue automatically.
- **Data-section morphing** — `--data-morph on` XOR-encodes
signature-bearing byte sequences in `.rdata` / `.data` and decodes
them at runtime via a polymorphic stub with an anti-emulation gate.
- **JSON + HTML reports** — per-offset before/after diffs, rule IDs,
and detection-coverage metrics.
- **PE hygiene** — `CheckSumMappedFile`, Authenticode strip,
reproducible timestamp, Rich-header `preserve|strip|randomize`.
- **Single static binary** — one `morphkatz.exe`, no runtime
dependencies.

## Quick start

[Permalink: Quick start](https://github.com/0xMohammedHassan/morphkatz#quick-start)

### Prerequisites

[Permalink: Prerequisites](https://github.com/0xMohammedHassan/morphkatz#prerequisites)

- **Windows 10+** / Windows Server 2019+, x64.
- **Visual Studio 2022 17.8+** with "Desktop development with C++" and the
MSVC v143 toolset.
- **CMake 3.27+** (bundled with recent VS installers).
- **[vcpkg](https://github.com/microsoft/vcpkg)**:



```
git clone https://github.com/microsoft/vcpkg
.\vcpkg\bootstrap-vcpkg.bat
[Environment]::SetEnvironmentVariable('VCPKG_ROOT', (Resolve-Path .\vcpkg), 'User')
```


### Build — classic Visual Studio `.sln` (one-click)

[Permalink: Build — classic Visual Studio .sln (one-click)](https://github.com/0xMohammedHassan/morphkatz#build--classic-visual-studio-sln-one-click)

MorphKatz does **not** commit `.sln` / `.vcxproj` files — they are generated
from `CMakeLists.txt` on demand so target wiring, include dirs, and vcpkg
linkage stay authoritative in one place. For the classic "double-click the
.sln" experience:

```
.\Open-in-VS.cmd                            # default: preset vs2022-x64
.\Open-in-VS.cmd -Preset vs2022-x64-asan    # ASan build
.\Open-in-VS.cmd -Fresh                     # nuke CMake cache first
.\Open-in-VS.cmd -NoOpen                    # configure only; for CI / scripting
```

`Open-in-VS.cmd` (a thin wrapper over `scripts\open-in-vs.ps1`) checks
`VCPKG_ROOT`, runs the CMake VS generator, and launches the generated
`build\<preset>\MorphKatz.sln` in the matching Visual Studio install
(located via `vswhere`). Once open, set `morphkatz` as the startup project
and hit F5.

Equivalent manual flow:

```
cmake --preset vs2022-x64
start build\vs2022-x64\MorphKatz.sln
```

### Build — VS 2022 "Open Folder" / CMake mode

[Permalink: Build — VS 2022 "Open Folder" / CMake mode](https://github.com/0xMohammedHassan/morphkatz#build--vs-2022-open-folder--cmake-mode)

```
# In Visual Studio: File > Open > Folder... -> (this repo)
# Select the vs2022-x64 configuration, hit F5.
# `.vs\launch.vs.json` is pre-wired with --version / --help / dry-run targets.
```

### Build — CLI only (Ninja)

[Permalink: Build — CLI only (Ninja)](https://github.com/0xMohammedHassan/morphkatz#build--cli-only-ninja)

```
cmake --preset ninja-x64-release
cmake --build --preset ninja-x64-release
ctest --preset ninja-x64-release --output-on-failure

.\build\ninja-x64-release\morphkatz.exe --version
```

### Presets

[Permalink: Presets](https://github.com/0xMohammedHassan/morphkatz#presets)

| Preset | Purpose |
| --- | --- |
| `vs2022-x64` | Emits `MorphKatz.sln` \+ `.vcxproj`. Default developer workflow. |
| `vs2022-x64-asan` | Same, with MSVC `/fsanitize=address`. |
| `ninja-x64-release` | CLI Release build. CI-fast. |
| `ninja-x64-debug` | CLI Debug build. |
| `clang-cl-asan` | `clang-cl` with ASan + UBSan. CI fuzzing. |

## Usage

[Permalink: Usage](https://github.com/0xMohammedHassan/morphkatz#usage)

### First-run / bare-invocation

[Permalink: First-run / bare-invocation](https://github.com/0xMohammedHassan/morphkatz#first-run--bare-invocation)

Double-clicking `morphkatz.exe` or running it with no arguments prints
a compact banner and the top five examples — no silent crash, no empty
help dump:

```
           /\_/\      /\_/\      /\_/\
          ( o.o )    ( -.- )    ( ^.^ )
           > ^ <      > ^ <      > ^ <
              \_________|_________/
                        |
                     [  PE  ]

               M o r p h K a t z

   N faces, one body - polymorphic PE rewriter (Windows x64)
               Coded by Mohammed Abuhassan

Usage:  morphkatz <input> [options]
        morphkatz compare <a> <b> [more...] [--report out.json]
        morphkatz scan    <input> [--bisect] [--report out.html]

Quick start:
  morphkatz payload.exe --seed 42 --report report.html
  morphkatz payload.exe --seed 1 --variants 8 --report batch.json
  morphkatz target.exe  --target yara/*.yar -vv
  morphkatz target.exe  --target-defender target.exe --report run.html
  morphkatz compare v0.exe v1.exe --report cmp.html
  morphkatz scan suspect.exe --bisect --report scan.json

Run 'morphkatz --help'         for all options.
Run 'morphkatz compare --help' for the comparison subcommand.
Run 'morphkatz scan --help'    for Defender scanning options.
Run 'morphkatz --version'      for build info.
```

### Full option surface

[Permalink: Full option surface](https://github.com/0xMohammedHassan/morphkatz#full-option-surface)

```
morphkatz <input.exe|input.bin> [options]

Input/output:
  -o, --output <path>            Default: <input>.patched.<ext>    (foo.exe -> foo.patched.exe)
      --backup                   Write <input>.bak (default on)
      --in-place                 Overwrite input (requires --no-backup)

Modes:
      --profile {safe,normal,aggressive}    Default: normal
      --target <rules.yar>                  Prioritise rewrites that break these YARA rules
      --rules <dir|file>                    Load custom YAML rule packs

Polymorphism:
      --seed <u64>               Reproducible run
      --mutation-budget <N>      Max rewrites per basic block
      --variants <N>             Emit N deterministic morphs (1..1000);
                                 outputs go to <output>_v<i>.<ext> plus a
                                 rolled-up <report>.summary.json

Verification:
      --verify {none,redisasm,unicorn}       Default: redisasm
      --verify-timeout-ms <N>    Default: 5000

PE options:
      --fix-checksum             Default on
      --strip-signature          Default off, warn if present
      --reproducible-timestamp <unix>           Default: keep original
      --rich-header {preserve,strip,randomize}  Default: preserve

Reporting:
      --report <path.json|path.html>
      --dry-run                  No file write; report-only
      --stats                    Print aggregate counts
  -v, --verbose                  Repeatable (-v, -vv, -vvv)
      --log-file <path>

Detection feedback:
      --target-defender <reference.exe>
                                 Run the deployed Microsoft Defender
                                 against <reference.exe> (Tier-1, via
                                 MpCmdRun.exe), peel every byte
                                 anchor with multi-anchor bisection,
                                 and feed them into the rule matcher
                                 priority alongside --target. Adds a
                                 `defender:` block to the report.
                                 See docs/scan.md.
      --auto-yara,--no-auto-yara
                                 When --target-defender flags a
                                 known family (e.g. Mimikatz), auto-
                                 load the bundled YARA hint pack at
                                 rules/yara/x64/<family>.yar so the
                                 rule matcher can boost candidates
                                 that touch family-specific bytes.
                                 Default: on. Ignored when --target
                                 is set explicitly. See
                                 rules/yara/README.md.

Data-section morphing:
      --data-morph {off|plan|on}
                                 Mutate signature-bearing byte
                                 sequences in .rdata / .data by
                                 XOR-encoding them on disk and
                                 decoding them at runtime via an
                                 appended .morph section. Default
                                 off; 'plan' is a read-only dry
                                 run that lists the atoms in the
                                 report. See docs/data-morph.md.
                                 --target-defender auto-escalates
                                 to 'on' when bisect anchors land
                                 in .rdata or .data and --data-morph
                                 wasn't pinned by the user.
      --decoder-placement {auto|ep-thunk|tls-callback}
                                 Where the runtime decoder lives.
                                 'auto' (default) prefers TLS
                                 callbacks when feasible, falls back
                                 to an entry-point thunk otherwise.
      --data-morph-min-len <bytes>      Default 4
      --data-morph-max-len <bytes>      Default 4096
                                 Length filter on candidate atoms.

Subcommands:
  morphkatz compare <a> <b> [c...] [--report out.json|out.html]
      Pairwise diff of 2+ binaries: aligned Hamming %, byte-histogram
      cosine, alphabet Jaccard, SHA-256, entropy. Useful for checking
      that --variants actually produced diverse outputs.

  morphkatz scan <input> [--bisect] [--bisect-mode {single|all}] \
                         [--bisect-scope {sections|sections-all|code|data|raw}] \
                         [--report out.json|out.html]
      Run Microsoft Defender (Tier-1, MpCmdRun-backed) against a
      single file. With --bisect, isolate the offending byte
      window(s); --bisect-mode all peels every anchor via
      multi-anchor bisection so signatures like Mimikatz!pz that
      span multiple regions are fully enumerated. --bisect-scope
      controls the PE-aware mask: 'sections' (default) keeps the
      buffer parseable on every iteration by masking only inside
      section payloads minus data-directory windows. See docs/scan.md.
```

### Batch + compare example

[Permalink: Batch + compare example](https://github.com/0xMohammedHassan/morphkatz#batch--compare-example)

```
# Emit 8 deterministic morphs and roll up a summary.
morphkatz.exe payload.exe --seed 1 --variants 8 --report batch.json

# Inspect pairwise diversity.
morphkatz.exe compare payload_v0.exe payload_v1.exe payload_v2.exe
```

## Writing your own rewrite rules

[Permalink: Writing your own rewrite rules](https://github.com/0xMohammedHassan/morphkatz#writing-your-own-rewrite-rules)

Rules are YAML under `rules/`. See [`docs/rule-schema.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/docs/rule-schema.md)
for the full schema. Minimal example:

```
version: 1
rules:
  - id: x64.zero.xor_to_sub
    match:
      mnemonic: XOR
      operand_count: 2
      constraints:
        - { op: 0, kind: register, class: gpr }
        - { op: 1, kind: register, class: gpr }
        - { same_register: [0, 1] }
        - { register_blacklist: [RSP] }
    rewrite:
      mnemonic: SUB
      operands:
        - { copy_from: 0 }
        - { copy_from: 1 }
    flags_effect: equivalent
    size_delta: 0
    weight: 1.0
```

Drop your rule into `rules/x64/equivalence/` or pass `--rules path/to/my.yaml`.

## Architecture & benchmarks

[Permalink: Architecture & benchmarks](https://github.com/0xMohammedHassan/morphkatz#architecture--benchmarks)

- [`docs/architecture.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/docs/architecture.md) — module map, end-to-end flow,
design rationale.
- [`docs/benchmarks.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/docs/benchmarks.md) — measurement plan; real
numbers land when the MalwareBazaar-backed harness in
[`docs/evasion_bench.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/docs/evasion_bench.md) runs end-to-end.
- [`docs/roadmap.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/docs/roadmap.md) — what's coming in v1.1
(Auto-Discover) and v1.2.

## Private research

[Permalink: Private research](https://github.com/0xMohammedHassan/morphkatz#private-research)

MorphKatz's data-section morphing and anti-emulation gate are backed by
original reverse-engineering research into Microsoft Defender's
`mpengine.dll` emulator internals and heuristic scoring model. This
research — covering emulator instruction budgets, heuristic trigger
conditions, and evasion-gate design — is maintained privately and is
**not included in this repository**.

If you are a security researcher interested in the technical details,
reach out via GitHub Issues or Discussions. We selectively share the
full research notes with verified security professionals, detection
engineers, and academic researchers on a case-by-case basis.

## Responsible use

[Permalink: Responsible use](https://github.com/0xMohammedHassan/morphkatz#responsible-use)

MorphKatz is a defensive-security research tool for red-team engagements,
malware analysis training, and AV/EDR product evaluation. Use only on
binaries you own or are authorised to test. Read
[`RESPONSIBLE_USE.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/RESPONSIBLE_USE.md) before shipping MorphKatz output at
anyone.

## Licensing

[Permalink: Licensing](https://github.com/0xMohammedHassan/morphkatz#licensing)

MorphKatz is licensed under the [GNU Affero General Public License v3.0\\
or later](https://github.com/0xMohammedHassan/morphkatz/blob/main/LICENSE). Use it freely in research, open-source projects,
internal tooling, or on your own laptop. If you expose MorphKatz
behaviour as a network service, AGPL-3.0 §13 requires you to publish
your modifications.

Project-wide policy documents:

- [`CONTRIBUTING.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/CONTRIBUTING.md) — DCO sign-off; CI enforces it
on every PR.
- [`TELEMETRY.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/TELEMETRY.md) — zero telemetry, documented and
enforced.
- [`TRADEMARK.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/TRADEMARK.md) — name and logo policy.
- [`SECURITY.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/SECURITY.md) — coordinated disclosure, supported
versions.
- [`NOTICE`](https://github.com/0xMohammedHassan/morphkatz/blob/main/NOTICE) — third-party component licences (Zydis, LIEF,
Unicorn, libyara, etc.).

## Contributing

[Permalink: Contributing](https://github.com/0xMohammedHassan/morphkatz#contributing)

Pull requests welcome — read [`CONTRIBUTING.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/CONTRIBUTING.md) first.
In short: DCO sign-off on every commit (`git commit -s`), tests for new
rules, no `using namespace` in headers, `/W4 /permissive-` warnings are
errors.

## Security

[Permalink: Security](https://github.com/0xMohammedHassan/morphkatz#security)

For security vulnerabilities, use GitHub Security Advisories. **Do not**
file a public issue. See [`SECURITY.md`](https://github.com/0xMohammedHassan/morphkatz/blob/main/SECURITY.md) for the
coordinated-disclosure timeline.

## Third-party libraries

[Permalink: Third-party libraries](https://github.com/0xMohammedHassan/morphkatz#third-party-libraries)

MorphKatz stands on the shoulders of:

- **[Zydis](https://github.com/zyantific/zydis)** — disassembler +
encoder fast enough to run on every instruction of a 10 MB binary.
- **[LIEF](https://github.com/lief-project/LIEF)** — PE parser that
doesn't pretend the Windows loader is simple.
- **[libyara](https://github.com/VirusTotal/yara)** — rule engine whose
AST is introspectable at compile time.
- **[Unicorn Engine](https://github.com/unicorn-engine/unicorn)** — the
semantic-verification backend.
- **[vcpkg](https://github.com/microsoft/vcpkg)** — dependency
management on Windows.

See [`NOTICE`](https://github.com/0xMohammedHassan/morphkatz/blob/main/NOTICE) for the formal attribution manifest and full
third-party licence list.

* * *

This codebase grew out of an earlier Python research prototype
( [Beatrice.py](https://github.com/raskolnikov90/Beatrice.py)). MorphKatz
is an independent C++20 reimplementation — different disassembler,
different encoder, different IR, external YAML rule packs, and many
engines (CFG recovery, EFLAGS liveness, Unicorn verify, YARA targeting,
data-section morphing, Defender feedback loop) that have no Python
counterpart. The targeted byte-pattern packs under
`rules/x64/targeted/` were ported from the prototype with the original
author's permission under MorphKatz's AGPL-3.0 licence.

## About

Polymorphic PE rewriter for Windows x64 , rewrites binaries into semantically identical but byte-different variants


### Resources

[Readme](https://github.com/0xMohammedHassan/morphkatz#readme-ov-file)

### License

[AGPL-3.0 license](https://github.com/0xMohammedHassan/morphkatz#AGPL-3.0-1-ov-file)

### Contributing

[Contributing](https://github.com/0xMohammedHassan/morphkatz#contributing-ov-file)

### Security policy

[Security policy](https://github.com/0xMohammedHassan/morphkatz#security-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xMohammedHassan/morphkatz).

[Activity](https://github.com/0xMohammedHassan/morphkatz/activity)

### Stars

[**186**\\
stars](https://github.com/0xMohammedHassan/morphkatz/stargazers)

### Watchers

[**2**\\
watching](https://github.com/0xMohammedHassan/morphkatz/watchers)

### Forks

[**32**\\
forks](https://github.com/0xMohammedHassan/morphkatz/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xMohammedHassan%2Fmorphkatz&report=0xMohammedHassan+%28user%29)

## [Releases](https://github.com/0xMohammedHassan/morphkatz/releases)

No releases published

## [Packages\  0](https://github.com/users/0xMohammedHassan/packages?repo_name=morphkatz)

No packages published

## [Contributors\  1](https://github.com/0xMohammedHassan/morphkatz/graphs/contributors)

- [![@0xMohammedHassan](https://avatars.githubusercontent.com/u/38003193?s=64&v=4)](https://github.com/0xMohammedHassan)[**0xMohammedHassan** Mo.TX](https://github.com/0xMohammedHassan)

## Languages

- [C++89.5%](https://github.com/0xMohammedHassan/morphkatz/search?l=c%2B%2B)
- [PowerShell6.2%](https://github.com/0xMohammedHassan/morphkatz/search?l=powershell)
- [CMake1.8%](https://github.com/0xMohammedHassan/morphkatz/search?l=cmake)
- [Python1.6%](https://github.com/0xMohammedHassan/morphkatz/search?l=python)
- Other0.9%

You can’t perform that action at this time.