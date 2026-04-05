"""
Threat actor profiles — Norway/Nordic focused intelligence database.
"""

THREAT_ACTORS = [
    {
        "name": "APT28",
        "slug": "apt28",
        "aliases": ["Fancy Bear", "STRONTIUM", "Sofacy", "Forest Blizzard", "Pawn Storm"],
        "origin": "Russia",
        "type": "nation-state",
        "status": "active",
        "risk_level": "critical",
        "first_seen": "2004",
        "targeting_nordic": True,
        "sectors": ["government", "defense", "energy", "media", "political parties"],
        "countries_targeted": ["Norway", "Germany", "USA", "Ukraine", "NATO members"],
        "description": (
            "Russian GRU Unit 26165 — one of the most active and aggressive APT groups globally. "
            "Conducted the 2020 cyberattack on Norway's parliament (Stortinget), exfiltrating "
            "emails from MPs and party staff. Targets Norwegian defense contractors, political "
            "organisations, and NATO infrastructure. Known for credential phishing using "
            "lookalike domains and exploitation of public-facing services."
        ),
        "ttps": [
            "spear phishing", "credential harvesting", "X-Agent implant",
            "Zebrocy malware", "living-off-the-land", "VPN exploitation",
            "OAuth token theft", "lookalike domain registration"
        ],
        "known_malware": ["X-Agent", "Zebrocy", "Sofacy", "CHOPSTICK", "SOURFACE"],
        "keywords": ["apt28", "fancy bear", "strontium", "sofacy", "forest blizzard", "pawn storm"],
    },
    {
        "name": "APT29",
        "slug": "apt29",
        "aliases": ["Cozy Bear", "NOBELIUM", "Midnight Blizzard", "The Dukes", "YTTRIUM"],
        "origin": "Russia",
        "type": "nation-state",
        "status": "active",
        "risk_level": "critical",
        "first_seen": "2008",
        "targeting_nordic": True,
        "sectors": ["government", "foreign policy", "think tanks", "defence", "energy"],
        "countries_targeted": ["Norway", "USA", "UK", "Germany", "Netherlands", "NATO members"],
        "description": (
            "Russian SVR (Foreign Intelligence Service) group. Highly sophisticated, patient, "
            "and stealthy. Conducted the SolarWinds supply chain attack affecting global "
            "government and enterprise targets including Norwegian entities. Targets Norwegian "
            "Ministry of Foreign Affairs and defence-adjacent organisations for political "
            "intelligence. Known for long-dwell-time intrusions with minimal detection footprint."
        ),
        "ttps": [
            "supply chain compromise", "spear phishing", "OAuth abuse",
            "cloud service abuse", "living-off-the-land", "password spraying",
            "MFA bypass", "trusted relationship exploitation"
        ],
        "known_malware": ["SUNBURST", "SUNSPOT", "WellMess", "WellMail", "MiniDuke", "CosmicDuke"],
        "keywords": ["apt29", "cozy bear", "nobelium", "midnight blizzard", "the dukes"],
    },
    {
        "name": "Sandworm",
        "slug": "sandworm",
        "aliases": ["VOODOO BEAR", "Seashell Blizzard", "IRIDIUM", "Unit 74455"],
        "origin": "Russia",
        "type": "nation-state",
        "status": "active",
        "risk_level": "critical",
        "first_seen": "2009",
        "targeting_nordic": True,
        "sectors": ["critical infrastructure", "energy", "industrial control systems", "government"],
        "countries_targeted": ["Ukraine", "Norway", "USA", "Georgia", "NATO members"],
        "description": (
            "Russian GRU Unit 74455 — responsible for the most destructive cyberattacks on "
            "record including NotPetya, attacks on Ukrainian power grids, and Olympic Destroyer. "
            "Norway's energy sector (including Equinor and offshore oil infrastructure) is a "
            "high-priority target given its role as Europe's primary gas supplier. "
            "Capable of attacks on industrial control systems (ICS/SCADA) and OT networks."
        ),
        "ttps": [
            "ICS/SCADA attacks", "wiper malware", "supply chain compromise",
            "spear phishing", "VPNFilter router compromise", "Industroyer deployment",
            "living-off-the-land", "lateral movement via trusted tools"
        ],
        "known_malware": ["NotPetya", "BlackEnergy", "Industroyer", "Cyclops Blink", "Olympic Destroyer"],
        "keywords": ["sandworm", "voodoo bear", "seashell blizzard", "notpetya", "industroyer"],
    },
    {
        "name": "Turla",
        "slug": "turla",
        "aliases": ["Snake", "Uroburos", "Waterbug", "Venomous Bear", "Secret Blizzard"],
        "origin": "Russia",
        "type": "nation-state",
        "status": "active",
        "risk_level": "critical",
        "first_seen": "2004",
        "targeting_nordic": True,
        "sectors": ["government", "foreign ministries", "defence", "embassies", "military"],
        "countries_targeted": ["Norway", "Germany", "France", "Ukraine", "NATO members"],
        "description": (
            "Highly sophisticated FSB-attributed group conducting long-term espionage campaigns "
            "against Western governments. Known for satellite-based C2 infrastructure and "
            "hijacking other APT groups' implants. Targets Norwegian foreign ministry and "
            "NATO-affiliated organisations. Operates with extreme patience — intrusions may "
            "persist undetected for years."
        ),
        "ttps": [
            "satellite-based C2", "hijacking other APT infrastructure",
            "kernel-level rootkits", "spear phishing", "watering hole",
            "COM object hijacking", "PDF exploit delivery"
        ],
        "known_malware": ["Snake/Uroburos", "Carbon", "Kazuar", "HyperStack", "TinyTurla"],
        "keywords": ["turla", "snake", "uroburos", "waterbug", "venomous bear", "secret blizzard"],
    },
    {
        "name": "Lazarus Group",
        "slug": "lazarus",
        "aliases": ["HIDDEN COBRA", "Guardians of Peace", "Zinc", "APT38", "TraderTraitor"],
        "origin": "North Korea",
        "type": "nation-state",
        "status": "active",
        "risk_level": "critical",
        "first_seen": "2009",
        "targeting_nordic": True,
        "sectors": ["finance", "cryptocurrency", "defence", "aerospace", "blockchain"],
        "countries_targeted": ["Norway", "Global", "South Korea", "USA", "Japan"],
        "description": (
            "North Korean state-sponsored group primarily targeting financial institutions "
            "and cryptocurrency platforms for hard currency generation to fund the regime. "
            "Norwegian crypto exchanges and blockchain companies are active targets. "
            "Also conducts espionage against Norwegian defence contractors and aerospace firms. "
            "Uses sophisticated job-lure social engineering (TraderTraitor campaign)."
        ),
        "ttps": [
            "cryptocurrency theft", "SWIFT targeting", "supply chain attacks",
            "job-themed spear phishing", "watering hole", "macOS malware",
            "LinkedIn luring", "trojanised developer tools"
        ],
        "known_malware": ["BLINDINGCAN", "AppleJeus", "COPPERHEDGE", "TraderTraitor toolkit"],
        "keywords": ["lazarus group", "hidden cobra", "apt38", "zinc", "tradertraitor"],
    },
    {
        "name": "Killnet",
        "slug": "killnet",
        "aliases": ["KillNet"],
        "origin": "Russia",
        "type": "hacktivist",
        "status": "active",
        "risk_level": "high",
        "first_seen": "2022",
        "targeting_nordic": True,
        "sectors": ["government", "critical infrastructure", "healthcare", "airports", "finance"],
        "countries_targeted": ["Norway", "NATO members", "USA", "Germany", "Finland"],
        "description": (
            "Pro-Russia hacktivist collective conducting politically motivated DDoS campaigns. "
            "Targeted Norwegian government websites and financial services following Norway's "
            "support for Ukraine. Operates via Telegram, recruiting volunteer botnet participants "
            "via DDoSia tool. Attacks are largely disruptive rather than destructive but "
            "have caused significant outages to public-facing government services."
        ),
        "ttps": [
            "DDoS", "DDoSia botnet tool", "Telegram coordination",
            "hacktivist recruitment", "Layer 7 HTTP floods", "amplification attacks"
        ],
        "known_malware": ["DDoSia"],
        "keywords": ["killnet", "kill net"],
    },
    {
        "name": "NoName057(16)",
        "slug": "noname057",
        "aliases": ["NoName", "NNNN"],
        "origin": "Russia",
        "type": "hacktivist",
        "status": "active",
        "risk_level": "high",
        "first_seen": "2022",
        "targeting_nordic": True,
        "sectors": ["government", "transport", "finance", "media", "critical infrastructure"],
        "countries_targeted": ["Norway", "NATO members", "Poland", "Czech Republic", "Denmark"],
        "description": (
            "Pro-Russia hacktivist group and one of the most active DDoS operators targeting "
            "NATO-aligned countries. Has conducted multiple documented attacks against Norwegian "
            "targets including Avinor (airports), Norwegian parliament websites, and public "
            "transport systems. Coordinates attacks via Telegram and distributes DDoSia, a "
            "volunteer DDoS tool with thousands of participants."
        ),
        "ttps": [
            "DDoS", "DDoSia volunteer tool", "Telegram coordination",
            "HTTP/HTTPS flooding", "target selection via Telegram voting"
        ],
        "known_malware": ["DDoSia"],
        "keywords": ["noname057", "no name 057", "noname05716"],
    },
    {
        "name": "TA505",
        "slug": "ta505",
        "aliases": ["Hive0065", "GRACEFUL SPIDER", "Evil Corp adjacent"],
        "origin": "Russia",
        "type": "cybercriminal",
        "status": "active",
        "risk_level": "high",
        "first_seen": "2014",
        "targeting_nordic": True,
        "sectors": ["finance", "retail", "healthcare", "manufacturing"],
        "countries_targeted": ["Norway", "Germany", "UK", "USA", "Scandinavia"],
        "description": (
            "Financially motivated threat actor known for large-scale malspam campaigns "
            "delivering banking trojans and ransomware. Norwegian financial institutions "
            "and enterprises are targets of credential harvesting and Dridex delivery campaigns. "
            "Has distributed FlawedAmmyy RAT and SDBbot across European targets including "
            "Scandinavian banks and retail chains."
        ),
        "ttps": [
            "malspam campaigns", "macro documents", "Dridex delivery",
            "Get2 downloader", "FlawedAmmyy RAT", "SDBbot", "Cl0p ransomware delivery"
        ],
        "known_malware": ["Dridex", "FlawedAmmyy", "SDBbot", "Get2", "Cl0p"],
        "keywords": ["ta505", "graceful spider", "hive0065"],
    },
    {
        "name": "ShinyHunters",
        "slug": "shinyhunters",
        "aliases": ["Shiny Hunters"],
        "origin": "Unknown (suspected French/Moroccan)",
        "type": "cybercriminal",
        "status": "active",
        "risk_level": "high",
        "first_seen": "2020",
        "targeting_nordic": True,
        "sectors": ["technology", "e-commerce", "finance", "telecom"],
        "countries_targeted": ["Global", "Norway", "Europe", "USA"],
        "description": (
            "Prolific data breach group that steals and sells large databases on BreachForums "
            "and dark web markets. Norwegian and Nordic companies in technology and e-commerce "
            "sectors are targets. Known for exploiting misconfigured cloud storage and "
            "exposed developer credentials to access production databases."
        ),
        "ttps": [
            "cloud misconfiguration exploitation", "credential stuffing",
            "exposed API key abuse", "database exfiltration", "BreachForums sales"
        ],
        "known_malware": [],
        "keywords": ["shinyhunters", "shiny hunters", "breachforums shinyhunters"],
    },
    {
        "name": "REvil / Sodinokibi Remnants",
        "slug": "revil",
        "aliases": ["Sodinokibi", "GOLD SOUTHFIELD", "REvil remnants"],
        "origin": "Russia",
        "type": "cybercriminal",
        "status": "active",
        "risk_level": "high",
        "first_seen": "2019",
        "targeting_nordic": True,
        "sectors": ["manufacturing", "legal", "finance", "agriculture", "technology"],
        "countries_targeted": ["Norway", "Europe", "USA", "Global"],
        "description": (
            "REvil (Sodinokibi) was one of the most prolific RaaS operations before Russian "
            "law enforcement arrests in 2022. Former affiliates and infrastructure have since "
            "migrated to other operations (RansomHub, BlackSuit). Norwegian manufacturing "
            "and legal sector firms remain targets of successor operations using REvil-derived "
            "techniques and repurposed affiliate networks."
        ),
        "ttps": [
            "RaaS", "double extortion", "Kaseya VSA exploitation",
            "supply chain attacks", "affiliate network", "data leak site"
        ],
        "known_malware": ["REvil/Sodinokibi", "GandCrab (predecessor)"],
        "keywords": ["revil", "sodinokibi", "gold southfield", "revil ransomware"],
    },
]

# All keywords for cross-referencing with hit database
THREAT_ACTOR_KEYWORDS = list({
    kw
    for actor in THREAT_ACTORS
    for kw in actor.get("keywords", [])
})
