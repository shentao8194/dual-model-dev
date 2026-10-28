---
name: dual-model-dev
description: Plan and outline in Codex, delegate drafting to Kimi, and use DeepSeek for proofreading and implementation through BytePlus international APIs. Use when the user requests this external writing, academic writing, or coding workflow.
---

# Dual Model Dev

## First run: account and local credentials

Resolve this skill's installed directory; all scripts below are relative to it. Use an available Python 3.10+ interpreter. Never assume a developer's absolute path.

Run `python scripts/workflow.py health`. If unconfigured, guide the user through [international onboarding](references/onboarding.md) before executing a task:
1. Open the official BytePlus console and explain registration and ModelArk access. The user completes account verification, agreements, purchases, and API key creation themselves.
2. Confirm the appropriate general-purpose or coding entitlement and the exact model IDs shown in their account. Do not promise domestic Agent Plan prices, an international Agent Plan, or specific model availability.
3. Have the user run `python scripts/setup.py` in their own interactive terminal. It opens official links on request and uses hidden local key input. Never ask for the key in chat, read its file, or pass it through command arguments.
4. Resume only after health reports configured. This checks local configuration, not provider authorization. Tell the user that task materials will be sent to BytePlus and incur their API charges. A real task is the connection test; do not silently make additional paid probes.

Existing users can skip account setup when already configured.

## Roles

- Codex: clarify the brief, collect supplied evidence, create a concrete outline or implementation plan, define acceptance criteria, and organize delivery.
- Writing and papers: Kimi writes complete Markdown/text from the Codex outline. A separate DeepSeek session checks logic, grammar, terminology, consistency, supported citations and natural prose, then edits the deliverable.
- Development: DeepSeek implements the Codex plan; the runner executes authorized test commands; a separate DeepSeek session reviews; Kimi performs final acceptance.
- Do not replace a failed external model with the host model or silently switch model IDs.

Preserve the user's requested language. This skill's instructions are English; generated work need not be.

## Evidence and prose

Write with concrete nouns and verbs, natural sentence variety, and an appropriate voice. Remove empty introductions, inflated claims, repetitive conclusions, formulaic transitions, irrelevant disclaimers, and defensive preambles. Do not replace useful work with excessive clarification or generic caution. Keep material uncertainty and genuine research limitations concise and specific.

For papers, define the research question, argument, sections, evidence and citation style. Never invent studies, citations, experiments, methods, data or results. The runner has no web search. If research is required, the host retrieves authoritative sources using available tools and passes attributable material to the task. Proofreading is not independent external fact verification. Do not promise to evade AI detection or misrepresent authorship.

## Run

Create a unique UTF-8 JSON request file using file tools, not shell interpolation:

```json
{
  "mode": "writing",
  "project_dir": "/absolute/path/to/output-folder",
  "task": "The user's complete brief, source material, language and constraints",
  "plan": "The host-authored outline and concrete acceptance criteria",
  "test_commands": [],
  "max_repairs": 1
}
```

Create a dedicated output folder if writing has no specified location. For development, use the authorized project directory and project-appropriate test argv arrays. Do not pass deployment, dependency installation, deletion or push commands. Tests execute project code: this is not an OS sandbox.

```sh
python scripts/workflow.py start /absolute/path/to/request.json
python scripts/workflow.py status JOB_ID
python scripts/workflow.py cancel JOB_ID
```

Store the returned job ID. Poll about every 20-30 seconds and report meaningful phase changes. Continue to completion; cancel only when asked. Do not load all source and logs back into the host context. A missing model or entitlement is a configuration issue, not permission to substitute a model.

Only `completed` means the configured workflow passed. Development without passing tests cannot complete. Writing uses editorial checks, not code tests. Report `failed` or `needs_attention` accurately, with the artifact directory. Failed runs retain edits and backups; do not blindly roll back over subsequent user edits.

Link the final document or code report and summarize token usage. For Word/PDF, use an available document skill to format the reviewed text without independently rewriting it. Email tasks create drafts, not sent messages.

## Limits

The CLI requires only Python's standard library. Optional MCP serving requires `mcp` and is not needed for this skill. The runner reads and writes bounded UTF-8 files within the project, excluding common private/generated paths. It cannot edit binary files, delete files, install dependencies or deploy. Limits default to 48 model calls, 4096 output tokens per call, 30 minutes and one development repair. Token thresholds stop future requests; they are not strict monetary caps. API/command timeouts and cancellation apply at call boundaries.

Local settings, credentials and run records live under `~/.dual-model-dev` (or `DUAL_MODEL_HOME`), outside the installed skill. Never include that directory in a public package or commit.
