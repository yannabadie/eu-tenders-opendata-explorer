#!/usr/bin/env python3
"""Deterministic Programmatic SEO Generator — EU Public Tenders & Open-Data Explorer.

Pure Python 3 stdlib (zero dependencies). Reads data/ted_snapshot_60.json (10 EU countries
x 6 high-value CPV sectors fetched live from api.ted.europa.eu/v3/notices/search) and generates:
  - index.html (EU procurement observatory + interactive same-origin explorer + paid rail cards)
  - sectors/index.html (searchable & country/sector-filterable hub of 60 EU procurement pages)
  - sectors/<country>-<sector>.html (60 unique pages with live counts, sample notices, JSON-LD)
  - sitemap.xml (62 URLs) & robots.txt
"""
from __future__ import annotations

import html
import json
from pathlib import Path

SITE_BASE = "https://yannabadie.github.io/eu-tenders-opendata-explorer"
LASTMOD = "2026-11-21"

# Direct conversion links to ALREADY-APPROVED live rails (zero invented codes!)
APIFY_TED_ACTOR = "https://apify.com/yannabadie/eu-public-tenders-ted-boamp?fpr=zuvzfw"
APIFY_PARTNER = "https://apify.com/?fpr=zuvzfw"
RAPIDAPI_TED = "https://rapidapi.com/YannAbadie/api/eu-ted-public-tenders-procurement-api"
RAPIDAPI_SUITE = "https://rapidapi.com/YannAbadie/api/eu-us-official-open-data-intelligence1"
ZYLA_INFO = "https://zylalabs.com/"
N8N_REPO = "https://github.com/yannabadie/official-opendata-mcp-n8n-templates"
MCP_REPO = "https://github.com/yannabadie/eu-us-opendata-mcp"
GH_ACTION_FACTURX = "https://github.com/marketplace/actions/factur-x-france-2026-2027-validator-en-16931-pdf-a-3"
GH_ACTION_CRA = "https://github.com/marketplace/actions/cra-sbom-guard-eu-cyber-resilience-act-art-14-scanner"
FACTURKIT_URL = "https://yannabadie.github.io/facturkit-2027/"
FACTURKIT_EN = "https://yannabadie.github.io/facturkit-2027/en.html"
GUMROAD_COCKPIT = "https://yannabadi.gumroad.com/l/hfxuuz"
GUMROAD_EU_GUIDE = "https://yannabadi.gumroad.com/l/eu-compliance-2026-2027-guide"
GUMROAD_EU_NOTION = "https://yannabadi.gumroad.com/l/eu-compliance-2026-2027-notion-pack"
GUMROAD_FREELANCE_NOTION = "https://yannabadi.gumroad.com/l/freelance-ei-france-2026-notion-cockpit"


def fmt_int(n: int) -> str:
    return f"{int(n):,}"


def render_header(prefix: str) -> str:
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a class="brand-lockup" href="{prefix}index.html" aria-label="EU Public Tenders Explorer Home">
        <span class="brand-mark" aria-hidden="true">EU</span>
        <span class="brand-text">
          <span class="brand-name">EU Public Tenders Explorer</span>
          <span class="brand-sub">TED API v3 Open-Data · 10 Countries × 6 CPV Sectors</span>
        </span>
      </a>
      <nav class="header-nav" aria-label="Primary navigation">
        <a class="nav-link" href="{prefix}index.html#explorer">Live Explorer</a>
        <a class="nav-link" href="{prefix}sectors/index.html">60 Sectors</a>
        <a class="nav-link" href="{RAPIDAPI_TED}" target="_blank" rel="noopener">RapidAPI</a>
        <a class="nav-link" href="{APIFY_TED_ACTOR}" target="_blank" rel="noopener noreferrer sponsored">Apify Actor</a>
        <a class="btn-nav" href="{MCP_REPO}" target="_blank" rel="noopener">Free MCP &amp; n8n</a>
      </nav>
    </div>
  </header>"""


def render_footer(prefix: str) -> str:
    return f"""  <footer class="site-footer">
    <div class="container">
      <p>
        <strong>EU Public Tenders &amp; Open-Data Explorer</strong> · Powered by official EU TED Search API v3 ·
        <a href="{prefix}index.html">Home</a> ·
        <a href="{prefix}sectors/index.html">All 60 Country × Sector Guides</a> ·
        <a href="{prefix}sitemap.xml">Sitemap</a> ·
        <a href="{RAPIDAPI_TED}" target="_blank" rel="noopener">RapidAPI TED API</a> ·
        <a href="{APIFY_PARTNER}" target="_blank" rel="noopener noreferrer sponsored">Apify ($5/mo Free Credits)</a> ·
        <a href="{FACTURKIT_EN}" target="_blank" rel="noopener">FacturKit 2027</a>
      </p>
      <p class="disclosure">Independent open-data procurement intelligence portal. All tender metadata originates from the European Union Publications Office (TED v3). Links to Apify include a transparent partner referral (<code>rel="sponsored"</code>) with $5/month free platform credits and zero extra cost.</p>
    </div>
  </footer>"""


def render_conversion_rails() -> str:
    return f"""        <div class="rails-grid">
          <article class="rail-card">
            <div>
              <span class="rail-tag live">Pay-Per-Event · $5/mo Free Credits</span>
              <h3>Apify Actor: EU TED + BOAMP Scraper</h3>
              <p>Run scheduled extractions of EU TED v3 &amp; French BOAMP tenders into JSON, CSV, Excel, or MCP agents at $3–4 / 1,000 notices (<code>256 MB</code> RAM).</p>
            </div>
            <a class="btn-rail" href="{APIFY_TED_ACTOR}" target="_blank" rel="noopener noreferrer sponsored">Run on Apify Store →</a>
          </article>

          <article class="rail-card">
            <div>
              <span class="rail-tag live">Hosted REST API · 100 Free Req/mo</span>
              <h3>RapidAPI &amp; Zyla EU TED Procurement API</h3>
              <p>Plug edge-cached, normalized JSON EU tender search directly into your CRM, Slack bot, or SaaS via RapidAPI (<code>$0/$19/$49/$149</code>) or <a href="{ZYLA_INFO}" target="_blank" rel="noopener">Zyla API Hub</a>.</p>
            </div>
            <a class="btn-rail" href="{RAPIDAPI_TED}" target="_blank" rel="noopener">Open RapidAPI Endpoint →</a>
          </article>

          <article class="rail-card">
            <div>
              <span class="rail-tag">Open-Source MIT · 0 €</span>
              <h3>n8n Workflows &amp; Claude/Cursor MCP Server</h3>
              <p>Deploy our 9 ready-to-import n8n tender alert templates (<code>v1.2.0</code>) or connect our official MCP Registry server (<code>eu-us-opendata-mcp v1.1.1</code>) in 60 seconds.</p>
            </div>
            <a class="btn-rail" href="{N8N_REPO}" target="_blank" rel="noopener">Get Free n8n &amp; MCP Kit →</a>
          </article>

          <article class="rail-card">
            <div>
              <span class="rail-tag">EU Compliance Toolkits</span>
              <h3>GitHub Marketplace Actions &amp; FacturKit 2027</h3>
              <p>Bidding on EU public contracts? Automate CRA Art. 14 SBOM checks (<code>CRA-SBOM-Guard</code>) and French Factur-X EN 16931 compliance (<code>FacturKit 2027</code> / <a href="{GUMROAD_COCKPIT}" target="_blank" rel="noopener noreferrer">Gumroad 79 €</a>).</p>
            </div>
            <a class="btn-rail" href="{GH_ACTION_CRA}" target="_blank" rel="noopener">CRA &amp; Factur-X Actions →</a>
          </article>
        </div>

        <h3 style="margin:26px 0 6px;font-size:1.15rem;">B2B Compliance Guides &amp; Notion Toolkits (Instant Download via Gumroad)</h3>
        <p class="section-sub" style="margin-bottom:14px;">Equip your agency, SaaS team, or freelance practice to win EU public tenders and satisfy 2026–2027 European compliance requirements today (one-time payment, VAT handled by Gumroad Merchant of Record):</p>
        <div class="rails-grid">
          <article class="rail-card">
            <div>
              <span class="rail-tag live">43-Page PDF Handbook · 24 €</span>
              <h3>EU Digital Compliance Guide 2026–2027</h3>
              <p>Practical playbook covering <strong>EU AI Act Art. 50</strong>, <strong>Cyber Resilience Act (CRA Art. 14)</strong>, and <strong>EAA / RGAA v5</strong> accessibility rules required in European public-sector RFPs.</p>
            </div>
            <a class="btn-rail" href="{GUMROAD_EU_GUIDE}" target="_blank" rel="noopener noreferrer">Get the EU Compliance Guide (24 €) →</a>
          </article>

          <article class="rail-card">
            <div>
              <span class="rail-tag live">Notion Command Center · 29 €</span>
              <h3>EU Digital Compliance Command Center</h3>
              <p>Ready-to-duplicate Notion pack (<strong>4 CSV databases + 4 operational SOPs</strong>) to track CRA SBOM scans, AI Act Art. 50 transparency logs, EAA audits, and bid compliance evidence.</p>
            </div>
            <a class="btn-rail" href="{GUMROAD_EU_NOTION}" target="_blank" rel="noopener noreferrer">Get the Notion Command Center (29 €) →</a>
          </article>

          <article class="rail-card">
            <div>
              <span class="rail-tag live">Notion Contractor Cockpit · 19 €</span>
              <h3>Freelance &amp; EI France 2026–2027 Cockpit</h3>
              <p>Turnkey Notion workspace for independent EU/French consultants &amp; BOAMP/TED bidders: revenue tracking, TVA 293 B thresholds, URSSAF provisions, and Factur-X PA compliance.</p>
            </div>
            <a class="btn-rail" href="{GUMROAD_FREELANCE_NOTION}" target="_blank" rel="noopener noreferrer">Get the Freelance Cockpit (19 €) →</a>
          </article>
        </div>"""


def build_sector_page(rec: dict, siblings: list[dict]) -> str:
    slug = rec["slug"]
    c = rec["country"]
    s = rec["sector"]
    open_cnt = int(rec.get("open_tenders_count", 0))
    samples = rec.get("samples", [])
    url = f"{SITE_BASE}/sectors/{slug}.html"

    c_name = html.escape(c["name"])
    s_name = html.escape(s["name"])
    cpv_h = html.escape(s["cpv_label"])
    portal_h = html.escape(c["portal"])
    meta_desc = (
        f"Live EU TED public tenders for {s['name']} in {c['name']} (CPV {s['cpv_label']}): "
        f"{fmt_int(open_cnt)} active calls for tenders ({LASTMOD}), official buyer samples, TED v3 query, RapidAPI & Apify automation."
    )

    sample_rows = []
    for n in samples:
        sample_rows.append(
            f'              <tr>'
            f'<td><span class="cpv-pill">{html.escape(n.get("cpv") or s["cpv_label"][:8])}</span></td>'
            f'<td><a href="{html.escape(n["url"])}" target="_blank" rel="noopener noreferrer"><strong>{html.escape(n["title"])}</strong></a>'
            f'<div style="font-size:0.78rem;color:var(--muted);">TED {html.escape(n["pub"])} · Published {html.escape(n.get("published") or "—")}</div></td>'
            f'<td>{html.escape(n["buyer"])}</td>'
            f'<td><span class="deadline-pill">{html.escape(n.get("deadline") or "Open")}</span></td>'
            f"</tr>"
        )
    if not sample_rows:
        sample_rows.append(
            '              <tr><td colspan="4">Run the live EU TED API v3 query below or our Apify/RapidAPI endpoint to retrieve newly published notices in real time.</td></tr>'
        )

    faq_items = [
        {
            "@type": "Question",
            "name": f"How many active {s['name']} public tenders are open in {c['name']} on EU TED?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"As of {LASTMOD}, the official EU TED Search API v3 lists {fmt_int(open_cnt)} active contract notices (cn-standard) in {c['name']} ({c['iso3']}) matching CPV {s['cpv_label']} with open submission deadlines.",
            },
        },
        {
            "@type": "Question",
            "name": f"Which CPV codes cover {s['name']} public procurement in {c['name']}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"The primary EU Common Procurement Vocabulary (CPV) filter for {s['name']} is {s['cpv_label']} (TED query expression: {s['cpv_query']}), covering {s['summary']}",
            },
        },
        {
            "@type": "Question",
            "name": f"How can I automate daily alerts for {c['name']} {s['name']} tenders?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"You can automate alerts at 0 € via our open-source n8n templates (official-opendata-mcp-n8n-templates) or MCP server (eu-us-opendata-mcp), run scheduled extractions on Apify Store (eu-public-tenders-ted-boamp), or integrate our hosted RapidAPI REST endpoint.",
            },
        },
    ]

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "EU Public Tenders Explorer", "item": f"{SITE_BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "60 Country × Sector Guides", "item": f"{SITE_BASE}/sectors/"},
                    {"@type": "ListItem", "position": 3, "name": f"{c['name']} — {s['name']}", "item": url},
                ],
            },
            {
                "@type": "Dataset",
                "name": f"EU TED Active Public Tenders — {c['name']} × {s['name']} (CPV {s['cpv_label']})",
                "description": meta_desc,
                "url": url,
                "spatialCoverage": f"{c['name']}, European Union",
                "dateModified": LASTMOD,
                "creator": {"@type": "Organization", "name": "Publications Office of the European Union (TED v3)"},
            },
            {"@type": "FAQPage", "mainEntity": faq_items},
        ],
    }

    curl_cmd = (
        f'curl -s -X POST "https://api.ted.europa.eu/v3/notices/search" \\\n'
        f'  -H "Content-Type: application/json" \\\n'
        f'  -d \'{{"query": "{rec["ted_query"]}", "fields": ["publication-number", "notice-title", "buyer-name", "deadline-receipt-tender-date-lot"], "limit": 20}}\''
    )

    sib_html = "\n".join(
        f'          <a class="sector-card" href="./{x["slug"]}.html">'
        f'<strong>{html.escape(x["country"]["name"])} — {html.escape(x["sector"]["name"])}</strong>'
        f'<span class="meta">ISO {x["country"]["iso3"]} · CPV {html.escape(x["sector"]["cpv_label"])}</span>'
        f'<div class="stats"><span>{fmt_int(x["open_tenders_count"])} open tenders</span><span style="color:var(--eu-blue-bright);">View →</span></div>'
        f"</a>"
        for x in siblings
    )

    faq_html = "\n".join(
        f'          <details><summary>{html.escape(q["name"])}</summary><p>{html.escape(q["acceptedAnswer"]["text"])}</p></details>'
        for q in faq_items
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c_name} {s_name} Public Tenders (EU TED CPV {cpv_h}) — Live {LASTMOD[:4]} Guide</title>
  <meta name="description" content="{html.escape(meta_desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{c_name} — {s_name} EU Public Tenders (TED v3)">
  <meta property="og:description" content="{html.escape(meta_desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <link rel="stylesheet" href="../assets/styles.css">
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
{render_header("../")}

  <main>
    <section class="hero">
      <div class="container">
        <div class="breadcrumb">
          <a href="../index.html">EU Public Tenders Explorer</a> ›
          <a href="./index.html">60 Country × Sector Guides</a> ›
          {c_name} — {s_name}
        </div>
        <div class="eyebrow">EU TED v3 · Country {c["iso3"]} ({c["iso2"]}) · CPV {cpv_h} · Updated {LASTMOD}</div>
        <h1>Live EU Public Tenders for {s_name} in {c_name}</h1>
        <p class="hero-lead">
          {html.escape(s["summary"])} Snapshot sourced directly from the official <strong>EU TED Search API v3</strong> for contracting authorities in <strong>{c_name}</strong> (national portal ecosystem: {portal_h}).
        </p>

        <div class="kpi-grid">
          <div class="kpi-card">
            <span class="kpi-val accent">{fmt_int(open_cnt)}</span>
            <span class="kpi-label">Active open calls for tenders (<code>cn-standard</code>, deadline &ge; {LASTMOD})</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val">{cpv_h}</span>
            <span class="kpi-label">Primary EU CPV classification codes</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val ok">{c["iso3"]}</span>
            <span class="kpi-label">Official TED buyer-country code ({c_name})</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val">Zero Key</span>
            <span class="kpi-label">Direct TED v3 API + RapidAPI, Apify &amp; MCP automation</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="panel">
          <h2>Recent Active Open Tenders — {c_name} × {s_name}</h2>
          <p class="section-sub">Verified official notices from <code>api.ted.europa.eu/v3/notices/search</code> (click any notice to inspect full tender documents on <code>ted.europa.eu</code>).</p>
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>CPV</th><th>Notice Title &amp; Reference</th><th>Contracting Authority</th><th>Deadline</th></tr>
              </thead>
              <tbody>
{chr(10).join(sample_rows)}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <h2>Automate {c_name} {s_name} Tender Intelligence &amp; EU Compliance</h2>
        <p class="section-sub">Turn public procurement monitoring into an automated pipeline with our hosted APIs, Pay-Per-Event Apify Actor, free n8n templates, and EU B2B compliance actions:</p>
{render_conversion_rails()}

        <div class="panel" style="margin-top:22px;">
          <h3 style="margin:0 0 6px;">Copy-Paste Official EU TED v3 API Query ({c_name} / {s_name})</h3>
          <p style="margin:0;font-size:0.88rem;color:var(--muted);">Or skip query maintenance and call our edge-cached JSON endpoints on <a href="{RAPIDAPI_TED}" target="_blank" rel="noopener">RapidAPI</a>, <a href="{APIFY_TED_ACTOR}" target="_blank" rel="noopener noreferrer sponsored">Apify Store</a>, or <a href="{MCP_REPO}" target="_blank" rel="noopener">eu-us-opendata-mcp</a>.</p>
          <pre>{html.escape(curl_cmd)}</pre>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>FAQ — {s_name} Procurement in {c_name}</h2>
        <div class="faq-list">
{faq_html}
        </div>

        <h2 style="margin-top:28px;">Related EU Procurement Guides</h2>
        <div class="sector-grid">
{sib_html}
        </div>
      </div>
    </section>
  </main>

{render_footer("../")}
</body>
</html>
"""


def build_directory_page(data: dict) -> str:
    url = f"{SITE_BASE}/sectors/"
    pages = data["pages"]
    countries = data["countries"]
    sectors = data["sectors"]

    c_pills = [f'<button type="button" class="dir-pill" data-country="all" aria-pressed="true">All Countries ({len(pages)})</button>']
    for c in countries:
        c_pills.append(f'<button type="button" class="dir-pill" data-country="{c["slug"]}" aria-pressed="false">{html.escape(c["name"])} ({c["iso2"]})</button>')

    s_pills = ['<button type="button" class="dir-pill" data-sector="all" aria-pressed="true">All 6 Sectors</button>']
    for s in sectors:
        s_pills.append(f'<button type="button" class="dir-pill" data-sector="{s["slug"]}" aria-pressed="false">{html.escape(s["name"])}</button>')

    cards = []
    for p in pages:
        hay = f"{p['country']['name']} {p['country']['iso3']} {p['sector']['name']} {p['sector']['cpv_label']}".lower()
        cards.append(
            f'          <a class="sector-card" href="./{p["slug"]}.html" '
            f'data-country="{p["country"]["slug"]}" data-sector="{p["sector"]["slug"]}" data-search="{html.escape(hay)}">'
            f'<strong>{html.escape(p["country"]["name"])} — {html.escape(p["sector"]["name"])}</strong>'
            f'<span class="meta">ISO {p["country"]["iso3"]} · CPV {html.escape(p["sector"]["cpv_label"])}</span>'
            f'<div class="stats"><span>{fmt_int(p["open_tenders_count"])} active tenders</span><span style="color:var(--eu-blue-bright);">Explore →</span></div>'
            f"</a>"
        )

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": "60 EU Public Tenders Country × CPV Sector Guides", "url": url, "dateModified": LASTMOD},
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "EU Public Tenders Explorer", "item": f"{SITE_BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "60 Country × Sector Guides", "item": url},
                ],
            },
            {
                "@type": "Dataset",
                "name": "EU TED Active Procurement Index — 10 Countries × 6 CPV Sectors",
                "description": "Directory of 60 EU procurement markets tracking live active EU TED v3 calls for tenders across 10 countries and 6 CPV sectors.",
                "url": url,
                "dateModified": LASTMOD,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Which countries and CPV sectors are covered?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The explorer covers 10 major European procurement markets (France, Germany, Spain, Italy, Netherlands, Belgium, Poland, Sweden, Austria, Ireland) across 6 high-value CPV sectors (IT & AI Software, Cybersecurity & Cloud, Construction & Green Energy, Healthcare & Pharma, Engineering & Consulting, Transport & Mobility).",
                        },
                    }
                ],
            },
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>60 EU Public Tenders Guides (10 Countries × 6 CPV Sectors) | TED Open-Data Explorer</title>
  <meta name="description" content="Search and filter 60 EU public procurement markets across 10 European countries and 6 high-value CPV sectors with live EU TED v3 tender counts and API automation.">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="../assets/styles.css">
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
{render_header("../")}

  <main>
    <section class="hero">
      <div class="container">
        <div class="breadcrumb"><a href="../index.html">EU Public Tenders Explorer</a> › 60 Country × Sector Guides</div>
        <div class="eyebrow">10 European Countries × 6 CPV Sectors · Live TED v3 Counts ({LASTMOD})</div>
        <h1>Directory of 60 EU Public Procurement Markets</h1>
        <p class="hero-lead">Filter by country, CPV sector, or keyword to inspect live active EU TED tenders, official buyer notices, and automated alerting recipes.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="controls">
          <div class="field">
            <label for="dir-search">Search country, sector, or CPV code</label>
            <input id="dir-search" type="search" placeholder="e.g. France, Cybersecurity, 72000000, Germany, Healthcare...">
          </div>
        </div>
        <div class="dir-pills">{" ".join(c_pills)}</div>
        <div class="dir-pills">{" ".join(s_pills)}</div>
        <p id="dir-count" style="font-size:0.86rem;color:var(--muted);margin:10px 0;">60 / 60 markets displayed</p>

        <div id="sector-list" class="sector-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <h2>Production APIs, Scrapers, n8n Templates &amp; EU Compliance Toolkits</h2>
        <p class="section-sub">Automate European public procurement alerts and equip your team for 2026–2027 EU compliance:</p>
{render_conversion_rails()}
      </div>
    </section>
  </main>

{render_footer("../")}
  <script>
  (function () {{
    var search = document.getElementById("dir-search");
    var cPills = document.querySelectorAll(".dir-pill[data-country]");
    var sPills = document.querySelectorAll(".dir-pill[data-sector]");
    var cards = document.querySelectorAll("#sector-list .sector-card");
    var count = document.getElementById("dir-count");
    var activeC = "all";
    var activeS = "all";

    function update() {{
      var q = (search && search.value ? search.value : "").trim().toLowerCase();
      var vis = 0;
      for (var i = 0; i < cards.length; i++) {{
        var c = cards[i];
        var ok = (activeC === "all" || c.getAttribute("data-country") === activeC)
          && (activeS === "all" || c.getAttribute("data-sector") === activeS)
          && (!q || (c.getAttribute("data-search") || "").indexOf(q) !== -1);
        c.hidden = !ok;
        if (ok) vis++;
      }}
      if (count) count.textContent = vis + " / " + cards.length + " markets displayed";
    }}

    if (search) search.addEventListener("input", update);
    for (var j = 0; j < cPills.length; j++) {{
      cPills[j].addEventListener("click", function (ev) {{
        var b = ev.currentTarget;
        activeC = b.getAttribute("data-country") || "all";
        for (var k = 0; k < cPills.length; k++) cPills[k].setAttribute("aria-pressed", cPills[k] === b ? "true" : "false");
        update();
      }});
    }}
    for (var m = 0; m < sPills.length; m++) {{
      sPills[m].addEventListener("click", function (ev) {{
        var b = ev.currentTarget;
        activeS = b.getAttribute("data-sector") || "all";
        for (var k = 0; k < sPills.length; k++) sPills[k].setAttribute("aria-pressed", sPills[k] === b ? "true" : "false");
        update();
      }});
    }}
  }})();
  </script>
</body>
</html>
"""


def build_home_page(data: dict) -> str:
    url = f"{SITE_BASE}/"
    pages = data["pages"]
    countries = data["countries"]
    sectors = data["sectors"]
    total_open = sum(int(p.get("open_tenders_count", 0)) for p in pages)
    total_samples = sum(len(p.get("samples", [])) for p in pages)

    c_opts = ['<option value="all">All 10 European Countries</option>'] + [
        f'<option value="{c["slug"]}">{html.escape(c["name"])} ({c["iso3"]})</option>' for c in countries
    ]
    s_opts = ['<option value="all">All 6 CPV Sectors</option>'] + [
        f'<option value="{s["slug"]}">{html.escape(s["name"])} ({html.escape(s["cpv_label"])})</option>' for s in sectors
    ]

    top_markets = sorted(pages, key=lambda p: p["open_tenders_count"], reverse=True)[:12]
    featured_cards = "\n".join(
        f'          <a class="sector-card" href="./sectors/{p["slug"]}.html">'
        f'<strong>{html.escape(p["country"]["name"])} — {html.escape(p["sector"]["name"])}</strong>'
        f'<span class="meta">ISO {p["country"]["iso3"]} · CPV {html.escape(p["sector"]["cpv_label"])}</span>'
        f'<div class="stats"><span>{fmt_int(p["open_tenders_count"])} active tenders</span><span style="color:var(--eu-blue-bright);">Open Guide →</span></div>'
        f"</a>"
        for p in top_markets
    )

    faq_items = [
        {
            "@type": "Question",
            "name": "How is the EU Public Tenders Explorer data sourced?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"All active call-for-tender counts and official notice samples are queried directly from the European Union Publications Office TED Search API v3 (api.ted.europa.eu/v3/notices/search), refreshed {LASTMOD}, covering 10 major EU countries across 6 CPV sectors.",
            },
        },
        {
            "@type": "Question",
            "name": "How can I connect EU TED tenders to Claude, Cursor, n8n, or my CRM?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Use our zero-dependency MIT MCP server (eu-us-opendata-mcp), our 9 free n8n workflow blueprints (official-opendata-mcp-n8n-templates), our hosted RapidAPI REST API (eu-ted-public-tenders-procurement-api), or our Pay-Per-Event Apify Actor (eu-public-tenders-ted-boamp).",
            },
        },
        {
            "@type": "Question",
            "name": "What EU B2B compliance rules affect suppliers bidding on public contracts in 2026–2027?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Software and digital suppliers face EU Cyber Resilience Act Art. 14 reporting (in force since September 11, 2026 — automated via our CRA-SBOM-Guard GitHub Action) and French B2B Factur-X EN 16931 e-invoicing (reception active since September 1, 2026 — supported via FacturKit 2027 and our Factur-X GitHub Action).",
            },
        },
    ]

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "EU Public Tenders & Open-Data Explorer", "url": url, "inLanguage": "en"},
            {
                "@type": "BreadcrumbList",
                "itemListElement": [{"@type": "ListItem", "position": 1, "name": "EU Public Tenders Explorer", "item": url}],
            },
            {
                "@type": "Dataset",
                "name": "EU Public Tenders Open-Data Snapshot (10 Countries × 6 CPV Sectors)",
                "description": f"{fmt_int(total_open)} active EU TED v3 public procurement calls across 60 country-by-sector markets.",
                "url": url,
                "dateModified": LASTMOD,
                "creator": {"@type": "Organization", "name": "Publications Office of the European Union (TED v3)"},
            },
            {"@type": "FAQPage", "mainEntity": faq_items},
        ],
    }

    faq_html = "\n".join(
        f'          <details><summary>{html.escape(q["name"])}</summary><p>{html.escape(q["acceptedAnswer"]["text"])}</p></details>'
        for q in faq_items
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EU Public Tenders &amp; Open-Data Explorer — 60 Country × CPV Sector Markets (TED v3)</title>
  <meta name="description" content="Explore {fmt_int(total_open)} live active EU TED public tenders across 10 European countries and 6 high-value CPV sectors, with direct RapidAPI, Apify, n8n, and MCP automation.">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="EU Public Tenders &amp; Open-Data Explorer (60 Markets)">
  <meta property="og:description" content="Live EU TED v3 public procurement intelligence across 10 European countries × 6 CPV sectors.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <link rel="stylesheet" href="./assets/styles.css">
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
{render_header("./")}

  <main>
    <section class="hero">
      <div class="container">
        <div class="eyebrow">Official EU TED Search API v3 · Updated {LASTMOD} · Zero Sign-Up Required</div>
        <h1>EU Public Tenders &amp; Open-Data Intelligence Explorer</h1>
        <p class="hero-lead">
          Track active European public procurement calls across <strong>10 EU countries × 6 high-value CPV sectors (60 dedicated market guides)</strong> and plug automated tender monitoring straight into <strong>Apify</strong>, <strong>RapidAPI</strong>, <strong>Zyla</strong>, <strong>n8n</strong>, or <strong>Claude / Cursor MCP</strong>.
        </p>

        <div class="kpi-grid">
          <div class="kpi-card">
            <span class="kpi-val accent">{fmt_int(total_open)}</span>
            <span class="kpi-label">Active open calls for tenders (<code>cn-standard</code>, deadline &ge; {LASTMOD})</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val">60 Markets</span>
            <span class="kpi-label">10 European countries × 6 CPV sectors</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val ok">{fmt_int(total_samples)} Notices</span>
            <span class="kpi-label">Verified live sample notices searchable below</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-val">4 Rails</span>
            <span class="kpi-label">Apify · RapidAPI · Zyla · Open-Source MCP &amp; n8n</span>
          </div>
        </div>
      </div>
    </section>

    <section id="explorer" class="section section-alt">
      <div class="container">
        <div id="ted-live-explorer" class="panel" data-snapshot-url="./data/ted_snapshot_60.json" data-page-prefix="./sectors/">
          <h2>Interactive EU Public Tenders Explorer (Zero CORS, Instant Filter)</h2>
          <p class="section-sub">Filter official EU TED v3 active calls for tenders by country, CPV sector, or keyword — and copy the ready-to-run TED v3 API query for your stack.</p>

          <div class="controls">
            <div class="field">
              <label for="ted-country">EU Country</label>
              <select id="ted-country">{"".join(c_opts)}</select>
            </div>
            <div class="field">
              <label for="ted-sector">CPV Sector</label>
              <select id="ted-sector">{"".join(s_opts)}</select>
            </div>
            <div class="field">
              <label for="ted-keyword">Keyword (title, buyer, CPV, TED ID)</label>
              <input id="ted-keyword" type="search" placeholder="e.g. cloud, hospital, solar, AI, railway...">
            </div>
          </div>

          <p id="ted-explorer-status" style="font-size:0.86rem;color:var(--muted);margin:0 0 12px;">Loading official EU TED v3 snapshot...</p>

          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>Country</th><th>CPV &amp; Sector</th><th>Notice Title &amp; Reference</th><th>Buyer</th><th>Deadline</th><th>Guide</th></tr>
              </thead>
              <tbody id="ted-results-tbody">
                <tr><td colspan="6">Loading official TED v3 notices...</td></tr>
              </tbody>
            </table>
          </div>

          <div style="margin-top:16px;">
            <strong style="font-size:0.88rem;">Live EU TED v3 API Query for Current Selection:</strong>
            <pre id="ted-curl-snippet"></pre>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Production APIs, Scrapers, n8n Templates &amp; EU Compliance Toolkits</h2>
        <p class="section-sub">Scale from manual search to automated procurement pipelines and EU tender readiness using our live, audited tools:</p>
{render_conversion_rails()}
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;">
          <div>
            <h2>Top 12 Most Active EU Procurement Markets ({LASTMOD})</h2>
            <p class="section-sub" style="margin-bottom:0;">Ranked by live active TED v3 open calls — or browse all 60 country × sector pages.</p>
          </div>
          <a class="btn-primary" href="./sectors/index.html">Browse all 60 markets →</a>
        </div>
        <div class="sector-grid">
{featured_cards}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>
  </main>

{render_footer("./")}
  <script src="./assets/ted-live.js"></script>
</body>
</html>
"""


def write_sitemap_and_robots(repo_root: Path, pages: list[dict]) -> int:
    urls = [
        (f"{SITE_BASE}/", LASTMOD, "weekly", "1.0"),
        (f"{SITE_BASE}/sectors/", LASTMOD, "weekly", "0.9"),
    ]
    for p in pages:
        urls.append((f"{SITE_BASE}/sectors/{p['slug']}.html", LASTMOD, "monthly", "0.75"))

    entries = [
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for loc, mod, freq, prio in urls
    ]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (repo_root / "sitemap.xml").write_text(xml, encoding="utf-8")
    (repo_root / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE}/sitemap.xml\n", encoding="utf-8")
    return len(urls)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    data = json.loads((repo_root / "data" / "ted_snapshot_60.json").read_text(encoding="utf-8"))
    pages = data["pages"]
    assert len(pages) == 60, f"Expected 60 pages, got {len(pages)}"
    assert len({p["slug"] for p in pages}) == 60, "Duplicate slugs detected"

    out_dir = repo_root / "sectors"
    out_dir.mkdir(parents=True, exist_ok=True)

    (repo_root / "index.html").write_text(build_home_page(data), encoding="utf-8")
    (out_dir / "index.html").write_text(build_directory_page(data), encoding="utf-8")

    for idx, rec in enumerate(pages):
        same_country = [x for x in pages if x["country"]["slug"] == rec["country"]["slug"] and x["slug"] != rec["slug"]]
        same_sector = [x for x in pages if x["sector"]["slug"] == rec["sector"]["slug"] and x["slug"] != rec["slug"]]
        siblings = (same_country[:2] + same_sector[idx % max(1, len(same_sector)):][:2] + same_sector)[:4]
        (out_dir / f"{rec['slug']}.html").write_text(build_sector_page(rec, siblings), encoding="utf-8")

    total_urls = write_sitemap_and_robots(repo_root, pages)
    print(f"Generated index.html + sectors/index.html + {len(pages)} sector pages; sitemap.xml updated ({total_urls} URLs) + robots.txt.")


if __name__ == "__main__":
    main()
