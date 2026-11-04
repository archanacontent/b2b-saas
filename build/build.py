"""Builds the B2B SaaS Product Launch Playbook site from docs/*.md into _site/."""
import html, os, re, shutil, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_site")
SITE = "https://archanacontent.github.io/b2b-saas/"
TITLE = "B2B SaaS Product Launch Playbook"
GA = "G-R5QPB9VQWB"

MODULES = [
    ("market-research", "Research", "Market Research", "Prove the problem and the demand before you spend."),
    ("icp-and-personas", "Buyers", "ICP And Personas", "Define the companies to pursue and the people who decide."),
    ("competitive-intelligence", "Rivals", "Competitive Intelligence", "Track rivals and give reps answers they can use mid-call."),
    ("positioning-and-messaging", "Positioning", "Positioning And Messaging", "Settle one reason to buy and say it the same way everywhere."),
    ("go-to-market-and-launch-plan", "GTM Plan", "Go-To-Market Plan", "Size the launch and fix who delivers what, and when."),
    ("launch-content-kit", "Content", "Launch Content", "Build every asset from one message hierarchy."),
    ("sales-enablement", "Sales", "Sales Enablement", "Prepare reps to sell from the first day."),
    ("demand-generation-support", "Demand", "Demand Generation", "Keep every campaign tied to the positioning."),
    ("performance-and-optimisation", "Performance", "Performance", "Agree on success early and feed the results back."),
]

def whole_sentences(text, limit=155):
    """Keep whole sentences up to the limit, so descriptions never stop mid-word."""
    if len(text) <= limit:
        return text
    out = ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        nxt = (out + " " + sent).strip()
        if len(nxt) > limit:
            break
        out = nxt
    return out or text[:limit].rsplit(" ", 1)[0] + "."

def head(title, desc, url, rel):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#143840">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{rel}assets/fonts/literata-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/playbook.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
</head><body>
<header class="top"><a href="{rel}">{TITLE}</a><a href="https://archanacontent.github.io/">Archana Panda</a></header>
"""

def tabs(current, rel):
    out = ['<nav class="tabs" aria-label="Modules">']
    for i, (slug, short, name, _) in enumerate(MODULES, 1):
        cur = ' aria-current="page"' if slug == current else ""
        out.append(f'<a class="tab" style="background:var(--t{i})" href="{rel}{slug}/"{cur} title="{name}">{short}</a>')
    out.append("</nav>")
    return "".join(out)

FOOT = '<p class="foot">Created by <a href="https://archanacontent.github.io/">Archana Panda</a>. Licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>'

# ---------- visuals ----------
def fig(inner, caption, cls=""):
    return f'<figure class="visual {cls}">{inner}<figcaption>{caption}</figcaption></figure>'

def v_scorecard():
    rows = [("Pain severity", 25, 4), ("Reachable market", 20, 3), ("Willingness to pay", 20, 1),
            ("Competitive gap", 15, 3), ("Fit with current product", 10, 5), ("Time to revenue", 10, 3)]
    r = []
    for name, w, s in rows:
        opts = "".join(f'<option{" selected" if n == s else ""}>{n}</option>' for n in range(1, 6))
        r.append(f'<div class="row"><label for="sc-{w}-{s}-{name[:3]}">{name}</label><span>{w}%</span>'
                 f'<select id="sc-{w}-{s}-{name[:3]}" data-w="{w}">{opts}</select></div>')
    inner = ('<div class="calc" data-calc>' + "".join(r) +
             '<div class="total" aria-live="polite"><b data-total>3.05</b><span class="verdict" data-verdict>Move to validation</span></div></div>')
    return fig(inner, "Change any score to see the weighted total and the verdict update. Under 3 goes back to research, 3 to 3.5 moves to validation, and above 3.5 is ready for positioning.")

def v_committee():
    nodes = [("Champion", "Head of Sales", 150, 60, 1), ("Decision-maker", "Founder or CEO", 450, 60, 5),
             ("Day-to-day user", "Sales reps", 150, 250, 2), ("Blocker", "Operations or finance lead", 450, 250, 4)]
    s = ['<svg viewBox="0 0 600 310" role="img" aria-label="Buying committee: the Head of Sales champions the deal, the founder decides, reps use the product and the operations or finance lead can block it.">']
    for _, _, x, y, _ in nodes:
        s.append(f'<line x1="300" y1="155" x2="{x}" y2="{y+20}" stroke="#86A9B0" stroke-width="2" stroke-dasharray="5 5"/>')
    s.append('<circle cx="300" cy="155" r="48" fill="#245A67" stroke="#F2D879" stroke-width="2"/><text x="300" y="161" text-anchor="middle" fill="#EEF5F6" font-family="Literata,serif" font-weight="700" font-size="17">The deal</text>')
    for role, person, x, y, t in nodes:
        s.append(f'<rect x="{x-125}" y="{y-22}" width="250" height="64" rx="6" fill="var(--t{t})"/>'
                 f'<text x="{x}" y="{y+2}" text-anchor="middle" fill="#0F2F37" font-family="Public Sans,sans-serif" font-weight="600" font-size="15">{role}</text>'
                 f'<text x="{x}" y="{y+24}" text-anchor="middle" fill="#0F2F37" font-family="Public Sans,sans-serif" font-size="14">{person}</text>')
    s.append("</svg>")
    return fig("".join(s), "Who plays which part in the worked example. Content and outreach need to reach all four before the decision.")

def v_positioning():
    pts = [("Enterprise CRM", 430, 200, 9), ("Freemium marketing-led CRM", 170, 250, 3), ("Pipeline-first sales CRM", 150, 95, 1), ("The product", 260, 70, 6)]
    s = ['<svg viewBox="0 0 600 340" role="img" aria-label="Positioning map: setup effort on the horizontal axis and price predictability on the vertical axis. The product sits at low setup effort and high predictability.">',
         '<rect x="60" y="20" width="520" height="270" fill="none" stroke="#86A9B0"/>',
         '<line x1="320" y1="20" x2="320" y2="290" stroke="rgba(238,245,246,.16)"/><line x1="60" y1="155" x2="580" y2="155" stroke="rgba(238,245,246,.16)"/>',
         '<text x="320" y="320" text-anchor="middle" fill="#B5CFD4" font-family="Public Sans,sans-serif" font-size="14">Setup effort, from low to high</text>',
         '<text x="22" y="155" text-anchor="middle" fill="#B5CFD4" font-family="Public Sans,sans-serif" font-size="14" transform="rotate(-90 22 155)">Price predictability as the team grows</text>']
    for name, x, y, t in pts:
        r = 12 if name == "The product" else 9
        stroke = ' stroke="#EEF5F6" stroke-width="3"' if name == "The product" else ""
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--t{t})"{stroke}/>'
                 f'<text x="{x+18}" y="{y+5}" fill="#EEF5F6" font-family="Public Sans,sans-serif" font-weight="{600 if name=="The product" else 500}" font-size="14.5">{name}</text>')
    s.append("</svg>")
    return fig("".join(s), "Where each competitor type sits on the two factors this buyer weighs most. Illustrative placement.")

def v_pyramid():
    lv = [("Headline promise", "Every deal, from first call to paid invoice, in one CRM your team will use.", 56, 6),
          ("Supporting messages", "One record for sales and billing. An assistant for the admin. A flat price per seat.", 72, 1),
          ("Proof points", "Setup time, hours saved per rep and the published price.", 86, 2),
          ("Call to action", "Start a 14-day trial with your own pipeline.", 100, 3)]
    inner = '<div class="pyramid">' + "".join(
        f'<div style="width:{w}%;background:var(--t{t})"><small>{k}</small>{v}</div>' for k, v, w, t in lv) + "</div>"
    return fig(inner, "The message hierarchy from the worked example. Short copy uses the top level, and long copy works down through every level.")

def v_timeline():
    ms = [("-8", "Positioning and pricing approved"), ("-6", "Beta begins"), ("-4", "Content in review"),
          ("-2", "Sales and support trained"), ("0", "Launch day"), ("+4", "First win/loss interviews"), ("+12", "90-day report")]
    lis = "".join(f'<li class="{"zero" if w == "0" else ""}"><b>Week {w}</b>{m}</li>' for w, m in ms)
    return fig(f'<div class="track"><ol>{lis}</ol></div>', "The launch timeline from the worked example, counted in weeks from launch day.")

def v_channels():
    rows = [("Webinars", 1, 3, 2), ("Events", 2, 3, 2), ("Email", 1, 3, 3), ("Outbound", 2, 2, 3), ("LinkedIn", 3, 2, 1)]
    cells = ['<div class="h">Channel</div><div class="h">Awareness</div><div class="h">Consideration</div><div class="h">Decision</div>']
    lab = {1: "Light", 2: "Medium", 3: "Strong"}
    for name, *v in rows:
        cells.append(f"<div>{name}</div>" + "".join(f'<div class="c{x}">{lab[x]}</div>' for x in v))
    leg = '<div class="legend"><span><i class="c1" style="background:rgba(242,216,121,.18)"></i>Light fit</span><span><i style="background:rgba(242,216,121,.45)"></i>Medium fit</span><span><i style="background:var(--t6)"></i>Strong fit</span></div>'
    return fig(f'<div class="matrix">{"".join(cells)}</div>{leg}', "How well each channel fits each buying stage. Illustrative, so adjust it to your own channel data.")

def v_emails():
    st = [("Email 1, launch day", "The follow-up that never went out"), ("Email 2, day 3", "What your reps do after 5 p.m."), ("Email 3, day 7", "Your pipeline, imported by Friday")]
    inner = '<div class="steps">' + "".join(f"<div><b>{a}</b>{b}</div>" for a, b in st) + "</div>"
    return fig(inner, "The three-email sequence across launch week. Send days are illustrative.")

def v_funnel():
    st = [("Awareness", "8,000 ICP visits", 100, 1), ("Engagement", "300 trials", 88, 2), ("Adoption", "60% import in week one", 76, 7),
          ("Pipeline", "120 qualified opportunities", 64, 3), ("Revenue", "Set with finance", 52, 6), ("Retention", "85% active at 90 days", 40, 5)]
    inner = '<div class="funnel">' + "".join(
        f'<div style="width:{w}%;background:var(--t{t})"><b>{a}</b><span>{b}</span></div>' for a, b, w, t in st) + "</div>"
    return fig(inner, "Targets from the worked example, from first visit to retained customer.")

def v_loop():
    s = ['<svg viewBox="0 0 600 300" role="img" aria-label="Feedback loop: win/loss interviews produce findings that go to product marketing, product and demand generation, whose changes improve the next launch.">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#86A9B0"/></marker></defs>']
    boxes = [("Win/loss interviews", 300, 40, 6), ("Product marketing", 110, 160, 4), ("Product", 300, 160, 1), ("Demand generation", 490, 160, 2), ("A sharper next launch", 300, 265, 5)]
    for a, b in [((300, 62), (130, 136)), ((300, 62), (300, 136)), ((300, 62), (470, 136)), ((130, 184), (280, 244)), ((300, 184), (300, 244)), ((470, 184), (320, 244))]:
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#86A9B0" stroke-width="2" marker-end="url(#ah)"/>')
    s.append('<path d="M420 268 C580 268 590 40 425 40" fill="none" stroke="#86A9B0" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#ah)"/>')
    for t, x, y, c in boxes:
        w = 200 if len(t) > 16 else 170
        s.append(f'<rect x="{x-w/2}" y="{y-22}" width="{w}" height="44" rx="6" fill="var(--t{c})"/>'
                 f'<text x="{x}" y="{y+5}" text-anchor="middle" fill="#0F2F37" font-family="Public Sans,sans-serif" font-weight="600" font-size="14.5">{t}</text>')
    s.append("</svg>")
    return fig("".join(s), "Each finding goes to the team that can act on it, and the dashed line returns the changes to the next launch.")


def v_stats():
    st = [("66%", "of buyers reported disruption, regret or both after a software purchase"),
          ("89%", "of those with regret first hit a problem during implementation"),
          ("50%", "named AI as the top outside factor shaping their goals")]
    inner = '<div class="stats">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in st) + "</div>"
    return fig(inner, 'Source: <a href="https://www.businesswire.com/news/home/20251007148096/en">Capterra 2026 Software Buying Trends</a>, 3,385 decision-makers across 11 countries.')

def v_icp_filter():
    st = [("All companies in the market", 100, 9), ("10 to 200 employees", 84, 1), ("Professional services or B2B distribution", 70, 2),
          ("Three to 25 people in sales", 56, 7), ("Outgrown spreadsheets or a free CRM", 44, 3), ("A buying trigger in the last 90 days", 34, 4)]
    inner = '<div class="funnel">' + "".join(f'<div style="width:{w}%;background:var(--t{t})"><b>{a}</b></div>' for a, w, t in st) + "</div>"
    return fig(inner, "Each ICP filter narrows the market until only firms ready to buy remain.")

def v_battle():
    win = ["Outgrown the free tier", "Needs invoicing and support in one system", "Wants a predictable price per seat"]
    lose = ["Marketing already runs on their platform", "Needs the largest integration library"]
    inner = ('<div class="split"><div class="win"><b>We win when</b><ul>' + "".join(f"<li>{x}</li>" for x in win) +
             '</ul></div><div class="lose"><b>We lose when</b><ul>' + "".join(f"<li>{x}</li>" for x in lose) + "</ul></div></div>")
    return fig(inner, "The battlecard's win and loss conditions side by side, for a rep to scan before a call.")

def v_posline():
    parts = [("For", "sales-led companies with 10 to 200 employees", 1), ("who", "lose deals to missed follow-ups,", 4),
             ("the product is", "a CRM with a built-in AI assistant", 2), ("that", "runs the path from first call to paid invoice.", 6),
             ("Unlike", "free tiers and admin-heavy enterprise CRMs,", 3), ("it", "includes invoicing, help desk and AI on one flat price.", 5)]
    inner = '<p class="posline">' + " ".join(f'<span class="k">{a}</span> <mark style="--c:var(--t{t})">{b}</mark>' for a, b, t in parts) + "</p>"
    return fig(inner, "The positioning statement read as one sentence. Each highlight comes from a field in the table.")

def v_tiers():
    tiers = [("Tier 1", "New product, new market or major pricing change", "Full campaign", 4, 100), ("Tier 2", "A feature that changes how buyers use the product", "Targeted campaign", 3, 88), ("Tier 3", "A minor improvement or fix", "Release notes", 2, 76)]
    inner = '<div class="tiers">' + "".join(f'<div style="width:{w}%;background:var(--t{t})"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c, t, w in tiers) + "</div>"
    return fig(inner, "Launch effort scales with the tier. Pick the tier before planning anything else.")

def v_raci():
    teams = ["Product marketing", "Head of marketing", "Sales", "Product", "Leadership", "Content", "Support"]
    tasks = [("Positioning", {"Product marketing": "R", "Head of marketing": "A", "Sales": "C", "Product": "C", "Leadership": "I"}),
             ("Pricing", {"Product marketing": "R", "Leadership": "A", "Sales": "C", "Content": "I", "Support": "I"}),
             ("Sales training", {"Product marketing": "R", "Sales": "A", "Product": "C", "Support": "I"}),
             ("Launch content", {"Content": "R", "Product marketing": "A", "Product": "C", "Sales": "I"}),
             ("Support readiness", {"Support": "R", "Leadership": "A", "Product marketing": "C", "Sales": "I"})]
    cells = ['<div class="h"></div>'] + [f'<div class="h vt">{t}</div>' for t in teams]
    for task, m in tasks:
        cells.append(f'<div class="task">{task}</div>' + "".join(f'<div class="r r-{m.get(t, "").lower() or "x"}">{m.get(t, "")}</div>' for t in teams))
    leg = '<div class="legend"><span><i style="background:var(--t2)"></i>R Responsible</span><span><i style="background:var(--t6)"></i>A Accountable</span><span><i style="background:var(--t1)"></i>C Consulted</span><span><i style="background:var(--t9)"></i>I Informed</span></div>'
    return fig(f'<div class="raci">{"".join(cells)}</div>{leg}', "The worked RACI as a grid. Each row has exactly one A.")

def v_wireframe():
    blocks = [("Hero", "Headline promise and trial button", 6, 64), ("Problem", "The buyer's pain in their words", 9, 30), ("Pillar 1", "Deal to invoice", 1, 40),
              ("Pillar 2", "AI assistant", 2, 40), ("Pillar 3", "Flat price", 3, 40), ("How it works", "Three first steps", 7, 30), ("Proof", "Beta quotes and ratings", 5, 30),
              ("Pricing cue", "Flat price per seat", 9, 24), ("Closing CTA", "Start a 14-day trial", 6, 34)]
    inner = '<div class="wire"><div class="bar"><i></i><i></i><i></i></div>'
    row = []
    for name, sub, t, h in blocks:
        cls = "pill" if name.startswith("Pillar") else "blk"
        row.append(f'<div class="{cls}" style="--c:var(--t{t});min-height:{h}px"><b>{name}</b><span>{sub}</span></div>')
    inner += row[0] + row[1] + '<div class="pills">' + "".join(row[2:5]) + "</div>" + "".join(row[5:]) + "</div>"
    return fig(inner, "The product page from the worked example, laid out top to bottom.")

def v_storyboard():
    sl = [("1", "Title and promise"), ("2", "The shift"), ("3", "The problem"), ("4", "What good looks like"), ("5", "How it works"),
          ("6", "Pillar 1"), ("7", "Pillar 2"), ("8", "Pillar 3"), ("9", "Customer proof"), ("10", "Pricing"), ("11", "Next steps")]
    col = {"1": 6, "2": 1, "3": 4, "4": 2, "5": 7, "6": 3, "7": 3, "8": 3, "9": 5, "10": 9, "11": 6}
    inner = '<div class="story">' + "".join(f'<div style="--c:var(--t{col[n]})"><i>{n}</i><span>{t}</span></div>' for n, t in sl) + "</div>"
    return fig(inner, "The deck as a storyboard. The buyer's story comes first, and the product arrives at slide 5.")

def v_discovery():
    st = [("Situation", 1), ("Problem", 4), ("Cost", 3), ("Decision", 5), ("Timing", 2)]
    inner = '<div class="chev">' + "".join(f'<div style="--c:var(--t{t})">{a}</div>' for a, t in st) + "</div>"
    return fig(inner, "Discovery runs in this order, and the product comes up only after the cost is clear.")

def v_agenda():
    seg = [("Why we built it", 15, 1), ("Positioning", 20, 4), ("Live demo", 20, 2), ("Competitors", 15, 3), ("Role-play", 20, 5), ("Assets", 10, 9)]
    inner = '<div class="agenda">' + "".join(f'<div style="flex:{m};background:var(--t{t})"><b>{m} min</b><span>{a}</span></div>' for a, m, t in seg) + "</div>"
    return fig(inner, "The 100-minute enablement session, sized by time.")

VISUALS = {"scorecard-calculator": v_scorecard, "committee": v_committee, "positioning-map": v_positioning,
           "pyramid": v_pyramid, "timeline": v_timeline, "channel-matrix": v_channels, "email-flow": v_emails,
           "kpi-funnel": v_funnel, "feedback-loop": v_loop, "stats": v_stats, "icp-filter": v_icp_filter, "battle-split": v_battle, "positioning-sentence": v_posline, "tier-stack": v_tiers, "raci-grid": v_raci, "page-wireframe": v_wireframe, "deck-storyboard": v_storyboard, "discovery-steps": v_discovery, "agenda-bar": v_agenda}

CALC_JS = """<script>
document.querySelectorAll('[data-calc]').forEach(function(c){
  function run(){var t=0;c.querySelectorAll('select').forEach(function(s){t+=(+s.value)*(+s.dataset.w)/100});
    c.querySelector('[data-total]').textContent=t.toFixed(2);
    c.querySelector('[data-verdict]').textContent=t<3?'Back to research':(t<=3.5?'Move to validation':'Ready for positioning');}
  c.addEventListener('change',run);run();});
</script>"""


ICONS = {
 "doc": '<path d="M7 3h7l5 5v13H7z" /><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "chart": '<path d="M4 20h16M7 16v-5M12 16V7M17 16v-8"/>',
 "check": '<path d="M5 12l4 4 10-10"/><rect x="3" y="3" width="18" height="18" rx="3"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2c2.9.3 5 2.6 5 5.8"/>',
 "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "mega": '<path d="M3 10v4h4l7 4V6L7 10z"/><path d="M17 9c1.5 1 1.5 5 0 6"/>',
 "stack": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
 "loop": '<path d="M20 12a8 8 0 1 1-3-6.2"/><path d="M20 4v5h-5"/>',
}
def icon_for(h):
    h = h.lower()
    for keys, ic in [(("brief", "announcement", "page", "collateral", "brochure", "case study", "one-pager", "statement"), "doc"),
                     (("scorecard", "kpi", "funnel"), "chart"), (("checklist",), "check"), (("persona", "committee", "profile"), "users"),
                     (("tracker", "battlecard", "comparison", "positioning"), "target"), (("tier", "raci"), "flag"),
                     (("timeline", "agenda"), "calendar"), (("channel", "campaign", "email"), "mega"), (("pillar", "hierarchy", "deck"), "stack"),
                     (("objection", "discovery", "win/loss", "value prop"), "chat"), (("feedback",), "loop")]:
        if any(k in h for k in keys):
            return ic
    return "doc"

def svg_icon(name):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def field_cards(html_table, filled=False):
    rows = re.findall(r"<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", html_table, flags=re.S)
    cls = "fields filled" if filled else "fields"
    out = [f'<div class="{cls}">']
    for k, v in rows:
        line = "" if filled else '<i class="write" aria-hidden="true"></i>'
        out.append(f'<div class="field"><b>{k}</b><p>{v}</p>{line}</div>')
    out.append("</div>")
    return "".join(out)

def transform(body, mod):
    # two-column guidance tables become field cards
    def tbl(m):
        t = m.group(0)
        hdr = re.findall(r"<th[^>]*>(.*?)</th>", t)
        if len(hdr) == 2 and hdr[1].startswith(("What", "Entry")) and hdr[0] != "Slide":
            return field_cards(t, filled=hdr[1] == "Entry")
        bodyrows = re.findall(r"<tr>(.*?)</tr>", t, flags=re.S)[1:]
        if bodyrows and all(re.fullmatch(r"(\s*<td[^>]*>\s*</td>\s*)+", r) for r in bodyrows):
            n = len(hdr)
            empty = ("<tr>" + "<td></td>" * n + "</tr>") * 4
            t = re.sub(r"<tbody>.*?</tbody>", "<tbody>" + empty + "</tbody>", t, flags=re.S).replace('<div class="table-wrap">', '<div class="table-wrap blank">')
        return t
    body = re.sub(r'<div class="table-wrap"><table>.*?</table></div>', tbl, body, flags=re.S)
    # section icons and anchors
    secs = []
    def h2(m):
        title = m.group(1)
        sid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        if title not in ("Worked Example", "Mistakes To Avoid"):
            secs.append((sid, title))
        return f'<h2 id="{sid}"><span class="badge" style="background:var(--t{mod})">{svg_icon(icon_for(title)) if title not in ("Worked Example", "Mistakes To Avoid") else svg_icon("check" if title == "Worked Example" else "flag")}</span>{title}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    chips = '<nav class="chips" aria-label="Templates in this module">' + "".join(
        f'<a href="#{sid}">{svg_icon(icon_for(t))}{t}</a>' for sid, t in secs) + "</nav>"
    # checklist bullets become check items
    body = re.sub(r'(<h2 id="demand-validation-checklist">.*?</p>\s*)<ul>(.*?)</ul>',
                  lambda m: m.group(1) + '<ul class="checks">' + re.sub(r"<li>", '<li><input type="checkbox" aria-label="Mark as done">', m.group(2)) + "</ul>", body, flags=re.S)
    return body, chips

# ---------- page assembly ----------
def render(md_text):
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    body = re.sub(r'<(t[hd]) style="text-align: (left|center|right);">', lambda m: f'<{m.group(1)}>' if m.group(2) == "left" else f'<{m.group(1)} class="c">', body)
    body = re.sub(r"<table>(.*?)</table>", r'<div class="table-wrap"><table>\1</table></div>', body, flags=re.S)
    body = re.sub(r"<!-- visual:([a-z-]+) -->", lambda m: VISUALS[m.group(1)](), body)
    # persona cards
    body = re.sub(r'(<h3>Persona: .*?</h3>\s*)<div class="table-wrap">(<table>.*?</table>)</div>',
                  r'\1<div class="persona">\2</div>', body, flags=re.S)
    # status chips
    body = re.sub(r"<td>(Ahead|Close|Behind)</td>", lambda m: f'<td><span class="chip {m.group(1).lower()}">{m.group(1)}</span></td>', body)
    # worked example and mistakes wrappers
    body = re.sub(r'(<h2>Worked Example</h2>.*?)(?=<h2>Mistakes To Avoid</h2>)', r'<section class="worked">\1</section>', body, flags=re.S)
    body = re.sub(r'(<h2>Mistakes To Avoid</h2>.*)$', r'<section class="mistakes">\1</section>', body, flags=re.S)
    return body

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)

def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "build", "assets"), os.path.join(OUT, "assets"))
    dl = os.path.join(ROOT, "templates")
    if os.path.isdir(dl):
        shutil.copytree(dl, os.path.join(OUT, "templates"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    for i, (slug, short, name, line) in enumerate(MODULES, 1):
        md = open(os.path.join(ROOT, "docs", slug + ".md"), encoding="utf-8").read()
        h1 = re.match(r"# (.+)", md).group(1)
        body = render(md)
        body, chips = transform(body, i)
        downloads = (f'<div class="download"><a class="btn primary" href="../templates/{i:02d}-{slug}.docx">Download blank templates (Word)</a>'
                     + (f'<a class="btn" href="../templates/launch-playbook-workbook.xlsx">Download the workbook (Excel)</a>' if slug in XLSX_MODULES else "")
                     + ('<a class="btn" href="../templates/sample-sales-deck.pdf">View the sample sales deck (PDF)</a><a class="btn" href="../templates/sample-sales-deck.pptx">Download the deck (PowerPoint)</a>' if slug == "sales-enablement" else "")
                     + "</div>")
        body = re.sub(r"(<h1>.*?</h1>)", lambda m: f'<span class="module-tag" style="background:var(--t{i})">Module {i} of 9</span>' + m.group(1), body, count=1)
        body = re.sub(r"(</p>\s*<h2 )", lambda m: "</p>" + chips + downloads + "<h2 ", body, count=1)
        prev = MODULES[i - 2] if i > 1 else None
        nxt = MODULES[i] if i < len(MODULES) else None
        pager = '<nav class="pager" aria-label="Module pages">'
        if prev:
            pager += f'<a href="../{prev[0]}/"><span>Previous</span>{prev[2]}</a>'
        if nxt:
            pager += f'<a class="next" href="../{nxt[0]}/"><span>Next</span>{nxt[2]}</a>'
        pager += "</nav>"
        intro = re.search(r"\n\n(.+?)\n", md).group(1)
        desc = whole_sentences(re.sub(r"\s+", " ", intro))
        page = (head(f"{h1} | {TITLE}", desc, SITE + slug + "/", "../") +
                f'<main class="binder"><article class="sheet"><div class="content">{body}{pager}{FOOT}</div></article>{tabs(slug, "../")}</main>' +
                CALC_JS + "</body></html>")
        write(os.path.join(OUT, slug, "index.html"), page)

    flow = '<ol class="flow">' + "".join(
        f'<li><span class="n" style="background:var(--t{i})">{i}</span><a href="{slug}/"><b>{name}</b><span>{line}</span></a></li>'
        for i, (slug, short, name, line) in enumerate(MODULES, 1)) + "</ol>"
    home_md = open(os.path.join(ROOT, "docs", "index.md"), encoding="utf-8").read()
    home_body = markdown.markdown(home_md)
    home_body = home_body.replace("<p>{{modules}}</p>", flow)
    home_body = re.sub(r"<h1>(.*?)</h1>\s*<p>(.*?)</p>", r'<div class="home-grid"><div><h1>\1</h1><p class="lede">\2</p></div>ART</div>', home_body, count=1, flags=re.S).replace("ART", '<div class="hero-art" aria-hidden="true"><div class="pg"><i class="t"></i><i></i><i></i><i class="c"></i><i></i></div><div class="pg"><i class="t"></i><i></i><i class="c"></i><i></i><i></i></div><div class="pg"><i class="t"></i><i></i><i></i><i class="c"></i><i></i><i></i></div><div class="tabstrip"><span style="background:var(--t1)"></span><span style="background:var(--t2)"></span><span style="background:var(--t3)"></span><span style="background:var(--t4)"></span><span style="background:var(--t5)"></span><span style="background:var(--t6)"></span><span style="background:var(--t7)"></span><span style="background:var(--t8)"></span><span style="background:var(--t9)"></span></div></div>')
    desc = "A go-to-market playbook for product marketing teams launching B2B SaaS products, from market research to the 90-day review."
    page = (head(TITLE, desc, SITE, "") +
            f'<main class="binder"><article class="sheet home"><div class="content">{home_body}{FOOT}</div></article>{tabs("", "")}</main></body></html>')
    write(os.path.join(OUT, "index.html"), page)
    print("built", OUT)

XLSX_MODULES = {"market-research", "competitive-intelligence", "go-to-market-and-launch-plan", "demand-generation-support", "performance-and-optimisation"}

if __name__ == "__main__":
    build()
