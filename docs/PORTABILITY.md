# Portability — leaving GitHub costs one afternoon, not a rewrite

GitHub is the **showroom**, not the vault. Everything here can move to Codeberg, GitLab, a self-hosted Forgejo or a plain disk without losing work.

## The five rules

| # | Rule | How this repo follows it |
|---|---|---|
| 1 | **Git is the source of truth** | All content is Markdown, Mermaid, SVG, YAML or code — plain files any host renders |
| 2 | **Checks live in scripts, not in CI files** | `scripts/check.sh` runs every gate on a laptop or any CI; `.github/workflows/ci.yml` is a 3-line wrapper |
| 3 | **Only free, open-source tools** | gitleaks (MIT), lychee (MIT/Apache), age (BSD). No paid GitHub features, no licence keys |
| 4 | **GitHub-only data is exported weekly** | `scripts/backup-github.sh` saves issues, PRs, reviews, releases, assets, discussions, labels, wikis as JSON + git bundles |
| 5 | **A second live copy exists** | `.github/workflows/mirror.yml` push-mirrors public repos to Codeberg or GitLab.com (free) once two secrets are added |

## What is GitHub-specific here, and its exit

| GitHub feature used | Portable equivalent | Effort to move |
|---|---|---|
| Actions workflows | `scripts/check.sh` runs as-is in GitLab CI, Forgejo Actions (same YAML syntax), Woodpecker or cron | Minutes |
| Issue forms / PR template | Plain Markdown templates; Forgejo reads `.forgejo/` or `.gitea/` copies | Minutes |
| Releases + attestations | Tags stay in git; assets are in the backup; SBOM files are plain SPDX JSON | Minutes |
| Discussions | Exported to JSON weekly | Read-only archive |
| Profile README / org `.github` | A static page (GitHub Pages output is plain HTML — host on Codeberg Pages or any static host) | An hour |
| Social preview, pins, contribution graph | Cosmetic; rebuilt from the same SVG assets | — |

## The weekly routine (runs on your own machine, no GitHub dependency)

```text
Sunday 03:00 IST  scripts/backup-github.sh  →  ~/github-backups/<stamp>.tar.gz(.age)
                  →  copy to encrypted Drive (your existing off-site copy)
                  →  keep 8 weekly + 6 monthly; verify SHA256SUMS on the newest
Quarterly         restore drill: git clone <repo>.bundle  — confirm it opens without GitHub
```

## One-time owner setup (free)

1. **Read-only backup token:** fine-grained token, all repos, permissions *Contents, Issues, Pull requests, Discussions, Metadata: read-only*. Stored only in the OS keychain or a secret store — never in a file.
2. **Mirror host:** a Codeberg or GitLab.com account → create empty repos with the same names → access token with write to those repos → add `MIRROR_URL` and `MIRROR_TOKEN` as repo secrets on the public showcase repos only.
3. **Encryption key (optional):** `age-keygen -o ~/.config/age/key.txt` → put the public `age1…` key in `AGE_RECIPIENT`. Keep the private key offline (password manager or printed).
4. **GitHub's own export (twice a year):** Settings → Account → *Export account data* — a second, independent copy produced by GitHub itself.

## What never leaves the private engine

Mirrors and backups copy what already exists. Private repos are backed up to **your** encrypted storage only and are never mirrored to a third-party host. The private-engine boundary (engine code, agent configurations and prompts, internal tooling, client and clinical modules) applies to every copy.
