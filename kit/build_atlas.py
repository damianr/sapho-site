#!/usr/bin/env python3
"""Deterministic sapho atlas builder.

Renders every products/*.md into a self-contained dashboard at dist/atlas/index.html.
Mechanical checks only (empty fields, thin sections, stale files) — editorial judgment
gaps come from running /atlas in a Claude session. Stdlib only; runs in CI on every push.
"""
import html
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "products"
OUT = ROOT / "dist" / "atlas" / "index.html"

FIELDS = ["one_liner", "audience", "status", "tracker", "links", "tags"]
SECTIONS = ["Problem & insight", "How it works", "Key decisions & rationale", "Positioning"]
THIN_WORDS = 40
STALE_DAYS = 45


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT).stdout.strip()


def parse(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    fm_raw, body = (m.group(1), m.group(2)) if m else ("", text)
    fm = {}
    current = None
    for line in fm_raw.splitlines():
        if re.match(r"^\s+\S", line) and current:  # nested block (links:)
            fm[current] = (fm[current] + "\n" + line.strip()).strip()
            continue
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if km:
            current = km.group(1)
            fm[current] = km.group(2).split("#")[0].strip()
    sections = {}
    for name in SECTIONS:
        sm = re.search(r"^## " + re.escape(name) + r"\n(.*?)(?=^## |\Z)", body, re.S | re.M)
        sections[name] = sm.group(1).strip() if sm else ""
    return fm, sections


def md(text):
    """Tiny markdown-to-HTML: escapes first, then bold/italic/code/links, bullets, paragraphs."""
    out, para, in_list = [], [], False

    def inline(s):
        s = html.escape(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            flush()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + inline(stripped[2:]) + "</li>")
        elif not stripped:
            flush()
            if in_list:
                out.append("</ul>")
                in_list = False
        else:
            if in_list and re.match(r"^\s{2,}", line):  # continuation of a bullet
                out[-1] = out[-1][:-5] + " " + inline(stripped) + "</li>"
            else:
                para.append(stripped)
    flush()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def field_state(fm, key):
    v = fm.get(key, "")
    if key == "links":
        return "ok" if v else "miss"
    if not v or v.upper().startswith("TODO") or v.lower() in ("none", "none yet", "null"):
        return "miss"
    return "ok"


def gaps_for(slug, fm, sections, age_days):
    gaps = []
    if field_state(fm, "tracker") == "miss":
        gaps.append(("tracker: is empty — operational state has no linked home.",
                     f"In my sapho corpus, fill the tracker: field of products/{slug}.md with its tracker project URL."))
    if field_state(fm, "links") == "miss":
        gaps.append(("links: is empty — no repo, domain, or deployed URL recorded.",
                     f"In my sapho corpus, add repo/domain/production links to products/{slug}.md frontmatter."))
    for name, body in sections.items():
        if len(body.split()) < THIN_WORDS:
            gaps.append((f'"{name}" is thin ({len(body.split())} words).',
                         f"Interview me to flesh out the '{name}' section of products/{slug}.md, then reconcile."))
    if age_days > STALE_DAYS:
        gaps.append((f"File untouched for {age_days} days — worth a re-read for drift.",
                     f"Read products/{slug}.md and interview me about what changed; reconcile any durable updates."))
    return gaps


def main():
    files = sorted(PRODUCTS.glob("*.md"))
    if not files:
        sys.exit("no product files found")
    commit = sh("git", "rev-parse", "--short", "HEAD") or "uncommitted"
    today = datetime.now(timezone.utc)
    projects = []
    for f in files:
        fm, sections = parse(f)
        slug = f.stem
        ts = sh("git", "log", "-1", "--format=%ct", "--", str(f))
        age = (today - datetime.fromtimestamp(int(ts), tz=timezone.utc)).days if ts else 0
        last = sh("git", "log", "-1", "--format=%ad (%h) %s", "--date=short", "--", str(f))
        projects.append({
            "slug": slug, "fm": fm, "sections": sections, "age": age, "last": last,
            "gaps": gaps_for(slug, fm, sections, age),
        })

    statuses = [p["fm"].get("status", "?") for p in projects]
    tracker_ok = sum(1 for p in projects if field_state(p["fm"], "tracker") == "ok")
    status_summary = " · ".join(
        f"{statuses.count(s)} {s}" for s in dict.fromkeys(statuses))

    cards, details = [], []
    for p in projects:
        fm, slug = p["fm"], p["slug"]
        name = fm.get("name", slug)
        gapn = len(p["gaps"])
        gapcls = "" if gapn else " ok"
        gaplabel = f"{gapn} gap{'s' if gapn != 1 else ''}" if gapn else "clean"
        tags = " · ".join(t.strip() for t in fm.get("tags", "").strip("[]").split(",") if t.strip())
        cards.append(f"""
      <button class="card" data-open="{slug}">
        <div class="card-top"><h2>{html.escape(name)}</h2><span class="chip">{html.escape(fm.get('status','?'))}</span></div>
        <p class="one">{html.escape(fm.get('one_liner',''))}</p>
        <div class="card-meta"><span class="tags">{html.escape(tags)}</span><span class="gapcount{gapcls}">{gaplabel}</span></div>
      </button>""")

        chips = "".join(
            f'<span class="f {field_state(fm, k)}">{k}{": missing" if field_state(fm, k) == "miss" else ""}</span>'
            for k in FIELDS)
        secs = "".join(
            f'<div class="sec"><h4>{html.escape(n.lower())}</h4>{md(b)}</div>'
            for n, b in p["sections"].items())
        gap_items = "".join(
            f'<div class="gap"><div class="g-txt"><span class="g-kind">mechanical</span>{html.escape(txt)}</div>'
            f'<button class="copy" data-copy="{html.escape(prompt, quote=True)}">copy prompt</button></div>'
            for txt, prompt in p["gaps"])
        gaps_block = (f'<div class="gaps"><h3>gaps · {gapn}</h3>{gap_items}</div>' if gapn
                      else '<div class="gaps clean"><h3>no mechanical gaps</h3></div>')
        details.append(f"""
  <article class="detail" id="detail-{slug}" hidden>
    <button class="back" data-back>← all projects</button>
    <div class="d-head"><h2>{html.escape(name)}</h2><span class="chip">{html.escape(fm.get('status','?'))}</span></div>
    <p class="d-one">{html.escape(fm.get('one_liner',''))}</p>
    <p class="d-meta">last touched: {html.escape(p['last'] or 'uncommitted')}</p>
    <div class="fm">{chips}</div>
    {secs}
    {gaps_block}
  </article>""")

    page = TEMPLATE.format(
        n=len(projects), status_summary=status_summary, tracker_ok=tracker_ok,
        date=today.strftime("%Y-%m-%d %H:%M UTC"), commit=commit,
        cards="".join(cards), details="".join(details))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    print(f"built {OUT.relative_to(ROOT)}: {len(projects)} projects, "
          f"{sum(len(p['gaps']) for p in projects)} mechanical gaps")


TEMPLATE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>sapho atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:dark;--bg:#08080b;--card:rgba(255,255,255,.03);--elev:rgba(255,255,255,.06);
--line:rgba(255,255,255,.08);--line2:rgba(255,255,255,.12);--t1:rgba(255,255,255,.9);
--t2:rgba(255,255,255,.6);--t3:rgba(255,255,255,.35);--purple:rgb(168,155,232);
--teal:rgb(80,195,158);--coral:rgb(232,142,110);--amber:rgb(242,192,108);
--font:"DM Mono",ui-monospace,"SF Mono",Menlo,monospace}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--t2);font-family:var(--font);font-size:.9rem;
line-height:1.7;-webkit-font-smoothing:antialiased;padding:0 1.5rem 4rem}}
::selection{{background:rgba(168,155,232,.3)}}
.wrap{{max-width:62rem;margin:0 auto}} a{{color:var(--purple)}} code{{color:var(--purple)}}
header{{display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:.5rem;padding:1.75rem 0 2.25rem}}
.wordmark{{font-size:1.15rem;font-weight:500;color:var(--t1)}}
.wordmark .stop{{color:var(--purple)}} .wordmark .app{{color:var(--t3);font-weight:400}}
.stamp{{font-size:.7rem;color:var(--t3);letter-spacing:.05em}} .stamp b{{color:var(--t2);font-weight:400}}
.strip{{display:flex;gap:2.2rem;flex-wrap:wrap;border:1px solid var(--line);background:var(--card);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.25rem}}
.stat .v{{color:var(--t1);font-size:1.05rem}} .stat .k{{color:var(--t3);font-size:.68rem;letter-spacing:.08em}}
.stat .v .warn{{color:var(--coral)}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem;margin-bottom:1.25rem}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
.card{{text-align:left;font-family:var(--font);color:var(--t2);background:var(--card);
border:1px solid var(--line);border-radius:12px;padding:1.3rem 1.5rem;cursor:pointer;
transition:border-color .15s,background .15s}}
.card:hover{{border-color:var(--purple);background:var(--elev)}}
.card:focus-visible,.back:focus-visible,.copy:focus-visible{{outline:2px solid var(--purple);outline-offset:2px}}
.card-top,.d-head{{display:flex;justify-content:space-between;align-items:baseline;gap:1rem}}
.card h2{{font-size:1rem;font-weight:500;color:var(--t1);margin:0 0 .35rem}}
.card .one{{font-size:.78rem;margin:0 0 .9rem;line-height:1.65}}
.chip{{font-size:.65rem;letter-spacing:.06em;border-radius:999px;padding:.15rem .6rem;
white-space:nowrap;color:var(--amber);border:1px solid rgba(242,192,108,.35)}}
.card-meta{{display:flex;justify-content:space-between;gap:1rem;font-size:.68rem;color:var(--t3)}}
.gapcount{{color:var(--coral)}} .gapcount.ok{{color:var(--teal)}} .tags{{color:var(--t3)}}
.detail[hidden],#overview[hidden]{{display:none}}
.back{{background:none;border:1px solid var(--line2);color:var(--t2);font-family:var(--font);
font-size:.72rem;border-radius:6px;padding:.4rem .9rem;cursor:pointer;margin-bottom:1.5rem}}
.back:hover{{border-color:var(--purple);color:var(--purple)}}
.d-head{{flex-wrap:wrap;margin-bottom:.4rem}} .d-head h2{{font-size:1.3rem;font-weight:500;color:var(--t1);margin:0}}
.d-one{{font-size:.85rem;margin:0 0 .6rem}} .d-meta{{font-size:.68rem;color:var(--t3);margin-bottom:1.5rem}}
.fm{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem}}
.fm .f{{font-size:.68rem;border:1px solid var(--line);border-radius:6px;padding:.25rem .7rem}}
.fm .f.ok{{color:var(--teal);border-color:rgba(80,195,158,.3)}}
.fm .f.miss{{color:var(--coral);border-color:rgba(232,142,110,.3)}}
.sec{{border-top:1px solid var(--line);padding:1.25rem 0}}
.sec h4{{font-size:.72rem;font-weight:400;letter-spacing:.08em;color:var(--purple);margin:0 0 .6rem}}
.sec p,.sec li{{font-size:.8rem}} .sec p{{margin:0 0 .7rem}} .sec ul{{margin:0 0 .7rem;padding-left:1.2rem}}
.sec li{{margin-bottom:.45rem}} .sec b{{color:var(--t1);font-weight:500}}
.gaps{{border:1px solid rgba(232,142,110,.25);background:rgba(232,142,110,.04);border-radius:12px;
padding:1.3rem 1.5rem;margin-top:1.5rem}}
.gaps.clean{{border-color:rgba(80,195,158,.25);background:rgba(80,195,158,.04)}}
.gaps h3{{font-size:.72rem;font-weight:400;letter-spacing:.08em;color:var(--coral);margin:0 0 1rem}}
.gaps.clean h3{{color:var(--teal);margin:0}}
.gap{{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;padding:.7rem 0;border-top:1px solid var(--line)}}
.gap:first-of-type{{border-top:none;padding-top:0}}
.gap .g-txt{{font-size:.78rem}} .gap .g-kind{{font-size:.62rem;letter-spacing:.08em;color:var(--t3);display:block}}
.copy{{font-family:var(--font);font-size:.65rem;white-space:nowrap;color:#08080b;background:var(--purple);
border:none;border-radius:6px;padding:.45rem .8rem;cursor:pointer;flex-shrink:0}}
.copy:hover{{filter:brightness(1.1)}}
.toast{{position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);background:var(--purple);
color:#08080b;font-size:.72rem;padding:.55rem 1rem;border-radius:6px;opacity:0;pointer-events:none;
transition:opacity .25s;z-index:30}} .toast.show{{opacity:1}}
footer{{font-size:.68rem;color:var(--t3);padding-top:2rem}}
</style></head><body>
<div class="wrap">
  <header>
    <span class="wordmark">sapho<span class="stop">.</span> <span class="app">atlas</span></span>
    <span class="stamp">{n} projects · built <b>{date}</b> from <b>{commit}</b> · mechanical view — run /atlas for judgment</span>
  </header>
  <div id="overview">
    <div class="strip">
      <div class="stat"><div class="v">{n}</div><div class="k">projects</div></div>
      <div class="stat"><div class="v">{status_summary}</div><div class="k">statuses</div></div>
      <div class="stat"><div class="v"><span class="warn">{tracker_ok}/{n}</span></div><div class="k">tracker links set</div></div>
    </div>
    <div class="grid">{cards}</div>
  </div>
  {details}
  <footer>rebuilt automatically on every push to the corpus · fixes route through chat: copy a prompt, paste into any AI</footer>
</div>
<div class="toast" id="toast">copied · paste into any AI session</div>
<script>
(function(){{
  var ov=document.getElementById('overview');
  function show(id){{ov.hidden=!!id;
    Array.prototype.forEach.call(document.querySelectorAll('.detail'),function(d){{d.hidden=(d.id!=='detail-'+id);}});
    window.scrollTo(0,0);}}
  Array.prototype.forEach.call(document.querySelectorAll('[data-open]'),function(c){{
    c.addEventListener('click',function(){{show(c.getAttribute('data-open'));}});}});
  Array.prototype.forEach.call(document.querySelectorAll('[data-back]'),function(b){{
    b.addEventListener('click',function(){{show(null);}});}});
  var toast=document.getElementById('toast'),timer;
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'),function(btn){{
    btn.addEventListener('click',function(){{
      var t=btn.getAttribute('data-copy');
      function done(){{toast.classList.add('show');clearTimeout(timer);
        timer=setTimeout(function(){{toast.classList.remove('show');}},2000);}}
      if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(done,done);}}
      else{{done();}}
    }});}});
}})();
</script></body></html>
"""

if __name__ == "__main__":
    main()
