# HappyHorse CLI first-publication receipt

Verified **2026-10-20 Asia/Shanghai** using the existing publisher identity. The shared new-project queue released this owner alone after its prior observed quota time; exactly **one** normal `publish=true` dispatch was made. No 429, retry, new account or permission change occurred.

- Public package: [happyhorse-cli 2026.10.19.4](https://pypi.org/project/happyhorse-cli/2026.10.19.4/).
- Official metadata: [version JSON](https://pypi.org/pypi/happyhorse-cli/2026.10.19.4/json).
- Normal workflow: [run 39320691210](https://github.com/AceDataCloud/HappyHorseCli/actions/runs/39320691210), build and publish successful, source `87d3e63bcde057c8b8492840e35a662c0b1d63c4`.
- Canonical source: Clis `7135f0673e7b58948969dd1aa296d98b17b7c395`, `happyhorse/`; mirror pyproject matches that source.
- Uploads: 2026-10-20 04:36:47/48 Asia/Shanghai. The date-based package version uses UTC, so the `2026.10.19` prefix is expected.

| Artifact | Official SHA-256 |
|---|---|
| happyhorse_cli-2026.10.19.4-py3-none-any.whl | 0d69518abae3a2e5c9492dabff142ffd3c4911d9ff48a15148ef31a7d93c86fa |
| happyhorse_cli-2026.10.19.4.tar.gz | eefab4fd6b3f1410b4f38589ce3005ed7d0eb928f6bcd4cec031b14bf37a2ba8 |

Both downloaded artifacts match those official hashes. The wheel and sdist UTF-8 README match the exact publishing source, including the existing service-specific API-key/current-price CTA with all four UTM fields. The initial version's source-stage installation note is now corrected in this follow-up source PR; immutable release files are not edited or republished.

A fresh Python 3.12 venv without system dependencies used a no-cache mirror-backed install of this exact public version. `uv pip check`, `happyhorse --help`, `happyhorse models` and `happyhorse --version` passed. No API credential was present and no search, generation or paid media request ran.

## Publication-state update

`service-packages.json` may now set `cli_published=true` with the versioned official metadata URL, source/run, both artifact hashes and clean-install receipt. Refresh the bundled ADC copy at the same time. The validator must reject promotion without the receipt; don't retain the temporary unconditional source-only guard after the first successful publication.

Canonical source remains `AceDataCloud/Clis/happyhorse`. Its normal mirror synchronization may publish a new date/run version after this guide update. Use that ordinary chain rather than dispatching the already successful first-publication run or overwriting immutable files. Read any later version separately before replacing this frozen first-release receipt.

## Separate business acceptance

Package publication, local model-reference output and a clean installation do not prove video generation, actual account/model access, terminal media, a unique bill, normal webpage service-term discovery or attributed signup/payment. Those require their own authorized checks. Save a generation's task ID and query the same task, never create another task merely to poll it.
