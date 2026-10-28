# Privacy

This local software has no analytics, advertising or hosted backend. It stores configuration, API credentials, requests, edited-file backups, reports and model usage on the user's computer under `~/.dual-model-dev` or `DUAL_MODEL_HOME`.

To perform a requested task it sends prompts and selected project files to the official BytePlus ModelArk API endpoint configured by the user, with the user's API key in the Authorization header. BytePlus's own terms and privacy policy govern that processing. Account registration takes place on BytePlus, not through this project. Optional setup browser links open only official BytePlus pages.

The user controls local retention. Remove local run directories or revoke the provider key when no longer needed. Credential files use restricted OS permissions but are not encrypted. Do not submit secrets or private run artifacts in GitHub issues. Maintainers only receive information users choose to post in public issues.
