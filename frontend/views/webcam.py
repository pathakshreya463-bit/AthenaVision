"""
views/webcam.py

AthenaVision — Live Monitoring ("Mission Control")

The flagship page of the platform: a large reserved live-camera area,
real-time-feeling metrics, recent detections, and an occupancy chart
placeholder, all wrapped in a NASA-mission-control aesthetic.

Backend integration
--------------------
This view is a thin presentation layer over the existing Flask backend.
No backend routes are modified or assumed beyond simple REST conventions —
every call is isolated in the "Backend client" section below, wrapped in
try/except so the page degrades gracefully (placeholder data + a visible
connection banner) if the Flask server is unreachable or the response
shape differs slightly from what's expected here.

Adjust API_BASE_URL and the ENDPOINTS dict to match your actual Flask
routes; nothing else in this file needs to change.

Expected (adjustable) response shapes:
    GET  {status}      -> {"state": "monitoring" | "idle" | "offline"}
    GET  {metrics}      -> {
                              "people_count": int,
                              "average_occupancy": float,
                              "peak_occupancy": int,
                              "monitoring_duration_seconds": int,
                              "stream_url": str | null,
                              "occupancy_history": [{"t": "...", "value": n}, ...]
                            }
    GET  {detections}  -> [{"timestamp": "...", "label": "...",
                             "confidence": 0.0-1.0, "zone": "..."}, ...]
    POST {start}       -> {"ok": true}
    POST {stop}        -> {"ok": true}

Usage:
    from views.webcam import render_webcam
    render_webcam()
"""

import os
from datetime import datetime, timezone
from pathlib import Path

import requests
import streamlit as st


# --------------------------------------------------------------------------
# Backend client
# --------------------------------------------------------------------------
API_BASE_URL = os.environ.get("ATHENAVISION_API_BASE_URL", "http://localhost:5000")
REQUEST_TIMEOUT_SECONDS = 3

ENDPOINTS = {
    "status": f"{API_BASE_URL}/api/status",
    "metrics": f"{API_BASE_URL}/api/metrics",
    "detections": f"{API_BASE_URL}/api/detections/recent",
    "start": f"{API_BASE_URL}/api/monitoring/start",
    "stop": f"{API_BASE_URL}/api/monitoring/stop",
    "stream": f"{API_BASE_URL}/video_feed",  # MJPEG-style stream endpoint, if served
}

_DEFAULT_METRICS = {
    "people_count": 0,
    "average_occupancy": 0.0,
    "peak_occupancy": 0,
    "monitoring_duration_seconds": 0,
    "stream_url": None,
    "occupancy_history": [],
}

_DEFAULT_DETECTIONS = [
    {"timestamp": "—", "label": "No detections yet", "confidence": None, "zone": "—"},
]


def fetch_status() -> dict:
    """GET current system status from the Flask backend."""
    try:
        resp = requests.get(ENDPOINTS["status"], timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        st.session_state["backend_connected"] = True
        return resp.json()
    except requests.exceptions.RequestException:
        st.session_state["backend_connected"] = False
        return {"state": "offline"}


def fetch_metrics() -> dict:
    """GET current metrics from the Flask backend, merged over safe defaults."""
    try:
        resp = requests.get(ENDPOINTS["metrics"], timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        st.session_state["backend_connected"] = True
        data = resp.json() or {}
        return {**_DEFAULT_METRICS, **data}
    except requests.exceptions.RequestException:
        st.session_state["backend_connected"] = False
        return dict(_DEFAULT_METRICS)


def fetch_recent_detections() -> list:
    """GET recent detection events from the Flask backend."""
    try:
        resp = requests.get(ENDPOINTS["detections"], timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        st.session_state["backend_connected"] = True
        data = resp.json()
        return data if isinstance(data, list) and data else list(_DEFAULT_DETECTIONS)
    except requests.exceptions.RequestException:
        st.session_state["backend_connected"] = False
        return list(_DEFAULT_DETECTIONS)


def start_monitoring() -> bool:
    """POST to the backend to start monitoring. Returns True on success."""
    try:
        resp = requests.post(ENDPOINTS["start"], timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        st.session_state["backend_connected"] = True
        return True
    except requests.exceptions.RequestException as exc:
        st.session_state["backend_connected"] = False
        st.session_state["last_error"] = str(exc)
        return False


def stop_monitoring() -> bool:
    """POST to the backend to stop monitoring. Returns True on success."""
    try:
        resp = requests.post(ENDPOINTS["stop"], timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        st.session_state["backend_connected"] = True
        return True
    except requests.exceptions.RequestException as exc:
        st.session_state["backend_connected"] = False
        st.session_state["last_error"] = str(exc)
        return False


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def _format_duration(seconds: int) -> str:
    seconds = max(0, int(seconds or 0))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def _init_session_state() -> None:
    defaults = {
        "monitoring_active": False,
        "monitoring_started_at": None,
        "last_duration_seconds": 0,
        "backend_connected": True,
        "last_error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _current_duration_seconds(backend_duration: int) -> int:
    """Prefer the backend-reported duration; fall back to a local timer."""
    if backend_duration:
        return backend_duration
    if st.session_state.get("monitoring_active") and st.session_state.get("monitoring_started_at"):
        delta = datetime.now(timezone.utc) - st.session_state["monitoring_started_at"]
        return int(delta.total_seconds())
    return st.session_state.get("last_duration_seconds", 0)


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------
def render_webcam() -> None:
    """Render the complete Live Monitoring / Mission Control page."""
    _init_session_state()
    _load_base_styles()
    _inject_page_styles()

    status = fetch_status()
    metrics = fetch_metrics()
    detections = fetch_recent_detections()

    # Reconcile local monitoring flag with backend-reported state, if present.
    backend_state = status.get("state")
    if backend_state == "monitoring":
        if not st.session_state["monitoring_active"]:
            st.session_state["monitoring_active"] = True
            st.session_state["monitoring_started_at"] = st.session_state["monitoring_started_at"] or datetime.now(timezone.utc)
    elif backend_state in ("idle", "offline") and st.session_state["monitoring_active"] is False:
        pass  # already consistent

    duration_seconds = _current_duration_seconds(metrics.get("monitoring_duration_seconds", 0))

    st.markdown('<div class="mc-container">', unsafe_allow_html=True)

    _render_header()
    _render_connection_banner()
    _render_status_row(status, duration_seconds)
    _render_metrics_row(metrics, duration_seconds)
    _render_camera_section(metrics, status)
    _render_controls(status)

    col_left, col_right = st.columns([1.15, 1], gap="large")
    with col_left:
        _render_recent_detections(detections)
    with col_right:
        _render_occupancy_chart(metrics.get("occupancy_history", []))

    st.markdown('</div>', unsafe_allow_html=True)  # close .mc-container


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------
def _render_header() -> None:
    st.markdown(
        """
        <div class="mc-header">
            <div class="mc-header__left">
                <div class="mc-eyebrow">AthenaVision · Mission Control</div>
                <div class="mc-title">Live Monitoring</div>
            </div>
            <div class="mc-header__right">
                <div class="mc-clock" id="mc-clock">--:--:--</div>
                <div class="mc-clock-label">Local Time</div>
            </div>
        </div>
        <script>
        (function() {
            function tick() {
                const el = window.parent.document.getElementById('mc-clock');
                if (el) {
                    el.textContent = new Date().toLocaleTimeString([], {hour12: false});
                }
            }
            tick();
            setInterval(tick, 1000);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def _render_connection_banner() -> None:
    if st.session_state.get("backend_connected"):
        return
    st.markdown(
        """
        <div class="mc-banner mc-banner--warning">
            <span class="mc-banner__dot"></span>
            Backend unreachable — displaying cached / placeholder telemetry.
            Check that the Flask service is running and API_BASE_URL is correct.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_status_row(status: dict, duration_seconds: int) -> None:
    state = status.get("state", "offline")
    state_meta = {
        "monitoring": {"label": "MONITORING", "class": "status--live"},
        "idle": {"label": "STANDBY", "class": "status--idle"},
        "offline": {"label": "OFFLINE", "class": "status--offline"},
    }.get(state, {"label": state.upper(), "class": "status--idle"})

    st.markdown(
        f"""
        <div class="mc-status-bar">
            <div class="mc-status-pill {state_meta['class']}">
                <span class="mc-status-dot"></span>
                {state_meta['label']}
            </div>
            <div class="mc-status-meta">
                Session duration <span class="mc-mono">{_format_duration(duration_seconds)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metrics_row(metrics: dict, duration_seconds: int) -> None:
    cards = [
        {"label": "People Count", "value": f"{metrics.get('people_count', 0):,}", "unit": "detected now"},
        {"label": "Average Occupancy", "value": f"{metrics.get('average_occupancy', 0):.1f}", "unit": "people / interval"},
        {"label": "Peak Occupancy", "value": f"{metrics.get('peak_occupancy', 0):,}", "unit": "session max"},
        {"label": "Monitoring Duration", "value": _format_duration(duration_seconds), "unit": "hh:mm:ss"},
    ]

    cols = st.columns(len(cards), gap="medium")
    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="mc-metric-card">
                    <div class="mc-metric-card__label">{card['label']}</div>
                    <div class="mc-metric-card__value">{card['value']}</div>
                    <div class="mc-metric-card__unit">{card['unit']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_camera_section(metrics: dict, status: dict) -> None:
    is_live = status.get("state") == "monitoring"
    stream_url = metrics.get("stream_url") or ENDPOINTS["stream"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    live_badge = (
        '<div class="mc-live-badge"><span class="mc-live-dot"></span>LIVE</div>'
        if is_live else
        '<div class="mc-live-badge mc-live-badge--idle"><span class="mc-live-dot"></span>STANDBY</div>'
    )

    st.markdown(
        f"""
        <div class="mc-camera-panel">
            <div class="mc-camera-panel__header">
                <div class="mc-camera-panel__title">Primary Feed — Camera 01</div>
                {live_badge}
            </div>

            <div class="mc-camera-frame" id="mc-camera-frame">
                <!-- Reserved area for the embedded live video stream.
                     If the Flask backend serves an MJPEG / video endpoint
                     (see ENDPOINTS["stream"] or metrics["stream_url"]),
                     it renders here automatically; otherwise the HUD
                     placeholder below remains visible. -->
                <img
                    src="{stream_url}"
                    class="mc-camera-feed"
                    alt="Live camera feed"
                    onload="this.style.opacity=1; document.getElementById('mc-camera-placeholder').style.display='none';"
                    onerror="this.style.display='none';"
                />
                <div class="mc-camera-placeholder" id="mc-camera-placeholder">
                    <div class="mc-scanline"></div>
                    <div class="mc-crosshair">
                        <span></span><span></span><span></span><span></span>
                    </div>
                    <div class="mc-camera-placeholder__text">
                        <div class="mc-camera-placeholder__icon">▣</div>
                        <div>Camera feed reserved</div>
                        <div class="mc-camera-placeholder__sub">Awaiting embedded video stream</div>
                    </div>
                </div>

                <div class="mc-corner mc-corner--tl"></div>
                <div class="mc-corner mc-corner--tr"></div>
                <div class="mc-corner mc-corner--bl"></div>
                <div class="mc-corner mc-corner--br"></div>

                <div class="mc-camera-timestamp mc-mono">{timestamp}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_controls(status: dict) -> None:
    is_active = st.session_state["monitoring_active"]

    st.markdown('<div class="mc-controls">', unsafe_allow_html=True)
    start_col, stop_col = st.columns(2, gap="medium")

    with start_col:
        if st.button(
            "▶  Start Monitoring",
            key="btn_start_monitoring",
            use_container_width=True,
            disabled=is_active,
        ):
            ok = start_monitoring()
            if ok:
                st.session_state["monitoring_active"] = True
                st.session_state["monitoring_started_at"] = datetime.now(timezone.utc)
                st.toast("Monitoring started", icon="🟢")
            else:
                st.toast("Could not reach backend to start monitoring", icon="⚠️")
            st.rerun()

    with stop_col:
        if st.button(
            "■  Stop Monitoring",
            key="btn_stop_monitoring",
            use_container_width=True,
            disabled=not is_active,
        ):
            ok = stop_monitoring()
            if st.session_state.get("monitoring_started_at"):
                elapsed = datetime.now(timezone.utc) - st.session_state["monitoring_started_at"]
                st.session_state["last_duration_seconds"] = int(elapsed.total_seconds())
            st.session_state["monitoring_active"] = False
            st.session_state["monitoring_started_at"] = None
            if ok:
                st.toast("Monitoring stopped", icon="🔴")
            else:
                st.toast("Could not reach backend to stop monitoring", icon="⚠️")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def _render_recent_detections(detections: list) -> None:
    st.markdown(
        """
        <div class="mc-panel">
            <div class="mc-panel__header">
                <div class="mc-panel__title">Recent Detections</div>
                <div class="mc-panel__badge">LOG</div>
            </div>
            <div class="mc-detections-list">
        """,
        unsafe_allow_html=True,
    )

    rows = []
    for item in detections:
        confidence = item.get("confidence")
        confidence_html = (
            f'<span class="mc-detection-confidence">{confidence * 100:.0f}%</span>'
            if isinstance(confidence, (int, float))
            else ""
        )
        rows.append(
            f"""
            <div class="mc-detection-row">
                <span class="mc-mono mc-detection-time">{item.get('timestamp', '—')}</span>
                <div class="mc-detection-main">
                    <div class="mc-detection-label">{item.get('label', 'Unknown event')}</div>
                    <div class="mc-detection-zone">{item.get('zone', '—')}</div>
                </div>
                {confidence_html}
            </div>
            """
        )
    st.markdown("".join(rows), unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)  # close list, panel


def _render_occupancy_chart(history: list) -> None:
    st.markdown(
        """
        <div class="mc-panel">
            <div class="mc-panel__header">
                <div class="mc-panel__title">Occupancy Over Time</div>
                <div class="mc-panel__badge">CHART</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    if history:
        try:
            import pandas as pd  # local import: optional dependency for charting only

            df = pd.DataFrame(history)
            if "t" in df.columns and "value" in df.columns:
                df = df.set_index("t")["value"]
            st.line_chart(df, use_container_width=True, height=260)
        except Exception:
            _render_chart_placeholder()
    else:
        _render_chart_placeholder()

    st.markdown("</div>", unsafe_allow_html=True)  # close panel


def _render_chart_placeholder() -> None:
    st.markdown(
        """
        <div class="mc-chart-placeholder">
            <div class="mc-chart-placeholder__grid"></div>
            <div class="mc-chart-placeholder__text">
                Awaiting occupancy data stream
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
def _load_base_styles() -> None:
    """Load the shared design-system stylesheet (frontend/assets/styles.css)."""
    css_path = Path(__file__).resolve().parent.parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def _inject_page_styles() -> None:
    st.markdown(
        """
        <style>
        #MainMenu, header[data-testid="stHeader"], footer,
        div[data-testid="stDecoration"], .stDeployButton {
            display: none !important;
        }
        .block-container { padding: 2.5rem 0 4rem 0 !important; max-width: 100% !important; }

        .mc-container {
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 clamp(20px, 5vw, 56px);
        }
        .mc-mono { font-family: 'JetBrains Mono', Consolas, monospace; }

        /* ---------------------------------------------------------- */
        /* Header                                                       */
        /* ---------------------------------------------------------- */
        .mc-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 28px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--glass-border, rgba(255,255,255,0.09));
        }
        .mc-eyebrow {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: var(--accent-cyan, #4cc9f0);
            margin-bottom: 8px;
        }
        .mc-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: clamp(1.8rem, 3.2vw, 2.6rem);
            color: var(--text-primary, #f4f5fb);
        }
        .mc-header__right { text-align: right; }
        .mc-clock {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 1.6rem;
            font-weight: 600;
            color: var(--accent-cyan, #4cc9f0);
            text-shadow: 0 0 16px rgba(76,201,240,0.5);
        }
        .mc-clock-label {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.68rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--text-muted, #7a7f9e);
        }

        /* ---------------------------------------------------------- */
        /* Connection banner                                            */
        /* ---------------------------------------------------------- */
        .mc-banner {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 18px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            margin-bottom: 20px;
        }
        .mc-banner--warning {
            background: rgba(255, 209, 102, 0.08);
            border: 1px solid rgba(255, 209, 102, 0.3);
            color: #ffd166;
        }
        .mc-banner__dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: #ffd166;
            box-shadow: 0 0 8px #ffd166;
            flex-shrink: 0;
        }

        /* ---------------------------------------------------------- */
        /* Status bar                                                    */
        /* ---------------------------------------------------------- */
        .mc-status-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }
        .mc-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 16px;
            border-radius: 999px;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            border: 1px solid transparent;
        }
        .mc-status-dot {
            width: 8px; height: 8px; border-radius: 50%;
        }
        .status--live {
            background: rgba(74, 222, 128, 0.1);
            border-color: rgba(74, 222, 128, 0.4);
            color: #4ade80;
        }
        .status--live .mc-status-dot {
            background: #4ade80;
            box-shadow: 0 0 10px #4ade80;
            animation: mcPulse 1.6s ease-in-out infinite;
        }
        .status--idle {
            background: rgba(255, 209, 102, 0.08);
            border-color: rgba(255, 209, 102, 0.3);
            color: #ffd166;
        }
        .status--idle .mc-status-dot { background: #ffd166; }
        .status--offline {
            background: rgba(255, 107, 157, 0.08);
            border-color: rgba(255, 107, 157, 0.3);
            color: #ff6b9d;
        }
        .status--offline .mc-status-dot { background: #ff6b9d; }

        @keyframes mcPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.3); }
        }

        .mc-status-meta {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: var(--text-muted, #7a7f9e);
        }

        /* ---------------------------------------------------------- */
        /* Metric cards                                                  */
        /* ---------------------------------------------------------- */
        .mc-metric-card {
            padding: 20px 22px;
            border-radius: 16px;
            background: var(--glass-fill, rgba(255,255,255,0.045));
            border: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        }
        .mc-metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(124, 92, 255, 0.4);
            box-shadow: 0 0 24px rgba(124, 92, 255, 0.2);
        }
        .mc-metric-card__label {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.68rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted, #7a7f9e);
        }
        .mc-metric-card__value {
            margin-top: 8px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2rem;
            color: var(--text-primary, #f4f5fb);
            text-shadow: 0 0 20px rgba(124, 92, 255, 0.25);
        }
        .mc-metric-card__unit {
            margin-top: 4px;
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: var(--text-muted, #7a7f9e);
        }

        /* ---------------------------------------------------------- */
        /* Camera panel                                                  */
        /* ---------------------------------------------------------- */
        .mc-camera-panel {
            margin: 32px 0 20px 0;
        }
        .mc-camera-panel__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        .mc-camera-panel__title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-primary, #f4f5fb);
        }
        .mc-live-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 14px;
            border-radius: 999px;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            background: rgba(255, 107, 157, 0.1);
            border: 1px solid rgba(255, 107, 157, 0.35);
            color: #ff6b9d;
        }
        .mc-live-badge--idle {
            background: rgba(122, 127, 158, 0.1);
            border-color: rgba(122, 127, 158, 0.35);
            color: var(--text-muted, #7a7f9e);
        }
        .mc-live-dot {
            width: 7px; height: 7px; border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 8px currentColor;
        }
        .mc-live-badge:not(.mc-live-badge--idle) .mc-live-dot {
            animation: mcPulse 1.2s ease-in-out infinite;
        }

        .mc-camera-frame {
            position: relative;
            width: 100%;
            aspect-ratio: 16 / 9;
            border-radius: 22px;
            overflow: hidden;
            background:
                radial-gradient(ellipse at center, rgba(76,201,240,0.06), transparent 70%),
                repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 32px),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 32px),
                #060815;
            border: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            box-shadow: 0 24px 70px rgba(0,0,0,0.55), inset 0 0 60px rgba(0,0,0,0.4);
        }

        .mc-camera-feed {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0;
            transition: opacity 0.6s ease;
        }

        .mc-camera-placeholder {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .mc-camera-placeholder__text {
            text-align: center;
            color: var(--text-muted, #7a7f9e);
            font-family: 'Inter', sans-serif;
            z-index: 2;
        }
        .mc-camera-placeholder__icon {
            font-size: 2.4rem;
            color: var(--accent-cyan, #4cc9f0);
            opacity: 0.6;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 16px rgba(76,201,240,0.4));
        }
        .mc-camera-placeholder__sub {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            margin-top: 6px;
            letter-spacing: 0.05em;
            opacity: 0.7;
        }

        .mc-scanline {
            position: absolute;
            left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(76,201,240,0.6), transparent);
            animation: mcScan 4.5s linear infinite;
            z-index: 1;
        }
        @keyframes mcScan {
            0% { top: 0%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }

        .mc-crosshair {
            position: absolute;
            inset: 0;
            pointer-events: none;
        }
        .mc-crosshair span {
            position: absolute;
            background: rgba(76,201,240,0.18);
        }
        .mc-crosshair span:nth-child(1),
        .mc-crosshair span:nth-child(2) {
            top: 50%; left: 0; right: 0; height: 1px; transform: translateY(-50%);
        }
        .mc-crosshair span:nth-child(3),
        .mc-crosshair span:nth-child(4) {
            left: 50%; top: 0; bottom: 0; width: 1px; transform: translateX(-50%);
        }

        .mc-corner {
            position: absolute;
            width: 26px; height: 26px;
            border: 2px solid var(--accent-cyan, #4cc9f0);
            opacity: 0.65;
            z-index: 3;
        }
        .mc-corner--tl { top: 14px; left: 14px; border-right: none; border-bottom: none; border-radius: 6px 0 0 0; }
        .mc-corner--tr { top: 14px; right: 14px; border-left: none; border-bottom: none; border-radius: 0 6px 0 0; }
        .mc-corner--bl { bottom: 14px; left: 14px; border-right: none; border-top: none; border-radius: 0 0 0 6px; }
        .mc-corner--br { bottom: 14px; right: 14px; border-left: none; border-top: none; border-radius: 0 0 6px 0; }

        .mc-camera-timestamp {
            position: absolute;
            bottom: 16px;
            right: 20px;
            font-size: 0.72rem;
            color: rgba(244,245,251,0.55);
            letter-spacing: 0.05em;
            z-index: 3;
        }

        /* ---------------------------------------------------------- */
        /* Controls                                                      */
        /* ---------------------------------------------------------- */
        .mc-controls { margin: 22px 0 40px 0; }
        div[data-testid="column"] .stButton > button {
            font-family: 'JetBrains Mono', Consolas, monospace !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em;
            border-radius: 14px !important;
            padding: 0.85em 1.4em !important;
        }

        div[data-testid="column"]:nth-of-type(1) .stButton > button {
            background: rgba(74, 222, 128, 0.1) !important;
            border: 1px solid rgba(74, 222, 128, 0.4) !important;
            color: #4ade80 !important;
        }
        div[data-testid="column"]:nth-of-type(1) .stButton > button:hover:not(:disabled) {
            background: rgba(74, 222, 128, 0.18) !important;
            box-shadow: 0 0 24px rgba(74, 222, 128, 0.35);
            transform: translateY(-2px);
        }

        div[data-testid="column"]:nth-of-type(2) .stButton > button {
            background: rgba(255, 107, 157, 0.1) !important;
            border: 1px solid rgba(255, 107, 157, 0.4) !important;
            color: #ff6b9d !important;
        }
        div[data-testid="column"]:nth-of-type(2) .stButton > button:hover:not(:disabled) {
            background: rgba(255, 107, 157, 0.18) !important;
            box-shadow: 0 0 24px rgba(255, 107, 157, 0.35);
            transform: translateY(-2px);
        }

        div[data-testid="column"] .stButton > button:disabled {
            opacity: 0.35 !important;
            transform: none !important;
            box-shadow: none !important;
        }

        /* ---------------------------------------------------------- */
        /* Generic glass panel (detections / chart)                      */
        /* ---------------------------------------------------------- */
        .mc-panel {
            border-radius: 20px;
            background: var(--glass-fill, rgba(255,255,255,0.045));
            border: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            overflow: hidden;
            height: 100%;
        }
        .mc-panel__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 22px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .mc-panel__title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary, #f4f5fb);
        }
        .mc-panel__badge {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.65rem;
            letter-spacing: 0.14em;
            color: var(--accent-cyan, #4cc9f0);
            border: 1px solid rgba(76,201,240,0.3);
            border-radius: 6px;
            padding: 3px 8px;
        }

        /* ---------------------------------------------------------- */
        /* Recent detections                                             */
        /* ---------------------------------------------------------- */
        .mc-detections-list { max-height: 320px; overflow-y: auto; }
        .mc-detection-row {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 14px 22px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: background 0.2s ease;
        }
        .mc-detection-row:last-child { border-bottom: none; }
        .mc-detection-row:hover { background: rgba(255,255,255,0.03); }
        .mc-detection-time {
            font-size: 0.72rem;
            color: var(--text-muted, #7a7f9e);
            white-space: nowrap;
            flex-shrink: 0;
        }
        .mc-detection-main { flex: 1; min-width: 0; }
        .mc-detection-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary, #f4f5fb);
        }
        .mc-detection-zone {
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: var(--text-muted, #7a7f9e);
            margin-top: 2px;
        }
        .mc-detection-confidence {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            color: var(--accent-cyan, #4cc9f0);
            flex-shrink: 0;
        }

        /* ---------------------------------------------------------- */
        /* Occupancy chart placeholder                                   */
        /* ---------------------------------------------------------- */
        .mc-chart-placeholder {
            position: relative;
            height: 260px;
            margin: 22px;
            border-radius: 14px;
            overflow: hidden;
            border: 1px dashed rgba(255,255,255,0.12);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .mc-chart-placeholder__grid {
            position: absolute;
            inset: 0;
            background:
                repeating-linear-gradient(0deg, rgba(255,255,255,0.04) 0px, rgba(255,255,255,0.04) 1px, transparent 1px, transparent 34px),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0px, rgba(255,255,255,0.04) 1px, transparent 1px, transparent 48px);
        }
        .mc-chart-placeholder__text {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
            color: var(--text-muted, #7a7f9e);
            z-index: 1;
        }

        /* ---------------------------------------------------------- */
        /* Responsive                                                     */
        /* ---------------------------------------------------------- */
        @media (max-width: 860px) {
            .mc-header { flex-direction: column; align-items: flex-start; gap: 14px; }
            .mc-header__right { text-align: left; }
            .mc-status-bar { flex-direction: column; align-items: flex-start; gap: 10px; }
        }
        @media (max-width: 600px) {
            .mc-camera-frame { aspect-ratio: 4 / 3; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )