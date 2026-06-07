"""
Flask application factory — wires up auth + dashboard blueprints.
"""

import logging
import os
import threading
import time
from datetime import timedelta

from flask import Flask, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger(__name__)

PASTE_SCAN_INTERVAL = int(os.getenv("PASTE_SCAN_INTERVAL", "420"))  # 7 minutes default


def _paste_monitor_loop():
    """Background thread: run paste monitor every PASTE_SCAN_INTERVAL seconds."""
    # Delay first run so the app has time to fully start
    time.sleep(30)
    while True:
        try:
            from darkweb_scanner.storage import Storage
            from darkweb_scanner.dashboard.dashboard_routes import _run_paste_scan_background
            logger.info("Paste monitor: scheduled scan starting...")
            _run_paste_scan_background(Storage())
            logger.info("Paste monitor: scheduled scan complete.")
        except Exception as e:
            logger.error(f"Paste monitor scheduler error: {e}")
        time.sleep(PASTE_SCAN_INTERVAL)


def create_app() -> Flask:
    app = Flask(__name__)

    app.secret_key = os.getenv("DASHBOARD_SECRET_KEY", "change-me-in-production")
    app.permanent_session_lifetime = timedelta(hours=12)

    # Trust X-Forwarded-Proto from nginx so url_for generates https:// URLs
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    from .auth_routes import auth_bp
    from .dashboard_routes import dashboard_bp
    from .channel_monitor_routes import channel_monitor_bp
    from .ransomware_live_routes import rw_live_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(channel_monitor_bp)
    app.register_blueprint(rw_live_bp)

    @app.route("/")
    def root():
        return redirect(url_for("dashboard.index"))

    # Start paste monitor background scheduler (runs every PASTE_SCAN_INTERVAL seconds)
    t = threading.Thread(target=_paste_monitor_loop, daemon=True, name="paste_monitor_scheduler")
    t.start()
    logger.info(f"Paste monitor scheduler started (interval: {PASTE_SCAN_INTERVAL}s)")

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("DASHBOARD_PORT", "8080"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
