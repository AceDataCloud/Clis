# ACE Music CLI

Create songs from an idea or custom lyrics, write lyrics, and retrieve the original task through Ace Data Cloud.

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/acemusic?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_cli_readme_documentation)

This new package is prepared for release alongside the ACE Music API. Verify package/API publication before use. Source development: `pip install -e ".[dev,test]"`.

Get an application API key at [Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_cli_readme_api_key). Check service access, allowed APIs, expiration and balance, then set the raw key privately:

```bash
export ACEDATACLOUD_API_TOKEN="your-api-key"
# After publication: pip install acemusic-cli
acemusic models
acemusic generate "A warm folk song about returning home"
acemusic generate --lyric-file lyrics.txt --style "warm acoustic folk" --title "Home"
acemusic lyrics "A song about returning home" --style "folk"
acemusic task ORIGINAL_TASK_ID
acemusic wait ORIGINAL_TASK_ID --interval 10 --timeout 600
acemusic download ORIGINAL_TASK_ID --output ./songs
acemusic history --page 1 --page-size 20
```

Generation submits once with async enabled and prints the task ID. Save it immediately. `wait` polls that same task and exits with an error on terminal failure or partial failure while preserving returned audio URLs. A wait timeout can be resumed with the original ID. A submission timeout has unknown outcome; reconcile it before another paid generation. Task lookup is authenticated and free. Lyrics are a separate priced request. Check [current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_cli_readme_pricing) for the applicable package.

Models: `acemusic-v1.1` (default), `acemusic-v1`. A music task targets two MP3 candidates. Upload, covers, continuation, voices, stems, WAV, MIDI and video export are not supported.

`download` accepts final Ace Data Cloud CDN audio URLs and preserves existing files. Tests mock HTTP and do not spend account credit. Run `ruff check .`, `ruff format --check .`, `pytest` and `python -m build`.
