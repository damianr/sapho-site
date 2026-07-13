#!/usr/bin/env python3
"""Generate install.html (the HTML mirror served at /install) from install.md.

Run after every edit to install.md: python3 scripts/gen_install_html.py
The HTML mirror exists because AI browsing tools read text/html most reliably;
install.md stays canonical.
"""
import html
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
spec = (root / "install.md").read_text()

page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>sapho — installation spec (for AI agents)</title>
<meta name="description" content="Capability-detecting setup instructions for installing or connecting sapho, the plain-files product source of truth.">
<link rel="alternate" type="text/plain" href="/install.md">
<style>
  body {{ margin: 0; background: #08080b; color: rgba(255,255,255,.75);
    font-family: ui-monospace, "SF Mono", Menlo, monospace; }}
  main {{ max-width: 54rem; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
  pre {{ white-space: pre-wrap; overflow-wrap: anywhere; font-size: .85rem; line-height: 1.7;
    font-family: inherit; margin: 0; }}
  p.top {{ font-size: .72rem; color: rgba(255,255,255,.4); }}
  p.top a {{ color: rgb(168,155,232); }}
</style></head><body><main>
<p class="top">This page is the HTML mirror of <a href="/install.md">/install.md</a> (canonical raw text). Same content; read either.</p>
<pre>
{html.escape(spec)}
</pre>
</main></body></html>
"""
(root / "install.html").write_text(page)
print(f"wrote install.html ({len(page)} bytes) from install.md")
