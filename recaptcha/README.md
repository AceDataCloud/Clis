# Recaptcha CLI

A command-line tool for reCAPTCHA verification via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install recaptcha-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Recognize reCAPTCHA v2 challenge images
recaptcha recognize /9j/4AAQSkZJRgAB... "/m/0k4j"

# Solve reCAPTCHA v2 and get a token
recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com

# Solve reCAPTCHA v3 and get a token
recaptcha token3 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com login

# Async mode
recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com --async

# Output raw JSON
recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com --json

# Show configuration
recaptcha config
```

## API Endpoints

- `POST /captcha/recognition/recaptcha2` — Recognize reCAPTCHA v2 challenge images
- `POST /captcha/token/recaptcha2` — Solve reCAPTCHA v2 and retrieve a token
- `POST /captcha/token/recaptcha3` — Solve reCAPTCHA v3 and retrieve a token

## License

MIT
