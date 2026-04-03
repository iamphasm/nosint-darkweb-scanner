# NOsint — Threat Intelligence Platform for Norway

An open-source, self-hosted threat intelligence platform focused on the Norwegian cybersecurity landscape.

NOsint is a rewrite and regional adaptation of the original [OSINT PH platform](https://github.com/osintph/darkweb-scanner) by Sigmund Brandstaetter, retargeted for Norway and the Nordic region.

**Version: 1.1.0 · License: AGPL v3**

---

## Installation

### Requirements

- A Linux server (Ubuntu 24.04 recommended)
- A domain name pointing to your server (optional, required for SSL)

### One-command deploy

```bash
curl -fsSL https://raw.githubusercontent.com/iamphasm/nosint-darkweb-scanner/main/deploy.sh -o /tmp/deploy.sh && sudo bash /tmp/deploy.sh
```

With domain and SSL:

```bash
DOMAIN=yourdomain.no SSL_EMAIL=you@yourdomain.no sudo bash /tmp/deploy.sh
```

The script installs Docker, clones the repo, configures Tor, generates secrets, sets up Nginx with Let's Encrypt SSL, and registers an admin user. You will have a running dashboard in approximately 10 minutes.

### Manual setup

```bash
git clone https://github.com/iamphasm/nosint-darkweb-scanner.git
cd nosint-darkweb-scanner
cp .env.example .env
# Edit .env with your API keys and domain
docker compose up -d
```

---

## Configuration

Key `.env` variables:

| Variable | Description |
|----------|-------------|
| `DOMAIN` | Your domain (e.g. `nti.phasm.no`) |
| `SSL_EMAIL` | Email for Let's Encrypt |
| `DATABASE_URL` | SQLite (default) or PostgreSQL |
| `DIGEST_TIMEZONE` | Timezone for daily digest (default: `Europe/Oslo`) |
| `MAILGUN_API_KEY` | Mailgun key for email delivery |
| `ABUSEIPDB_API_KEY` | AbuseIPDB for IP investigation |
| `VIRUSTOTAL_API_KEY` | VirusTotal for IP/domain lookups |
| `OTX_API_KEY` | AlienVault OTX threat feeds |
| `RANSOMWARE_LIVE_API_KEY` | Ransomware.live PRO API |
| `HIBP_API_KEY` | Have I Been Pwned breach lookups |
| `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` | Telegram channel monitoring |

See `.env.example` for the full list.

---

## Features

> Features are documented here as they are verified working. This list grows with each release.

- **Dark web scanner** — Crawls .onion sites over Tor, matches configurable keywords, stores hits with full context (URL, depth, surrounding text). Alerts via webhook or email on hits.

*(More features will be documented as they are verified in the Norwegian deployment)*

---

## Credits

Based on the original [OSINT PH darkweb-scanner](https://github.com/osintph/darkweb-scanner) by Sigmund Brandstaetter — an open-source threat intelligence platform built for the Philippine cybersecurity landscape. This project adapts and extends that work for Norway and the Nordic region.

---

## License

[AGPL v3](LICENSE)
