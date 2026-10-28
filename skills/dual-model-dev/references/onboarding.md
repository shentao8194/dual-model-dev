# BytePlus international onboarding

1. Visit https://console.byteplus.com/ and register or sign in. Complete any identity or regional eligibility checks yourself.
2. Open ModelArk. Consult https://docs.byteplus.com/en/docs/ModelArk/api-key for current API-key instructions. Create a dedicated key for this local integration in the correct region; never paste it into a chat or issue.
3. For writing and academic work, use a general-purpose ModelArk API entitlement. Default international OpenAI-compatible endpoint: `https://ark.ap-southeast.bytepluses.com/api/v3`.
4. Coding Plan is a separate offering with `https://ark.ap-southeast.bytepluses.com/api/coding/v3`. Its current documentation restricts its use to coding scenarios. This package rejects writing mode on that endpoint. Check https://docs.byteplus.com/en/docs/modelark/coding-plan-personal-plan-overview before subscribing.
5. Enable suitable Kimi and DeepSeek models and copy their actual model IDs or inference endpoint IDs from your console. Availability, pricing, context limits and tools support vary. Domestic Kimi K3.1 Pro / DeepSeek V4.1 Flash IDs are not assumed to exist internationally. If either family is unavailable, stop and contact BytePlus; do not buy a plan on the assumption that this skill provides model access.
6. Run `python scripts/setup.py` in an interactive local terminal. Choose the entitlement, enter the two model IDs, and paste your dedicated key into the hidden prompt. Existing accounts need not register again.
7. Run `python scripts/workflow.py health`, then invoke `$dual-model-dev` with your task. The initial local check is free and offline. Actual model calls incur provider charges.

The account belongs to the user. This project neither sells API access nor collects keys. Key files use user-only permissions (Windows ACL or POSIX modes); they are not encrypted at rest. Do not put the state folder inside a repository or cloud-shared folder. A 401 indicates authentication failure for the selected endpoint; it does not prove that a user copied the wrong kind of key.
