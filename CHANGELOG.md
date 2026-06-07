# Changelog

All notable changes to this project will be documented in this file.
The format follows **Keep a Changelog**. This project adheres to **Semantic Versioning**.

## [1.0.2] - 2026-04-03

### Changed
- **Platform rebrand: OSINT PH → NOsint** — all branding, domain references, and User-Agent strings updated throughout the codebase
- Domain changed from `osintph.info` to `phasm.no` (all subdomains updated)
- GitHub repository renamed from `osintph/darkweb-scanner` to `iamphasm/nosint-darkweb-scanner`
- User-Agent strings updated from `OSINTPH/*` to `NOsint/*`
- Default email domain updated from `intel.osintph.info` to `intel.phasm.no`
- PDF filenames, report IDs, and footers updated to reflect new brand
- Regional focus retargeted from Southeast Asia (Philippines) to Norway/Nordic
- README rewritten for Norwegian deployment context

## [1.0.1] - 2026-03-15

### Added
- **Intelligence Dashboard (Home tab)** — new start page replacing the crawler stats as the default landing page
  - Regional threat level indicator (HIGH/ELEVATED/MODERATE) based on live SEA victim counts
  - KPI bar: RW groups, total victims, press reports, crawl hits, seeds, keywords
  - Live recent victims feed from ransomware.live PRO
  - Top active groups ranked by victim count with SEA targeting flags
  - SEA victim breakdown bar chart by country (PH, ID, MY, TH, VN, SG) with real counts
  - ThreatFox IOC mini-feed (latest 8 IOCs)
  - Ransomware press feed filtered for SEA-relevant articles
  - Quick actions grid for common workflows
  - System status panel showing all API/service health
- **ransomware.live PRO API integration** (`ransomware_live.py` + `ransomware_live_routes.py`)
  - Full PRO API client covering all documented endpoints: groups, victims, IOCs, negotiations, press, ransom notes, YARA rules, SEC 8-K filings, CSIRT directory, sectors
  - `/api/rwlive/*` Flask blueprint with 20+ endpoints
  - Graceful fallback to unauthenticated v2 API when no PRO key is set
  - Local `RANSOMWARE_GROUPS` data merged with live API data for SEA context enrichment
  - Composite endpoints for single-call data bundles (`/api/rwlive/home-data`, `/api/rwlive/ransomware-tab-data`)
  - SEA-specific convenience endpoints (`/api/rwlive/victims/sea`, `/api/rwlive/press/recent?sea=1`)
- **IOC Feed tab** — live indicators of compromise with sub-tabs for ThreatFox, URLhaus, and Feodo Tracker
  - Stats bar: total IOCs, IPs, domains, URLs, hashes
  - Searchable/filterable table with type chips, malware family, confidence bars, reporter
  - All feeds proxied through backend to avoid CORS restrictions
- **Backend proxy routes** in `dashboard_routes.py`
  - `POST /api/proxy/threatfox` — ThreatFox API proxy with `Auth-Key` header injection
  - `POST /api/proxy/urlhaus` — URLhaus recent URLs proxy
  - `GET /api/proxy/feodo` — Feodo Tracker C2 blocklist proxy
  - `GET /api/whiteintel/alerts` — WhiteIntel credential alerts proxy
  - `GET /api/whiteintel/search` — WhiteIntel domain search proxy
- **Crawls tab** — renamed from "Dashboard" tab, preserves all existing crawler session/stats UI
- New environment variables: `RANSOMWARE_LIVE_API_KEY`, `THREATFOX_API_KEY`, `WHITEINTEL_API_KEY`

### Changed
- Default landing page is now the Intelligence Dashboard (Home tab) instead of the Crawls tab
- Nav tab order updated: Dashboard (Home) → Crawls → Keywords → Seeds → ... → IOC Feed → ...
- `ransomware_live.py` press endpoints now correctly unwrap `{results:[...]}` response wrapper from PRO API
- SEA victim counts now fetch up to 500 victims per country instead of capped at 20
- Group display on Home tab uses live victim counts from ransomware.live (not local static data)

### Fixed
- ThreatFox 401 errors — correct `Auth-Key` header now used (was `API-KEY`)
- JS syntax errors from nested quotes in `querySelector` `onclick` attributes — replaced with `hdGoTo()` helper
- Press feed returning empty — PRO API wraps response in `{results:[...]}` which is now unwrapped
- SEA breakdown bars all showing 20 — removed per-country cap, now shows real counts

## [1.0.0] - 2026-03-10

### Added
- **DNSDumpster enrichment** — `POST /api/dns/investigations/<id>/enrich` fetches additional passive DNS records from DNSDumpster and merges them into the investigation; requires `DNSDUMPSTER_API_KEY` in `.env`
- **Certificate Transparency tab** — dedicated Cert History view in the DNS tab
  - Live fetch from crt.sh with stat strip: total certs, active, expired, expiring soon, unique SANs
  - Certificate issuers bar chart and issuance-by-year timeline chart
  - SAN list with copy-to-clipboard button
  - Full cert table with 50-row pagination and colour-coded status (active / expiring / expired)
- **OSINT Toolkit tab** — seven proxied OSINT tools accessible directly from the dashboard without leaving the UI: Shodan, Censys, GreyNoise, URLScan, MXToolbox, SecurityTrails, and VirusTotal; plus curated OSINT resource links
- **PDF world map** — Infrastructure Recon PDF now includes a real world map (Playwright + jsvectormap screenshot) with active country markers; layout updated so map appears between the pie charts and ASN table on page 1
- **PDF certificate section** — rich Certificate Transparency section in PDF export with stat strip, issuer bar chart, issuance timeline, and full colour-coded cert table
- `playwright>=1.40` added to dependencies; Chromium installed at Docker build time for server-side map rendering

### Changed
- PDF Infrastructure Overview layout: world map now sits between the overview charts and the ASN detail table on page 1; subdomain graph moved to its own page
- Docker app image now installs Chromium system dependencies and runs `playwright install chromium` during build — no manual setup required

### Fixed
- `GET /api/dns/certs/<domain>` route now registered with `strict_slashes=False` to handle trailing slash variants
- Cert history 502 errors caused by nginx timeout on slow crt.sh responses — resolved by reducing default request timeout

## [0.9.1] - 2026-03-07

### Fixed
- `genProjectSelect` dropdown not populating with projects on Keywords tab load
- API returns plain array but code was reading `pd.projects` — fixed to `Array.isArray(pd)`
- `.panel` CSS `overflow:hidden` was clipping the dropdown — changed to `visible`
- Flask template cache required `docker compose restart` to pick up changes

### Changed
- `_populateGenProjectDropdown()` extracted as standalone function, called on tab switch

## [0.9.0] - 2026-03-09

### Added
- **Active subdomain brute-force** (`dns_crawler.py`)
  - 100-entry built-in wordlist covering common prefixes: `www`, `api`, `mail`, `vpn`, `dev`, `staging`, `admin`, `portal`, `git`, `ci`, `monitor`, `db`, and more
  - Runs in parallel (50 workers) via `ThreadPoolExecutor` — typically completes in under 5 seconds
  - Results tagged with `source: bruteforce` to distinguish from passive discovery
- **TCP port scanner** — 30 common ports, per-port timeout configurable, returns open/closed/filtered
- **HTTP/HTTPS directory enumeration** — probes 70 common paths, surfaces all non-404 responses with status, content-length, and redirect destination
- **Two new API endpoints**: `POST /api/dns/investigations/<id>/scan` and `GET /api/dns/investigations/<id>/scan/status`
- **Redesigned DNS tab UI** — six view tabs: Graph, Subdomains, Ports, Directories, Email Security, DNS Records
- **Channel Monitor tab** — on-demand Telegram channel scraping from the dashboard
  - Auto-translates messages to English via `deep-translator`
  - Downloads photos and videos; packages results as a ZIP
  - Live streaming log with job history

### Changed
- `dns_crawler.py` — `run_dns_recon()` now includes Phase 2b (active brute-force) automatically
- `app.py` — registers `channel_monitor_bp` blueprint
- `pyproject.toml` — adds `deep-translator` and `langdetect` to dashboard dependencies

## [0.6.0] - 2026-02-23

### Added
- **PostgreSQL migration** — platform now runs on PostgreSQL 16 (was SQLite)
  - `postgres:16-alpine` service added to Docker Compose
  - `pg_data` named volume for persistent storage

## [0.5.0] - 2026-02-22

### Added
- **Web Check integration** — on-demand OSINT analysis for any domain as a separate Docker service
- **Projects feature** — scoped monitoring engagements with per-project keywords, domains, entities, and hit tracking
- **Paste Monitor** — monitors rentry.co for keyword hits
- **Telegram scraper enhancements** — expanded to 49 channels covering SEA/PH threat intel

## [0.4.0] - 2026-02-21

### Added
- DNS Reconnaissance module — passive + active DNS recon, zone transfer attempts, crt.sh enumeration, HackerTarget subdomain discovery, geolocation, SPF/DMARC/DKIM analysis, PDF export

## [0.3.0] - 2026-02-15

### Added
- Curated daily threat intelligence digest — CISA KEV, OTX pulses, URLhaus, Feodo Tracker, RSS feeds; PDF generation and HTML email delivery via Mailgun

## [0.2.0] - 2026-02-01

### Added
- IP Investigation module — AbuseIPDB + VirusTotal lookups with history
- Ransomware tracker — 12+ active groups with SEA victim focus
- Threat actor profiles — APT and criminal groups targeting SEA
- Telegram channel scraper — monitors configurable public channels
- TOTP two-factor authentication and OAuth (Google/GitHub)
- PDF report generation via ReportLab
- Role-based access control (admin / analyst)

## [0.1.0] - 2024-01-01

### Added
- Async BFS crawler with configurable depth and concurrency
- Tor circuit rotation via stem
- Keyword scanner with category support and context windows
- SQLite and PostgreSQL storage backends via SQLAlchemy
- Webhook and email alerting
- Flask dashboard with real-time hit viewer
- Docker Compose setup
- CLI with `scan`, `stats`, `hits`, `check-tor` commands 
