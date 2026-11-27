"""Events for trip.ics. Times are local Guatemala time (UTC-6, no DST).

SLEEP: all-day blocks "where you sleep" (start date, nights, place).
TIMED: fixed-time events (date, start, end, title, location, note).
Anchors point into the guide: sleep blocks link to the stop's section, timed
events to their day's section (each day in Part 2 has a "day's plan" that
these events mirror; keep the two in step). Free time is an event too,
titled "Free: ...", so every day shows what is planned. Alternatives for the
same slot are separate events titled "Option 1: ...", "Option 2: ...", with
overlapping times (each gets its own UID).
"""

GUIDE = "https://toldry.github.io/guatemala-trip-2026/"

S21 = "#21-antigua--acatenango-1317-dec"
S22 = "#22-lake-atitlán-1720-dec"
S24 = "#23-xela--tajumulco-2024-dec"
S25 = "#24-cobán-lanquín--semuc-champey-2427-dec"
S26 = "#25-tikal--yaxhá-2729-dec"
S27 = "#26-río-dulce--the-drive-home-2931-dec"

# One anchor per day, 13–31 Dec
D13 = "#sun-13-dec--land-2125-pick-up-the-car-drive-to-antigua"
D14 = "#mon-14-dec--antigua-with-a-morning-bike-ride-"
D15 = "#tue-15-dec--acatenango-day-1-hike-up-to-camp-"
D16 = "#wed-16-dec--acatenango-day-2-summit-at-sunrise-back-to-antigua-"
D17 = "#thu-17-dec--antigua--lake-atitlán-then-wander-san-juan"
D18 = "#fri-18-dec--indian-nose-at-sunrise-then-swimming-"
D19 = "#sat-19-dec--volcán-san-pedro-3020-m-"
D20 = "#sun-20-dec--a-last-lake-morning-then-drive-to-xela"
D21 = "#mon-21-dec--laguna-chicabal-then-a-calm-afternoon-in-xela"
D22 = "#tue-22-dec--tajumulco-day-1-hike-up-to-camp-"
D23 = "#wed-23-dec--tajumulco-day-2-summit-at-sunrise-then-hot-springs-"
D24 = "#thu-24-dec--xela--cobán-8-h"
D25 = "#fri-25-dec--cobán--lanquín-2-h-"
D26 = "#sat-26-dec--semuc-champey-"
D27 = "#sun-27-dec--lanquín--el-remate-65-h-"
D28 = "#mon-28-dec--tikal-at-opening--yaxhá-at-sunset"
D29 = "#tue-29-dec--yaxhá--río-dulce-45-h--hot-waterfall-"
D30 = "#wed-30-dec--río-dulce--gua-56-h-fly-at-0230"
D31 = "#thu-31-dec--fly-home-at-0230-"

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
    # Sun 13
    ("2026-12-13", "21:25", "23:00", "✈ Land at GUA, immigration, pick up the car",
     "La Aurora International Airport", "Photograph the car; confirm the 30 Dec return.", D13),
    ("2026-12-13", "23:00", "23:59", "🚗 Drive GUA → Antigua (~1 h), check in",
     "Antigua Guatemala", "The trip's only night drive. Tell the hotel you arrive ~midnight.", D13),
    # Mon 14
    ("2026-12-14", "09:00", "12:00", "🚲 Antigua bike ride (Old Town Outfitters)",
     "Old Town Outfitters, 7a Calle Poniente 23, Antigua", "Golden Arches or Las Tierras Altas.", D14),
    ("2026-12-14", "12:00", "13:30", "🍽 Lunch in Antigua", "Antigua Guatemala", "", D14),
    ("2026-12-14", "13:30", "16:30", "🚶 Free: wander Antigua (Arco, La Merced, market)",
     "Arco de Santa Catalina, Antigua", "Pick up any rented Acatenango gear.", D14),
    ("2026-12-14", "16:30", "17:45", "⛰ Cerro de la Cruz viewpoint",
     "Cerro de la Cruz, Antigua", "Sunset ~17:35. Daylight only.", D14),
    ("2026-12-14", "18:30", "21:00", "🍽 Dinner; pack for Acatenango",
     "Antigua Guatemala", "Leave the big bags with the hotel.", D14),
    # Tue 15
    ("2026-12-15", "08:00", "15:00", "⛰ Acatenango: pick-up, hike up to camp",
     "Antigua Guatemala", "Pick-up time depends on the operator: check the booking.", D15),
    ("2026-12-15", "15:00", "17:30", "Option 1: 🛌 Rest at camp",
     "Volcán Acatenango", "", D15),
    ("2026-12-15", "15:00", "17:30", "Option 2: ⛰ Fuego ridge add-on",
     "Volcán Acatenango", "Only if you booked the add-on.", D15),
    ("2026-12-15", "17:30", "21:00", "🌋 Evening at camp: dinner, watch Fuego erupt",
     "Volcán Acatenango", "Early night: summit start ~04:00.", D15),
    # Wed 16
    ("2026-12-16", "04:00", "13:00", "⛰ Acatenango summit at sunrise, descend to Antigua",
     "Volcán Acatenango", "", D16),
    ("2026-12-16", "13:00", "17:00", "🛌 Free: rest in Antigua (shower, nap, lunch)",
     "Antigua Guatemala", "Nothing planned.", D16),
    ("2026-12-16", "17:00", "18:00", "💵 ATM: cash for Lake Atitlán; check bloqueos",
     "Antigua Guatemala", "No ATMs in San Juan or Santa Clara.", D16),
    ("2026-12-16", "18:30", "21:00", "🍽 Easy dinner, early night", "Antigua Guatemala", "", D16),
    # Thu 17
    ("2026-12-17", "08:00", "11:30", "🚗 Drive Antigua → Lake Atitlán (~3 h)",
     "San Juan La Laguna", "Steep descent from Santa Clara: low gear.", D17),
    ("2026-12-17", "11:30", "13:00", "🛏 Check in, lunch", "San Juan La Laguna", "", D17),
    ("2026-12-17", "13:00", "17:30", "🚶 Free: wander San Juan La Laguna, enjoy the lake",
     "San Juan La Laguna",
     "Nothing booked. Ideas: weaving cooperatives (MayAchik' free tour), "
     "painters' galleries, mural lanes, coffee at La Voz, Mirador Kaqasiiwaan "
     "at sunset (Q20–Q30), a first swim.", D17),
    ("2026-12-17", "18:00", "21:00", "🍽 Dinner in San Juan or San Pedro",
     "San Juan La Laguna", "Early night: Indian Nose at 04:00.", D17),
    # Fri 18
    ("2026-12-18", "04:00", "08:00", "🌄 Indian Nose sunrise hike",
     "Rostro Maya, Santa Clara La Laguna", "Only with a community guide or tour. Cash.", D18),
    ("2026-12-18", "08:00", "12:30", "Option 1: 🛌 Free: breakfast, nap, slow morning",
     "San Juan La Laguna", "Nothing planned.", D18),
    ("2026-12-18", "09:00", "11:00", "Option 2: 🛶 Kayak or paddleboard on the lake",
     "San Pedro La Laguna",
     "Mornings are calmer than afternoons (Xocomil wind). ~US$10/h single, $20 double.", D18),
    ("2026-12-18", "09:00", "09:45", "Option 3: ⛵ Lancha San Juan → Panajachel",
     "Panajachel dock", "≈ Q25–Q35 each. Then a tuk-tuk (Q10 each) or 15 min walk.", D18),
    ("2026-12-18", "10:30", "12:30", "Option 3: 🪢 Zipline + butterfly dome, Reserva Natural Atitlán",
     "Reserva Natural Atitlán, Panajachel",
     "Check in 10:30 for the 11:00 group. Q310 (1 h 30) or Q450 (2 h) each, entry included.", D18),
    ("2026-12-18", "12:30", "13:30", "Option 3: 🍽 Lunch in Panajachel", "Panajachel", "", D18),
    ("2026-12-18", "13:30", "14:00", "Option 3: ⛵ Lancha Panajachel → San Marcos",
     "San Marcos La Laguna dock", "Then Cerro Tzankujil until 17:00.", D18),
    ("2026-12-18", "12:30", "13:00", "⛵ Lancha San Juan → San Marcos",
     "San Juan La Laguna dock", "Q20–Q25 each. With Option 3, from Panajachel at 13:30 instead.", D18),
    ("2026-12-18", "13:00", "17:00", "🏊 Cerro Tzankujil, swim",
     "Cerro Tzankujil, San Marcos La Laguna", "Q20 each, cash. Last lanchas ~17:00–18:00.", D18),
    ("2026-12-18", "18:00", "21:00", "🍽 Dinner in San Juan", "San Juan La Laguna", "", D18),
    # Sat 19
    ("2026-12-19", "06:00", "15:00", "Option 1: ⛰ San Pedro volcano",
     "Volcán San Pedro, San Pedro La Laguna",
     "Tuk-tuk to the park office ~06:00. Q100 entry + guide Q150–Q200.", D19),
    ("2026-12-19", "08:00", "14:00", "Option 2: 🚲 Lake-villages bike ride",
     "San Juan La Laguna", "San Juan → San Pablo → San Marcos, swim stop.", D19),
    ("2026-12-19", "15:30", "17:00", "🏊 Cool-down swim in the lake", "San Juan La Laguna", "", D19),
    ("2026-12-19", "18:00", "21:00", "🧳 Dinner, pay the lodge in cash, pack",
     "San Juan La Laguna", "Check bloqueos on the CA-1. Leave at 07:00.", D19),
    # Sun 20
    ("2026-12-20", "08:00", "11:30", "Option 1: 🏊 Free: last lake morning, swim",
     "San Juan La Laguna", "Or the kayak, if you skipped it on the 18th.", D20),
    ("2026-12-20", "09:00", "10:30", "Option 2: 🧶 Free: weaving or coffee session",
     "San Juan La Laguna", "MayAchik' workshops from Q65.", D20),
    ("2026-12-20", "11:30", "12:30", "🛏 Check out (cash), lunch", "San Juan La Laguna", "", D20),
    ("2026-12-20", "12:30", "15:00", "🚗 Drive San Juan → Xela (~2.5 h)",
     "Quetzaltenango", "Check for bloqueos on the CA-1 the evening before.", D20),
    ("2026-12-20", "15:00", "18:30", "🚶 Free: check in, wander Xela's centre",
     "Parque Centro América, Quetzaltenango", "Optional: visit your Tajumulco operator.", D20),
    ("2026-12-20", "18:30", "21:00", "🍽 Dinner in Xela", "Quetzaltenango", "Taxi after ~21:00.", D20),
    # Mon 21
    ("2026-12-21", "07:15", "08:00", "🚗 Drive Xela → Laguna Chicabal (~45 min)",
     "San Martín Sacatepéquez", "", D21),
    ("2026-12-21", "08:00", "12:00", "⛰ Laguna Chicabal",
     "Laguna Chicabal, San Martín Sacatepéquez", "Open 08:00–13:00. No swimming (sacred). Q20.", D21),
    ("2026-12-21", "12:00", "13:00", "🚗 Back to Xela, lunch", "Quetzaltenango", "", D21),
    ("2026-12-21", "13:00", "17:30", "🛌 Free: calm afternoon in Xela",
     "Parque Centro América, Quetzaltenango", "Nothing planned. Hot springs are on the 23rd.", D21),
    ("2026-12-21", "18:00", "19:00", "📋 Tajumulco briefing (Quetzaltrekkers)",
     "Quetzaltenango", "Only if booked with Quetzaltrekkers.", D21),
    ("2026-12-21", "19:00", "21:00", "🍽 Dinner; pack for Tajumulco",
     "Quetzaltenango", "Leave the big bags at the hotel.", D21),
    # Tue 22
    ("2026-12-22", "05:00", "14:00", "Option 1: ⛰ Tajumulco: transport + hike up to camp",
     "Volcán Tajumulco", "Departure time per operator.", D22),
    ("2026-12-22", "14:00", "20:00", "Option 1: ⛺ Evening at Tajumulco camp",
     "Volcán Tajumulco", "Nothing else planned. Early night.", D22),
    ("2026-12-22", "09:00", "18:00", "Option 2: 🛌 Free day in Xela (Tajumulco off)",
     "Quetzaltenango", "Rest; pack for the pre-dawn Santa María hike.", D22),
    # Wed 23
    ("2026-12-23", "04:00", "14:00", "Option 1: ⛰ Tajumulco summit at sunrise, back to Xela",
     "Volcán Tajumulco", "", D23),
    ("2026-12-23", "02:30", "11:00", "Option 2: ⛰ Volcán Santa María sunrise hike",
     "Volcán Santa María, Quetzaltenango", "Start time per operator.", D23),
    ("2026-12-23", "14:00", "14:45", "🚗 Shower, then drive Xela → Zunil",
     "Zunil", "~30–45 min.", D23),
    ("2026-12-23", "14:45", "17:00", "Option 1: ♨ Fuentes Georginas hot springs",
     "Fuentes Georginas, Zunil", "Q60 + Q25 parking, cash.", D23),
    ("2026-12-23", "14:45", "17:00", "Option 2: ♨ Private steam sauna, Las Cumbres",
     "Las Cumbres, Zunil", "About Q75 each per hour.", D23),
    ("2026-12-23", "17:00", "17:45", "🚗 Back to Xela before dark",
     "Quetzaltenango", "Sunset ~17:50.", D23),
    ("2026-12-23", "18:00", "21:00", "🍽 Dinner, fill the tank, check bloqueos",
     "Quetzaltenango", "Leave at 06:00 tomorrow.", D23),
    # Thu 24
    ("2026-12-24", "06:00", "14:00", "🚗 Drive Xela → Cobán (~8 h)",
     "Cobán", "Heavy Christmas Eve traffic around Guatemala City.", D24),
    ("2026-12-24", "14:00", "18:00", "🚶 Free: wander Cobán, El Calvario steps, ATM",
     "Templo El Calvario, Cobán", "Draw cash for Lanquín and Semuc.", D24),
    ("2026-12-24", "19:00", "23:59", "🎄 Nochebuena: tamales, midnight fireworks",
     "Cobán", "Ask the hotel ahead about dinner; many places close.", D24),
    # Fri 25
    ("2026-12-25", "07:30", "09:00", "☕ Free: slow Christmas breakfast in Cobán",
     "Cobán", "Top up cash if needed.", D25),
    ("2026-12-25", "09:00", "11:00", "🚗 Drive Cobán → Lanquín (~2 h)",
     "Lanquín", "Winding road.", D25),
    ("2026-12-25", "11:00", "13:00", "🛏 Check in, lunch", "Lanquín", "", D25),
    ("2026-12-25", "13:00", "16:00", "🏊 River tubing",
     "Río Lanquín", "Via your lodge; ask if it runs on Christmas Day.", D25),
    ("2026-12-25", "17:00", "18:30", "🦇 Grutas de Lanquín: bats at dusk",
     "Grutas de Lanquín", "Q30 each.", D25),
    ("2026-12-25", "18:30", "21:00", "🍽 Dinner at the lodge", "Lanquín", "Don't drive after dark.", D25),
    # Sat 26
    ("2026-12-26", "07:30", "08:00", "🚙 4×4 pickup Lanquín → Semuc",
     "Lanquín", "Leave the car in Lanquín.", D26),
    ("2026-12-26", "08:00", "16:00", "🏊 Semuc Champey + K'anba cave + El Mirador",
     "Semuc Champey", "Bring Q110 each for entry. Pools before 10:30 or after 15:00.", D26),
    ("2026-12-26", "16:00", "21:00", "🛌 Free: evening at the lodge, pack",
     "Lanquín", "Leave at 06:30 tomorrow.", D26),
    # Sun 27
    ("2026-12-27", "06:30", "13:00", "🚗 Drive Lanquín → El Remate (~6.5 h)",
     "El Remate, Petén", "Car ferry at Sayaxché. Draw cash in Flores.", D27),
    ("2026-12-27", "13:00", "14:00", "🛏 Check in, lunch", "El Remate, Petén", "", D27),
    ("2026-12-27", "14:00", "17:30", "Option 1: 🏊 Free: swim in Lake Petén Itzá",
     "El Remate, Petén", "Back before dark (~17:30).", D27),
    ("2026-12-27", "14:00", "17:30", "Option 2: 🚲 Free: lakeshore bike ride",
     "El Remate, Petén", "Bikes from the hotel, Q35–Q80/day. Back before dark.", D27),
    ("2026-12-27", "18:00", "21:00", "Option 1: 🍽 Quiet dinner in El Remate",
     "El Remate, Petén", "Early night: leave for Tikal ~05:20.", D27),
    ("2026-12-27", "18:00", "21:00", "Option 2: 🍽 Evening in Flores",
     "Flores, Petén", "30 min away. Early night: leave for Tikal ~05:20.", D27),
    # Mon 28
    ("2026-12-28", "05:20", "06:00", "🚗 Drive El Remate → Tikal (~35 min)",
     "Tikal National Park", "", D28),
    ("2026-12-28", "06:00", "12:30", "🏛 Tikal (gate opens 06:00)",
     "Tikal National Park", "Ticket bought online in advance.", D28),
    ("2026-12-28", "12:30", "14:30", "🚗 Lunch, drive Tikal → Yaxhá (~1.5 h), check in",
     "Ecolodge El Sombrero, Yaxhá", "Last 11 km dirt road.", D28),
    ("2026-12-28", "14:30", "18:00", "🌅 Yaxhá at sunset (with guide)",
     "Yaxhá National Park", "Park closes 17:00; sunset needs a guide. Q80 entry.", D28),
    ("2026-12-28", "18:30", "21:00", "🍽 Dinner at the lodge", "Ecolodge El Sombrero, Yaxhá", "", D28),
    # Tue 29
    ("2026-12-29", "07:00", "12:00", "🚗 Drive Yaxhá → Río Dulce (~4.5 h)",
     "Río Dulce", "", D29),
    ("2026-12-29", "12:00", "13:00", "🛏 Check in, lunch", "Río Dulce", "", D29),
    ("2026-12-29", "13:00", "16:30", "🏊 Finca El Paraíso hot waterfall",
     "Finca El Paraíso, El Estor road", "Closes 17:00. Q15–Q20, cash.", D29),
    ("2026-12-29", "17:00", "21:00", "🛌 Free: evening at the river lodge",
     "Río Dulce", "Swim from the dock, dinner on the river.", D29),
    # Wed 30
    ("2026-12-30", "08:00", "09:45", "Option 1: 🏊 Free: morning swim from the dock",
     "Río Dulce", "", D30),
    ("2026-12-30", "08:00", "09:45", "Option 2: 🏰 Free: Castillo de San Felipe",
     "Castillo de San Felipe de Lara, Río Dulce", "Opens 08:00.", D30),
    ("2026-12-30", "10:00", "16:00", "🚗 Drive Río Dulce → GUA (~5–6 h)",
     "Guatemala City", "Leave by 10:00 at the latest.", D30),
    ("2026-12-30", "16:00", "20:30", "Option 1: 🛏 Refuel, day room at Hilton Garden Inn",
     "Hilton Garden Inn, Zona 9, Guatemala City",
     "Bookable by the hour on HotelsByDay. Dinner there.", D30),
    ("2026-12-30", "21:00", "21:30", "Option 1: 🚗 Return the rental car",
     "La Aurora International Airport", "Confirm desk hours / key drop.", D30),
    ("2026-12-30", "16:00", "16:45", "Option 2: 🚗 Refuel, return the rental car",
     "La Aurora International Airport", "In daylight; then the guesthouse shuttle.", D30),
    ("2026-12-30", "17:00", "23:00", "Option 2: 🛏 Rest at an airport guesthouse (Zona 13)",
     "Zona 13, Guatemala City",
     "E.g. Casa Aurora or L'Aurora Inn (24 h shuttle). Shuttle back ~23:00.", D30),
    ("2026-12-30", "23:30", "23:59", "✈ Be at the terminal",
     "La Aurora International Airport", "", D30),
    # Thu 31
    ("2026-12-31", "00:00", "02:30", "✈ Airside, wait at the gate",
     "La Aurora International Airport", "", D31),
    ("2026-12-31", "02:30", "03:00", "✈ Flight departs",
     "La Aurora International Airport", "Nothing else planned in Guatemala.", D31),
]

_uids = [(e[0], e[1], e[3].split(":")[0] if e[3].startswith("Option") else "")
         for e in TIMED]
assert len(_uids) == len(set(_uids)), "two events share a date, start time and option"
