"""
Paste site monitor — polls public paste sites for Nordic/Norwegian patterns.

Active sources:
  - pastebin.com/archive  (public archive listing, no API key needed)
  - rentry.co/recent      (confirmed working)
  - pastes.io             (public pastes listing)

Excluded:
  - termbin.com: write-only netcat service, no public listing endpoint
  - controlc.com: removed public recent page
  - hastebin.com: returns errors (endpoint dead)
  - ghostbin.com: domain dead
  - psbdmp.ws: API down
"""
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15
POLL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── Nordic pattern definitions ──────────────────────────────────────────────────

NORDIC_PATTERNS = {
    # Norwegian mobile: +47 followed by 8 digits starting with 4 or 9
    "nordic_mobile":    re.compile(r'(\+47[\s-]?)?\b[49]\d{7}\b'),
    # Nordic country-code TLDs
    "nordic_tld":       re.compile(r'\b[\w.-]+\.(no|se|dk|fi|is)\b', re.IGNORECASE),
    # Norwegian government/municipality domains
    "nordic_gov":       re.compile(r'\b[\w.-]+\.(dep|kommune|stat|mil)\.no\b', re.IGNORECASE),
    # Nordic/Norwegian bank names
    "nordic_bank":      re.compile(
        r'\b(DNB|Nordea|SpareBank\s*1?|Handelsbanken|Santander\s*Bank|'
        r'Storebrand|Gjensidige|KLP|Kommunalbanken|Sbanken|Bulder\s*Bank|'
        r'Norwegian\s*Bank)\b',
        re.IGNORECASE,
    ),
    # Norwegian personnummer: DDMMYY + 5 digits (11 digits total)
    "no_personnummer":  re.compile(
        r'\b(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}[\s-]?\d{5}\b'
    ),
    # Swedish personnummer: YYYYMMDD-NNNN or YYMMDD[-+]\d{4}
    "se_personnummer":  re.compile(
        r'\b(?:(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])|'
        r'\d{6})[-+]\d{4}\b'
    ),
    # Danish CPR: DDMMYY-NNNN
    "dk_cpr":           re.compile(
        r'\b(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}-\d{4}\b'
    ),
    # Norwegian organization number: 9 digits starting with 8 or 9 (optionally spaced NNN NNN NNN)
    "no_orgnr":         re.compile(r'\b[89]\d{2}[\s]?\d{3}[\s]?\d{3}\b'),
}

CONTEXT_WINDOW = 120  # chars around match to capture as context


@dataclass
class PasteSource:
    name: str
    archive_url: str
    base_url: str
    poll_interval: int  # seconds
    last_polled: float = field(default=0.0)
    enabled: bool = field(default=True)

    def is_due(self) -> bool:
        return self.enabled and (time.time() - self.last_polled >= self.poll_interval)

    def mark_polled(self):
        self.last_polled = time.time()


SOURCES = [
    PasteSource("pastebin",  "https://pastebin.com/archive",    "https://pastebin.com",  300),
    PasteSource("rentry",    "https://rentry.co/recent",        "https://rentry.co",     300),
    PasteSource("pastesio",  "https://pastes.io/public",        "https://pastes.io",     300),
]


def _safe_get(url: str, timeout: int = REQUEST_TIMEOUT) -> Optional[requests.Response]:
    try:
        r = requests.get(url, headers=POLL_HEADERS, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        logger.warning(f"Paste fetch failed {url}: {e}")
        return None


def _extract_context(text: str, match) -> str:
    start = max(0, match.start() - CONTEXT_WINDOW)
    end = min(len(text), match.end() + CONTEXT_WINDOW)
    return text[start:end].replace('\n', ' ').strip()


def scan_paste_content(text: str, url: str, paste_id: str,
                       source_name: str, storage) -> int:
    """Scan paste text against Nordic patterns. Returns number of hits saved."""
    hits = 0
    seen_patterns = set()

    for pattern_name, regex in NORDIC_PATTERNS.items():
        for match in regex.finditer(text):
            key = (pattern_name, match.group(0)[:50])
            if key in seen_patterns:
                continue
            seen_patterns.add(key)

            context = _extract_context(text, match)
            storage.save_paste_hit(
                paste_id=paste_id,
                url=url,
                source=source_name,
                matched_pattern=pattern_name,
                matched_value=match.group(0)[:200],
                context=context,
            )
            hits += 1

    return hits


# ── Source-specific scrapers ───────────────────────────────────────────────────

def _get_pastebin_urls() -> list[tuple[str, str]]:
    """Scrape pastebin.com/archive for recent public pastes."""
    r = _safe_get("https://pastebin.com/archive")
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Pastebin paste IDs: 8 alphanumeric chars
        if re.match(r"^/[a-zA-Z0-9]{8}$", href):
            paste_id = href.strip("/")
            results.append((paste_id, f"https://pastebin.com/raw/{paste_id}"))
    return results[:50]


def _get_rentry_urls() -> list[tuple[str, str]]:
    r = _safe_get("https://rentry.co/recent")
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.match(r"^/[a-zA-Z0-9_-]{4,20}$", href) and href not in (
            '/recent', '/new', '/login', '/register', '/raw'
        ):
            paste_id = href.strip("/")
            results.append((paste_id, f"https://rentry.co{href}/raw"))
    return results[:50]



def _get_pastesio_urls() -> list[tuple[str, str]]:
    r = _safe_get("https://pastes.io/public")
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # pastes.io slugs: alphanumeric, 6–16 chars
        if re.match(r"^/[a-zA-Z0-9_-]{6,16}$", href) and href not in (
            '/public', '/new', '/login', '/register', '/trending'
        ):
            paste_id = href.strip("/")
            results.append((paste_id, f"https://pastes.io/raw/{paste_id}"))
    return results[:50]


SOURCE_SCRAPERS = {
    "pastebin": _get_pastebin_urls,
    "rentry":   _get_rentry_urls,
    "pastesio": _get_pastesio_urls,
}


def probe_sources() -> dict:
    """Test which sources are reachable. Returns {source_name: bool}."""
    results = {}
    for source in SOURCES:
        scraper = SOURCE_SCRAPERS.get(source.name)
        if not scraper:
            results[source.name] = False
            continue
        try:
            urls = scraper()
            results[source.name] = len(urls) > 0
            logger.info(f"probe {source.name}: {len(urls)} URLs found")
        except Exception as e:
            results[source.name] = False
            logger.warning(f"probe {source.name} failed: {e}")
    return results


# ── Main monitor loop ──────────────────────────────────────────────────────────

def run_paste_monitor(storage, single_run: bool = False) -> dict:
    """
    Poll all paste sources and scan new pastes for Nordic patterns.
    If single_run=True, poll all sources once and return.
    Returns summary dict.
    """
    total_scanned = 0
    total_hits = 0
    total_new = 0

    for source in SOURCES:
        if not single_run and not source.is_due():
            continue

        scraper = SOURCE_SCRAPERS.get(source.name)
        if not scraper:
            continue

        logger.info(f"Polling {source.name}...")
        try:
            paste_urls = scraper()
        except Exception as e:
            logger.warning(f"Scraper error {source.name}: {e}")
            source.mark_polled()
            continue

        logger.info(f"{source.name}: found {len(paste_urls)} pastes")

        for paste_id, raw_url in paste_urls:
            if storage.is_paste_seen(source.name, paste_id):
                continue

            total_new += 1
            r = _safe_get(raw_url)
            if not r:
                storage.mark_paste_seen(source.name, paste_id, raw_url, had_hits=False)
                continue

            text = r.text
            if len(text) > 500_000:
                storage.mark_paste_seen(source.name, paste_id, raw_url, had_hits=False)
                continue

            hits = scan_paste_content(text, raw_url, paste_id, source.name, storage)
            storage.mark_paste_seen(source.name, paste_id, raw_url, had_hits=hits > 0)
            total_scanned += 1
            total_hits += hits

            if hits > 0:
                logger.info(f"[{source.name}] {paste_id} — {hits} Nordic pattern hits")

            time.sleep(0.3)

        source.mark_polled()

    return {
        "scanned": total_scanned,
        "new_pastes": total_new,
        "hits": total_hits,
        "timestamp": datetime.utcnow().isoformat(),
    }
