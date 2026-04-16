# Agent Instructions

## General Rules
- This project uses `rbenv` and takes the Ruby version from `.ruby-version`. If you see the wrong Ruby version in your shell, force the correct one with the `RBENV_VERSION` env variable.
- Keep the site as a static Jekyll project. Do not add a runtime backend, CMS, or database-backed content model unless explicitly requested.
- Treat `_data/locales/`, shared includes, layouts, and metadata files as the single source of truth for localized content and SEO-related page metadata.
- Keep strings out of layouts and includes when practical. Prefer locale-backed data over hardcoded copy in templates.
- Build for multilingual support, but implement only the locales explicitly requested.
- Write copy for the musician's task, the tool's behavior, and the musical outcome. Avoid SEO-speak or self-referential page-strategy language like "search intent", "landing page", "visitors", "wording", or "this page exists".
- Keep copy musical and goal-oriented by default. Favor language about key, tempo, feel, tuning, rehearsal, singers, and file handling over browser, page, website, SEO, or content-strategy framing unless the technical detail is genuinely necessary.
- Avoid filler technical phrasing in user-facing copy. Do not lean on lines like "fast local starting point", "local processing", "on your device", or "remote server" unless the technical detail is actually useful to the user.
- Never expose internal route or data structure concepts in user-facing copy.

## Localization Rules
- When translating or reviewing localized copy, preserve domain-specific musical terminology. In Russian, prefer `утилиты для музыкантов` over `музыкальные инструменты` for the product category, translate musical `key` as `тональность` rather than `ключ`, and avoid leaning on `опорные тоны` when a more natural phrase like `эталонный тон` or `устойчивая нота` fits better.
- Always verify the target locale before translating or reviewing. Do not reuse copy from another language just because the alphabet looks similar.
- For Ukrainian specifically, treat Russian and Ukrainian as separate languages with separate review passes. Reject Russian-only letters like `ы`, `э`, `ё`, and `ъ` in Ukrainian copy unless the string is intentionally naming another language, locale, or quoted foreign text.
- When translating tool names into target languages, take localized tool names from the `appName` key in these extension locale files:
  - Pitch Changer: `~/projects/extensions/pitch-changer/_locales/[LOCALE_NAME]/messages.json`
  - Tone Generator: `~/projects/extensions/tone-generator/_locales/[LOCALE_NAME]/messages.json`
  - Speed Changer: `~/projects/extensions/bpm-changer/_locales/[LOCALE_NAME]/messages.json`
- When adding localized FAQ or cross-links for tempo changes, take the BPM Changer extension URL from `~/projects/extensions/musiciantools-online/config/site_settings.yml` under `site.extension_promos.bpm_changer_extension.primary_url`, but keep only the main canonical part of the link and remove tracking query parameters like `?utm_source=...`. Take the localized Speed Changer tool URL from the same file's `site.base_url` plus `~/projects/extensions/musiciantools-online/config/locales/[LOCALE].yml` `routes.speed_changer`, with `/<locale>/` added for non-default locales, and keep those links free of extra query parameters as well.
- Treat those `appName` values as SEO-significant inputs, not display-only suggestions. If the `appName` value includes a local-language name, keep that as the primary localized tool name unless there is a strong product reason not to.
- For non-English locales, localize search-facing canonicals and visible terminology when the locale has stable native musician-facing phrasing. Do not preserve English by default just because the implementation started in English.
- Keep internal ids and non-user-facing keys locale-neutral.
- Translation review should check missing keys, untranslated English strings, grammar, and locale-specific musical terminology conventions.
- Validate rendered localized pages in context, not just raw locale data, because interpolation and layout can still break otherwise-correct translations.

## SEO / Metadata Rules
- Generate localized canonical tags, `hreflang`, sitemap entries, and JSON-LD from the same shared source data where possible. Do not maintain parallel hardcoded sources of truth.
- Emit `hreflang` only for locales that actually exist.
- Keep only preferred canonical URLs in `sitemap.xml`.
- Shared assets, legal redirects, and structured data can stay shared across locales unless the feature explicitly needs locale-specific variants.

## Validation Rules
- Run `bundle exec jekyll build` after user-visible or metadata-affecting changes.
- Spot-check generated files in `_site/` when changing localized metadata, canonicals, `hreflang`, sitemap output, or switcher behavior.
- When changing the locale switcher or redirect logic, verify both `/` and `/ru/` output and make sure the generated HTML still exposes crawlable language links.
- For user-visible visual changes, also run `PYENV_VERSION=3.10.16 python scripts/visual_review.py` after `bundle exec jekyll build` and inspect the generated screenshots in `tmp/ui_reviews/` before finishing.
- When the changed area is narrower than the full page, pass a stable selector such as `--selector '[data-ui-review="hero-topbar"]'` so the screenshot focuses on the affected UI.
- Always run Playwright screenshot review outside the sandbox.
- During screenshot review, verify the visual result itself, not just element presence. Check alignment, spacing, wrapping, clipping, and whether the intended control actually reads correctly in context, following the same visual-review discipline used in `musiciantools-online`.

## Commit Policy
- Default behavior: commit meaningful completed changes with a descriptive message.
- If the user asks for several distinct changes, implement and commit each one separately instead of bundling them together.
- NEVER run `git` commands in parallel.
- After any change is validated, commit it in the same turn unless the user explicitly asks not to commit.
- Do not leave validated work uncommitted unless the user explicitly asks not to commit.
- Keep commit scope coherent so implementation, metadata, and docs that belong together land together.
