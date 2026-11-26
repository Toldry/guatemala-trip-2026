"""Build the static HTML site (no Jekyll) for GitHub Pages.

Sources: src/versions/<semver>.md (one file per version)
Output:  the repository root:
    index.html          latest version (honours ?v=X.Y.Z by redirecting)
    vX.Y.Z/             each version (v1/ … v5/ redirect to X.0.0)
    assets/             css + js, versions.json
"""
import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

import markdown

SRC = Path(__file__).resolve().parent.parent / "src" / "versions"
OUT = Path(__file__).resolve().parent.parent

def V(vid, date, label, summary):
    return {"id": vid, "date": date, "label": label, "summary": summary}


# Semantic versions: MAJOR = the plan changes, MINOR = content added,
# PATCH = corrections. Each has src/versions/<id>.md.
VERSIONS = [
    V("1.0.0", "22 Nov 2026", "First draft",
      "Driving loop: Antigua, Atitlán, Chichi festival, Xela, Semuc, Tikal."),
    V("2.0.0", "23 Nov 2026", "For first-timers, flying to Tikal",
      "An introduction to each place; fly GUA ↔ Flores for Tikal and Yaxhá."),
    V("3.0.0", "23 Nov 2026", "Driving to Tikal and back",
      "No flights: Semuc Champey, Tikal and Yaxhá by car, then back to GUA."),
    V("4.0.0", "23 Nov 2026", "Flights, swimming, bookings",
      "Fits the 21:25 arrival and 02:30 departure; swimming, operators, maps."),
    V("5.0.0", "23 Nov 2026", "€ prices, links, safety",
      "Q + € prices, links, crowd notes, health and safety, new maps."),
    V("5.0.1", "23 Nov 2026", "List fix", "Nested lists display correctly."),
    V("5.1.0", "23 Nov 2026", "Medicine kit explained",
      "Every medicine explained; jargon spelled out."),
    V("5.1.1", "23 Nov 2026", "Daily timeline",
      "A gridline for every day on the timeline."),
    V("5.2.0", "23 Nov 2026", "Practical notes per stop",
      "Notes box per stop; summary lists link back."),
    V("5.2.1", "23 Nov 2026", "Car type", "Small SUV, not a 4×4, and why."),
    V("5.3.0", "23 Nov 2026", "Car pick-up options",
      "Where to pick up the car; Antigua parking."),
    V("5.3.1", "23 Nov 2026", "Dengue", "December dengue risk."),
    V("6.0.0", "23 Nov 2026", "Car from the airport, new maps",
      "Car picked up on arrival; 30 m terrain maps."),
    V("6.1.0", "23 Nov 2026", "Trip cost", "Low/high cost estimate."),
    V("6.2.0", "23 Nov 2026", "Cycling",
      "Antigua bike ride; two cycling swap options."),
    V("6.3.0", "23 Nov 2026", "Daily distances",
      "Walking and cycling km per day, low–high."),
    V("6.4.0", "24 Nov 2026", "Calendar feed",
      "trip.ics to subscribe to in Google Calendar."),
    V("6.5.0", "24 Nov 2026", "Naturism",
      "Clothing-optional options near the route."),
    V("6.5.1", "24 Nov 2026", "Swimwear note removed",
      "Removed the Atitlán swimwear note."),
    V("6.6.0", "24 Nov 2026", "Works offline",
      "Installable app; guide and calendar links work offline."),
    V("6.7.0", "26 Nov 2026", "A plan for every day",
      "Every day 13–31 Dec has its own section and calendar events."),
    V("6.8.0", "26 Nov 2026", "Options side by side",
      "Alternative plans shown as Option 1 / Option 2, in the guide and calendar."),
    V("6.9.0", "26 Nov 2026", "Hot springs after Tajumulco",
      "Hot springs move to 23 Dec, after the summit; 21 Dec afternoon is free."),
    V("6.10.0", "26 Nov 2026", "Kayak on Atitlán",
      "Optional morning kayak or paddleboard on Lake Atitlán, 18 Dec."),
    V("6.11.0", "26 Nov 2026", "Day room on 30 Dec",
      "A day room before the 02:30 flight, with or without the car."),
]
LATEST = VERSIONS[-1]["id"]


# ------------------------------------------------------------ markdown
def slugify(value, separator="-"):
    """GitHub-style heading ids (keeps accented letters)."""
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value).strip().lower()
    value = "".join(ch for ch in value
                    if ch in " -_" or unicodedata.category(ch)[0] in "LN")
    return value.replace(" ", separator)


BARE_URL = re.compile(
    r"(?<![<\"'=\]/])(?<!\]\()\b((?:https?://|www\.)[^\s<>)\]|]+[^\s<>)\]|.,;:!?'\"])")


def linkify_bare_urls(text):
    """Wrap bare URLs in <...> so Markdown turns them into links."""
    out = []
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code or line.startswith("<pre"):
            out.append(line)
            continue
        out.append(BARE_URL.sub(
            lambda m: (f"<{m.group(1)}>" if m.group(1).startswith("http")
                       else f"[{m.group(1)}](https://{m.group(1)})"), line))
    return "\n".join(out)


LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+\.) ")


def normalise_lists(text):
    """Python-Markdown needs 4-space nesting and a blank line before lists."""
    out = []
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```") or line.startswith("<pre"):
            in_code = not in_code if line.startswith("```") else in_code
        match = LIST_ITEM.match(line)
        if match and not in_code:
            indent = len(match.group(1))
            line = " " * (indent * 2) + line.lstrip()
            previous = out[-1] if out else ""
            if previous.strip() and not LIST_ITEM.match(previous) \
                    and not previous.startswith(" ") and indent == 0:
                out.append("")
        out.append(line)
    return "\n".join(out)


def render(md_text, depth):
    prefix = "../" * depth
    md_text = re.sub(r'\{\{\s*"/maps/([^"]+)\.png"\s*\|\s*relative_url\s*\}\}',
                     lambda m: f"{prefix}maps/web/{m.group(1)}.jpg", md_text)
    md_text = md_text.replace("- [ ] ", "- ☐ ")
    md_text = linkify_bare_urls(md_text)
    md_text = normalise_lists(md_text)
    converter = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "md_in_html",
                    "toc"],
        extension_configs={"toc": {"slugify": slugify}},
        output_format="html5")
    body = converter.convert(md_text)
    toc_html = sidebar_toc(converter.toc_tokens)
    # the in-page "Contents" list is only needed when there's no sidebar
    body = re.sub(r"(<p><strong>Contents</strong></p>\s*<ul>.*?</ul>\s*</li>\s*</ul>)",
                  r'<div class="inline-toc">\1</div>', body, count=1,
                  flags=re.S)
    body = body.replace("<img ", '<img loading="lazy" ')
    body = re.sub(r'<a href="(https?://[^"]+)"',
                  r'<a href="\1" target="_blank" rel="noopener"', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    body = body.replace("</table>", "</table></div>")
    return body, toc_html


def sidebar_toc(tokens):
    """Nested <nav> list of h2-h4 headings for the sticky sidebar."""
    flat = []

    def walk(items):
        for item in items:
            flat.append((item["level"], item["id"], item["name"]))
            walk(item["children"])
    walk(tokens)
    while flat and flat[0][0] != 2:
        flat.pop(0)
    flat = [entry for entry in flat if 2 <= entry[0] <= 4]
    if not flat:
        return ""
    out, depth = [], 1
    out.append('<ul class="toc-l2">')
    previous = 2
    for level, anchor, name in flat:
        if level > previous:
            for lv in range(previous + 1, level + 1):
                out.append(f'<ul class="toc-l{lv}">')
        elif level < previous:
            for _ in range(previous - level):
                out.append("</li></ul>")
            out.append("</li>")
        elif out[-1] != '<ul class="toc-l2">':
            out.append("</li>")
        out.append(f'<li><a href="#{anchor}" data-level="{level}">{name}</a>')
        previous = level
    for _ in range(previous - 2):
        out.append("</li></ul>")
    out.append("</li></ul>")
    return ('<aside class="sidebar" aria-label="Contents">'
            '<div class="sidebar-inner">'
            '<div class="toc-head"><span>Contents</span>'
            '<span class="toc-progress"><span id="toc-progress-bar"></span>'
            '</span></div>'
            '<nav class="toc" id="toc"><span class="toc-marker" '
            'id="toc-marker"></span>' + "".join(out) + "</nav></div></aside>")


# ------------------------------------------------------------ template
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{prefix}assets/site.css">
<link rel="manifest" href="{prefix}manifest.webmanifest">
<meta name="theme-color" content="#0f3d3e">
<link rel="icon" href="{prefix}assets/icon-192.png">
<link rel="apple-touch-icon" href="{prefix}assets/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Guatemala 2026">
{redirect}
</head>
<body class="{body_class}" data-version="{version}" data-latest="{latest}" data-prefix="{prefix}">
<nav class="version-line" aria-label="Versions">{version_line}</nav>
<div class="layout{layout_class}">
{sidebar}
<main class="content">
{body}
</main>
</div>
<footer class="site-footer">
  Built for two hikers · maps from <a href="https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM" target="_blank" rel="noopener">Copernicus DEM</a>, <a href="https://github.com/globalmaps/gmgt10" target="_blank" rel="noopener">Global Map Guatemala</a> and <a href="https://www.naturalearthdata.com" target="_blank" rel="noopener">Natural Earth</a> · photos from <a href="https://commons.wikimedia.org" target="_blank" rel="noopener">Wikimedia Commons</a>
</footer>
<script src="{prefix}assets/site.js"></script>
{mermaid}
</body>
</html>
"""

MERMAID = """<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: false, theme: "neutral" });
  await mermaid.run({ querySelector: "pre.mermaid" });
</script>"""

# ?v=6.2.0 (or ?v=5, meaning 5.0.0) on the root page jumps to that version
REDIRECT = """<script>
  (function () {
    var v = new URLSearchParams(location.search).get("v");
    if (!v) return;
    if (/^\\d+$/.test(v)) v = v + ".0.0";
    if (/^\\d+\\.\\d+\\.\\d+$/.test(v) && v !== "%s") {
      location.replace("v" + v + "/" + location.hash);
    }
  })();
</script>""" % LATEST

CSS = """
:root {
  --ink: #1f2937; --muted: #6b7280; --line: #e5e7eb; --paper: #fffdf8;
  --accent: #c2410c; --accent-2: #15803d; --link: #1d4ed8;
  --warn-bg: #fff7ed; --warn-line: #fdba74;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 1rem; }
.version-line {
  max-width: 1300px; margin: 0 auto; padding: .5rem 1rem 0;
  font-size: .85rem; color: var(--muted);
}
.version-line a { color: var(--muted); }
.version-line strong { color: var(--ink); }
.version-line .old-note { color: #b45309; }
body {
  margin: 0; color: var(--ink); background: var(--paper);
  font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
a { color: var(--link); text-underline-offset: 2px; }
a:hover { color: var(--accent); }
.site-header {
  position: sticky; top: 0; z-index: 10; background: #0f3d3e; color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.bar {
  max-width: 1300px; margin: 0 auto; padding: .55rem 1rem;
  display: flex; gap: 1rem; align-items: center; justify-content: space-between;
  flex-wrap: wrap;
}
.brand { color: #fff; font-weight: 700; text-decoration: none; }
.tools { display: flex; gap: .6rem; align-items: center; flex-wrap: wrap; }
.version-picker { font-size: .9rem; display: flex; gap: .4rem; align-items: center; }
select {
  font: inherit; font-size: .9rem; padding: .3rem .5rem; border-radius: 6px;
  border: 1px solid #94a3b8; max-width: 22rem;
}
.button {
  color: #0f3d3e; background: #fde68a; padding: .3rem .75rem;
  border-radius: 6px; text-decoration: none; font-size: .9rem; font-weight: 600;
}
.button.ghost { background: transparent; color: #fff; border: 1px solid #94a3b8; }
.banner {
  background: #fef3c7; color: #78350f; text-align: center; padding: .45rem 1rem;
  font-size: .95rem;
}
.banner a { color: #7c2d12; font-weight: 700; }
.content { max-width: 920px; margin: 0 auto; padding: 1.5rem 1.1rem 4rem; }
h1 { font-size: 2.1rem; line-height: 1.2; margin: .6rem 0 .2rem; color: #0f3d3e; }
h2 {
  font-size: 1.7rem; margin-top: 3rem; padding-bottom: .3rem;
  border-bottom: 3px solid var(--accent); color: #0f3d3e;
}
h3 { font-size: 1.35rem; margin-top: 2.4rem; color: #134e4a; }
h4 { font-size: 1.12rem; margin-top: 1.8rem; color: #7c2d12; }
h5 { font-size: 1rem; margin-top: 1.4rem; color: #374151; text-transform: none; }
h1 + h3 { margin-top: 0; color: var(--muted); font-weight: 500; }
img { max-width: 100%; height: auto; border-radius: 8px; display: block; margin: .6rem auto; }
p > em:only-child, img + em { display: block; text-align: center; color: var(--muted); font-size: .92rem; }
blockquote {
  margin: 1.2rem 0; padding: .7rem 1rem; background: var(--warn-bg);
  border-left: 4px solid var(--warn-line); border-radius: 6px;
}
blockquote p { margin: .35rem 0; }
.table-wrap { overflow-x: auto; margin: 1rem 0; }
table { border-collapse: collapse; width: 100%; font-size: .93rem; }
th, td { border: 1px solid var(--line); padding: .45rem .6rem; vertical-align: top; }
th { background: #f1f5f9; text-align: left; }
tr:nth-child(even) td { background: #fafaf9; }
code { background: #f1f5f9; padding: .05rem .3rem; border-radius: 4px; font-size: .9em; }
pre { background: #f8fafc; padding: .8rem; border-radius: 8px; overflow-x: auto; line-height: 1.3; }
pre code { background: none; padding: 0; }
pre.mermaid { background: transparent; text-align: center; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2.5rem 0; }
.site-footer { text-align: center; color: var(--muted); font-size: .85rem; padding: 2rem 1rem; }
/* embedded in the compare page */
body.embed .version-line, body.embed .site-footer { display: none; }
body.embed .content { padding-top: .5rem; }
/* compare page */
.compare-controls { display: flex; gap: 1rem; flex-wrap: wrap; align-items: end; margin: 1rem 0; }
.compare-controls label { display: flex; flex-direction: column; font-size: .9rem; gap: .25rem; }
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; }
.compare-grid iframe {
  width: 100%; height: calc(100vh - 13rem); border: 1px solid var(--line);
  border-radius: 8px; background: #fff;
}
body.compare .content { max-width: 1600px; }
.version-list { padding-left: 1.2rem; }
@media (max-width: 900px) { .compare-grid { grid-template-columns: 1fr; } }

/* ---- sidebar table of contents (wide screens) ---- */
.sidebar { display: none; }
@media (min-width: 1200px) {
  .layout.has-sidebar {
    display: grid; grid-template-columns: 300px minmax(0, 920px);
    gap: 2.5rem; max-width: 1300px; margin: 0 auto; padding: 0 1rem;
  }
  .layout.has-sidebar .content { margin: 0; }
  .layout.has-sidebar .inline-toc { display: none; }
  .sidebar { display: block; }
  .sidebar-inner {
    position: sticky; top: 1rem; max-height: calc(100vh - 2rem);
    margin-top: 1.5rem; display: flex; flex-direction: column;
    border-right: 1px solid var(--line);
  }
  body.embed .layout.has-sidebar { display: block; }
  body.embed .sidebar { display: none; }
  body.embed .inline-toc { display: block; }
}
.toc-head {
  display: flex; flex-direction: column; gap: .4rem; padding: 0 1rem .6rem .2rem;
  font-size: .78rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted);
}
.toc-progress {
  display: block; height: 3px; background: var(--line); border-radius: 3px;
  overflow: hidden;
}
#toc-progress-bar {
  display: block; height: 100%; width: 0; border-radius: 3px;
  background: linear-gradient(90deg, var(--accent-2), var(--accent));
  transition: width .15s linear;
}
.toc {
  position: relative; overflow-y: auto; overscroll-behavior: contain;
  padding: .2rem .6rem 2rem 0; scrollbar-width: thin;
  mask-image: linear-gradient(to bottom, transparent 0, #000 .8rem,
                              #000 calc(100% - 1.6rem), transparent 100%);
}
.toc ul { list-style: none; margin: 0; padding: 0; }
.toc a {
  position: relative; display: block; padding: .22rem .5rem .22rem .9rem;
  border-radius: 6px; color: #475569; text-decoration: none;
  font-size: .86rem; line-height: 1.35;
  transition: color .2s, background-color .2s;
}
.toc a:hover { color: var(--accent); background: rgba(194,65,12,.06); }
.toc a[data-level="2"] {
  font-weight: 700; color: #0f3d3e; margin-top: .7rem; font-size: .9rem;
}
.toc .toc-l2 > li:first-child > a { margin-top: 0; }
.toc a[data-level="3"] { padding-left: 1.4rem; }
.toc a[data-level="4"] { padding-left: 2.3rem; font-size: .8rem; color: #64748b; }
/* day-level entries fold away unless their chapter is the one being read */
.toc .toc-l4 {
  max-height: 0; overflow: hidden; opacity: 0;
  transition: max-height .4s ease, opacity .3s ease;
}
.toc li.open > .toc-l4 { max-height: 40rem; opacity: 1; }
.toc a.active { color: var(--accent); font-weight: 600; }
.toc a.in-path:not(.active) { color: #0f3d3e; }
.toc-marker {
  position: absolute; left: 0; top: 0; width: 3px; height: 0;
  border-radius: 3px; background: var(--accent); opacity: 0;
  transition: transform .3s cubic-bezier(.2,.8,.2,1),
              height .3s cubic-bezier(.2,.8,.2,1), opacity .3s;
}
/* briefly highlight the heading you jumped to */
h2, h3, h4, h5 { scroll-margin-top: 1rem; }
.flash { animation: flash 1.6s ease; }
@keyframes flash {
  0% { background: rgba(253,230,138,.9); }
  100% { background: transparent; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .toc-marker, .toc .toc-l4, #toc-progress-bar { transition: none; }
  .flash { animation: none; }
}
"""

JS = r"""


// ---- links with #section (e.g. from calendar events): re-align after
// images above the section have loaded and shifted the layout ----
(function () {
  if (!location.hash) return;
  function align() {
    var el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (el && Math.abs(el.getBoundingClientRect().top) > 40) {
      el.scrollIntoView({ block: "start" });
    }
  }
  window.addEventListener("load", function () {
    align(); setTimeout(align, 600); setTimeout(align, 1500);
  });
})();

// ---- offline: register the service worker (scope = site root) ----
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    var prefix = document.body.dataset.prefix || "";
    navigator.serviceWorker.register(prefix + "sw.js").catch(function () {});
  });
}

// ---- sidebar table of contents: scroll tracking ----
(function () {
  var toc = document.getElementById("toc");
  if (!toc) return;
  var marker = document.getElementById("toc-marker");
  var progress = document.getElementById("toc-progress-bar");
  var links = Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']"));
  var targets = links.map(function (a) {
    return document.getElementById(decodeURIComponent(a.hash.slice(1)));
  });
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var activeIndex = -1;

  function headerOffset() {
    var header = document.querySelector(".site-header");
    return (header ? header.offsetHeight : 0) + 24;
  }

  function placeMarker(link) {
    if (!link) { marker.style.opacity = 0; return; }
    var navBox = toc.getBoundingClientRect();
    var box = link.getBoundingClientRect();
    var top = box.top - navBox.top + toc.scrollTop;
    marker.style.transform = "translateY(" + top + "px)";
    marker.style.height = box.height + "px";
    marker.style.opacity = 1;
  }

  function keepVisible(link) {
    var navBox = toc.getBoundingClientRect();
    var box = link.getBoundingClientRect();
    var margin = navBox.height * 0.3;
    var delta = 0;
    if (box.top < navBox.top + margin) delta = box.top - navBox.top - margin;
    else if (box.bottom > navBox.bottom - margin)
      delta = box.bottom - navBox.bottom + margin;
    if (delta) toc.scrollBy({ top: delta, behavior: reduced ? "auto" : "smooth" });
  }

  function setActive(index) {
    if (index === activeIndex) return;
    activeIndex = index;
    links.forEach(function (a) { a.classList.remove("active", "in-path"); });
    toc.querySelectorAll("li.open").forEach(function (li) { li.classList.remove("open"); });
    if (index < 0) { placeMarker(null); return; }
    var link = links[index];
    link.classList.add("active");
    // open the chapter that holds the active entry, and mark its ancestors
    var li = link.parentElement;
    var level = link.dataset.level;
    var chapter = level === "4" ? li.parentElement.closest("li") : li;
    if (chapter && chapter.querySelector(":scope > .toc-l4")) chapter.classList.add("open");
    var ancestor = li.parentElement.closest("li");
    while (ancestor && toc.contains(ancestor)) {
      var a = ancestor.querySelector(":scope > a");
      if (a) a.classList.add("in-path");
      ancestor = ancestor.parentElement.closest("li");
    }
    // wait for the fold animation before measuring
    placeMarker(link);
    setTimeout(function () { placeMarker(link); keepVisible(link); }, 420);
  }

  var ticking = false;
  function update() {
    ticking = false;
    var line = headerOffset() + 8;
    var index = -1;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i] && targets[i].getBoundingClientRect().top <= line) index = i;
      else if (targets[i]) break;
    }
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (max > 0 && window.scrollY >= max - 2) index = targets.length - 1;
    setActive(index);
    var fraction = max > 0 ? Math.min(1, window.scrollY / max) : 0;
    progress.style.width = (fraction * 100).toFixed(1) + "%";
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener("resize", function () {
    placeMarker(links[activeIndex]);
  });
  update();

  // flash the heading you jump to, from the sidebar or any in-page link
  document.addEventListener("click", function (event) {
    var a = event.target.closest("a[href^='#']");
    if (!a) return;
    var target = document.getElementById(decodeURIComponent(a.hash.slice(1)));
    if (!target) return;
    target.classList.remove("flash");
    void target.offsetWidth;
    target.classList.add("flash");
  });
})();
"""

def version_line(prefix, current):
    """One line of links to every version; the current one in bold."""
    items = []
    for meta in VERSIONS:
        vid = meta["id"]
        href = prefix if vid == LATEST else f"{prefix}v{vid}/"
        label = vid + (" (latest)" if vid == LATEST else "")
        title = html.escape(f'{meta["label"]}: {meta["summary"]}')
        if vid == current:
            items.append(f'<strong title="{title}">{label}</strong>')
        else:
            items.append(f'<a href="{href}" title="{title}">{label}</a>')
    note = ""
    if current and current != LATEST:
        note = (' <span class="old-note">· you\'re reading an older '
                f'version; <a href="{prefix}">go to the latest</a></span>')
    return "Versions: " + " · ".join(items) + note


def page(title, body, depth, version, body_class="", redirect=False,
         sidebar=""):
    prefix = "../" * depth
    return PAGE.format(
        title=html.escape(title), prefix=prefix, body=body, version=version,
        sidebar=sidebar, layout_class=" has-sidebar" if sidebar else "",
        version_line=version_line(prefix, version),
        latest=LATEST, body_class=body_class,
        redirect=REDIRECT if redirect else "",
        mermaid=MERMAID if 'class="mermaid"' in body else "")


OLD_ALIAS = {"v1": "1.0.0", "v2": "2.0.0", "v3": "3.0.0", "v4": "4.0.0",
             "v5": "5.0.0"}
STUB = """<!doctype html><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=../v{vid}/">
<link rel="canonical" href="../v{vid}/">
<script>location.replace("../v{vid}/" + location.hash);</script>
<a href="../v{vid}/">Version {vid}</a>"""


SW_TEMPLATE = r"""// Offline support for the Guatemala guide. Generated by build_site.py.
const VERSION = "__VERSION__";
const CORE = "core-" + VERSION;      // latest page, assets, maps, photos
const RUNTIME = "runtime-v1";        // older versions, CDN code, extras
const PRECACHE = __PRECACHE__;       // same-origin, relative to scope
const PHOTOS = __PHOTOS__;           // cross-origin images on the page
const MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CORE);
    await cache.addAll(PRECACHE);
    // chart code from the CDN: best effort, needs CORS for a module
    try {
      const res = await fetch(MERMAID, { mode: "cors" });
      if (res.ok) await cache.put(MERMAID, res);
    } catch (e) { /* the chart just won't draw offline */ }
    // photos: best effort, opaque responses are fine for <img>
    await Promise.all(PHOTOS.map(async (url) => {
      try {
        const res = await fetch(url, { mode: "no-cors" });
        await cache.put(url, res);
      } catch (e) { /* keep going */ }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith("core-") && key !== CORE) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});

async function fromCache(request) {
  return (await caches.match(request, { ignoreSearch: true }))
      || (await caches.match(request.url.split("#")[0], { ignoreSearch: true }));
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  const sameOrigin = url.origin === self.location.origin;

  // pages: network first (3 s), then the cached copy
  if (request.mode === "navigate") {
    event.respondWith((async () => {
      try {
        const res = await Promise.race([
          fetch(request),
          new Promise((_, reject) => setTimeout(() => reject("slow"), 3000)),
        ]);
        if (res.ok) {
          const cache = await caches.open(sameOrigin && url.pathname.match(/\/v\d/) ? RUNTIME : CORE);
          cache.put(request.url.split("?")[0], res.clone());
        }
        return res;
      } catch (e) {
        return (await fromCache(request))
            || (await caches.match(self.registration.scope))
            || Response.error();
      }
    })());
    return;
  }

  // everything else: cache first, fill the cache on the way
  event.respondWith((async () => {
    const hit = await fromCache(request);
    if (hit) return hit;
    try {
      const res = await fetch(request);
      if (res.ok || res.type === "opaque") {
        (await caches.open(RUNTIME)).put(request, res.clone());
      }
      return res;
    } catch (e) {
      return Response.error();
    }
  })());
});
"""


def make_icons():
    """Two app icons: three volcano peaks over a lake, drawn with PIL."""
    from PIL import Image, ImageDraw
    for size in (192, 512):
        scale = 4
        s = size * scale
        img = Image.new("RGB", (s, s), "#0f3d3e")
        draw = ImageDraw.Draw(img)
        draw.ellipse([s * .62, s * .14, s * .80, s * .32], fill="#f2b45a")
        for left, peak, right, height, colour in (
                (.02, .30, .58, .30, "#3f6b5a"),
                (.38, .66, .98, .24, "#2f5a4b"),
                (.20, .50, .80, .38, "#e8dcc4")):
            draw.polygon([(s * left, s * .72), (s * (peak - .04), s * height),
                          (s * (peak + .04), s * height), (s * right, s * .72)],
                         fill=colour)
        draw.rectangle([0, s * .72, s, s], fill="#2f7fa6")
        for row in (.80, .88):
            draw.line([(s * .18, s * row), (s * .82, s * row)],
                      fill="#7fb8d4", width=max(2, s // 90))
        img.resize((size, size), Image.LANCZOS).save(
            OUT / "assets" / f"icon-{size}.png", optimize=True)


def make_web_maps():
    """Smaller JPEG copies of the map PNGs for the page and offline cache."""
    from PIL import Image
    out = OUT / "maps" / "web"
    out.mkdir(exist_ok=True)
    for png in sorted((OUT / "maps").glob("*.png")):
        target = out / (png.stem + ".jpg")
        if target.exists() and target.stat().st_mtime >= png.stat().st_mtime:
            continue
        im = Image.open(png).convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)),
                           Image.LANCZOS)
        im.save(target, quality=82, optimize=True, progressive=True)


def build_pwa(latest_html):
    make_icons()
    make_web_maps()
    manifest = {
        "name": "Guatemala · 13–31 December 2026",
        "short_name": "Guatemala 2026",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#fffdf7",
        "theme_color": "#0f3d3e",
        "icons": [
            {"src": "assets/icon-192.png", "sizes": "192x192",
             "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any maskable"},
        ],
    }
    (OUT / "manifest.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2))
    used = sorted(set(re.findall(r'src="(maps/web/[^"]+)"', latest_html)))
    precache = ["./", "assets/site.css", "assets/site.js",
                "assets/icon-192.png", "assets/icon-512.png",
                "manifest.webmanifest", "trip.ics", *used]
    photos = sorted(set(html.unescape(u) for u in re.findall(
        r'<img[^>]+src="(https://[^"]+)"', latest_html)))
    import hashlib
    stamp = hashlib.sha1(latest_html.encode()).hexdigest()[:10]
    sw = (SW_TEMPLATE.replace("__VERSION__", f"{LATEST}-{stamp}")
          .replace("__PRECACHE__", json.dumps(precache, indent=2))
          .replace("__PHOTOS__", json.dumps(photos, indent=2)))
    (OUT / "sw.js").write_text(sw)


def build_ics():
    """trip.ics: all-day 'where you sleep' blocks + timed events, in UTC."""
    import datetime as dt
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "calendar_data", SRC.parent / "calendar.py")
    cal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cal)
    offset = dt.timedelta(hours=6)  # Guatemala is UTC-6 all year
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def esc(text):
        return (text.replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\n", "\\n"))

    def fold(line):
        raw = line.encode("utf-8")
        out = []
        while len(raw) > 75:
            cut = 75 if not out else 74
            while (raw[cut] & 0xC0) == 0x80:  # don't split a UTF-8 char
                cut -= 1
            out.append(raw[:cut].decode("utf-8"))
            raw = raw[cut:]
        out.append(raw.decode("utf-8"))
        return "\r\n ".join(out)

    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//guatemala-trip-2026//EN", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", "X-WR-CALNAME:Guatemala 2026",
             "X-WR-TIMEZONE:America/Guatemala",
             "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
             "X-PUBLISHED-TTL:PT6H"]

    def event(uid, start_lines, summary, location, note, anchor):
        url = cal.GUIDE + anchor
        description = (note + "\n\n" if note else "") + "Guide: " + url
        lines.extend(["BEGIN:VEVENT", f"UID:{uid}@guatemala-trip-2026",
                      f"DTSTAMP:{stamp}", *start_lines,
                      f"SUMMARY:{esc(summary)}",
                      f"LOCATION:{esc(location)}",
                      f"DESCRIPTION:{esc(description)}",
                      f"URL:{url}", "TRANSP:TRANSPARENT", "END:VEVENT"])

    for start, nights, place, location, anchor in cal.SLEEP:
        day = dt.date.fromisoformat(start)
        end = day + dt.timedelta(days=nights)
        event(f"sleep-{start}", [f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
                                 f"DTEND;VALUE=DATE:{end:%Y%m%d}"],
              f"🛏 {place}", location, f"{nights} night(s).", anchor)
    for date, begin, finish, title, location, note, anchor in cal.TIMED:
        def utc(clock):
            local = dt.datetime.fromisoformat(f"{date}T{clock}")
            return (local + offset).strftime("%Y%m%dT%H%M%SZ")
        option = re.match(r"Option (\d+):", title)
        suffix = f"-opt{option.group(1)}" if option else ""
        event(f"{date}-{begin.replace(':', '')}{suffix}",
              [f"DTSTART:{utc(begin)}", f"DTEND:{utc(finish)}"],
              title, location, note, anchor)
    lines.append("END:VCALENDAR")
    (OUT / "trip.ics").write_bytes(
        ("\r\n".join(fold(l) for l in lines) + "\r\n").encode("utf-8"))


def main():
    for target in list(OUT.iterdir()):
        name = target.name
        if (name in ("_config.yml", "index.md", "_includes", "_data",
                     "compare", "assets") or re.fullmatch(r"v[\d.]+", name)):
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
    (OUT / ".nojekyll").write_text("")
    (OUT / "assets").mkdir()
    (OUT / "assets" / "site.css").write_text(CSS.lstrip())
    (OUT / "assets" / "site.js").write_text(JS.lstrip())
    (OUT / "assets" / "versions.json").write_text(
        json.dumps(VERSIONS, ensure_ascii=False, indent=2))

    for meta in VERSIONS:
        vid = meta["id"]
        source = (SRC / f"{vid}.md").read_text()
        title = f"{vid} · Guatemala · 13–31 Dec 2026"
        folder = OUT / f"v{vid}"
        folder.mkdir()
        body, sidebar = render(source, 1)
        (folder / "index.html").write_text(
            page(title, body, 1, vid, sidebar=sidebar))
        if vid == LATEST:
            body, sidebar = render(source, 0)
            (OUT / "index.html").write_text(
                page("Guatemala · 13–31 December 2026", body, 0, vid,
                     redirect=True, sidebar=sidebar))
    # keep the old /v1/ … /v5/ links working
    for old, vid in OLD_ALIAS.items():
        (OUT / old).mkdir()
        (OUT / old / "index.html").write_text(STUB.format(vid=vid))
    build_ics()
    build_pwa((OUT / "index.html").read_text())
    print("built", [v["id"] for v in VERSIONS])


if __name__ == "__main__":
    main()
