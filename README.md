# Guatemala trip guide · 13–31 December 2026

A 19-day self-drive itinerary for two hikers: volcano treks (Acatenango,
Tajumulco, San Pedro), swimming stops (Lake Atitlán, Semuc Champey,
Finca El Paraíso hot waterfall) and Maya cities (Tikal, Yaxhá).

**Read it here:** https://toldry.github.io/guatemala-trip-2026/

## Contents

| Path | What |
|---|---|
| `index.md` | The guide (rendered by GitHub Pages / Jekyll, Cayman theme) |
| `maps/` | Annotated route maps (PNG) |
| `scripts/make_maps.py` | Script that draws the maps |
| `_includes/head-custom.html` | Adds Mermaid rendering for the timeline chart |

## Regenerating the maps

The maps use public-domain [Natural Earth](https://www.naturalearthdata.com)
data and the shaded-relief raster bundled with `basemap-data`.

```bash
pip install geopandas matplotlib pillow basemap-data
mkdir -p data && cd data
base=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
for layer in ne_10m_admin_0_countries ne_10m_lakes ne_10m_lakes_north_america \
    ne_10m_rivers_lake_centerlines ne_10m_rivers_north_america ne_10m_roads \
    ne_10m_land ne_10m_admin_1_states_provinces_lines; do
  curl -sfO "$base/$layer.geojson"
done
cd .. && python scripts/make_maps.py
```

The script currently has absolute paths for the data and output folders
(`DATA_DIR`, `OUT_DIR`, `RELIEF_PATH`); adjust them at the top of the file.

Photos are hot-linked from Wikimedia Commons; credits are in
[section 14 of the guide](https://toldry.github.io/guatemala-trip-2026/#14-photo--data-credits).
