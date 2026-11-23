"""Build the static HTML site (no Jekyll) for GitHub Pages.

Sources: /home/claude/site-src/versions/v*.md
Output:  the repository root:
    index.html          latest version (honours ?v=N by redirecting)
    v1/ ... vN/         each version
    compare/            side-by-side comparison of any two versions
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

VERSIONS = [
    {"id": 1, "date": "22 Nov 2026", "label": "First draft",
     "summary": "Driving loop: Antigua, Atitlán, Chichi festival, Xela, "
                "Semuc, Tikal."},
    {"id": 2, "date": "23 Nov 2026", "label": "For first-timers, flying to Tikal",
     "summary": "An introduction to each place; fly GUA ↔ Flores for Tikal "
                "and Yaxhá."},
    {"id": 3, "date": "23 Nov 2026", "label": "Driving to Tikal and back",
     "summary": "No flights: Semuc Champey, Tikal and Yaxhá by car, then "
                "back to GUA."},
    {"id": 4, "date": "23 Nov 2026", "label": "Flights, swimming, bookings",
     "summary": "Fits the 21:25 arrival and 02:30 departure; swimming stops, "
                "operators, maps and photos."},
    {"id": 5, "date": "23 Nov 2026", "label": "€ prices, links, safety",
     "summary": "Q + € prices, links everywhere, crowd and traffic notes, "
                "tips, health and safety, 5 new maps."},
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
    md_text = re.sub(r'\{\{\s*"/(maps/[^"]+)"\s*\|\s*relative_url\s*\}\}',
                     lambda m: prefix + m.group(1), md_text)
    md_text = md_text.replace("- [ ] ", "- ☐ ")
    md_text = linkify_bare_urls(md_text)
    md_text = normalise_lists(md_text)
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "md_in_html",
                    "toc"],
        extension_configs={"toc": {"slugify": slugify}},
        output_format="html5")
    body = body.replace("<img ", '<img loading="lazy" ')
    body = re.sub(r'<a href="(https?://[^"]+)"',
                  r'<a href="\1" target="_blank" rel="noopener"', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    body = body.replace("</table>", "</table></div>")
    return body


# ------------------------------------------------------------ template
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{prefix}assets/site.css">
{redirect}
</head>
<body class="{body_class}" data-version="{version}" data-latest="{latest}" data-prefix="{prefix}">
<header class="site-header">
  <div class="bar">
    <a class="brand" href="{prefix}">Guatemala · 13–31 Dec 2026</a>
    <nav class="tools">
      <label class="version-picker">Version
        <select id="version-select" aria-label="Choose a version"></select>
      </label>
      <a class="button" href="{prefix}compare/">Compare versions</a>
      <a class="button ghost" href="https://github.com/Toldry/guatemala-trip-2026" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </div>
  <div id="old-version-banner" class="banner" hidden></div>
</header>
<main class="content">
{body}
</main>
<footer class="site-footer">
  Built for two hikers · maps from <a href="https://www.naturalearthdata.com" target="_blank" rel="noopener">Natural Earth</a> · photos from <a href="https://commons.wikimedia.org" target="_blank" rel="noopener">Wikimedia Commons</a>
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

# ?v=N on the root page jumps to that version, before anything renders
REDIRECT = """<script>
  (function () {
    var v = new URLSearchParams(location.search).get("v");
    if (v && /^\\d+$/.test(v) && v !== "%s") {
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
html { scroll-behavior: smooth; scroll-padding-top: 4.5rem; }
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
  max-width: 1100px; margin: 0 auto; padding: .55rem 1rem;
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
body.embed .site-header, body.embed .site-footer { display: none; }
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
"""

JS = r"""
(function () {
  var body = document.body;
  var prefix = body.dataset.prefix || "";
  var current = parseInt(body.dataset.version || "0", 10);
  var latest = parseInt(body.dataset.latest || "0", 10);
  var params = new URLSearchParams(location.search);
  if (params.get("embed") === "1") body.classList.add("embed");

  fetch(prefix + "assets/versions.json").then(function (r) { return r.json(); })
    .then(function (versions) {
      var select = document.getElementById("version-select");
      if (!select) return;
      versions.slice().reverse().forEach(function (v) {
        var option = document.createElement("option");
        option.value = v.id;
        option.textContent = "v" + v.id + " · " + v.date + " · " + v.label +
          (v.id === latest ? " (latest)" : "");
        if (v.id === current) option.selected = true;
        select.appendChild(option);
      });
      if (!current) {
        var placeholder = document.createElement("option");
        placeholder.textContent = "Choose…";
        placeholder.selected = true;
        placeholder.disabled = true;
        select.insertBefore(placeholder, select.firstChild);
      }
      select.addEventListener("change", function () {
        var id = parseInt(select.value, 10);
        location.href = id === latest ? prefix : prefix + "v" + id + "/";
      });
      if (current && current !== latest) {
        var banner = document.getElementById("old-version-banner");
        banner.hidden = false;
        banner.innerHTML = "You're viewing <strong>version " + current +
          "</strong>, an older version. <a href='" + prefix +
          "'>Go to the latest (v" + latest + ")</a> · <a href='" + prefix +
          "compare/?a=" + current + "&b=" + latest + "'>Compare with latest</a>";
      }
    });
})();
"""

COMPARE_BODY = """
<h1>Compare versions</h1>
<p>Pick two versions to read side by side. Each one scrolls independently.</p>
<div class="compare-controls">
  <label>Left
    <select id="left"></select>
  </label>
  <label>Right
    <select id="right"></select>
  </label>
  <a class="button" id="swap" href="#">⇄ Swap</a>
</div>
<div class="compare-grid">
  <iframe id="frame-left" title="Left version"></iframe>
  <iframe id="frame-right" title="Right version"></iframe>
</div>
<h2>All versions</h2>
<ol class="version-list" id="version-list" reversed></ol>
<script>
(function () {
  var params = new URLSearchParams(location.search);
  fetch("../assets/versions.json").then(function (r) { return r.json(); })
    .then(function (versions) {
      var latest = versions[versions.length - 1].id;
      var left = document.getElementById("left");
      var right = document.getElementById("right");
      var list = document.getElementById("version-list");
      versions.slice().reverse().forEach(function (v) {
        [left, right].forEach(function (select) {
          var option = document.createElement("option");
          option.value = v.id;
          option.textContent = "v" + v.id + " · " + v.date + " · " + v.label;
          select.appendChild(option);
        });
        var item = document.createElement("li");
        item.value = v.id;
        item.innerHTML = "<a href='../v" + v.id + "/'><strong>v" + v.id +
          " · " + v.label + "</strong></a> (" + v.date + ")" +
          (v.id === latest ? " <em>latest</em>" : "") + "<br>" + v.summary;
        list.appendChild(item);
      });
      left.value = params.get("a") || Math.max(1, latest - 1);
      right.value = params.get("b") || latest;
      function load() {
        document.getElementById("frame-left").src = "../v" + left.value + "/?embed=1";
        document.getElementById("frame-right").src = "../v" + right.value + "/?embed=1";
        history.replaceState(null, "", "?a=" + left.value + "&b=" + right.value);
      }
      left.addEventListener("change", load);
      right.addEventListener("change", load);
      document.getElementById("swap").addEventListener("click", function (e) {
        e.preventDefault();
        var a = left.value; left.value = right.value; right.value = a; load();
      });
      load();
    });
})();
</script>
"""


def page(title, body, depth, version, body_class="", redirect=False):
    prefix = "../" * depth
    return PAGE.format(
        title=html.escape(title), prefix=prefix, body=body, version=version,
        latest=LATEST, body_class=body_class,
        redirect=REDIRECT if redirect else "",
        mermaid=MERMAID if 'class="mermaid"' in body else "")


def main():
    # clean old Jekyll artefacts
    for name in ("_config.yml", "index.md", "_includes", "_data", "compare",
                 "assets") + tuple(f"v{i}" for i in range(1, 20)):
        target = OUT / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    (OUT / ".nojekyll").write_text("")
    (OUT / "assets").mkdir()
    (OUT / "assets" / "site.css").write_text(CSS.lstrip())
    (OUT / "assets" / "site.js").write_text(JS.lstrip())
    (OUT / "assets" / "versions.json").write_text(
        json.dumps(VERSIONS, ensure_ascii=False, indent=2))

    for meta in VERSIONS:
        source = (SRC / f"v{meta['id']}.md").read_text()
        title = f"v{meta['id']} · Guatemala · 13–31 Dec 2026"
        folder = OUT / f"v{meta['id']}"
        folder.mkdir()
        (folder / "index.html").write_text(
            page(title, render(source, 1), 1, meta["id"]))
        if meta["id"] == LATEST:
            (OUT / "index.html").write_text(
                page("Guatemala · 13–31 December 2026", render(source, 0), 0,
                     meta["id"], redirect=True))

    (OUT / "compare").mkdir()
    (OUT / "compare" / "index.html").write_text(
        page("Compare versions · Guatemala guide", COMPARE_BODY, 1, 0,
             body_class="compare"))
    print("built", [v["id"] for v in VERSIONS])


if __name__ == "__main__":
    main()
