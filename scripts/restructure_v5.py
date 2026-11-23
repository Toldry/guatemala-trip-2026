"""Restructure the v5 guide into nested parts and add new content.

Input: the flat v5 guide (sections "## N. Title").
Output: Part 1 Plan / Part 2 Day by day / Part 3 Practical / Part 4 Credits,
with crowd & traffic notes, new maps, health & safety and tips sections.
"""
import re
import sys
import unicodedata

path = sys.argv[1]
source = open(path).read()

MAP = '![{alt}]({{{{ "/maps/{file}" | relative_url }}}})'


def map_img(file, alt):
    return MAP.format(alt=alt, file=file)


# ---------------------------------------------------------------- split
header, _, rest = source.partition("\n---\n\n## 1. ")
rest = "## 1. " + rest
sections = {}
for block in re.split(r"\n(?=## \d+\. )", rest):
    match = re.match(r"## (\d+)\. ([^\n]+)\n", block)
    number = int(match.group(1))
    body = block[match.end():].strip()
    body = re.sub(r"\n---\s*$", "", body).strip()
    sections[number] = (match.group(2), body)


def demote(text, levels=1):
    return re.sub(r"^(#{2,5}) ", lambda m: "#" * (len(m.group(1)) + levels)
                  + " ", text, flags=re.M)


def insert_after(text, marker, addition):
    index = text.find(marker)
    assert index >= 0, f"marker not found: {marker[:60]}"
    end = text.find("\n\n", index)
    end = len(text) if end < 0 else end
    return text[:end] + "\n\n" + addition + text[end:]


def replace_once(text, old, new):
    assert old in text, f"not found: {old[:60]}"
    return text.replace(old, new, 1)


def crowd_box(lines):
    items = "\n".join(f"> - {line}" for line in lines)
    return "> **👥 Crowds & 🚗 traffic here**\n>\n" + items


# ------------------------------------------------------- Part 2 regions
# 4. Antigua & Acatenango
title4, body4 = sections[4]
body4 = demote(body4)
body4 = insert_after(body4, "**What it is.**", crowd_box([
    "👥 **Antigua centre** gets busy on weekends and in holiday weeks, "
    "with day-trippers from Guatemala City, though its cobbled streets have "
    "little through-traffic. Go early in the morning for quiet streets and "
    "photos at the Arco.",
    "👥 **Acatenango base camps:** in peak season, hundreds of hikers "
    "from dozens of operators camp on the same ridge. The summit is busy at "
    "sunrise; the views make up for it.",
    "🚗 **Airport ↔ Antigua road** via Guatemala City: heavy traffic at rush "
    "hours. At 22:30 on the 13th it will be quieter.",
]) + "\n\n" + map_img("map-04-antigua.png",
                      "Map of Antigua, the volcanoes and the airport"))
body4 = replace_once(
    body4,
    "Immigration and bags take 30–60 minutes, so expect to leave the airport "
    "around 22:30. **Don't drive at night**, especially on your first "
    "evening. Pre-book a transfer:",
    "Immigration and bags take 30–60 minutes, so expect to leave the airport "
    "around 22:30.\n\n"
    "##### Why not pick up the car tonight?\n"
    "- **Unlit roads:** highways outside the cities are mostly unlit, with "
    "unmarked speed bumps, unlit vehicles and road works that are hard to see "
    "in the dark. US government staff are told to avoid driving outside "
    "Guatemala City at night.\n"
    "- **An unfamiliar late-night route:** after a long flight you'd have to "
    "cross Guatemala City and take the twisty mountain road down to Antigua "
    "in a car you don't know.\n"
    "- **Slow pickup:** airport rental cars are collected from a separate "
    "parking building across from the terminal, which is slow late at "
    "night.\n"
    "- **You don't need it yet:** Antigua is walkable, and the Acatenango tours "
    "include transport, so a car would sit in paid parking until the 17th. "
    "Picking up on the 17th saves 4 rental days.\n\n"
    "If you'd rather have the car from day one, sleep near the airport on the "
    "13th and collect it on the morning of the 14th.\n\n"
    "##### Getting from the airport to Antigua\n"
    "Pre-book a transfer:")
body4 = replace_once(body4, "**Operators** (all depart",
                     "##### Acatenango operators\nAll depart")
body4 = body4.replace("Antigua with transport, gear, meals and park fees; book now, because December is peak season):",
                      "Antigua with transport, gear, meals and park fees. Book now, because December is peak season.")

# 5. Lake Atitlán
title5, body5 = sections[5]
body5 = demote(body5)
body5 = insert_after(body5, "**What it is.**", crowd_box([
    "👥🚗 **Panajachel** is the lake's busy hub: tuk-tuks, buses, a long "
    "souvenir street and weekend crowds from the capital. You only pass "
    "near it.",
    "👥 **San Pedro La Laguna** is the backpacker party village, loud at "
    "night and especially at weekends. San Juan next door is much calmer, "
    "which is why it's your base.",
    "👥 **Indian Nose** has a small crowd of a few dozen people at sunrise. "
    "**Cerro Tzankujil** is busiest on weekend afternoons; Friday the 18th "
    "should be fine.",
    "🚗 Villages are linked by **narrow, steep roads with tuk-tuks**. "
    "Around the lake, the boats are the pleasant way to get about.",
]))

# 6. Chichicastenango
title6, body6 = sections[6]
body6 = demote(body6)
body6 = insert_after(body6, "**What it is.**", crowd_box([
    "👥👥 **This is the most crowded stop on the trip, on purpose.** Sunday "
    "market day plus festival week means packed alleys, tour buses from "
    "Antigua and Panajachel (they arrive around 10:00–14:00), firecrackers "
    "and pickpockets. I'd count it as one of your \"special occasion\" "
    "exceptions. If you'd rather skip it, drive straight from Atitlán to Xela "
    "(about 2.5 h) and have a slower morning by the lake.",
    "🚗 Parking is scarce on market days. Use a guarded *parqueo* on the "
    "edge of town and walk in.",
]))
body6 = body6.replace("#### Is the Santo Tomás", "#### Is the Santo Tomás")

# 7. Xela & Tajumulco
title7, body7 = sections[7]
body7 = demote(body7)
body7 = replace_once(
    body7, map_img("map-02-highlands.png", "Map of the highlands section"),
    map_img("map-02-highlands.png", "Map of the highlands section")
    + "\n\n" + map_img("map-05-xela.png",
                       "Map of the area around Xela, with San Marcos "
                       "Department hatched"))
body7 = insert_after(body7, "**What it is.**", crowd_box([
    "🚗 **Xela is a real city:** traffic, asphalt and exhaust in the centre and "
    "on the ring roads. The historic centre around Parque Centro América is "
    "pleasant on foot.",
    "🚗 **Cuatro Caminos** (the junction you pass on 20 and 24 Dec) is a "
    "busy truck-and-bus crossroads.",
    "👥 **Fuentes Georginas** gets local family crowds at weekends and "
    "holidays. Monday the 21st should be calmer; arrive after lunch, once the "
    "morning tours have gone.",
    "👥 **Tajumulco** is far less crowded than Acatenango: a few groups at "
    "camp, no huts.",
]))
body7 = replace_once(
    body7, "> ⚠️ **Access check.**",
    "> 🛑 **Read before booking Tajumulco: official travel advice.** Tajumulco "
    "lies in **San Marcos Department**. Since March 2026 the **US State "
    "Department has rated San Marcos \"Level 4: Do Not Travel\"** because of "
    "cartel and gang crime, and its staff may not go there at all. The **UK "
    "FCDO** advises against travel only within 5 km of the Mexican border, a "
    "strip Tajumulco is outside of. **Check your own government's advice and "
    "your travel insurance** (some policies don't cover areas under a "
    "do-not-travel warning) before choosing. **Plan B, Volcán Santa María "
    "(3,772 m), is in Quetzaltenango Department, right above Xela, and has no "
    "such warning.** It's a hard 1,500 m climb, best done as a pre-dawn hike for "
    "sunrise, looking down on the erupting Santiaguito dome. Quetzaltrekkers "
    "and Adrenalina both run it.\n\n"
    "> ⚠️ **Access check.**")

# 8. Cobán, Lanquín & Semuc
title8, body8 = sections[8]
body8 = demote(body8)
body8 = insert_after(body8, "**What it is.**", crowd_box([
    "👥 **Semuc Champey** is very busy from about 10:30 to 15:00, when "
    "hostel tours arrive, and Christmas week brings domestic tourists too. "
    "Be at the gate at opening and swim before the crowds, or come back for "
    "the last two hours.",
    "👥 **K'anba cave** tours leave every half hour in groups. Take the first "
    "one of the day.",
    "🚗 **Cobán** is a busy town with narrow, congested streets. The "
    "**Cobán–Lanquín road** is winding with lots of pickups, but traffic is "
    "light.",
]))
body8 = replace_once(body8, "**Where to stay (2 nights, 25–26 Dec):**",
                     "#### Where to stay in Lanquín (25–26 Dec)\n")
body8 = replace_once(
    body8,
    map_img("map-03-north.png", "Map of the north and east section"),
    map_img("map-03-north.png", "Map of the north and east section"))

# 9. Tikal & Yaxhá
title9, body9 = sections[9]
body9 = demote(body9)
body9 = insert_after(body9, "**What it is.**", crowd_box([
    "👥 **Tikal's Gran Plaza and Temple IV** fill up with tour groups from "
    "about 09:30 to 14:00, more so in the Christmas–New Year week. Arriving at "
    "06:00 gives you 2–3 calm hours. The outer groups (Mundo Perdido, "
    "Temple VI) stay quiet all day.",
    "👥 **Yaxhá** is quiet except at sunset on Temple 216, where 30–80 "
    "people gather. It's still nothing like Tikal.",
    "🚗 **Flores / Santa Elena:** tuk-tuks, traffic and a busy causeway. "
    "Your base, El Remate, is a quiet village.",
]) + "\n\n" + map_img("map-06-peten.png",
                      "Map of Tikal, Yaxhá and Lake Petén Itzá"))
body9 = body9.replace("### Mon 28 Dec", "#### Mon 28 Dec")

# 10. Río Dulce
title10, body10 = sections[10]
body10 = demote(body10)
body10 = (map_img("map-07-izabal.png", "Map of Río Dulce and Lake Izabal")
          + "\n\n" + crowd_box([
              "🚗 **Río Dulce town** sits on the main Petén highway. Trucks "
              "grind over the big bridge day and night, and the strip under "
              "it is noisy and congested. **Stay at a lodge on the river away "
              "from the bridge** (all of those listed are), not in town.",
              "👥 **Finca El Paraíso** is a favourite local day out, so it "
              "gets crowded at weekends and holidays. The 29th is a Tuesday "
              "but falls in holiday week, so go mid-afternoon after the lunch "
              "crowd.",
              "🚗 **30 Dec, CA-9 into Guatemala City:** heavy truck traffic "
              "and the capital's afternoon jams, which is why you should "
              "leave by 10:00.",
          ]) + "\n\n" + body10)
body10 = replace_once(body10, "**Where to stay** (on Booking.com, checked Nov 2026):",
                      "#### Where to stay in Río Dulce (29 Dec)\nPrices and ratings from Booking.com, checked Nov 2026:")

# --------------------------------------------------------- Part 3 text
TIPS = """### 3.1 Getting by in Guatemala

#### Money
- **The currency is the quetzal (Q).** At the time of writing, €1 ≈ Q8.43. Carry **small notes** (Q5–Q50). Tuk-tuks, boats, market stalls and park gates often can't change a Q200 note.
- **Cash is essential:** San Juan and Santa Clara have no ATMs, Tikal has none, and many park gates and lanchas take cash only. Draw money in Antigua, Panajachel, Xela, Cobán and Flores.
- **Use ATMs inside banks or shopping centres** during opening hours, not stand-alone street machines, where card skimming is more common.
- **Tipping:** about 10 % in sit-down restaurants (check whether *propina* is already on the bill). For hiking guides, Q50–Q100 (€5.9–€12) per person per day is usual. Round up for drivers.

#### Language & people
- Your Spanish will make a huge difference. Use *usted* with older people and officials. In the highlands, many people speak Spanish as a second language after a Mayan language, so speak clearly and simply.
- Greet people when you walk into a shop or a room (*buenos días* / *buenas tardes*). It matters here.
- **Ask before photographing people**, especially women, children and ceremonies, and never photograph inside the Santo Tomás church in Chichicastenango. Some people will ask for a small payment for a photo, which is fair.
- **Bargaining:** it's normal in markets (Chichi, Antigua's handicraft market), but keep it friendly. Don't haggle in shops with fixed prices, or over a few quetzales with a weaver.

#### Food & water
- **Don't drink tap water**, and don't use it to brush your teeth. Most hotels and hostels have big refill jugs, so bring a refillable bottle.
- Street food is fine if it's **hot, cooked in front of you and busy**. Be careful with raw salads and unpeeled fruit, and with ice outside tourist restaurants.
- Try *pepián* (a spiced meat stew), *kak'ik* (Q'eqchi' turkey soup, a Cobán speciality), *tamales* (especially on Christmas Eve), *chuchitos*, *rellenitos* (sweet plantain), and *atol* (a hot corn drink).

#### Everyday practicalities
- **Toilet paper goes in the bin, not the toilet**, almost everywhere. Carry your own paper and hand gel; public toilets often charge Q1–Q3 (€0.1–€0.4).
- Get a local **SIM or eSIM** (Tigo and Claro are the two networks) and use **WhatsApp**, which is how hotels, guides and tour operators communicate.
- Download **offline maps** (Google Maps or Maps.me) and **Waze**. Mobile signal disappears on parts of the Lanquín and Sayaxché roads.
- Electricity is 120 V with US-style plugs (types A/B), so European travellers need adapters.

### 3.2 What to avoid
- **Driving at night:** see [§3.5](#35-driving).
- **Zone 18 of Guatemala City, the city of Villa Nueva and Zone 3** are high-crime areas. Your route never goes there.
- **Chicken buses and street-hailed white taxis.** They're colourful, but US government staff are banned from using both because of crime and accidents. Use Uber in Guatemala City and Antigua, taxis your hotel calls for you, and tuk-tuks in towns.
- **Walking between Lake Atitlán villages on lakeside trails** without a guide: these isolated paths have a history of robberies. Take the boats.
- **Showing off valuables:** keep your phone away on busy streets, leave jewellery at home, and carry a day's cash in a front pocket.
- **Illegal drugs:** the penalties are harsh, and the trade behind them is violent.
- **Hikes on Volcán de Agua or Pacaya without a reputable guide:** armed robberies of hikers have been reported there.
- **Getting into political protests or road blockades** (*bloqueos*). If you meet one, turn round and wait it out.
- **Feeding or touching dogs:** rabies is present, and post-exposure vaccine is only available in larger city hospitals.

### 3.3 Health

> I'm not a doctor. **Book a travel-clinic appointment now.** Your trip is 3 weeks away, and some vaccines need time to take effect. The clinic can also prescribe the medicines marked ℞ below.

#### Vaccines
- **Recommended for most travellers (CDC):** hepatitis A and typhoid, plus routine vaccines (MMR, tetanus–diphtheria–pertussis, polio). Travel clinics also often suggest hepatitis B.
- **Rabies:** consider it, since you'll be in rural areas and around dogs. In Guatemala, treatment after a bite is only available in larger city hospitals.
- **No vaccine is required for entry** if you're coming directly from Europe or the US.

#### Mosquitoes: dengue, malaria
- **Dengue:** Guatemala had record dengue numbers in 2024. The mosquitoes bite **by day**, mostly in the lowlands and towns: Lanquín, Semuc, Petén, Río Dulce. Use DEET or picaridin repellent and wear long sleeves at dusk in the lowlands.
- **Malaria:** CDC says there's no risk in Antigua, Guatemala City or around Lake Atitlán, and only low risk in rural lowlands such as Petén. For your route, CDC advises **bite prevention rather than pills**. Confirm this with your clinic.

#### Altitude
- You'll sleep at **~3,600 m (Acatenango) and ~4,000 m (Tajumulco or Santa María)**. The route climbs gradually (see the [altitude chart](#11-the-trip-at-a-glance)), but headaches and poor sleep at camp are common.
- **Warning signs:** a headache that painkillers don't fix, vomiting, confusion, or breathlessness at rest. Tell your guide and **go down**; descending is the treatment.
- ℞ **Acetazolamide** can help prevent altitude sickness. Ask your doctor whether it suits you.

#### Suggested medicine kit (for two people)
| Item | Why |
|---|---|
| Your regular prescriptions, plus copies of the prescriptions | Pharmacies may not carry the same brands |
| Painkillers (paracetamol / ibuprofen) | Altitude headaches, sore legs |
| Oral rehydration salts | Traveller's diarrhoea, hot days in Petén |
| Loperamide | For long drive days only (don't use it if you have a fever or blood in the stool) |
| ℞ A standby antibiotic for traveller's diarrhoea | Your doctor decides which one |
| ℞ Acetazolamide | Altitude, see above |
| Motion-sickness tablets | The Lanquín and Atitlán roads are very winding |
| Antihistamine tablets + hydrocortisone cream | Bites, allergies |
| DEET/picaridin repellent, SPF 50 sunscreen, lip balm with SPF | The sun is fierce at altitude; mosquitoes in the lowlands |
| Blister plasters, tape, antiseptic, small bandages | Volcano descents are hard on feet |
| Water-filter bottle or purification tablets | Backup for refills |
| Thermometer | Dengue and other fevers: see a doctor if you get a high fever |

**Pharmacies** (*farmacias*: Farmacias Galeno, Cruz Verde, Batres) are everywhere in towns, and many medicines are sold without a prescription. Bring your own anyway, because quality and brands vary.

**Hospitals:** the best private hospitals are in Guatemala City (e.g. Hospital Herrera Llerandi, Centro Médico) and Antigua (Hospital Privado Hermano Pedro). **Get travel insurance that covers medical evacuation and volcano hiking.**

### 3.4 Safety & where to be careful at night

Guatemala has high violent-crime rates overall, but most of it is gang-related and concentrated in parts of Guatemala City and some border areas. The tourist route is generally safe **by day**. At night, it depends on the place:

| Place | After dark | Notes |
|---|---|---|
| **Antigua** centre | 🟢 Early evening is fine on busy, lit streets | Police say most muggings happen **22:00–03:00**. After 22:00, take a tuk-tuk or Uber, even for short trips. Tourist police patrol Cerro de la Cruz by day only. |
| **Guatemala City** Zones 10, 13 (airport) | 🟡 Inside venues or cars only | Don't walk around at night. **Avoid Zone 18, Zone 3 and Villa Nueva entirely.** |
| **Lake Atitlán** villages | 🟢 San Juan / centre of San Pedro, early evening | 🔴 **No walking on trails between villages, especially after dark.** Unlit lanes, few people. The last lanchas run at about 17:00–18:00. |
| **Indian Nose** (pre-dawn) | 🟡 Go with a community guide or tour | Robberies on the trail have been reported in the past. Guided groups are the norm now. |
| **Chichicastenango** | – | Daytime only on your plan. Watch for pickpockets in the market crowds. |
| **Xela** centre | 🟢 Around Parque Centro América, early evening | Take a taxi after about 21:00. |
| **Lanquín / Semuc** | 🟡 Stay at your lodge | Dark, unlit roads; nothing to walk to. |
| **El Remate / Flores** | 🟢 Flores island is lively and fine in the evening | El Remate is very quiet. Use a torch. |
| **Tikal / Yaxhá** | 🟡 With a guide only | Attacks on visitors in the Petén parks have been reported in the past, including on sunrise tours. Sunrise and sunset entry requires a guide anyway. |
| **Río Dulce** | 🟡 Stay at your lodge | The town strip under the bridge isn't somewhere to wander at night. |
| **Any road outside towns** | 🔴 Don't drive | See [§3.5](#35-driving). |

#### Emergency numbers
- **Tourist assistance (ASISTUR / tourist police):** call **1500** or +502 2290 2810, or WhatsApp **+502 5188 1819**. Answered in Spanish and English, 24/7.
- **General emergencies:** 911 · **Volcano alerts:** [INSIVUMEH](https://insivumeh.gob.gt) · **Official travel advice:** [US State Dept](https://travel.state.gov/en/international-travel/travel-advisories/guatemala.html) · [UK FCDO](https://www.gov.uk/foreign-travel-advice/guatemala)
- Register your trip with your own embassy (most countries have an online system).

"""

DRIVING_EXTRA = """- **Check for road blockades** (*bloqueos*) the evening before each long drive, by asking your hotel or searching "bloqueos" with the route name. The UK FCDO has noted a state of emergency in **Nahualá and Santa Catarina Ixtahuacán (Sololá)**, a long-running land dispute next to the **CA-1 highway you use on 17, 20 and 24 Dec**. Ask locally whether that stretch is calm.
- **Night driving:** unlit roads, unmarked speed bumps, unlit vehicles and the risk of crime are why every drive in this guide ends by about 17:00. Sunset is around 17:30.
"""

# --------------------------------------------------------- assemble
title1, body1 = sections[1]
title2, body2 = sections[2]
title3, body3 = sections[3]
title11, body11 = sections[11]
title12, body12 = sections[12]
title13, body13 = sections[13]
title14, body14 = sections[14]

body1 = body1.replace(
    "\n| Date | Where you sleep |",
    "\n" + map_img("chart-08-altitude.png", "Altitude day by day") +
    "\n\n| Date | Where you sleep |", 1)
body2 = replace_once(
    body2, "- **The timeline chart renders again**",
    "- **New Part 3, \"Practical\":** getting by, what to avoid, health "
    "(vaccines, medicine kit, altitude) and where it's safe to walk at night.\n"
    "- **👥 Crowds & 🚗 traffic boxes** in every chapter, so you can avoid "
    "the busy spots.\n"
    "- **Five new graphics:** close-up maps of Antigua, Xela, Petén and Río "
    "Dulce, plus an altitude chart.\n"
    "- **Tajumulco advisory:** the US rates San Marcos Department "
    "(where Tajumulco is) \"Do Not Travel\". Santa María is now set out as Plan B.\n"
    "- **Nested sections**, for easier navigation.\n"
    "- **The timeline chart renders again**")

body13 = body13.replace("- **Never drive after dark.** Every drive day above is "
                        "timed to finish in daylight; sunset is around 17:30.\n",
                        DRIVING_EXTRA)

parts = [
    "## Part 1 · Plan",
    "### 1.1 The trip at a glance\n\n" + demote(body1, 2),
    "### 1.2 What changed in this version\n\n" + demote(body2, 2),
    "### 1.3 Guatemala in brief\n\n" + demote(body3, 2),
    "### 1.4 Booking checklist\n\n" + demote(body12, 2),
    "---\n\n## Part 2 · Day by day",
    "### 2.1 " + title4 + "\n\n" + body4,
    "### 2.2 " + title5 + "\n\n" + body5,
    "### 2.3 " + title6 + "\n\n" + body6,
    "### 2.4 " + title7 + "\n\n" + body7,
    "### 2.5 " + title8 + "\n\n" + body8,
    "### 2.6 " + title9 + "\n\n" + body9,
    "### 2.7 " + title10 + "\n\n" + body10,
    "---\n\n## Part 3 · Practical",
    TIPS.strip(),
    "### 3.5 Driving\n\n" + demote(body13, 2),
    "### 3.6 Swimming spots on the route\n\n" + demote(body11, 2),
    "---\n\n## Part 4 · Credits",
    "### 4.1 Photo & data credits\n\n" + demote(body14, 2),
]
document = "\n\n".join(parts)

# day headings inside regions were "###" in v4 -> now "####"; fix any that
# arrived at the wrong level after demotion (they started as "### ").
document = re.sub(r"^##### (Sun|Mon|Tue|Wed|Thu|Fri|Sat) ", r"#### \1 ",
                  document, flags=re.M)


# --------------------------------------------------------- anchors & TOC
def gfm_slug(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # drop links
    text = re.sub(r"[*_`]", "", text)
    text = text.strip().lower()
    text = "".join(ch for ch in text
                   if ch in " -" or unicodedata.category(ch)[0] in "LN"
                   or ch == "_")
    return text.replace(" ", "-")


toc_lines = ["**Contents**", ""]
for match in re.finditer(r"^(##|###) (.+)$", document, flags=re.M):
    level, title = match.groups()
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title)
    if level == "##":
        toc_lines.append(f"- **[{plain}](#{gfm_slug(title)})**")
    else:
        toc_lines.append(f"  - [{plain}](#{gfm_slug(title)})")

anchors = {re.match(r"(\d\.\d)", m.group(1)).group(1): gfm_slug(m.group(1))
           for m in re.finditer(r"^### (\d\.\d .+)$", document, flags=re.M)}
old_to_new = {"1": "1.1", "2": "1.2", "3": "1.3", "4": "2.1", "5": "2.2",
              "6": "2.3", "7": "2.4", "8": "2.5", "9": "2.6", "10": "2.7",
              "11": "3.6", "12": "1.4", "13": "3.5", "14": "4.1"}
document = re.sub(
    r"\[§(\d+)\]\(#[^)]+\)",
    lambda m: f"[§{old_to_new[m.group(1)]}](#{anchors[old_to_new[m.group(1)]]})",
    document)
document = re.sub(r"\[§(\d\.\d)\]\(#[^)]+\)",
                  lambda m: f"[§{m.group(1)}](#{anchors[m.group(1)]})",
                  document)
document = document.replace("(#11-the-trip-at-a-glance)",
                            f"(#{anchors['1.1']})")

header = re.sub(r"\*\*Contents\*\*\n(?:\d+\. .+\n)+", "\n".join(toc_lines)
                + "\n", header)
open(path, "w").write(header.rstrip() + "\n\n---\n\n" + document + "\n")
print("anchors:", anchors)
