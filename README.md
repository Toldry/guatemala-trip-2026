# Guatemala trip guide · 13–31 December 2026

A 19-day self-drive itinerary for two hikers: volcano treks, swimming spots
and Maya cities, with booking options, prices in Q and €, maps, and health
and safety notes.

**Read it:** https://toldry.github.io/guatemala-trip-2026/

- The main page always shows the **latest version**. Older versions live at
  `/v1/` … `/vN/`, and `?v=N` on the main page jumps to one.
- **Compare any two versions side by side:**
  https://toldry.github.io/guatemala-trip-2026/compare/

## How the site is built

Plain static HTML; there's no Jekyll (`.nojekyll`).

| Path | What |
|---|---|
| `index.html`, `v*/index.html`, `compare/` | Generated pages |
| `assets/` | Stylesheet, version switcher script, `versions.json` |
| `maps/` | Annotated maps and the altitude chart |
| `src/versions/v*.md` | Text of each version (input for the build) |
| `scripts/build_site.py` | Builds the HTML (`pip install markdown`) |
| `scripts/make_maps.py` | Draws the maps from Natural Earth data |

To add a version: write `src/versions/vN.md`, add an entry to `VERSIONS`
in `scripts/build_site.py`, then run `python scripts/build_site.py`.
