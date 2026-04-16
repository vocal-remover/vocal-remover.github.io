# Vocal Remover
Lightning-fast [Vocal Remover](https://removevocalsfromasong.com/) helps musicians, teachers, singers, podcasters, and creators separate vocals from music in seconds.

This repo contains the Jekyll source for the product website hosted on GitHub Pages: https://removevocalsfromasong.com/.

## Local development
1. Use the Ruby version from [.ruby-version](/Users/navi/projects/extensions/vocal-remover.github.io/.ruby-version).
2. Install gems with `bundle install`.
3. Start the site with `bundle exec jekyll serve`.
4. Open the local URL printed by Jekyll and test `/`, `/blog/set-high-performance-gpu-for-chrome-edge-on-windows/`, and `/llms.txt`.
5. For screenshot reviews, build with `bundle exec jekyll build` and run `PYENV_VERSION=3.10.16 python scripts/visual_review.py`.

## Localization
- English lives at `/`.
- Locale copy is stored in `_data/locales/`.
- Shared layouts and includes render the site as static HTML and are ready for additional locale data files and locale-prefixed routes later.

## Deployment
- GitHub Pages is deployed through the workflow in [.github/workflows/pages.yml](/Users/navi/projects/extensions/vocal-remover.github.io/.github/workflows/pages.yml).
- The workflow builds the site with Jekyll `4.4.1` on Ruby `4.0.2` and uploads the generated `_site` artifact to Pages.
