"""Usage: python shot.py out.png url [wait_s]. Logs in to local Grafana (demo creds) when url is on :13000."""
import sys
from playwright.sync_api import sync_playwright
out, url = sys.argv[1], sys.argv[2]
wait = int(sys.argv[3]) if len(sys.argv) > 3 else 4
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    if ":13000" in url:
        pg.goto("http://localhost:13000/login")
        pg.fill("input[name=user]", "admin"); pg.fill("input[name=password]", "exp5-demo-only")
        pg.keyboard.press("Enter"); pg.wait_for_url("**/", timeout=15000)
    pg.goto(url); pg.wait_for_timeout(wait * 1000)
    pg.screenshot(path=out, full_page=url.startswith("https://github") or "docker.com" in url)
    b.close()
