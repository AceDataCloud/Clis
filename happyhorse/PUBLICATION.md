# HappyHorse CLI publication handoff

Checked 2026-10-19. This is an execution checklist, not a package-release receipt.

The existing source is `AceDataCloud/Clis/happyhorse`; the live service already
has an independently distributed `mcp-happyhorse`. Do not duplicate its API
client into a new codebase or mark this source-only CLI as published.

## Gate and next executable sequence

The existing PyPI publisher identity works. The coordinating release queue
reports the new-project allowance resumes on **2026-10-20**. This is a
publisher-quota wait, not a request to register a new account or grant access.

1. Re-read the current Clis main and existing HappyHorse repository/PR inventory.
   If no mirror has been created, create `AceDataCloud/HappyHorseCli` under the
   existing bot identity; do not create an empty mirror before its source and
   workflow are ready. Use the same single-source/mirror convention as SunoCli.
2. Submit one scoped Clis PR adding the `happyhorse` mapping to `sync.yaml` and
   the root mirror inventory. Keep the package directory unchanged except for
   verified release metadata. Retain source-only status until the first PyPI
   receipt exists; do not prematurely set `cli_published=true` in the catalog.
3. Configure the mirror's standard build/test/date-version publish workflow,
   excluding `.github` from source synchronization as in the existing mirrors.
   Reuse the existing organization publisher access. If an actual authentication
   error occurs, report its exact job/error and selected-repository secret
   requirement; do not ask for a new PyPI registration or put tokens in chat.
4. After the coordinating shared merge and mirror synchronization, run the
   ordinary package checks and first publish when the project allowance permits.
   Use a unique date version, not the source scaffold's `0.1.0` as a current
   registry assertion. Do not create a placeholder PyPI project for reservation.
5. Read the official PyPI JSON and compare owner/source URLs, package README,
   permissions/pricing CTA and wheel SHA-256. Install in a new isolated
   environment and run only `happyhorse --help` and `happyhorse models` first.
   These steps do not require a key or send a generation request.
6. Only after those receipts, update `service-packages.json`, its bundled ADC
   copy and documentation together. Include the exact package/repository/version
   receipt in that follow-up PR, removing the temporary source-only guard.

## Separate business acceptance

A successful publish or local model table does not prove video generation,
account access, terminal media, a unique bill or attributed signup/payment.
Those require their own authorized checks. Preserve the returned task ID and
query that same task rather than starting a second generation to poll it.
