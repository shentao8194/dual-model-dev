# Dual Model Dev

Codex plans. Kimi drafts. DeepSeek checks and implements.

A local Agent Skill for writing, academic drafting and software maintenance using your own BytePlus international ModelArk account. English instructions; output in the user's requested language. No hosted proxy, bundled API key or telemetry.

## Install

```sh
npx skills add shentao8194/dual-model-dev --skill dual-model-dev
```

Alternatively copy `skills/dual-model-dev` into your agent's skills directory. Python 3.10+ and local shell/file access are required. This is a desktop/local-execution skill, not a browser-only GPT Action.

## First use

Invoke `$dual-model-dev`. The skill guides you to BytePlus registration and ModelArk access, then asks you to run `python scripts/setup.py` from the installed skill directory. The local wizard explains endpoints, prompts for account-supported Kimi/DeepSeek IDs and captures your API key without echoing it. No key goes into chat or this repository. Existing accounts can skip registration.

Writing uses the general-purpose API. Coding Plan is optional for coding only. Do not assume China's Agent Plan entitlements or model IDs apply internationally. Review [onboarding](skills/dual-model-dev/references/onboarding.md) before purchasing.

## Workflow

| Task | Plan | Draft / implement | Review | Acceptance |
| --- | --- | --- | --- | --- |
| Writing / papers | Codex | Kimi | DeepSeek edits | Editorial verdict |
| Development | Codex | DeepSeek | Independent DeepSeek session | Tests and Kimi |

The host retains its model. External work is performed by the configured API models. Natural prose guidance removes empty boilerplate and irrelevant disclaimers while retaining real uncertainty and source integrity. No fabricated citations or AI-detection guarantees.

## Privacy and execution

Project content needed for tasks is sent directly to the configured official BytePlus endpoint. Keys and run history live outside the package in `~/.dual-model-dev`. Commands are provided by the host, never invented/executed by an external model. Tests can execute project code; the runner is not a security sandbox. Failed runs preserve edits and backups. See [PRIVACY.md](PRIVACY.md).

## Validation

```sh
python -m unittest discover -s tests -v
```

Tests use mocked model responses and temporary projects. The domestic prototype passed a live coding smoke test; the international distribution has not been live-tested against a BytePlus international account. Exact models must be verified in your account.

## Support

Use this repository's Issues page. Never attach API keys, credential files or raw private run folders. This is an independent community project, not an official BytePlus, OpenAI, Kimi or DeepSeek product.
