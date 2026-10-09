# Install from this independent repository (authorized users)

This repository alone supports installation, use, tests, and packaging. The other language edition is not a dependency. Both editions use the same skill names; select one language per host scope, or use separate project scopes.

Download `fde-research-en-v2.3.0.zip` from this repository's Releases, verify its adjacent `.sha256` file, and extract the top-level `fde-research/` folder. Alternatively clone this repository or use Code → Download ZIP, then run the installer from the repository root containing `SKILL.md`. GitHub source archives may include a branch suffix; do not use that as the installation folder name.

Ordinary investigation requires an agent with file access. Installation and static checks require Python 3.10+; maintenance tests use 3.12. The installer copies only manifest-listed skill resources, excludes Git/CI/evidence, and refuses to overwrite an existing installation.

## Windows / PowerShell

```powershell
# Claude Code
python -B -X utf8 scripts/release_package.py --install "$env:USERPROFILE/.claude/skills/fde-research"
# Codex: choose this destination instead
python -B -X utf8 scripts/release_package.py --install "$env:USERPROFILE/.agents/skills/fde-research"
```

## macOS / Linux

```sh
# Claude Code
python3 -B scripts/release_package.py --install "$HOME/.claude/skills/fde-research"
# Codex: choose this destination instead
python3 -B scripts/release_package.py --install "$HOME/.agents/skills/fde-research"
```

For a project installation, set the destination to the actual project's `.claude/skills/fde-research` or `.agents/skills/fde-research` path. The installed package does not need a separate source checkout to remain present. Restart the host session and confirm the loaded root `SKILL.md`. In Claude Code try `/fde-research I want AI to improve our department's NGS analysis efficiency; guide the investigation first`. In Codex select the discovered `fde-research` skill or provide its actual entry path. Request "only skill 2, baseline analysis" to use a single stage. Grouped installation does not promise nine independently registered native commands. See [unified entry](unified-entry.md).

For upgrades, back up the old installation outside the host scan scope, compare customizations, and free the intended destination before reinstalling. Never silently merge over it. Keep customer inputs/outputs and runtime environments outside the toolkit. See [runtime guidance](runtime-and-installation.md) for optional Word/browser capabilities.
