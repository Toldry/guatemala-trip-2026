"""Add named links to the v5 guide."""
import re
import sys
from urllib.parse import quote_plus

path = sys.argv[1]
text = open(path).read()


def maps(query):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)


def wiki(title):
    return "https://en.wikipedia.org/wiki/" + title


def sub_once(old, new, count=1):
    """Replace the first occurrence; whitespace in `old` matches any whitespace."""
    global text
    pattern = re.compile(r"\s+".join(re.escape(part) for part in old.split()))
    match = pattern.search(text)
    assert match, f"not found: {old[:70]}"
    text = text[:match.start()] + new + text[match.end():]


# ---- 1. bare URLs -> named links -----------------------------------------
named = {
    "https://www.viator.com/tours/Guatemala-City/Shared-Arrival-Transfer-Guatemala-City-Airport-to-Antigua/d4595-3022ANTAPTHTL":
        "Gray Line on Viator",
    "https://www.civitatis.com/en/guatemala-city/transfers": "Civitatis",
    "https://www.viator.com/en-AU/tours/Guatemala-City/Private-Trasport-Guatemala-City-Airport-to-Antigua/d4595-140323P9":
        "Viator private transfer",
    "https://insivumeh.gob.gt": "INSIVUMEH (national volcano institute)",
    "https://www.oxexpeditions.com": "oxexpeditions.com",
    "https://www.thoroughlytravel.com/acatenango-volcano-tour-companies/":
        "Thoroughly Travel: 12 Acatenango operators compared",
    "https://turisteando.wetravel.com/trips/rostro-maya-indian-nose-hike-san-juan-la-laguna-turisteando-7327314571":
        "book",
    "https://www.quetzaltrekkers.com/xela/tajumulco/": "Quetzaltrekkers: Tajumulco",
    "https://www.wetravel.com/trips/tajumulco-the-highest-volcano-all-over-central-america-from-xela-adrenalina-tours-59714273":
        "Adrenalina on WeTravel",
    "https://www.expedia.com/things-to-do/from-lanquin-semuc-champey-park-and-kanba-cave-guided-tour.a4569960.activity-details":
        "Marvelus on Expedia",
    "https://boletos.culturaguate.gob.gt/en/": "Ministry of Culture ticket portal",
    "https://www.wetravel.com/trips/yaxha-sunset-tour-from-flores-turisteando-40775668": "book",
    "https://www.booking.com/pool/city/gt/rio-dulce.html": "Booking.com: Río Dulce hotels",
    "https://www.nationalcar.com/en/car-rental-locations/gt/antigua-k606.html": "National, Antigua office",
    "https://www.alamo.com/en/car-rental-locations/gt/antigua-k607.html": "Alamo, Antigua office",
    "https://www.enterprise.com/en/car-rental-locations/gt/antigua-k60p.html": "Enterprise, Antigua office",
    "https://www.booking.com": "Booking.com",
    "https://www.hostelworld.com": "Hostelworld",
    "https://www.airbnb.com": "Airbnb",
    "https://www.naturalearthdata.com": "naturalearthdata.com",
}
# longest first so prefixes (booking.com) don't clobber longer URLs
for url in sorted(named, key=len, reverse=True):
    label = named[url]
    pattern = re.compile(r"(?<!\]\()(?<![\[<])" + re.escape(url) + r"(?![\w/.-])")
    text = pattern.sub(f"[{label}]({url})", text)

# Commons credit URLs -> "file page" links
text = re.sub(
    r"(?<!\]\()(?<!\[)(https://commons\.wikimedia\.org/wiki/File:[^\s·)]+)",
    r"[file page](\1)", text)

# cleanups around the converted URLs
sub_once("(Civitatis); other listings", "; other listings")
sub_once("| [Civitatis](https://www.civitatis.com/en/guatemala-city/transfers) · ",
         "| [Civitatis](https://www.civitatis.com/en/guatemala-city/transfers) · ")
sub_once('| https://www.viator.com (search "Acatenango") |',
         "| [Viator: Acatenango tours](https://www.viator.com/searchResults/all?text=Acatenango) |")
sub_once("Side-by-side comparison of 12 operators: [Thoroughly Travel: 12 Acatenango operators compared]",
         "Side-by-side comparison: [Thoroughly Travel: 12 Acatenango operators compared]")
sub_once("from San Juan ([book](", "from San Juan ([book on WeTravel](")
sub_once("Turisteando, Q222 (€26; listed as US$29) ([book](",
         "Turisteando, Q222 (€26; listed as US$29) ([book on WeTravel](")
sub_once("· www.adrenalinatours.com", "· [adrenalinatours.com](https://www.adrenalinatours.com)")
sub_once("Search page: [Booking.com", "Search all: [Booking.com")

# ---- 2. operators, lodges and tours without links --------------------------
CENTRAL_AMERICA = "https://centralamerica.com/experiencing/travel/choosing-the-best-acatenango-volcano-hike"
THOROUGH = "https://www.thoroughlytravel.com/acatenango-volcano-tour-companies/"
sub_once("| via Viator or the comparison below |",
         f"| [Viator](https://www.viator.com/searchResults/all?text=Wicho%20Charlie%20Acatenango) · [comparison]({THOROUGH}) |")
sub_once("recommended by centralamerica.com | via the comparison below |",
         f"recommended by [centralamerica.com]({CENTRAL_AMERICA}) | [comparison]({THOROUGH}) · [map]({maps('Soy Tours Antigua Guatemala')}) |")
sub_once("**Tours With Vick**, Q344 (€41; listed as US$45), rated 9.6/10 \"Exceptional\" on Travelocity.",
         "**Tours With Vick**, Q344 (€41; listed as US$45), rated 9.6/10 \"Exceptional\" on Travelocity "
         "([book](https://www.travelocity.com/things-to-do/sunrise-hike-tour-on-indians-nose-mountain.a44904460.activity-details)).")
sub_once("Another Xela operator (Monte Verde Tours)",
         "Another Xela operator ([Monte Verde Tours](https://monteverdetours.rezdy.com/catalog/388612/all-hikes))")
sub_once("| **Greengos** (hostel by the park entrance) |",
         f"| **[Greengos]({maps('Greengos Hostel Semuc Champey')})** (hostel by the park entrance) |")
sub_once("| via the hostel |", f"| [Booking.com](https://www.booking.com/searchresults.html?ss=Greengos+Semuc+Champey) |")
sub_once("| **El Retiro** (lodge on the river) |",
         f"| **[El Retiro]({maps('El Retiro Lodge Lanquin')})** (lodge on the river) |")
sub_once("| via the lodge |", "| [Booking.com](https://www.booking.com/searchresults.html?ss=El+Retiro+Lanquin) |")
sub_once("Pre-booked options include Mayan World Travel's sunrise tour from Flores",
         "Pre-booked options include [Mayan World Travel's sunrise tour from Flores]"
         "(https://www.travelocity.com/things-to-do/tikal-sunrise-from-flores-more-archaeological-tour.a48111107.activity-details)")
sub_once("and Tikal Express's sunrise tour;",
         "and [Tikal Express's sunrise tour](https://www.expedia.co.uk/things-to-do/tikal-privade-tour-all-included.a51730204.activity-details);")
sub_once("Tour options from Flores: Adrenalina Tours sunset tour,",
         "Tour options from Flores: [Adrenalina Tours](https://www.adrenalinatours.com) sunset tour,")
sub_once("Mayan World Travel shared sunset tour,",
         "[Mayan World Travel shared sunset tour](https://www.travelocity.com/things-to-do/flores-yaxha-shared-sunset-tour-with-transportation-guide.a47982324.activity-details),")
sub_once("**Ecolodge El Sombrero** sits", "**[Ecolodge El Sombrero](https://www.travelocity.com/Flores-Hotels-El-Sombrero-Ecolodge.h132844709.Hotel-Information)** "
         f"([map]({maps('Ecolodge El Sombrero Yaxha')})) sits")
sub_once("Find it on Expedia, Travelocity or Booking.com.",
         "Find it on [Travelocity](https://www.travelocity.com/Flores-Hotels-El-Sombrero-Ecolodge.h132844709.Hotel-Information), "
         "[Expedia](https://www.expedia.com/Laguna-Yaxha-Hotels.d3000007574.Travel-Guide-Hotels) or "
         "[Booking.com](https://www.booking.com/searchresults.html?ss=Ecolodge+El+Sombrero+Yaxha).")
for name, query in (("Boatique Hotel & Marina", "Boatique Hotel Marina Rio Dulce"),
                    ("Nanajuana Río Dulce", "Nanajuana Rio Dulce"),
                    ("Hacienda Tijax Jungle Lodge", "Hacienda Tijax Rio Dulce")):
    sub_once(f"| **{name}** |",
             f"| **[{name}](https://www.booking.com/searchresults.html?ss={quote_plus(query)})** |")
sub_once("| **Casa Perico** |", "| **[Casa Perico](https://www.booking.com/hotel/gt/casa-perico.html)** |")
sub_once("| Uber |", "| [Uber](https://www.uber.com/gt/en/) |")

# ---- 3. places: Wikipedia + map links ------------------------------------
place_links = [
    ("**What it is.** Antigua was", f"**What it is.** [Antigua]({wiki('Antigua_Guatemala')}) was"),
    ("climb **Cerro de la Cruz**", f"climb **[Cerro de la Cruz]({maps('Cerro de la Cruz Antigua Guatemala')})**"),
    ("Walk the Arco de Santa Catalina, La Merced,",
     f"Walk the [Arco de Santa Catalina]({wiki('Arco_de_Santa_Catalina')}), [La Merced]({maps('Iglesia de La Merced Antigua Guatemala')}),"),
    ("directly facing\n**Fuego**", f"directly facing\n**[Fuego]({wiki('Volcán_de_Fuego')})**"),
    ("Before dawn you summit Acatenango (3,976 m)",
     f"Before dawn you summit [Acatenango]({wiki('Acatenango')}) (3,976 m)"),
    ("down to\n**San Juan La Laguna**", f"down to\n**[San Juan La Laguna]({wiki('San_Juan_La_Laguna')})**"),
    ("**What it is.** Atitlán is", f"**What it is.** [Atitlán]({wiki('Lake_Atitlán')}) is"),
    ("- **Indian Nose (Rostro Maya), 2,550 m.**",
     f"- **[Indian Nose (Rostro Maya)]({maps('Indian Nose Rostro Maya mirador Santa Clara La Laguna')}), 2,550 m.**"),
    ("- **Afternoon: Cerro Tzankujil, San Marcos.**",
     f"- **Afternoon: [Cerro Tzankujil]({maps('Reserva Natural Cerro Tzankujil San Marcos La Laguna')}), San Marcos.** "
     "([Lonely Planet](https://www.lonelyplanet.com/points-of-interest/cerro-tzankujil/1360016))"),
    ("### Sat 19 Dec — Volcán San Pedro (3,020 m) ⛰️",
     f"### Sat 19 Dec — [Volcán San Pedro]({wiki('Volcán_San_Pedro')}) (3,020 m) ⛰️"),
    ("You register at the park office on the north-west edge of San Pedro La Laguna.",
     f"You register at the [park office]({maps('Parque Ecológico Volcán San Pedro La Laguna')}) on the north-west edge of "
     f"[San Pedro La Laguna]({wiki('San_Pedro_La_Laguna')})."),
    ("**What it is.** Chichi is", f"**What it is.** [Chichicastenango]({wiki('Chichicastenango')}) (Chichi) is"),
    ("The white church of Santo Tomás was built",
     f"The white [church of Santo Tomás]({wiki('Iglesia_de_Santo_Tomás')}) was built"),
    ("**What it is.** Xela (\"SHEH-la\") is", f"**What it is.** [Xela]({wiki('Quetzaltenango')}) (\"SHEH-la\") is"),
    ("- **Morning: Laguna Chicabal (2,712 m).**",
     f"- **Morning: [Laguna Chicabal]({maps('Laguna Chicabal San Martin Sacatepequez')}) (2,712 m).** "
     f"([volcano on Wikipedia]({wiki('Chicabal')}))"),
    ("- **Afternoon: Fuentes Georginas hot springs.**",
     f"- **Afternoon: [Fuentes Georginas]({maps('Fuentes Georginas Zunil')}) hot springs.**"),
    ("### Tue 22 – Wed 23 Dec — Tajumulco overnight (4,220 m) ⛰️",
     f"### Tue 22 – Wed 23 Dec — [Tajumulco]({wiki('Volcán_Tajumulco')}) overnight (4,220 m) ⛰️"),
    ("**Volcán Santa María (3,772 m)**", f"**[Volcán Santa María]({wiki('Santa_María_(volcano)')}) (3,772 m)**"),
    ("Adrenalina's office is just off Parque Centro América",
     f"Adrenalina's [office]({maps('Adrenalina Tours Quetzaltenango')}) is just off Parque Centro América"),
    ("Cobán is the hub;\n**Lanquín**", f"[Cobán]({wiki('Cobán')}) is the hub;\n**[Lanquín]({wiki('Lanquín')})**"),
    ("and the base for\n**Semuc Champey**.", f"and the base for\n**[Semuc Champey]({wiki('Semuc_Champey')})**."),
    ("visit the\n**Grutas de Lanquín**", f"visit the\n**[Grutas de Lanquín]({maps('Grutas de Lanquin')})**"),
    ("**swim off a dock in Lake Petén Itzá**",
     f"**swim off a dock in [Lake Petén Itzá]({wiki('Lake_Petén_Itzá')})**"),
    ("**Why El Remate rather than Flores?**",
     f"**Why [El Remate]({maps('El Remate Peten Guatemala')}) rather than [Flores]({wiki('Flores,_Petén')})?**"),
    ("**What it is.** Tikal was", f"**What it is.** [Tikal]({wiki('Tikal')}) was"),
    ("Its steep temples rise", "Its steep temples rise"),
    ("canopy, and the jungle around them is alive with spider and howler monkeys, toucans and coatis.\n**Yaxhá**",
     f"canopy, and the jungle around them is alive with spider and howler monkeys, toucans and coatis.\n**[Yaxhá]({wiki('Yaxha')})**"),
    ("south on the main paved highway via Poptún to **Río Dulce**",
     f"south on the main paved highway via Poptún to **[Río Dulce]({maps('Rio Dulce Fronteras Izabal')})**"),
    ("**Afternoon: Finca El Paraíso hot waterfall**",
     f"**Afternoon: [Finca El Paraíso hot waterfall]({maps('Finca El Paraiso hot waterfall El Estor')})** "
     "([Lonely Planet](https://www.lonelyplanet.com/guatemala/attractions/turicentro-el-paraiso/a/poi-sig/1331618/358403))"),
    ("visit the **Castillo de San Felipe de Lara**",
     f"visit the **[Castillo de San Felipe de Lara]({wiki('Castle_of_San_Felipe_de_Lara')})**"),
    ("where Lake Izabal drains", f"where [Lake Izabal]({wiki('Lake_Izabal')}) drains"),
    ("many place names are Nahuatl,", f"many place names are [Nahuatl]({wiki('Nahuatl')}),"),
]
for old, new in place_links:
    if old != new:
        sub_once(old, new)

open(path, "w").write(text)
print("ok")
