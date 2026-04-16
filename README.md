# Vocal Remover
Lightning-fast [Vocal Remover](https://removevocalsfromasong.com/) helps musicians, teachers, singers, podcasters, and creators separate vocals from music in seconds.

This repo contains the Jekyll source for the product website hosted on GitHub Pages: https://removevocalsfromasong.com/.

## Local development
1. Use the Ruby version from [.ruby-version](/Users/navi/projects/extensions/vocal-remover.github.io/.ruby-version).
2. Install gems with `bundle install`.
3. Start the site with `bundle exec jekyll serve`.
4. Open the local URL printed by Jekyll and test `/`, `/blog/set-high-performance-gpu-for-chrome-edge-on-windows/`, and `/llms.txt`.

## Localization
- English lives at `/`.
- Locale copy is stored in `_data/locales/`.
- Shared layouts and includes render the site as static HTML and are ready for additional locale data files and locale-prefixed routes later.

## Deployment
- GitHub Pages should build this site with Jekyll `4.4.1` on Ruby `4.0.2`.
