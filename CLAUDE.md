# Guatemala trip 2026 — project notes for Claude

Trip guide for two hikers, **13–31 Dec 2026**, rental car picked up and returned at
Guatemala City airport (GUA). Published at https://toldry.github.io/guatemala-trip-2026/

## Repo layout

- `src/versions/<semver>.md` — one markdown source per guide version. Latest is the
  highest version number (6.6.0 at the time of writing). Never edit old versions;
  copy the latest to a new file and bump the version.
- `scripts/build_site.py` — builds the site. Contains the `VERSIONS` list
  (`V(id, date, label, summary)`), sidebar TOC, version line, `build_ics()`,
  PWA build (`build_pwa()`, `SW_TEMPLATE`, icons, web-sized maps).
- `src/calendar.py` — `SLEEP` and `TIMED` event lists for `trip.ics`
  (times stored in UTC = Guatemala time + 6 h; stable UIDs).
- `scripts/make_maps.py` — route maps (Copernicus DEM, Global Map Guatemala,
  Natural Earth, networkx routing). Data lives outside the repo.
- Built output: `index.html` (latest), `vX.Y.Z/` (old versions), `v1/`…`v5/`
  redirect stubs, `trip.ics`, `sw.js`, `manifest.webmanifest`.
- `planning/` — research and booking notes that are not (yet) in the guide.

## Conventions

- **Semantic versioning, one version per change.** Each change gets its own
  `src/versions/X.Y.Z.md`, a `VERSIONS` entry, a rebuild, and its own commit
  titled `X.Y.Z: <what changed>`.
- Rebuild with `python3 scripts/build_site.py` and check the output before committing.
- Push with `git -c push.negotiate=true push origin main`.
- Commit trailer must credit `Co-Authored-By: Toldry <toldry@gmail.com>`.
- Metric units. Plain-text URLs in chat replies.

## Owner preferences (for chat replies)

- No sycophancy; push back when wrong; state confidence when unsure ("~80 % sure").
- Give both unix and PowerShell syntax when they differ; each command in its own fenced block.
- Light linguistics trivia welcome, not forced.
- If a question depends on location and none is given, ask.

## Open threads

See `planning/booking-research.md` for the car rental, insurance and Acatenango
research and the list of open to-dos.
