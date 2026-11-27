"""Events for public-transport.ics, the car-free alternative.

Same format as calendar.py (local Guatemala time, UTC-6; "Free: ..." events
for free time; "Option 1: ...", "Option 2: ..." for alternatives, with
overlapping times). Anchors point into public-transport/index.html; each day
in Part 2 of src/public-transport.md has a "day's plan" that these events
mirror, so keep the two in step.
"""

GUIDE = "https://toldry.github.io/guatemala-trip-2026/public-transport/"

S21 = "#21-antigua--acatenango-1317-dec"
S22 = "#22-lake-atitlán-1720-dec"
S23 = "#23-xela--tajumulco-2024-dec"
S24 = "#24-cobán-lanquín--semuc-champey-2427-dec"
S25 = "#25-flores--tikal-2729-dec"
S26 = "#26-río-dulce--back-to-the-airport-2931-dec"

# One anchor per day, 13–31 Dec
D13 = "#sun-13-dec--land-2125-transfer-to-antigua"
D14 = "#mon-14-dec--antigua-with-a-morning-bike-ride-"
D15 = "#tue-15-dec--acatenango-day-1-hike-up-to-camp-"
D16 = "#wed-16-dec--acatenango-day-2-summit-at-sunrise-back-to-antigua-"
D17 = "#thu-17-dec--shuttle-to-lake-atitlán-then-wander-san-juan"
D18 = "#fri-18-dec--indian-nose-at-sunrise-then-swimming-"
D19 = "#sat-19-dec--volcán-san-pedro-3020-m-"
D20 = "#sun-20-dec--a-last-lake-morning-then-shuttle-to-xela"
D21 = "#mon-21-dec--laguna-chicabal-by-bus-then-a-calm-afternoon-in-xela"
D22 = "#tue-22-dec--tajumulco-day-1-hike-up-to-camp-"
D23 = "#wed-23-dec--tajumulco-day-2-summit-at-sunrise-then-hot-springs-"
D24 = "#thu-24-dec--xela--cobán-by-shuttle-or-two-buses"
D25 = "#fri-25-dec--cobán--lanquín-by-microbus-"
D26 = "#sat-26-dec--semuc-champey-"
D27 = "#sun-27-dec--lanquín--flores-by-driver-or-shuttle"
D28 = "#mon-28-dec--tikal-with-or-without-yaxhá"
D29 = "#tue-29-dec--flores--río-dulce-by-shuttle--hot-waterfall-"
D30 = "#wed-30-dec--río-dulce--guatemala-city-by-pullman-fly-at-0230"
D31 = "#thu-31-dec--fly-home-at-0230-"

SLEEP = [
    ("2026-12-13", 2, "Antigua", "Antigua Guatemala", S21),
    ("2026-12-15", 1, "Acatenango camp (~3,600 m)", "Volcán Acatenango", S21),
    ("2026-12-16", 1, "Antigua", "Antigua Guatemala", S21),
    ("2026-12-17", 3, "San Juan La Laguna", "San Juan La Laguna", S22),
    ("2026-12-20", 2, "Xela", "Quetzaltenango", S23),
    ("2026-12-22", 1, "Tajumulco camp (~4,000 m)", "Volcán Tajumulco", S23),
    ("2026-12-23", 1, "Xela", "Quetzaltenango", S23),
    ("2026-12-24", 1, "Cobán", "Cobán, Alta Verapaz", S24),
    ("2026-12-25", 2, "Lanquín", "Lanquín, Alta Verapaz", S24),
    ("2026-12-27", 2, "Flores", "Flores, Petén", S25),
    ("2026-12-29", 1, "Río Dulce", "Río Dulce, Izabal", S26),
]

TIMED = [
    # Sun 13
    ("2026-12-13", "21:25", "22:30", "✈ Land at GUA, immigration, bags",
     "La Aurora International Airport", "", D13),
    ("2026-12-13", "22:30", "23:45", "Option 1: 🚐 Private transfer GUA → Antigua",
     "Antigua Guatemala", "~US$72 for the car incl. night surcharge. Driver waits in arrivals.", D13),
    ("2026-12-13", "22:30", "23:59", "Option 2: 🚐 Gray Line shared shuttle GUA → Antigua",
     "Antigua Guatemala", "~US$16 each, min. 2 at night. May wait for other flights.", D13),
    # Mon 14
    ("2026-12-14", "09:00", "12:00", "🚲 Antigua bike ride (Old Town Outfitters)",
     "Old Town Outfitters, 7a Calle Poniente 23, Antigua", "Golden Arches or Las Tierras Altas.", D14),
    ("2026-12-14", "12:00", "13:30", "🍽 Lunch in Antigua", "Antigua Guatemala", "", D14),
    ("2026-12-14", "13:30", "16:30", "🚶 Free: wander Antigua (Arco, La Merced, market)",
     "Arco de Santa Catalina, Antigua", "Pick up any rented Acatenango gear.", D14),
    ("2026-12-14", "16:30", "17:45", "⛰ Cerro de la Cruz viewpoint",
     "Cerro de la Cruz, Antigua", "Sunset ~17:35. Daylight only.", D14),
    ("2026-12-14", "18:30", "21:00", "🍽 Dinner; pack for Acatenango",
     "Antigua Guatemala", "Leave the big bags with the hotel. Tuk-tuk after 22:00.", D14),
    # Tue 15
    ("2026-12-15", "08:00", "15:00", "⛰ Acatenango: pick-up, hike up to camp",
     "Antigua Guatemala", "Operator transport. Pick-up time: check the booking.", D15),
    ("2026-12-15", "15:00", "17:30", "Option 1: 🛌 Rest at camp", "Volcán Acatenango", "", D15),
    ("2026-12-15", "15:00", "17:30", "Option 2: ⛰ Fuego ridge add-on",
     "Volcán Acatenango", "Only if you booked the add-on.", D15),
    ("2026-12-15", "17:30", "21:00", "🌋 Evening at camp: dinner, watch Fuego erupt",
     "Volcán Acatenango", "Early night: summit start ~04:00.", D15),
    # Wed 16
    ("2026-12-16", "04:00", "13:00", "⛰ Acatenango summit at sunrise, ride back to Antigua",
     "Volcán Acatenango", "", D16),
    ("2026-12-16", "13:00", "17:00", "🛌 Free: rest in Antigua (shower, nap, lunch)",
     "Antigua Guatemala", "Nothing planned.", D16),
    ("2026-12-16", "17:00", "18:00", "💵 ATM: cash for the lake; confirm tomorrow's shuttle",
     "Antigua Guatemala", "No ATMs in San Juan or Santa Clara. Shuttle pickup 08:30.", D16),
    ("2026-12-16", "18:30", "21:00", "🍽 Easy dinner, early night", "Antigua Guatemala", "", D16),
    # Thu 17
    ("2026-12-17", "08:30", "12:00", "🚐 Shuttle Antigua → San Pedro La Laguna (~3–3.5 h)",
     "San Pedro La Laguna", "US$22–25 each. Hotel pickup.", D17),
    ("2026-12-17", "12:00", "12:15", "🛺 Tuk-tuk San Pedro → San Juan", "San Juan La Laguna",
     "≈ Q10–Q20. Agree the price first.", D17),
    ("2026-12-17", "12:15", "13:30", "🛏 Check in, lunch", "San Juan La Laguna", "", D17),
    ("2026-12-17", "13:30", "17:30", "🚶 Free: wander San Juan La Laguna, enjoy the lake",
     "San Juan La Laguna",
     "Nothing booked. Ideas: weaving cooperatives, painters' galleries, "
     "coffee, Mirador Kaqasiiwaan at sunset, a first swim.", D17),
    ("2026-12-17", "18:00", "21:00", "🍽 Dinner; book a 04:00 tuk-tuk for Indian Nose",
     "San Juan La Laguna", "Early night.", D17),
    # Fri 18
    ("2026-12-18", "04:00", "08:00", "🌄 Indian Nose sunrise hike",
     "Rostro Maya, Santa Clara La Laguna", "Only with a community guide or tour. Cash.", D18),
    ("2026-12-18", "08:00", "12:30", "Option 1: 🛌 Free: breakfast, nap, slow morning",
     "San Juan La Laguna", "Nothing planned.", D18),
    ("2026-12-18", "09:00", "11:00", "Option 2: 🛶 Kayak or paddleboard on the lake",
     "San Pedro La Laguna", "Mornings are calmer. ~US$10/h single, $20 double.", D18),
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
     "San Juan La Laguna", "Confirm tomorrow's shuttle time to Xela.", D19),
    # Sun 20
    ("2026-12-20", "08:00", "11:30", "Option 1: 🏊 Free: last lake morning, swim",
     "San Juan La Laguna", "Or the kayak, if you skipped it on the 18th.", D20),
    ("2026-12-20", "09:00", "10:30", "Option 2: 🧶 Free: weaving or coffee session",
     "San Juan La Laguna", "MayAchik' workshops from Q65.", D20),
    ("2026-12-20", "11:30", "12:15", "🛏 Check out (cash), early lunch, tuk-tuk to San Pedro",
     "San Pedro La Laguna", "", D20),
    ("2026-12-20", "12:30", "15:00", "🚐 Shuttle San Pedro → Xela (~2–2.5 h)",
     "Quetzaltenango", "US$33–40 each. Departure time per operator.", D20),
    ("2026-12-20", "15:00", "18:30", "🚶 Free: check in, wander Xela's centre",
     "Parque Centro América, Quetzaltenango", "Optional: visit your Tajumulco operator.", D20),
    ("2026-12-20", "18:30", "21:00", "🍽 Dinner in Xela", "Quetzaltenango", "Taxi after ~21:00.", D20),
    # Mon 21
    ("2026-12-21", "06:45", "07:45", "Option 1: 🐔 Chicken bus Xela → Laguna Chicabal stop",
     "San Martín Sacatepéquez",
     "Towards Colomba/Coatepeque, Q5–Q15. Ask for 'la parada de la laguna'.", D21),
    ("2026-12-21", "07:15", "07:55", "Option 2: 🚕 Taxi Xela → Laguna Chicabal",
     "San Martín Sacatepéquez", "≈ Q300–Q400 return with waiting (estimate).", D21),
    ("2026-12-21", "08:00", "12:30", "⛰ Laguna Chicabal",
     "Laguna Chicabal, San Martín Sacatepéquez", "Open 08:00–13:00. No swimming (sacred). Q20.", D21),
    ("2026-12-21", "12:30", "13:30", "🚌 Back to Xela, lunch", "Quetzaltenango", "", D21),
    ("2026-12-21", "13:30", "17:30", "🛌 Free: calm afternoon in Xela",
     "Parque Centro América, Quetzaltenango", "Nothing planned. Hot springs are on the 23rd.", D21),
    ("2026-12-21", "18:00", "19:00", "📋 Tajumulco briefing (Quetzaltrekkers)",
     "Quetzaltenango", "Only if booked with Quetzaltrekkers.", D21),
    ("2026-12-21", "19:00", "21:00", "🍽 Dinner; pack for Tajumulco",
     "Quetzaltenango", "Leave the big bags at the hotel.", D21),
    # Tue 22
    ("2026-12-22", "05:00", "14:00", "Option 1: ⛰ Tajumulco: transport + hike up to camp",
     "Volcán Tajumulco", "Operator transport. Departure time per operator.", D22),
    ("2026-12-22", "14:00", "20:00", "Option 1: ⛺ Evening at Tajumulco camp",
     "Volcán Tajumulco", "Nothing else planned. Early night.", D22),
    ("2026-12-22", "09:00", "18:00", "Option 2: 🛌 Free day in Xela (Tajumulco off)",
     "Quetzaltenango", "Rest; pack for the pre-dawn Santa María hike.", D22),
    # Wed 23
    ("2026-12-23", "04:00", "14:00", "Option 1: ⛰ Tajumulco summit at sunrise, back to Xela",
     "Volcán Tajumulco", "", D23),
    ("2026-12-23", "02:30", "11:00", "Option 2: ⛰ Volcán Santa María sunrise hike",
     "Volcán Santa María, Quetzaltenango", "Start time per operator.", D23),
    ("2026-12-23", "14:00", "14:30", "🚿 Quick shower at the hotel", "Quetzaltenango", "", D23),
    ("2026-12-23", "14:30", "18:00", "Option 1: ♨ Fuentes Georginas by shuttle",
     "Fuentes Georginas, Zunil", "Collectivo shuttle at 14:30, ~US$25 each incl. entry.", D23),
    ("2026-12-23", "14:30", "17:30", "Option 2: ♨ Las Cumbres steam sauna, by bus to Zunil",
     "Las Cumbres, Zunil", "Bus Q5–Q10; sauna ~Q75 each per hour. Back before dark.", D23),
    ("2026-12-23", "18:00", "21:00", "🍽 Dinner; confirm tomorrow's transport",
     "Quetzaltenango", "Shuttle pickup 07:00 (Option 1) or bus at 05:00 (Option 2).", D23),
    # Thu 24
    ("2026-12-24", "07:00", "17:00", "Option 1: 🚐 Shuttle Xela → Cobán (~10 h)",
     "Cobán", "Adrenalina's Xela → Lanquín shuttle, US$75 each; get off in Cobán.", D24),
    ("2026-12-24", "05:00", "09:00", "Option 2: 🚌 Álamo bus Xela → Guatemala City",
     "Guatemala City", "~Q105 each.", D24),
    ("2026-12-24", "09:00", "10:00", "Option 2: 🚕 Uber to the Monja Blanca terminal",
     "Monja Blanca terminal, Guatemala City", "≈ Q50–Q80.", D24),
    ("2026-12-24", "10:00", "15:00", "Option 2: 🚌 Monja Blanca bus Guatemala City → Cobán",
     "Cobán", "Q105–Q125 each, roughly hourly. Christmas Eve: be early.", D24),
    ("2026-12-24", "15:30", "17:30", "Option 2: 🚶 Free: wander Cobán, El Calvario, ATM",
     "Templo El Calvario, Cobán", "With Option 1, just draw cash on arrival.", D24),
    ("2026-12-24", "07:00", "15:00", "Option 3: 🚗 Private driver Xela → Cobán (~8 h)",
     "Cobán", "≈ US$250–400 for the car (estimate). Book a week ahead.", D24),
    ("2026-12-24", "15:30", "17:30", "Option 3: 🚶 Free: wander Cobán, El Calvario, ATM",
     "Templo El Calvario, Cobán", "", D24),
    ("2026-12-24", "19:00", "23:59", "🎄 Nochebuena: tamales, midnight fireworks",
     "Cobán", "Ask the hotel ahead about dinner; many places close.", D24),
    # Fri 25
    ("2026-12-25", "07:30", "09:00", "☕ Free: slow Christmas breakfast in Cobán",
     "Cobán", "El Calvario if you arrived late yesterday.", D25),
    ("2026-12-25", "09:00", "11:30", "Option 1: 🚐 Microbus Cobán → Lanquín (~2–2.5 h)",
     "Lanquín", "From the market, Q40–Q50 each. Fewer on Christmas Day.", D25),
    ("2026-12-25", "09:30", "11:30", "Option 2: 🚕 Lodge driver Cobán → Lanquín",
     "Lanquín", "≈ Q500–Q700 for the car (estimate).", D25),
    ("2026-12-25", "11:30", "13:00", "🛏 Check in, lunch", "Lanquín", "", D25),
    ("2026-12-25", "13:00", "16:00", "🏊 River tubing",
     "Río Lanquín", "Via your lodge; ask if it runs on Christmas Day.", D25),
    ("2026-12-25", "17:00", "18:30", "🦇 Grutas de Lanquín: bats at dusk",
     "Grutas de Lanquín", "Q30 each.", D25),
    ("2026-12-25", "18:30", "21:00", "🍽 Dinner at the lodge", "Lanquín", "", D25),
    # Sat 26
    ("2026-12-26", "07:30", "08:00", "🛻 Pickup truck Lanquín → Semuc", "Lanquín", "", D26),
    ("2026-12-26", "08:00", "16:00", "🏊 Semuc Champey + K'anba cave + El Mirador",
     "Semuc Champey", "Bring Q110 each for entry. Pools before 10:30 or after 15:00.", D26),
    ("2026-12-26", "16:00", "21:00", "🛌 Free: evening at the lodge, pack",
     "Lanquín", "Shuttle to Flores at 08:00 tomorrow.", D26),
    # Sun 27
    ("2026-12-27", "08:00", "15:30", "Option 2: 🚗 Private driver Lanquín → Flores (~7.5 h)",
     "Flores, Petén", "US$325 for the car. Door to door.", D27),
    ("2026-12-27", "08:00", "16:00", "Option 1: 🚐 Shuttle Lanquín → Flores (~8 h)",
     "Flores, Petén", "US$40–45 each. Drop-off at the 'I love Petén' letters.", D27),
    ("2026-12-27", "16:00", "16:30", "🛺 Tuk-tuk to the island, check in", "Flores, Petén", "", D27),
    ("2026-12-27", "16:30", "17:45", "🚶 Free: sunset walk round Flores island, ATM",
     "Flores, Petén", "Draw cash for Tikal (no ATMs there).", D27),
    ("2026-12-27", "18:00", "21:00", "🍽 Dinner in Flores", "Flores, Petén",
     "Confirm tomorrow's pickup time. Early night.", D27),
    # Mon 28
    ("2026-12-28", "07:00", "19:30", "Option 1: 🏛 Tikal + 🌅 Yaxhá sunset day tour",
     "Tikal National Park", "~US$55 each with transport and guide; entries extra. Times per operator.", D28),
    ("2026-12-28", "04:30", "06:00", "Option 2: 🚐 Early shuttle Flores → Tikal",
     "Tikal National Park", "Ticket bought online in advance.", D28),
    ("2026-12-28", "06:00", "12:30", "Option 2: 🏛 Tikal (gate opens 06:00)",
     "Tikal National Park", "Hire a guide at the gate.", D28),
    ("2026-12-28", "12:30", "14:00", "Option 2: 🚐 Shuttle Tikal → Flores", "Flores, Petén", "", D28),
    ("2026-12-28", "14:00", "17:30", "Option 2: 🏊 Free: swim in Lake Petén Itzá",
     "Flores, Petén", "Or a lancha ride round the island.", D28),
    ("2026-12-28", "19:30", "21:30", "🍽 Dinner in Flores, early night", "Flores, Petén",
     "Shuttle to Río Dulce at 06:00.", D28),
    # Tue 29
    ("2026-12-29", "06:00", "10:00", "🚐 Shuttle Flores → Río Dulce (~4 h)",
     "Río Dulce, Izabal", "US$23–36 each. Drop-off at Colifato, Mirador del Río mall.", D29),
    ("2026-12-29", "10:00", "10:30", "⛵ Boat or tuk-tuk to the lodge", "Río Dulce, Izabal", "", D29),
    ("2026-12-29", "10:30", "12:00", "🛏 Check in, lunch", "Río Dulce, Izabal", "", D29),
    ("2026-12-29", "12:00", "12:30", "🎫 Buy tomorrow's Litegua ticket in town",
     "Río Dulce, Izabal", "Confirm the departure time (~09:30).", D29),
    ("2026-12-29", "12:30", "13:30", "🚐 Colectivo towards El Estor, to Finca El Paraíso",
     "Finca El Paraíso, El Estor road", "From below the bridge, ~Q15 each.", D29),
    ("2026-12-29", "13:30", "15:45", "🏊 Finca El Paraíso hot waterfall",
     "Finca El Paraíso, El Estor road", "Q15–Q20, cash. Closes 17:00.", D29),
    ("2026-12-29", "15:45", "16:45", "🚐 Colectivo back to Río Dulce",
     "Río Dulce, Izabal", "Last one passes ~16:30–17:00. Don't cut it fine.", D29),
    ("2026-12-29", "17:00", "21:00", "🛌 Free: evening at the river lodge",
     "Río Dulce, Izabal", "Swim from the dock, dinner on the river.", D29),
    # Wed 30
    ("2026-12-30", "07:30", "09:00", "Option 1: 🏊 Free: morning swim from the dock",
     "Río Dulce, Izabal", "", D30),
    ("2026-12-30", "08:00", "09:00", "Option 2: 🏰 Free: Castillo de San Felipe",
     "Castillo de San Felipe de Lara, Río Dulce", "Opens 08:00. Tuk-tuk, 3 km.", D30),
    ("2026-12-30", "09:00", "09:30", "⛵ To the Litegua stop in town", "Río Dulce, Izabal", "", D30),
    ("2026-12-30", "09:30", "15:30", "🚌 Litegua pullman Río Dulce → Guatemala City (~6 h)",
     "Guatemala City", "Q120–Q145 each. Fuente del Norte if Litegua is full.", D30),
    ("2026-12-30", "15:30", "16:15", "Option 1: 🚕 Uber to the Hilton Garden Inn (Zona 9)",
     "Hilton Garden Inn, Zona 9, Guatemala City", "≈ Q60.", D30),
    ("2026-12-30", "16:15", "22:30", "Option 1: 🛏 Day room and dinner, Hilton Garden Inn",
     "Hilton Garden Inn, Zona 9, Guatemala City", "Bookable by the hour on HotelsByDay.", D30),
    ("2026-12-30", "22:30", "23:00", "Option 1: 🚕 Uber to the airport",
     "La Aurora International Airport", "≈ Q40–Q80.", D30),
    ("2026-12-30", "15:30", "16:30", "Option 2: 🚕 Uber to an airport guesthouse (Zona 13)",
     "Zona 13, Guatemala City", "E.g. L'Aurora Inn or Casa Aurora.", D30),
    ("2026-12-30", "16:30", "23:00", "Option 2: 🛏 Rest and dinner at the guesthouse",
     "Zona 13, Guatemala City", "Free airport shuttle at ~23:00 (L'Aurora Inn).", D30),
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
