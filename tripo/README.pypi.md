# Tripo CLI by Ace Data Cloud

Generate 3D models from text or reference views, import or convert models, and check, rig or retarget an animation.

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. Copy the key shown in **API KEY**, check that the application has Tripo access, and set `ACEDATACLOUD_API_TOKEN` to the copied value.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

```bash
tripo generate --json '{"prompt":"A wooden chair","texture":"none"}' --idempotency-key chair-example-01
tripo tasks <task-id>
tripo models convert --json '{"model_id":"<model-id>","format":"FBX"}'
tripo animations rig_check --json '{"model_id":"<model-id>"}'
tripo tasks --batch <first-task-id> <second-task-id>
```

Submission defaults to asynchronous mode. Poll the returned ID until `response.success` is set. Download the file at `response.data[0].model_url`. For rig checks read `riggable` instead. Use `--trace` to look up trace IDs. JSON input accepts the operation options from the API contract, including image URLs, texture quality, conversion settings and animation presets. Paid operations use the application's Ace Credits. Import, rig check and task lookup are free.
