"""Events for trip.ics. Times are local Guatemala time (UTC-6, no DST).

SLEEP: all-day blocks "where you sleep" (start date, nights, place).
TIMED: fixed-time events (date, start, end, title, location, note).
Anchors point into the guide so each event links to its section.
"""

GUIDE = "https://toldry.github.io/guatemala-trip-2026/"

S21 = "#21-antigua--acatenango-1317-dec"
S22 = "#22-lake-atitlán-1720-dec"
S23 = "#23-chichicastenango-20-dec"
S24 = "#24-xela--tajumulco-2024-dec"
S25 = "#25-cobán-lanquín--semuc-champey-2427-dec"
S26 = "#26-tikal--yaxhá-2729-dec"
S27 = "#27-río-dulce--the-drive-home-2931-dec"

SLEEP = [
    ("2026-12-13", 2, "Antigua", "Antigua Guatemala", S21),
    ("2026-12-15", 1, "Acatenango camp (~3,600 m)", "Volcán Acatenango", S21),
    ("2026-12-16", 1, "Antigua", "Antigua Guatemala", S21),
    ("2026-12-17", 3, "San Juan La Laguna", "San Juan La Laguna", S22),
    ("2026-12-20", 2, "Xela", "Quetzaltenango", S24),
    ("2026-12-22", 1, "Tajumulco camp (~4,000 m)", "Volcán Tajumulco", S24),
    ("2026-12-23", 1, "Xela", "Quetzaltenango", S24),
    ("2026-12-24", 1, "Cobán", "Cobán, Alta Verapaz", S25),
    ("2026-12-25", 2, "Lanquín", "Lanquín, Alta Verapaz", S25),
    ("2026-12-27", 1, "El Remate", "El Remate, Petén", S26),
    ("2026-12-28", 1, "Ecolodge El Sombrero, Yaxhá", "Yaxhá, Petén", S26),
    ("2026-12-29", 1, "Río Dulce", "Río Dulce, Izabal", S27),
]

TIMED = [
    ("2026-12-13", "21:25", "23:59", "✈ Land at GUA, pick up car, drive to Antigua",
     "La Aurora International Airport", "Drive ~1 h; tell the hotel you arrive ~midnight.", S21),
    ("2026-12-14", "09:00", "12:00", "🚲 Antigua bike ride (Old Town Outfitters)",
     "Old Town Outfitters, 7a Calle Poniente 23, Antigua", "Golden Arches or Las Tierras Altas.", S21),
    ("2026-12-15", "08:00", "17:00", "⛰ Acatenango: hike to camp",
     "Antigua Guatemala", "Pick-up time depends on the operator: check the booking.", S21),
    ("2026-12-16", "04:00", "13:00", "⛰ Acatenango summit at sunrise, descend",
     "Volcán Acatenango", "", S21),
    ("2026-12-17", "08:00", "12:00", "🚗 Drive Antigua → Lake Atitlán (~3 h)",
     "San Juan La Laguna", "Check for bloqueos on the CA-1 the evening before.", S22),
    ("2026-12-18", "04:00", "08:00", "🌄 Indian Nose sunrise hike",
     "Rostro Maya, Santa Clara La Laguna", "Only with a community guide or tour. Cash.", S22),
    ("2026-12-18", "13:00", "17:00", "🏊 Cerro Tzankujil, swim",
     "Cerro Tzankujil, San Marcos La Laguna", "Q20 each, cash. Last lanchas ~17:00–18:00.", S22),
    ("2026-12-19", "06:00", "15:00", "⛰ San Pedro volcano (or 🚲 lake-villages ride)",
     "Volcán San Pedro, San Pedro La Laguna", "Swap option: bike ride instead.", S22),
    ("2026-12-20", "07:00", "09:30", "🚗 Drive San Juan → Chichicastenango (~2.5 h)",
     "Chichicastenango", "", S23),
    ("2026-12-20", "09:30", "13:30", "🛍 Chichicastenango Sunday market",
     "Chichicastenango", "No photos inside Santo Tomás church.", S23),
    ("2026-12-20", "13:30", "15:30", "🚗 Drive Chichicastenango → Xela (~2 h)",
     "Quetzaltenango", "", S24),
    ("2026-12-21", "08:00", "12:00", "⛰ Laguna Chicabal",
     "Laguna Chicabal, San Martín Sacatepéquez", "Open 08:00–13:00. No swimming (sacred). Q20.", S24),
    ("2026-12-21", "13:30", "17:00", "♨ Hot springs: Fuentes Georginas / Las Cumbres",
     "Zunil", "Fuentes Georginas Q60 + Q25 parking, cash.", S24),
    ("2026-12-21", "18:00", "19:00", "📋 Tajumulco briefing (Quetzaltrekkers)",
     "Quetzaltenango", "Only if booked with Quetzaltrekkers.", S24),
    ("2026-12-22", "05:00", "17:00", "⛰ Tajumulco: hike to camp",
     "Volcán Tajumulco", "Departure time per operator.", S24),
    ("2026-12-23", "04:00", "14:00", "⛰ Tajumulco summit at sunrise, back to Xela",
     "Volcán Tajumulco", "", S24),
    ("2026-12-24", "06:00", "14:00", "🚗 Drive Xela → Cobán (~8 h)",
     "Cobán", "Heavy Christmas Eve traffic around Guatemala City.", S25),
    ("2026-12-25", "09:00", "11:00", "🚗 Drive Cobán → Lanquín (~2 h)",
     "Lanquín", "Draw cash in Cobán first.", S25),
    ("2026-12-25", "13:00", "17:00", "🏊 Lanquín caves + river tubing",
     "Grutas de Lanquín", "", S25),
    ("2026-12-26", "08:00", "16:00", "🏊 Semuc Champey + K'anba cave",
     "Semuc Champey", "Leave the car in Lanquín; hostel 4×4 pickup.", S25),
    ("2026-12-27", "06:30", "13:00", "🚗 Drive Lanquín → El Remate (~6.5 h)",
     "El Remate, Petén", "Car ferry at Sayaxché. Draw cash in Flores.", S25),
    ("2026-12-28", "06:00", "13:00", "🏛 Tikal (gate opens 06:00)",
     "Tikal National Park", "Ticket bought online in advance.", S26),
    ("2026-12-28", "14:30", "18:00", "🌅 Yaxhá at sunset (with guide)",
     "Yaxhá National Park", "Park closes 17:00; sunset needs a guide. Q80 entry.", S26),
    ("2026-12-29", "07:00", "12:00", "🚗 Drive Yaxhá → Río Dulce (~4.5 h)",
     "Río Dulce", "", S27),
    ("2026-12-29", "13:00", "16:30", "🏊 Finca El Paraíso hot waterfall",
     "Finca El Paraíso, El Estor road", "Closes 17:00. Q15–Q20, cash.", S27),
    ("2026-12-30", "10:00", "16:00", "🚗 Drive Río Dulce → GUA (~5–6 h)",
     "Guatemala City", "Leave by 10:00 at the latest.", S27),
    ("2026-12-30", "21:00", "21:30", "🚗 Return the rental car",
     "La Aurora International Airport", "Confirm desk hours / key drop.", S27),
    ("2026-12-30", "23:30", "23:59", "✈ Be at the terminal",
     "La Aurora International Airport", "", S27),
    ("2026-12-31", "02:30", "03:00", "✈ Flight departs",
     "La Aurora International Airport", "", S27),
]
