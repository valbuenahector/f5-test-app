import os
from datetime import datetime, timezone

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)

THEME_PRESETS = {
    "f5red": "#ED1C24",
    "blue": "#1D4ED8",
    "green": "#15803D",
    "purple": "#7E22CE",
    "orange": "#C2410C",
}
DEFAULT_THEME = "f5red"


def get_theme_color():
    raw = os.environ.get("THEME_COLOR", DEFAULT_THEME).strip()
    if raw.startswith("#"):
        return raw
    return THEME_PRESETS.get(raw.lower(), THEME_PRESETS[DEFAULT_THEME])


def get_deployment_name():
    return os.environ.get("DEPLOYMENT_NAME", "unnamed")


@app.context_processor
def inject_deployment_info():
    return {
        "theme_color": get_theme_color(),
        "deployment_name": get_deployment_name(),
    }


def build_client_info():
    forwarded_for = request.headers.get("X-Forwarded-For")
    return {
        "ip": request.remote_addr,
        "forwarded_for": forwarded_for,
        "real_ip": request.headers.get("X-Real-IP"),
        "method": request.method,
        "path": request.path,
        "query_string": request.query_string.decode("utf-8"),
        "host": request.host,
        "scheme": request.scheme,
        "user_agent": request.headers.get("User-Agent"),
        "headers": dict(request.headers),
        "cookies": request.cookies,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.route("/")
def index():
    return render_template("index.html", client=build_client_info())


@app.route("/api/whoami")
def api_whoami():
    return jsonify(build_client_info())


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/set-cookie")
def set_cookie():
    resp = make_response(
        render_template(
            "index.html",
            client=build_client_info(),
            cookie_just_set=True,
        )
    )
    resp.set_cookie("f5_demo_cookie", f"set-at-{datetime.now(timezone.utc).isoformat()}")
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
