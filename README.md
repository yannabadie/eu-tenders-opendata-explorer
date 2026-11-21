# EU Public Tenders & Open-Data Explorer (60 Country × CPV Sector Pages)

Static, zero-backend (`0.00 €/mo`) European public procurement intelligence portal covering **10 EU countries × 6 high-value CPV sectors (60 programmatic SEO pages)** built on live **EU TED Search API v3 (`api.ted.europa.eu/v3/notices/search`)** data.

- **Live Portal (GitHub Pages)**: https://yannabadie.github.io/eu-tenders-opendata-explorer/
- **60 Sector Directory**: https://yannabadie.github.io/eu-tenders-opendata-explorer/sectors/
- **Official Data Source**: European Union Tenders Electronic Daily (TED API v3, zero-key public open data).

## Regenerate Deterministically

```bash
python3 scripts/build_sectors.py
```

Generates `index.html`, `sectors/index.html`, `60` `/sectors/<country>-<sector>.html` pages with `FAQPage` + `Dataset` + `BreadcrumbList` JSON-LD, `sitemap.xml` (`62` URLs), and `robots.txt`.

## Production Automation & Hosted APIs

- **Hosted REST API (RapidAPI Hub)**: [EU TED Public Tenders Procurement API](https://rapidapi.com/YannAbadie/api/eu-ted-public-tenders-procurement-api) & [EU & US Official Open-Data Intelligence (5-in-1)](https://rapidapi.com/YannAbadie/api/eu-us-official-open-data-intelligence1)
- **Zyla API Hub (`80 %` Creator Hub)**: Edge-cached Cloudflare Worker Open-Data syndication
- **Apify Pay-Per-Event Actor (`$3–4 / 1k`, `$5/mo` free credits)**: [EU Public Tenders (TED + BOAMP) Actor](https://apify.com/yannabadie/eu-public-tenders-ted-boamp?fpr=zuvzfw) *(partner link)*
- **Open-Source MCP Server & n8n Templates (MIT)**: [`eu-us-opendata-mcp`](https://github.com/yannabadie/eu-us-opendata-mcp) · [`official-opendata-mcp-n8n-templates`](https://github.com/yannabadie/official-opendata-mcp-n8n-templates)
- **EU B2B Compliance Toolkits**: [FacturKit 2027 (Factur-X)](https://yannabadie.github.io/facturkit-2027/) · [CRA-SBOM-Guard (GitHub Marketplace)](https://github.com/marketplace/actions/cra-sbom-guard-eu-cyber-resilience-act-art-14-scanner) · [Factur-X Validator (GitHub Marketplace)](https://github.com/marketplace/actions/factur-x-france-2026-2027-validator-en-16931-pdf-a-3)

## License

MIT — Official EU TED notice metadata reproduced under EU Open Data / TED reuse rules.
