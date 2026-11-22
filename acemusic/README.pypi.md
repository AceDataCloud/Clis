# ACE Music CLI

Create songs from an idea or custom lyrics, write lyrics, and retrieve the original task through Ace Data Cloud.

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/acemusic?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen)

This new package is prepared for release alongside the ACE Music API. Verify package/API publication before use. Source development: `pip install -e ".[dev,test]"`.

Get an application API key at [Applications](https://platform.acedata.cloud/console/applications?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen). Check service access, allowed APIs, expiration and balance, then set the raw key privately:

```bash
export ACEDATACLOUD_API_TOKEN="your-api-key"
# After publication: pip install acemusic-cli
acemusic models
acemusic generate "A warm folk song about returning home"
acemusic generate --lyric-file lyrics.txt --style "warm acoustic folk" --title "Home"
acemusic lyrics "A song about returning home" --style "folk"
acemusic upload https://example.com/owned-audio.mp3 --name "My reference" --audio-id OWNED_ANCHOR_AUDIO_ID
acemusic cover OWNED_AUDIO_ID --lyric-file lyrics.txt --style "warm acoustic folk"
acemusic mashup OWNED_AUDIO_A OWNED_AUDIO_B --lyric-file lyrics.txt --style "warm acoustic folk" --audio-influence 60
acemusic task ORIGINAL_TASK_ID
acemusic wait ORIGINAL_TASK_ID --interval 10 --timeout 600
acemusic download ORIGINAL_TASK_ID --output ./songs
acemusic history --page 1 --page-size 20
```

Generation submits once with async enabled and prints the task ID. Save it immediately. `wait` polls that same task and exits with an error on terminal failure or partial failure while preserving returned audio URLs. A wait timeout can be resumed with the original ID. A submission timeout has unknown outcome; reconcile it before another paid generation. Task lookup is authenticated and free. Lyrics are a separate priced request. Check [current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen) for the applicable package.

Models: `acemusic-v1.1` (default), `acemusic-v1`. Generation, cover and mashup target two MP3 candidates. Upload is a separate priced operation importing one track; it never creates a cover implicitly. Cover and mashup require `acemusic-v1.1` (selected automatically), lyrics/style and caller-owned compatible platform audio IDs returned by successful tasks, not task IDs. Mashup takes exactly two distinct references. `--audio-influence` is 1–100 (default 60); title is optional for reference actions. An upload may use `--audio-id` to anchor it to an existing owned source for later reference use. Wait for the upload to succeed before using its returned audio ID. The service validates source ownership and compatibility; do not change references or upload again automatically on rejection. Final failed/partial generation groups and failed imports are free under current service rules. Continuation, voices, stems, WAV, MIDI and video export remain unsupported.

`download` accepts final Ace Data Cloud CDN audio URLs and preserves existing files. Tests mock HTTP and do not spend account credit. Run `ruff check .`, `ruff format --check .`, `pytest` and `python -m build`.
