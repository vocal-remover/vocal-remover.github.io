#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import re
import socket
import threading
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover - operator-facing setup error
    raise SystemExit(
        "Playwright for Python is not available. Run this script with "
        "`PYENV_VERSION=3.10.16 python scripts/visual_review.py ...`."
    ) from exc


class QuietStaticHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture local Playwright screenshots from the built _site output."
    )
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        help="Path to capture from the local review server. Repeat for multiple pages.",
    )
    parser.add_argument(
        "--selector",
        help="Optional CSS selector to crop the screenshot to a specific region.",
    )
    parser.add_argument(
        "--wait-for-selector",
        help="Optional CSS selector to wait for before capturing.",
    )
    parser.add_argument(
        "--label",
        help="Optional filename label. When used with multiple paths, the path slug is appended.",
    )
    parser.add_argument(
        "--out-dir",
        default="tmp/ui_reviews",
        help="Directory where screenshots should be written.",
    )
    parser.add_argument(
        "--site-dir",
        default="_site",
        help="Directory to serve locally. Defaults to the Jekyll build output.",
    )
    parser.add_argument(
        "--viewport",
        default="1440x1200",
        help="Viewport as WIDTHxHEIGHT. Defaults to 1440x1200.",
    )
    parser.add_argument(
        "--delay-ms",
        type=int,
        default=1200,
        help="Extra delay after page load before capturing.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Navigation and selector timeout in milliseconds.",
    )
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="Capture the full page instead of just the viewport.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface for the temporary local server.",
    )
    return parser.parse_args()


def parse_viewport(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", value)
    if not match:
        raise SystemExit(f"Invalid --viewport value: {value!r}. Use WIDTHxHEIGHT.")
    return int(match.group(1)), int(match.group(2))


def normalize_path(path: str) -> str:
    if not path:
        return "/"
    return path if path.startswith("/") else f"/{path}"


def slugify_path(path: str) -> str:
    normalized = normalize_path(path).strip("/")
    if not normalized:
        return "home"
    return re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()


def build_filename(label: str | None, path: str, multi_path: bool) -> str:
    path_slug = slugify_path(path)
    if not label:
        return f"{path_slug}.png"
    if multi_path:
        return f"{label}-{path_slug}.png"
    return f"{label}.png"


def reserve_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


@contextlib.contextmanager
def static_server(directory: Path, host: str) -> int:
    port = reserve_port(host)
    handler = functools.partial(QuietStaticHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer((host, port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield port
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main() -> int:
    args = parse_args()
    paths = args.paths or ["/", "/ru/"]
    viewport_width, viewport_height = parse_viewport(args.viewport)

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.exists():
        raise SystemExit(
            f"Site directory {site_dir} does not exist. Run `bundle exec jekyll build` first."
        )

    session_dir = Path(args.out_dir).resolve() / time.strftime("%Y%m%d-%H%M%S")
    session_dir.mkdir(parents=True, exist_ok=True)

    with static_server(site_dir, args.host) as port:
        base_url = f"http://{args.host}:{port}"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                color_scheme="light",
                device_scale_factor=1,
            )

            try:
                for path in paths:
                    page = context.new_page()
                    try:
                        url = f"{base_url}{normalize_path(path)}"
                        page.goto(url, wait_until="load", timeout=args.timeout_ms)
                        wait_selector = args.wait_for_selector or args.selector
                        if wait_selector:
                            page.wait_for_selector(wait_selector, timeout=args.timeout_ms)
                        page.wait_for_timeout(args.delay_ms)

                        output_path = session_dir / build_filename(
                            args.label,
                            path,
                            multi_path=len(paths) > 1,
                        )

                        if args.selector:
                            page.locator(args.selector).first.screenshot(path=str(output_path))
                        else:
                            page.screenshot(path=str(output_path), full_page=args.full_page)

                        print(output_path)
                    finally:
                        page.close()
            finally:
                context.close()
                browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
