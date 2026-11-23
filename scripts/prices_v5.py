"""Rewrite every price in the v5 guide as quetzales + euros.

Rates: XE mid-market, 15 Nov 2026: Q1 = EUR 0.118624 = USD 0.130839.
"""
import re
import sys

EUR_PER_Q = 0.118624
Q_PER_USD = 1 / 0.130839


def euro(q):
    value = q * EUR_PER_Q
    return f"€{value:.1f}" if value < 10 else f"€{round(value):,}"


def quetzal(q):
    return f"Q{round(q):,}" if q < 1000 else f"Q{round(q / 10) * 10:,}"


def q_range(low, high=None):
    if high is None:
        return f"{quetzal(low)} ({euro(low)})"
    return f"{quetzal(low)}–{quetzal(high)} ({euro(low)}–{euro(high)})"


def usd_range(prefix, low, high=None):
    lo_q = low * Q_PER_USD
    if high is None:
        return f"{prefix}{quetzal(lo_q)} ({euro(lo_q)}; listed as US${low:g})"
    hi_q = high * Q_PER_USD
    return (f"{prefix}{quetzal(lo_q)}–{quetzal(hi_q)} "
            f"({euro(lo_q)}–{euro(hi_q)}; listed as US${low:g}–{high:g})")


text = open(sys.argv[1]).read()

# Exchange-rate note: swap for a placeholder so no pass touches it
RATE_NOTE = re.compile(r"Exchange rate used:\s*>?\s*\*\*about Q7\.6 = US\$1\*\*\s*\(the currency is the quetzal,\s*>?\s*written GTQ or Q\)\.")
assert RATE_NOTE.search(text), "rate note not found"
text = RATE_NOTE.sub("@@RATE_NOTE@@", text)

# Special cases first
text = text.replace("Q660 (~US$87)", "Q660 (€78)")
text = text.replace("about US$72 to 117", "about US$72–117")
text = text.replace("110 GTQ", "Q110")
# Quetzal amounts not already followed by a euro conversion
qre = re.compile(r"(?<![\w$])Q(\d[\d,]*)(?:–(\d[\d,]*))?(?! ?\(€)(?![\d,])")
def q_sub(m):
    low = float(m.group(1).replace(",", ""))
    high = float(m.group(2).replace(",", "")) if m.group(2) else None
    return q_range(low, high)
text = qre.sub(q_sub, text)
usd = re.compile(r"(~|about |\+)?US\$(\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))?(?!\))")
text = usd.sub(lambda m: usd_range(
    {"~": "~", "about ": "about ", "+": "+", None: ""}[m.group(1)],
    float(m.group(2)), float(m.group(3)) if m.group(3) else None), text)

text = text.replace(
    "Exchange rate used:\n> **about Q7.6 = US$1** (the currency is the quetzal, "
    "written GTQ or Q).",
    "Prices are shown in **quetzales (Q) and euros (€)** at the mid-market\n"
    "> rate of 15 Nov 2026 (**€1 ≈ Q8.43**; US$1 ≈ Q7.64). Where an operator "
    "lists a\n> dollar price, the original is in brackets. Card and cash rates "
    "will be a few % worse.")

text = text.replace("@@RATE_NOTE@@", (
    "Prices are shown in **quetzales (Q) and euros (€)** at the\n"
    "> mid-market rate of 15 Nov 2026 (**€1 ≈ Q8.43**). Where an operator lists\n"
    "> a dollar price, the original is noted. Card and cash rates will be a few\n"
    "> % worse."))
open(sys.argv[1], "w").write(text)
