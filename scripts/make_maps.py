"""Annotated route maps for the Guatemala guide.

Data: Natural Earth (public domain) vectors, plus the Natural Earth
shaded-relief raster bundled in the basemap-data package.
Rendering: matplotlib + geopandas (all open source).
"""
import math
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from PIL import Image

DATA_DIR = Path("/home/claude/guide/data")
OUT_DIR = Path("/home/claude/guide/maps")
RELIEF_PATH = Path(
    "/usr/local/lib/python3.13/site-packages/mpl_toolkits/"
    "basemap_data/shadedrelief.jpg"
)

COLOR_WATER = "#a9cfe6"
COLOR_LAND = "#f3efe4"
COLOR_NEIGHBOR = "#e2ded3"
COLOR_BORDER = "#8a8579"
COLOR_ROAD = "#b9ab93"
COLOR_TEXT = "#2b2b2b"
SEGMENT_COLORS = {
    "transfer": "#7a7a7a",
    "highlands": "#c2410c",
    "north": "#15803d",
    "return": "#1d4ed8",
}

# ---------------------------------------------------------------- places
# (longitude, latitude); approximate, good to ~1 km
PLACES = {
    "GUA": (-90.527, 14.583),
    "Guatemala City": (-90.507, 14.634),
    "Antigua": (-90.734, 14.557),
    "Chimaltenango": (-90.820, 14.661),
    "Los Encuentros": (-91.135, 14.776),
    "Sololá": (-91.183, 14.773),
    "Panajachel": (-91.157, 14.740),
    "Santa Clara La Laguna": (-91.305, 14.713),
    "Santa Clara turnoff": (-91.300, 14.772),
    "San Juan La Laguna": (-91.287, 14.694),
    "San Pedro La Laguna": (-91.272, 14.693),
    "San Marcos La Laguna": (-91.258, 14.724),
    "Cerro Tzankujil": (-91.263, 14.719),
    "Indian Nose": (-91.300, 14.711),
    "Santiago Atitlán": (-91.230, 14.636),
    "Chichicastenango": (-91.111, 14.943),
    "Totonicapán": (-91.361, 14.911),
    "Cuatro Caminos": (-91.442, 14.905),
    "Xela": (-91.518, 14.845),
    "Zunil": (-91.484, 14.784),
    "Fuentes Georginas": (-91.479, 14.748),
    "Laguna Chicabal": (-91.653, 14.789),
    "San Marcos": (-91.795, 14.965),
    "Tuichán (trailhead)": (-91.862, 15.020),
    "Sanarate": (-90.192, 14.795),
    "El Rancho": (-90.020, 14.927),
    "Santa Cruz Verapaz": (-90.431, 15.374),
    "Cobán": (-90.371, 15.470),
    "Pajal": (-90.040, 15.620),
    "Lanquín": (-89.980, 15.576),
    "Semuc Champey": (-89.959, 15.534),
    "Sebol": (-89.990, 15.830),
    "Raxruhá": (-90.040, 15.867),
    "Sayaxché": (-90.190, 16.525),
    "Flores": (-89.892, 16.929),
    "Ixlú": (-89.683, 16.975),
    "El Remate": (-89.694, 16.995),
    "Tikal": (-89.623, 17.222),
    "Yaxhá turnoff": (-89.445, 17.010),
    "Yaxhá": (-89.403, 17.076),
    "Poptún": (-89.417, 16.329),
    "Río Dulce": (-88.996, 15.659),
    "Castillo de San Felipe": (-88.993, 15.637),
    "Finca El Paraíso": (-89.208, 15.591),
    "La Ruidosa": (-88.840, 15.475),
    "Teculután": (-89.715, 14.990),
    "La Soledad (Acatenango trailhead)": (-90.835, 14.526),
    "Santiaguito": (-91.570, 14.742),
    "Mundo Maya airport": (-89.866, 16.915),
    "Santa Elena": (-89.880, 16.920),
    "Ecolodge El Sombrero": (-89.420, 17.058),
    "El Estor": (-89.345, 15.530),
    "Livingston": (-88.750, 15.828),
    "Cerro de la Cruz": (-90.730, 14.565),
}

VOLCANOES = {
    "Acatenango\n3,976 m": (-90.876, 14.501),
    "Fuego\n3,763 m": (-90.881, 14.475),
    "Agua\n3,760 m": (-90.743, 14.465),
    "Pacaya\n2,552 m": (-90.601, 14.381),
    "San Pedro\n3,020 m": (-91.266, 14.656),
    "Tolimán\n3,158 m": (-91.189, 14.612),
    "Atitlán\n3,537 m": (-91.186, 14.583),
    "Santa María\n3,772 m": (-91.552, 14.756),
    "Tajumulco\n4,220 m": (-91.903, 15.044),
    "Chicabal\n2,712 m": (-91.656, 14.783),
}

# Route legs: waypoints follow the main roads (approximate, smoothed).
ROUTE_LEGS = [
    ("transfer", ["GUA", "Antigua"]),
    ("highlands", ["Antigua", "Chimaltenango", "Los Encuentros",
                   "Santa Clara turnoff", "Santa Clara La Laguna",
                   "San Juan La Laguna"]),
    ("highlands", ["San Juan La Laguna", "Santa Clara La Laguna",
                   "Santa Clara turnoff", "Los Encuentros",
                   "Chichicastenango"]),
    ("highlands", ["Chichicastenango", "Los Encuentros", "Totonicapán",
                   "Cuatro Caminos", "Xela"]),
    ("north", ["Xela", "Cuatro Caminos", "Los Encuentros", "Chimaltenango",
               "Guatemala City", "Sanarate", "El Rancho",
               "Santa Cruz Verapaz", "Cobán"]),
    ("north", ["Cobán", "Pajal", "Lanquín"]),
    ("north", ["Lanquín", "Pajal", "Sebol", "Raxruhá", "Sayaxché",
               "Flores", "Ixlú", "El Remate"]),
    ("north", ["El Remate", "Tikal"]),
    ("north", ["Tikal", "Ixlú", "Yaxhá turnoff", "Yaxhá"]),
    ("return", ["Yaxhá", "Yaxhá turnoff", "Ixlú", "Poptún", "Río Dulce"]),
    ("return", ["Río Dulce", "La Ruidosa", "Teculután", "El Rancho",
                "Sanarate", "Guatemala City", "GUA"]),
]

# Side trips by tour / short drive (dotted)
SIDE_TRIPS = [
    ["Antigua", "Acatenango\n3,976 m"],
    ["Xela", "Tuichán (trailhead)", "Tajumulco\n4,220 m"],
    ["Xela", "Laguna Chicabal"],
    ["Xela", "Zunil", "Fuentes Georginas"],
    ["Lanquín", "Semuc Champey"],
    ["Río Dulce", "Finca El Paraíso"],
]


def coordinates(name):
    if name in PLACES:
        return PLACES[name]
    return VOLCANOES[name]


# --------------------------------------------------------------- helpers
def catmull_rom(points, iterations=4):
    """Chaikin corner cutting: smooth, stays inside the waypoints' hull."""
    pts = np.asarray(points, dtype=float)
    for _ in range(iterations):
        if len(pts) < 3:
            return pts
        new = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            new.append(0.75 * a + 0.25 * b)
            new.append(0.25 * a + 0.75 * b)
        new.append(pts[-1])
        pts = np.array(new)
    return pts


def _unused_catmull_rom(points, samples_per_segment=24):
    """Smooth a polyline through its points (centripetal-ish, uniform)."""
    pts = np.asarray(points, dtype=float)
    if len(pts) < 3:
        return pts
    padded = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]])
    out = []
    for i in range(1, len(padded) - 2):
        p0, p1, p2, p3 = padded[i - 1:i + 3]
        for t in np.linspace(0, 1, samples_per_segment, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


def halo(width=3, color="white"):
    return [path_effects.withStroke(linewidth=width, foreground=color)]


def load_layers(bounds):
    min_lon, min_lat, max_lon, max_lat = bounds
    bbox = (min_lon - 1, min_lat - 1, max_lon + 1, max_lat + 1)
    layers = {
        "land": gpd.read_file(DATA_DIR / "ne_10m_land.geojson", bbox=bbox),
        "countries": gpd.read_file(
            DATA_DIR / "ne_10m_admin_0_countries.geojson", bbox=bbox),
        "lakes": gpd.read_file(DATA_DIR / "ne_10m_lakes.geojson", bbox=bbox),
        "lakes_na": gpd.read_file(
            DATA_DIR / "ne_10m_lakes_north_america.geojson", bbox=bbox),
        "rivers": gpd.read_file(
            DATA_DIR / "ne_10m_rivers_lake_centerlines.geojson", bbox=bbox),
        "rivers_na": gpd.read_file(
            DATA_DIR / "ne_10m_rivers_north_america.geojson", bbox=bbox),
        "roads": gpd.read_file(DATA_DIR / "ne_10m_roads.geojson", bbox=bbox),
        "admin1": gpd.read_file(
            DATA_DIR / "ne_10m_admin_1_states_provinces_lines.geojson",
            bbox=bbox),
    }
    return layers


def draw_relief(ax, bounds, alpha):
    """Overlay the Natural Earth shaded relief, cropped to bounds."""
    min_lon, min_lat, max_lon, max_lat = bounds
    image = Image.open(RELIEF_PATH)
    width, height = image.size
    def to_px(lon, lat):
        return ((lon + 180) / 360 * width, (90 - lat) / 180 * height)
    left, top = to_px(min_lon, max_lat)
    right, bottom = to_px(max_lon, min_lat)
    crop = image.crop((int(left), int(top), int(math.ceil(right)),
                       int(math.ceil(bottom))))
    crop = crop.resize((crop.width * 8, crop.height * 8), Image.BICUBIC)
    grey = np.asarray(crop.convert("L"), dtype=float) / 255.0
    # Turn the relief into a soft shadow layer (dark = shade)
    shade = np.clip((grey - grey.mean()) * 2.2, -1, 1)
    rgba = np.zeros(shade.shape + (4,))
    rgba[..., :3] = np.where(shade[..., None] < 0, 0.25, 1.0)
    rgba[..., 3] = np.abs(shade) * alpha
    crop_bounds = (
        int(left) / width * 360 - 180,
        int(math.ceil(right)) / width * 360 - 180,
        90 - int(math.ceil(bottom)) / height * 180,
        90 - int(top) / height * 180,
    )
    ax.imshow(rgba, extent=crop_bounds, origin="upper", zorder=2,
              interpolation="bilinear")


def base_map(ax, bounds, layers, relief_alpha=0.0, show_roads=True,
             detail_rivers=True):
    min_lon, min_lat, max_lon, max_lat = bounds
    ax.set_facecolor(COLOR_WATER)
    layers["countries"].plot(ax=ax, color=COLOR_NEIGHBOR, edgecolor="none",
                             zorder=1)
    gtm = layers["countries"][layers["countries"]["ADM0_A3"] == "GTM"]
    gtm.plot(ax=ax, color=COLOR_LAND, edgecolor="none", zorder=1.2)
    if relief_alpha:
        draw_relief(ax, bounds, relief_alpha)
    layers["admin1"][layers["admin1"]["ADM0_A3"] == "GTM"].plot(
        ax=ax, color="#cfc8b6", linewidth=0.5, linestyle=(0, (4, 3)),
        zorder=3)
    layers["countries"].boundary.plot(ax=ax, color=COLOR_BORDER,
                                      linewidth=1.0, zorder=3.2)
    rivers = layers["rivers_na"] if detail_rivers else layers["rivers"]
    rivers.plot(ax=ax, color="#7fb3d5", linewidth=0.8, zorder=3.5)
    layers["rivers"].plot(ax=ax, color="#7fb3d5", linewidth=0.9, zorder=3.5)
    for key in ("lakes", "lakes_na"):
        layers[key].plot(ax=ax, color=COLOR_WATER, edgecolor="#6fa4c7",
                         linewidth=0.6, zorder=4)
    if show_roads:
        layers["roads"].plot(ax=ax, color=COLOR_ROAD, linewidth=0.8,
                             zorder=4.5)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    mid_lat = (min_lat + max_lat) / 2
    ax.set_aspect(1 / math.cos(math.radians(mid_lat)))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555")
        spine.set_linewidth(1.2)


def draw_routes(ax, line_width=3.2, side_trips=True):
    for segment, names in ROUTE_LEGS:
        points = [coordinates(n) for n in names]
        smooth = catmull_rom(points)
        ax.plot(smooth[:, 0], smooth[:, 1], color="white",
                linewidth=line_width + 2.4, solid_capstyle="round",
                zorder=6)
        ax.plot(smooth[:, 0], smooth[:, 1],
                color=SEGMENT_COLORS[segment], linewidth=line_width,
                solid_capstyle="round", zorder=6.5)
    if side_trips:
        for names in SIDE_TRIPS:
            points = catmull_rom([coordinates(n) for n in names])
            ax.plot(points[:, 0], points[:, 1], color="#444",
                    linewidth=1.6, linestyle=(0, (1.5, 2)), zorder=6.6)


def draw_volcanoes(ax, names=None, label=True, fontsize=7.5, offsets=None):
    offsets = offsets or {}
    for name, (lon, lat) in VOLCANOES.items():
        if names is not None and name not in names:
            continue
        ax.plot(lon, lat, marker="^", markersize=8, color="#6b4f3a",
                markeredgecolor="white", markeredgewidth=0.8, zorder=7)
        if label:
            dx, dy, ha = offsets.get(name, (0.012, -0.004, "left"))
            ax.text(lon + dx, lat + dy, name, fontsize=fontsize,
                    color="#5a4030", ha=ha, va="top", zorder=8,
                    linespacing=0.95, path_effects=halo(2.5))


def day_badge(ax, lon, lat, text, color, dx=0.0, dy=0.0, size=9,
              ha="center"):
    ax.annotate(
        text, xy=(lon, lat), xytext=(lon + dx, lat + dy),
        fontsize=size, fontweight="bold", color="white", ha=ha,
        va="center", zorder=10,
        bbox=dict(boxstyle="round,pad=0.32", fc=color, ec="white", lw=1.2),
        arrowprops=dict(arrowstyle="-", color=color, lw=1.2,
                        shrinkA=0, shrinkB=3)
        if (dx or dy) else None,
    )


def place_dot(ax, name, label=None, dx=0.015, dy=0.0, ha="left",
              fontsize=9, bold=False, kind="town"):
    lon, lat = coordinates(name)
    style = {
        "town": dict(marker="o", markersize=6, color="#222"),
        "swim": dict(marker="o", markersize=10, color="#0284c7"),
        "hike": dict(marker="^", markersize=10, color="#6b4f3a"),
        "sight": dict(marker="s", markersize=7, color="#7c3aed"),
        "airport": dict(marker="P", markersize=11, color="#111"),
    }[kind]
    ax.plot(lon, lat, markeredgecolor="white", markeredgewidth=1.2,
            linestyle="none", zorder=9, **style)
    if kind == "swim":
        ax.text(lon, lat - 0.0005, "≈", fontsize=7, color="white",
                ha="center", va="center", fontweight="bold", zorder=9.5)
    if label is not None:
        ax.text(lon + dx, lat + dy, label, fontsize=fontsize,
                fontweight="bold" if bold else "normal", color=COLOR_TEXT,
                ha=ha, va="center", zorder=9.6, path_effects=halo(3))


def scale_bar(ax, bounds, km, position=(0.05, 0.05)):
    min_lon, min_lat, max_lon, max_lat = bounds
    mid_lat = (min_lat + max_lat) / 2
    deg = km / (111.32 * math.cos(math.radians(mid_lat)))
    x0 = min_lon + (max_lon - min_lon) * position[0]
    y0 = min_lat + (max_lat - min_lat) * position[1]
    height = (max_lat - min_lat) * 0.008
    for i in range(4):
        ax.add_patch(plt.Rectangle(
            (x0 + deg * i / 4, y0), deg / 4, height,
            facecolor="#222" if i % 2 == 0 else "white",
            edgecolor="#222", lw=0.8, zorder=11))
    for frac, text in ((0, "0"), (0.5, f"{km // 2}"), (1, f"{km} km")):
        ax.text(x0 + deg * frac, y0 + height * 2.2, text, fontsize=8,
                ha="center", va="bottom", zorder=11, path_effects=halo(2.5))


def north_arrow(ax, position=(0.95, 0.9)):
    ax.annotate("N", xy=position, xytext=(position[0], position[1] - 0.07),
                xycoords="axes fraction", ha="center", va="center",
                fontsize=12, fontweight="bold", zorder=12,
                arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.6),
                path_effects=halo(3))


def title_box(ax, title, subtitle, position=(0.015, 0.985)):
    ax.text(*position, title, transform=ax.transAxes, fontsize=17,
            fontweight="bold", va="top", ha="left", color="#1f2937",
            zorder=13, path_effects=halo(4))
    ax.text(position[0], position[1] - 0.045, subtitle,
            transform=ax.transAxes, fontsize=10, va="top", ha="left",
            color="#374151", zorder=13, path_effects=halo(3))


def credits(ax, extra="", overview=False):
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.text(0.745 if overview else 0.995, 0.004,
            "Data: Natural Earth (public domain). Routes approximate. "
            "Made with matplotlib & geopandas." + extra,
            transform=ax.transAxes, fontsize=6.5, ha="right", va="bottom",
            color="#555", zorder=13, path_effects=halo(2))


# ------------------------------------------------------------ map 1
def overview_map():
    bounds = (-92.35, 13.65, -88.15, 17.85)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(11, 11.6), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.55, detail_rivers=True)
    draw_routes(ax, line_width=3.0)
    draw_volcanoes(ax, names={"Acatenango\n3,976 m", "Tajumulco\n4,220 m"},
                   offsets={"Acatenango\n3,976 m": (-0.03, -0.03, "right"),
                            "Tajumulco\n4,220 m": (-0.05, 0.02, "right")})

    stops = [
        # name, label, badge, badge offset, kind, label offset
        ("GUA", "Guatemala City (GUA)\n✈ land 13 Dec 21:25\n✈ fly 31 Dec 02:30",
         "13 · 30", (0.30, -0.55), "airport", (0.07, -0.13, "left")),
        ("Antigua", "Antigua", "13–17", (-0.05, -0.42), "town",
         (-0.05, 0.06, "right")),
        ("San Juan La Laguna", "Lake Atitlán", "17–20", (-0.55, -0.32),
         "swim", (-0.06, -0.075, "right")),
        ("Chichicastenango", "Chichicastenango", "20", (0.05, 0.33), "sight",
         (0.06, 0.0, "left")),
        ("Xela", "Xela", "20–24", (-0.35, 0.35), "town", (0.05, -0.06,
                                                         "left")),
        ("Cobán", "Cobán", "24", (-0.35, 0.18), "town", (0.06, -0.04,
                                                        "left")),
        ("Lanquín", "Lanquín &\nSemuc Champey", "25–27", (0.42, 0.13),
         "swim", (0.06, -0.15, "left")),
        ("El Remate", "El Remate (Lake Petén Itzá)", "27–28",
         (-0.65, 0.00), "swim", (0.06, -0.08, "left")),
        ("Tikal", "Tikal", "28", (-0.38, 0.22), "sight", (0.06, 0.03,
                                                         "left")),
        ("Yaxhá", "Yaxhá", "28–29", (0.38, 0.20), "sight", (0.06, -0.05,
                                                           "left")),
        ("Río Dulce", "Río Dulce", "29–30", (0.35, 0.35), "swim",
         (0.06, -0.06, "left")),
    ]
    for name, label, badge, (bdx, bdy), kind, (ldx, ldy, ha) in stops:
        lon, lat = coordinates(name)
        place_dot(ax, name, label, dx=ldx, dy=ldy, ha=ha, kind=kind,
                  fontsize=9.5, bold=True)
        color = "#111827"
        day_badge(ax, lon, lat, badge, color, dx=bdx, dy=bdy, size=9)

    # Region labels
    for text, lon, lat, size in (
        ("PETÉN\nlowland rainforest", -90.55, 17.25, 12),
        ("WESTERN HIGHLANDS", -91.7, 15.45, 11),
        ("ALTA VERAPAZ\ncloud forest", -90.75, 15.95, 10.5),
        ("MEXICO", -91.95, 16.45, 13),
        ("BELIZE", -88.55, 17.1, 12),
        ("HONDURAS", -88.55, 14.75, 12),
        ("EL SALVADOR", -89.55, 13.88, 11),
        ("Pacific Ocean", -90.9, 13.80, 11),
        ("Caribbean\nSea", -88.32, 16.12, 10),
    ):
        ax.text(lon, lat, text, fontsize=size, color="#6b6458",
                ha="center", va="center", style="italic",
                fontweight="bold" if text.isupper() else "normal",
                alpha=0.85, zorder=5, linespacing=1.0,
                path_effects=halo(3, COLOR_LAND))

    title_box(ax, "Guatemala · 13–31 December",
              "Hiking, swimming and Maya cities. Badges show nights "
              "/ days at each stop.")
    legend_items = [
        Line2D([0], [0], color=SEGMENT_COLORS["highlands"], lw=3.5,
               label="Highlands loop (13–24 Dec)"),
        Line2D([0], [0], color=SEGMENT_COLORS["north"], lw=3.5,
               label="North to Petén (24–28 Dec)"),
        Line2D([0], [0], color=SEGMENT_COLORS["return"], lw=3.5,
               label="Return via Río Dulce (29–30 Dec)"),
        Line2D([0], [0], color=SEGMENT_COLORS["transfer"], lw=3.5,
               label="Night shuttle, airport → Antigua"),
        Line2D([0], [0], color="#444", lw=1.6, ls=(0, (1.5, 2)),
               label="Hike or side trip"),
        Line2D([0], [0], marker="o", color="#0284c7", lw=0, markersize=10,
               markeredgecolor="white", label="Swimming stop"),
        Line2D([0], [0], marker="^", color="#6b4f3a", lw=0, markersize=10,
               markeredgecolor="white", label="Volcano hike"),
        Line2D([0], [0], marker="s", color="#7c3aed", lw=0, markersize=8,
               markeredgecolor="white", label="Culture / ruins"),
    ]
    legend = ax.legend(handles=legend_items, loc="upper left",
                       bbox_to_anchor=(0.01, 0.905), fontsize=8.5,
                       frameon=True, framealpha=0.92, edgecolor="#999",
                       title="Legend", title_fontsize=9.5)
    legend.set_zorder(14)
    scale_bar(ax, bounds, 100, position=(0.03, 0.035))
    north_arrow(ax)
    credits(ax, overview=True)

    # Inset: where is Guatemala
    inset = ax.inset_axes([0.755, 0.012, 0.235, 0.2])
    inset_bounds = (-118, 6, -76, 33)
    world = gpd.read_file(DATA_DIR / "ne_10m_admin_0_countries.geojson",
                          bbox=inset_bounds)
    inset.set_facecolor(COLOR_WATER)
    world.plot(ax=inset, color=COLOR_NEIGHBOR, edgecolor="#999",
               linewidth=0.3)
    world[world["ADM0_A3"] == "GTM"].plot(ax=inset, color="#c2410c")
    inset.set_xlim(inset_bounds[0], inset_bounds[2])
    inset.set_ylim(inset_bounds[1], inset_bounds[3])
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_xlabel("")
    inset.set_ylabel("")
    inset.set_aspect(1 / math.cos(math.radians(20)))
    for name, lon, lat in (("USA", -100, 31), ("MEXICO", -103, 23.5)):
        inset.text(lon, lat, name, fontsize=6, ha="center", color="#555")
    for spine in inset.spines.values():
        spine.set_edgecolor("#555")
    fig.savefig(OUT_DIR / "map-01-overview.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


# ------------------------------------------------------------ map 2
def highlands_map():
    bounds = (-92.02, 14.33, -90.40, 15.17)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(13, 7.6), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.35)
    draw_routes(ax, line_width=3.4)
    draw_volcanoes(ax, offsets={
        "Acatenango\n3,976 m": (-0.018, 0.035, "right"),
        "Fuego\n3,763 m": (-0.02, -0.005, "right"),
        "Agua\n3,760 m": (0.015, -0.005, "left"),
        "Pacaya\n2,552 m": (0.015, 0.035, "left"),
        "San Pedro\n3,020 m": (-0.015, -0.008, "right"),
        "Tolimán\n3,158 m": (0.015, 0.02, "left"),
        "Atitlán\n3,537 m": (0.015, -0.005, "left"),
        "Santa María\n3,772 m": (-0.012, 0.04, "right"),
        "Tajumulco\n4,220 m": (0.016, 0.035, "left"),
        "Chicabal\n2,712 m": (-0.015, -0.012, "right"),
    })
    entries = [
        ("GUA", "GUA airport", "town", (0.015, -0.03, "left")),
        ("Antigua", "Antigua (1,530 m)", "town", (0.015, 0.03, "left")),
        ("Chichicastenango", "Chichicastenango\nSunday market",
         "sight", (0.018, 0.0, "left")),
        ("Xela", "Xela (2,330 m)", "town", (0.016, 0.022, "left")),
        ("San Juan La Laguna", "San Juan", "town",
         (-0.012, -0.022, "right")),
        ("Panajachel", "Panajachel", "town", (0.014, 0.012, "left")),
        ("Fuentes Georginas", "Fuentes Georginas\nhot springs", "swim",
         (0.02, -0.03, "left")),
        ("Laguna Chicabal", "Laguna Chicabal\n(sacred – no swimming)",
         "town", (-0.016, 0.04, "right")),
        ("San Marcos", "San Marcos", "town", (0.014, -0.012, "left")),
        ("Cerro Tzankujil", "", "swim", (0, 0, "left")),
        ("Guatemala City", "Guatemala City", "town",
         (0.015, 0.02, "left")),
    ]
    for name, label, kind, (dx, dy, ha) in entries:
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=9.5, bold=kind != "town" or name in (
                      "Antigua", "Xela"))
    badges = [
        ("Antigua", "13–14 Dec · Antigua", (-0.02, 0.17)),
        ("Acatenango\n3,976 m", "15–16 · Acatenango overnight",
         (-0.30, -0.10)),
        ("San Juan La Laguna", "17–19 · Lake Atitlán: swim,\n"
         "Indian Nose, San Pedro volcano", (-0.36, -0.16)),
        ("Chichicastenango", "20 · Market stop", (0.03, 0.12)),
        ("Fuentes Georginas", "21 · Chicabal + hot springs",
         (0.12, -0.17)),
        ("Tajumulco\n4,220 m", "22–23 · Tajumulco overnight",
         (0.33, -0.06)),
        ("Xela", "24 · leave for Cobán →", (0.33, 0.13)),
    ]
    for name, text, (dx, dy) in badges:
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#9a3412", dx=dx, dy=dy, size=8.5)
    ax.text(-91.17, 14.665, "Lake\nAtitlán", fontsize=9, color="#1e5a85",
            ha="center", style="italic", zorder=8, path_effects=halo(2))
    ax.text(-90.47, 14.98, "to Cobán →\n(24 Dec)", fontsize=9,
            color=SEGMENT_COLORS["north"], fontweight="bold", ha="center",
            zorder=8, path_effects=halo(3))
    title_box(ax, "The Western Highlands · 13–24 December",
              "Altitude builds step by step: Antigua 1,530 m → Atitlán "
              "1,560 m → Xela 2,330 m → Tajumulco summit 4,220 m")
    scale_bar(ax, bounds, 30, position=(0.03, 0.05))
    north_arrow(ax, position=(0.04, 0.32))
    credits(ax)
    fig.savefig(OUT_DIR / "map-02-highlands.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


# ------------------------------------------------------------ map 3
def north_map():
    bounds = (-91.05, 14.30, -88.55, 17.62)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(10, 11.2), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.45)
    draw_routes(ax, line_width=3.4)
    entries = [
        ("GUA", "GUA airport\n✈ 31 Dec 02:30", "airport",
         (0.03, -0.075, "left")),
        ("Cobán", "Cobán", "town", (0.03, 0.03, "left")),
        ("Lanquín", "Lanquín\ncaves · river tubing", "swim",
         (-0.035, 0.07, "right")),
        ("Semuc Champey", "Semuc Champey\nturquoise pools", "swim",
         (0.03, -0.075, "left")),
        ("Sayaxché", "Sayaxché\n(car ferry)", "town",
         (-0.03, 0.0, "right")),
        ("Flores", "Flores", "town", (-0.03, -0.03, "right")),
        ("El Remate", "El Remate\nlake swim", "swim", (0.03, -0.06,
                                                      "left")),
        ("Tikal", "Tikal", "sight", (0.03, 0.02, "left")),
        ("Yaxhá", "Yaxhá\nsunset", "sight", (0.03, 0.0, "left")),
        ("Poptún", "Poptún", "town", (0.03, 0.0, "left")),
        ("Río Dulce", "Río Dulce", "swim", (0.03, 0.045, "left")),
        ("Finca El Paraíso", "Finca El Paraíso\nhot waterfall", "swim",
         (0.0, 0.09, "center")),
        ("Guatemala City", "Guatemala City", "town",
         (0.03, 0.035, "left")),
    ]
    for name, label, kind, (dx, dy, ha) in entries:
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=9.5, bold=kind != "town")
    badges = [
        ("Cobán", "24 · Xela → Cobán, ~8 h", (-0.42, 0.20)),
        ("Lanquín", "25 · Lanquín", (0.40, 0.33)),
        ("Semuc Champey", "26 · Semuc day", (0.25, -0.38)),
        ("Sayaxché", "27 · → El Remate, ~6.5 h", (-0.45, 0.22)),
        ("Tikal", "28 · Tikal → Yaxhá", (-0.55, 0.06)),
        ("Finca El Paraíso", "29 · → Río Dulce, ~4.5 h\n+ hot waterfall",
         (-0.30, 0.55)),
        ("Guatemala City", "30 · → GUA, ~5–6 h\nfly 02:30",
         (0.80, -0.12)),
    ]
    for name, text, (dx, dy) in badges:
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#14532d", dx=dx, dy=dy, size=8.5)
    for text, lon, lat in (
        ("Lake\nPetén Itzá", -89.80, 17.06),
        ("Lake Izabal", -89.12, 15.48),
    ):
        ax.text(lon, lat, text, fontsize=9, color="#1e5a85", ha="center",
                style="italic", zorder=8, path_effects=halo(2))
    ax.text(-91.0, 14.95, "← from Xela\n(24 Dec)", fontsize=9,
            color=SEGMENT_COLORS["north"], fontweight="bold", ha="left",
            zorder=8, path_effects=halo(3))
    for text, lon, lat in (("MEXICO", -90.85, 17.3),
                           ("BELIZE", -88.75, 16.9),
                           ("HONDURAS", -88.75, 14.6)):
        ax.text(lon, lat, text, fontsize=11, color="#6b6458",
                fontweight="bold", style="italic", ha="center", zorder=5,
                path_effects=halo(3, COLOR_LAND))
    title_box(ax, "North & East · 24–30 December",
              "Cloud forest, jungle pools, Maya cities and a hot "
              "waterfall, then back to the airport")
    scale_bar(ax, bounds, 50, position=(0.05, 0.27))
    north_arrow(ax, position=(0.95, 0.80))
    credits(ax)
    fig.savefig(OUT_DIR / "map-03-north.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


# ------------------------------------------------------------ map 4
def atitlan_map():
    bounds = (-91.37, 14.55, -91.08, 14.80)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(10, 8.4), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.0, show_roads=False)
    draw_volcanoes(ax, names={"San Pedro\n3,020 m", "Tolimán\n3,158 m",
                              "Atitlán\n3,537 m"},
                   fontsize=10,
                   offsets={"San Pedro\n3,020 m": (0.006, -0.002, "left"),
                            "Tolimán\n3,158 m": (0.006, 0.012, "left"),
                            "Atitlán\n3,537 m": (0.006, -0.002, "left")})
    villages = [
        ("San Juan La Laguna", "San Juan La Laguna\n(your base)", "town",
         (-0.006, -0.01, "right"), True),
        ("San Pedro La Laguna", "San Pedro", "town",
         (0.006, -0.008, "left"), False),
        ("San Marcos La Laguna", "San Marcos", "town",
         (0.004, 0.009, "left"), False),
        ("Panajachel", "Panajachel", "town", (0.005, 0.007, "left"),
         False),
        ("Santiago Atitlán", "Santiago Atitlán", "town",
         (0.006, -0.004, "left"), False),
        ("Sololá", "Sololá", "town", (0.005, 0.004, "left"), False),
        ("Santa Clara La Laguna", "Santa Clara", "town",
         (-0.005, 0.006, "right"), False),
    ]
    for name, label, kind, (dx, dy, ha), bold in villages:
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=10, bold=bold)
    place_dot(ax, "Cerro Tzankujil", "Cerro Tzankujil\njump platform & "
              "swim", dx=0.008, dy=-0.002, ha="left", kind="swim",
              fontsize=10, bold=True)
    place_dot(ax, "Indian Nose", "Indian Nose\nsunrise viewpoint",
              dx=-0.007, dy=0.006, ha="right", kind="hike", fontsize=10,
              bold=True)
    # Hiking trails (schematic)
    trail_nose = catmull_rom([(-91.287, 14.694), (-91.297, 14.700),
                              (-91.300, 14.711)])
    trail_pedro = catmull_rom([(-91.272, 14.693), (-91.270, 14.675),
                               (-91.266, 14.656)])
    for trail in (trail_nose, trail_pedro):
        ax.plot(trail[:, 0], trail[:, 1], color="#6b4f3a", lw=2,
                ls=(0, (2, 1.5)), zorder=7)
    boat = catmull_rom([(-91.287, 14.694), (-91.275, 14.705),
                        (-91.262, 14.716)])
    ax.plot(boat[:, 0], boat[:, 1], color="#0369a1", lw=1.8,
            ls=(0, (4, 2)), zorder=7)
    ax.text(-91.271, 14.712, "lancha\n~10 min", fontsize=8,
            color="#0369a1", ha="center", zorder=8, path_effects=halo(2))
    badges = [
        ("Indian Nose", "18 Dec · 04:00 start", (-0.05, 0.03)),
        ("San Pedro\n3,020 m", "19 Dec · 4–6 h hike", (-0.06, -0.035)),
        ("Cerro Tzankujil", "18 Dec · afternoon swim", (0.06, 0.04)),
    ]
    for name, text, (dx, dy) in badges:
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#9a3412", dx=dx, dy=dy, size=9)
    ax.text(-91.19, 14.70, "Lake Atitlán\n1,560 m · up to ~340 m deep",
            fontsize=11, color="#1e5a85", ha="center", style="italic",
            zorder=8, path_effects=halo(2))
    title_box(ax, "Lake Atitlán · 17–20 December",
              "Lake outline at Natural Earth 1:10m resolution; "
              "trails schematic")
    scale_bar(ax, bounds, 5, position=(0.05, 0.05))
    north_arrow(ax, position=(0.95, 0.86))
    credits(ax)
    fig.savefig(OUT_DIR / "map-04-atitlan.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


# ------------------------------------------------------------ extras
COLOR_CROWD = "#ea580c"
COLOR_TRAFFIC = "#57534e"


def caution(ax, lon, lat, text, kind="crowd", dx=0.0, dy=0.0, ha="left",
            fontsize=8.5):
    """Orange (crowds) or grey (traffic/asphalt) warning label."""
    color = COLOR_CROWD if kind == "crowd" else COLOR_TRAFFIC
    marker = "D" if kind == "crowd" else "s"
    ax.plot(lon, lat, marker=marker, markersize=8, color=color,
            markeredgecolor="white", markeredgewidth=1.0, zorder=9.2)
    ax.annotate(text, xy=(lon, lat), xytext=(lon + dx, lat + dy),
                fontsize=fontsize, color="white", ha=ha, va="center",
                zorder=10,
                bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="white",
                          lw=1, alpha=0.95),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.1)
                if (dx or dy) else None)


def caution_legend(ax, extra=(), loc="lower right", anchor=None):
    items = [
        Line2D([0], [0], marker="D", color=COLOR_CROWD, lw=0, markersize=9,
               markeredgecolor="white", label="Expect crowds"),
        Line2D([0], [0], marker="s", color=COLOR_TRAFFIC, lw=0,
               markersize=9, markeredgecolor="white",
               label="Traffic / busy roads"),
        Line2D([0], [0], marker="o", color="#0284c7", lw=0, markersize=10,
               markeredgecolor="white", label="Swimming"),
        Line2D([0], [0], marker="^", color="#6b4f3a", lw=0, markersize=10,
               markeredgecolor="white", label="Volcano / hike"),
        *extra,
    ]
    kwargs = dict(handles=items, loc=loc, fontsize=8.5, frameon=True,
                  framealpha=0.93, edgecolor="#999")
    if anchor:
        kwargs["bbox_to_anchor"] = anchor
    legend = ax.legend(**kwargs)
    legend.set_zorder(14)


def antigua_map():
    bounds = (-91.02, 14.30, -90.42, 14.74)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(11, 8.4), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.45)
    draw_routes(ax, line_width=3.4, side_trips=False)
    trail = catmull_rom([coordinates("Antigua"),
                         coordinates("La Soledad (Acatenango trailhead)"),
                         coordinates("Acatenango\n3,976 m")])
    ax.plot(trail[:, 0], trail[:, 1], color="#444", lw=1.8,
            ls=(0, (1.5, 2)), zorder=6.6)
    draw_volcanoes(ax, names={"Acatenango\n3,976 m", "Fuego\n3,763 m",
                              "Agua\n3,760 m", "Pacaya\n2,552 m"},
                   fontsize=9.5,
                   offsets={"Acatenango\n3,976 m": (-0.012, 0.03, "right"),
                            "Fuego\n3,763 m": (-0.012, -0.004, "right"),
                            "Agua\n3,760 m": (0.012, -0.004, "left"),
                            "Pacaya\n2,552 m": (0.012, -0.004, "left")})
    for name, label, kind, (dx, dy, ha) in (
        ("Antigua", "Antigua (1,530 m)", "town", (0.012, 0.02, "left")),
        ("GUA", "GUA airport", "airport", (0.012, -0.02, "left")),
        ("Guatemala City", "Guatemala City", "town", (0.012, 0.015, "left")),
        ("Chimaltenango", "Chimaltenango", "town", (0.012, 0.01, "left")),
        ("La Soledad (Acatenango trailhead)", "La Soledad\ntrailhead",
         "town", (-0.012, 0.0, "right")),
    ):
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=10, bold=name == "Antigua")
    for name, text, (dx, dy) in (
        ("GUA", "13 Dec · land 21:25 → night shuttle", (0.0, -0.13)),
        ("Antigua", "13–14 & 16 Dec · Antigua", (0.13, 0.10)),
        ("Acatenango\n3,976 m", "15–16 Dec · overnight hike,\ncamp ~3,600 m facing Fuego",
         (-0.02, 0.17)),
    ):
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#9a3412", dx=dx, dy=dy, size=9)
    caution(ax, -90.868, 14.512,
            "Acatenango base camps: hundreds\nof hikers on peak-season nights",
            dx=-0.11, dy=-0.09, ha="center")
    caution(ax, -90.726, 14.545,
            "Antigua centre: busy at weekends;\ncobbled, few cars", dx=0.10,
            dy=-0.07, ha="left")
    caution(ax, -90.60, 14.62,
            "Guatemala City ↔ Antigua road:\nheavy traffic, avoid rush hour",
            kind="traffic", dx=0.03, dy=0.07, ha="left")
    caution_legend(ax, loc="lower left", anchor=(0.01, 0.08))
    title_box(ax, "Antigua & the volcano trio · 13–17 December",
              "Fuego erupts every few minutes; Acatenango is the "
              "dormant neighbour you climb")
    scale_bar(ax, bounds, 10, position=(0.04, 0.035))
    north_arrow(ax, position=(0.96, 0.88))
    credits(ax)
    fig.savefig(OUT_DIR / "map-04-antigua.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


def xela_map():
    bounds = (-92.12, 14.62, -91.30, 15.16)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(11, 7.8), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.4)
    departments = gpd.read_file(
        DATA_DIR / "ne_10m_admin_1_states_provinces.geojson",
        bbox=(bounds[0] - 1, bounds[1] - 1, bounds[2] + 1, bounds[3] + 1))
    san_marcos = departments[(departments["adm0_a3"] == "GTM")
                             & (departments["name"] == "San Marcos")]
    san_marcos.plot(ax=ax, facecolor="#dc2626", alpha=0.10,
                    edgecolor="#b91c1c", linewidth=1.6, hatch="///",
                    zorder=3.6)
    ax.text(-92.03, 14.80,
            "SAN MARCOS DEPT.\nUS advisory (Mar 2026):\nLevel 4 · Do Not Travel",
            fontsize=9.5, color="#991b1b", fontweight="bold", ha="center",
            zorder=8, path_effects=halo(3))
    draw_routes(ax, line_width=3.4)
    draw_volcanoes(ax, names={"Tajumulco\n4,220 m", "Santa María\n3,772 m",
                              "Chicabal\n2,712 m"}, fontsize=9.5,
                   offsets={"Tajumulco\n4,220 m": (0.012, 0.035, "left"),
                            "Santa María\n3,772 m": (-0.01, 0.035, "right"),
                            "Chicabal\n2,712 m": (-0.012, -0.012, "right")})
    for name, label, kind, (dx, dy, ha) in (
        ("Xela", "Xela (2,330 m)", "town", (0.012, 0.02, "left")),
        ("Fuentes Georginas", "Fuentes Georginas\nhot springs", "swim",
         (0.014, -0.012, "left")),
        ("Laguna Chicabal", "Laguna Chicabal", "town",
         (-0.012, 0.016, "right")),
        ("Zunil", "Zunil", "town", (0.012, 0.0, "left")),
        ("San Marcos", "San Marcos", "town", (0.012, -0.012, "left")),
        ("Tuichán (trailhead)", "Tuichán\ntrailhead", "town",
         (0.012, -0.01, "left")),
        ("Cuatro Caminos", "Cuatro Caminos", "town", (0.0, 0.022, "center")),
        ("Santiaguito", "Santiaguito\n(active dome)", "town",
         (-0.012, -0.02, "right")),
    ):
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=9.5, bold=name == "Xela")
    for name, text, (dx, dy) in (
        ("Laguna Chicabal", "21 Dec · 08:00–13:00 only", (-0.05, 0.10)),
        ("Fuentes Georginas", "21 Dec · afternoon soak", (0.02, -0.08)),
        ("Tajumulco\n4,220 m", "22–23 Dec · Plan A: Tajumulco", (0.30, 0.03)),
        ("Santa María\n3,772 m", "Plan B: Santa María\n(Quetzaltenango Dept.)",
         (-0.17, -0.07)),
    ):
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#9a3412", dx=dx, dy=dy, size=8.8)
    caution(ax, -91.505, 14.86, "Xela: city traffic, asphalt", kind="traffic",
            dx=0.08, dy=-0.09)
    caution(ax, -91.442, 14.905, "Cuatro Caminos: busy\nhighway junction",
            kind="traffic", dx=-0.16, dy=0.08, ha="center")
    caution_legend(ax, loc="upper right", anchor=(0.995, 0.86))
    title_box(ax, "Around Xela · 20–24 December",
              "Hatched area: San Marcos Department, where Tajumulco stands")
    scale_bar(ax, bounds, 10, position=(0.04, 0.035))
    north_arrow(ax, position=(0.97, 0.97))
    credits(ax)
    fig.savefig(OUT_DIR / "map-05-xela.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


def peten_map():
    bounds = (-90.02, 16.82, -89.28, 17.32)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(11, 7.8), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.25)
    draw_routes(ax, line_width=3.6, side_trips=False)
    for name, label, kind, (dx, dy, ha) in (
        ("Flores", "Flores (island)", "town", (-0.012, 0.012, "right")),
        ("Santa Elena", "Santa Elena", "town", (-0.012, -0.012, "right")),
        ("Mundo Maya airport", "Mundo Maya\nairport (FRS)", "airport",
         (0.012, -0.018, "left")),
        ("El Remate", "El Remate\nlake swim", "swim", (0.014, 0.012, "left")),
        ("Ixlú", "Ixlú junction", "town", (0.012, -0.014, "left")),
        ("Tikal", "Tikal", "sight", (0.014, 0.0, "left")),
        ("Yaxhá", "Yaxhá", "sight", (0.014, 0.01, "left")),
        ("Ecolodge El Sombrero", "Ecolodge\nEl Sombrero", "town",
         (0.012, -0.016, "left")),
    ):
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=10, bold=kind != "town")
    for name, text, (dx, dy) in (
        ("El Remate", "27 Dec · swim, sleep", (-0.20, 0.10)),
        ("Tikal", "28 Dec · 06:00 opening → 12:30", (-0.27, 0.0)),
        ("Yaxhá", "28 Dec · sunset (guide)\nsleep at El Sombrero", (0.06, 0.12)),
    ):
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#14532d", dx=dx, dy=dy, size=9)
    caution(ax, -89.623, 17.222,
            "Tikal Gran Plaza: tour groups\n09:30–14:00, holiday week",
            dx=0.20, dy=0.05)
    caution(ax, -89.892, 16.929,
            "Flores/Santa Elena: tuk-tuks,\ntraffic, busy waterfront",
            kind="traffic", dx=0.03, dy=-0.10)
    caution_legend(ax, loc="lower right")
    ax.text(-89.80, 17.005, "Lake Petén Itzá", fontsize=10, color="#1e5a85",
            style="italic", ha="center", zorder=8, path_effects=halo(2))
    title_box(ax, "Tikal, Yaxhá & Lake Petén Itzá · 27–29 December",
              "Lowland rainforest; arrive at Tikal at opening to beat "
              "heat and crowds")
    scale_bar(ax, bounds, 10, position=(0.04, 0.035))
    north_arrow(ax, position=(0.96, 0.86))
    credits(ax)
    fig.savefig(OUT_DIR / "map-06-peten.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


def izabal_map():
    bounds = (-89.48, 15.38, -88.68, 15.88)
    layers = load_layers(bounds)
    fig, ax = plt.subplots(figsize=(11, 7.4), dpi=200)
    base_map(ax, bounds, layers, relief_alpha=0.3)
    draw_routes(ax, line_width=3.6)
    for name, label, kind, (dx, dy, ha) in (
        ("Río Dulce", "Río Dulce town", "swim", (0.014, 0.014, "left")),
        ("Castillo de San Felipe", "Castillo de\nSan Felipe (1652)", "sight",
         (-0.012, -0.022, "right")),
        ("Finca El Paraíso", "Finca El Paraíso\nhot waterfall", "swim",
         (0.0, 0.035, "center")),
        ("El Estor", "El Estor", "town", (-0.012, 0.0, "right")),
        ("Livingston", "Livingston\n(boat only)", "town",
         (-0.012, 0.0, "right")),
        ("La Ruidosa", "La Ruidosa junction", "town", (0.012, 0.0, "left")),
    ):
        place_dot(ax, name, label, dx=dx, dy=dy, ha=ha, kind=kind,
                  fontsize=10, bold=kind != "town")
    for name, text, (dx, dy) in (
        ("Finca El Paraíso", "29 Dec · swim, closes 17:00", (-0.02, 0.14)),
        ("La Ruidosa", "30 Dec · → GUA, leave by 10:00", (-0.05, -0.05)),
    ):
        lon, lat = coordinates(name)
        day_badge(ax, lon, lat, text, "#1e3a8a", dx=dx, dy=dy, size=9)
    caution(ax, -88.996, 15.659,
            "Río Dulce town: trucks on the\nbridge highway, noisy & busy",
            kind="traffic", dx=0.12, dy=0.10)
    caution(ax, -89.208, 15.591,
            "El Paraíso: local crowds\non weekends & holidays", dx=-0.05,
            dy=-0.12, ha="center")
    caution_legend(ax, loc="lower left", anchor=(0.01, 0.08))
    ax.text(-89.25, 15.50, "Lake Izabal", fontsize=11, color="#1e5a85",
            style="italic", ha="center", zorder=8, path_effects=halo(2))
    title_box(ax, "Río Dulce & Lake Izabal · 29–30 December",
              "Where Guatemala's biggest lake drains to the Caribbean")
    scale_bar(ax, bounds, 10, position=(0.04, 0.035))
    north_arrow(ax, position=(0.96, 0.86))
    credits(ax)
    fig.savefig(OUT_DIR / "map-07-izabal.png", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)


def altitude_chart():
    days = list(range(13, 31))
    sleep = [1530, 1530, 3600, 1530, 1560, 1560, 1560, 2330, 2330, 4000,
             2330, 1320, 400, 400, 120, 220, 10, 1500]
    high = [1530, 1530, 3600, 3976, 2000, 2550, 3020, 2330, 2712, 4000,
            4220, 2330, 1320, 400, 400, 230, 220, 1500]
    labels = ["Antigua", "Antigua", "Acatenango camp", "Antigua",
              "Atitlán", "Atitlán", "Atitlán", "Xela", "Xela",
              "Tajumulco camp", "Xela", "Cobán", "Lanquín", "Lanquín",
              "El Remate", "Yaxhá", "Río Dulce", "GUA"]
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=200)
    ax.bar(days, high, color="#d6d3d1", width=0.7,
           label="Highest point reached that day")
    ax.plot(days, sleep, color="#c2410c", lw=2.8, marker="o",
            label="Where you sleep", zorder=3)
    for day, alt, name in zip(days, sleep, labels):
        ax.text(day, alt + 120, name, rotation=60, fontsize=8, ha="left",
                va="bottom", color="#7c2d12")
    for day, alt in zip(days, high):
        if alt >= 3000:
            ax.text(day, alt + 60, f"{alt:,} m", ha="center", fontsize=8,
                    fontweight="bold", color="#44403c")
    ax.axhline(2500, color="#9ca3af", lw=1, ls="--")
    ax.text(30.4, 2540, "2,500 m: altitude sickness\npossible above here",
            fontsize=8, color="#6b7280", ha="right", va="bottom")
    ax.set_xticks(days)
    ax.set_xticklabels([f"{d}" for d in days])
    ax.set_xlabel("December 2026")
    ax.set_ylabel("Altitude (m)")
    ax.set_ylim(0, 5200)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", frameon=False)
    ax.set_title("Altitude day by day (approximate)", loc="left",
                 fontsize=14, fontweight="bold")
    fig.savefig(OUT_DIR / "chart-08-altitude.png", bbox_inches="tight",
                pad_inches=0.1)
    plt.close(fig)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    overview_map()
    highlands_map()
    north_map()
    antigua_map()
    xela_map()
    peten_map()
    izabal_map()
    altitude_chart()
    print("done")
