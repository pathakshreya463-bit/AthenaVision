"""
views/home.py

AthenaVision homepage — the "control center" landing view.

Layout (top to bottom):
    1. Full-screen hero            (components/hero.py)
    2. Workspace cards             (components/cards.py)
    3. Recent Activity
    4. Quick Statistics
    5. Project Information
    6. Footer

All Streamlit default chrome is hidden and the page content is rendered in
a centered, max-width column with generous, consistent spacing between
sections so the page reads as one designed surface rather than a stack of
default Streamlit widgets.

Usage:
    from views.home import render_home
    render_home()
"""

from pathlib import Path

import streamlit as st

from components.hero import render_hero
from components.cards import render_cards, get_active_view, WORKSPACES


# --------------------------------------------------------------------------
# Placeholder data
# (Swap these for real backend calls — shape is stable, so downstream
#  rendering does not need to change when wired to live data.)
# --------------------------------------------------------------------------
RECENT_ACTIVITY = [
    {
        "time": "2 min ago",
        "event": "Motion detected",
        "location": "Library — Reading Hall B",
        "severity": "info",
    },
    {
        "time": "11 min ago",
        "event": "Occupancy threshold reached",
        "location": "Lecture Hall 3",
        "severity": "warning",
    },
    {
        "time": "27 min ago",
        "event": "New session started",
        "location": "Collaborative Studio — East Wing",
        "severity": "success",
    },
    {
        "time": "48 min ago",
        "event": "Camera reconnected",
        "location": "Library — North Entrance",
        "severity": "success",
    },
    {
        "time": "1 hr ago",
        "event": "Unusual activity flagged",
        "location": "Classroom 214",
        "severity": "alert",
    },
]

QUICK_STATS = [
    {"label": "Active Cameras", "value": "128", "delta": "+4 today", "trend": "up"},
    {"label": "Detections Today", "value": "3,482", "delta": "+12.4%", "trend": "up"},
    {"label": "Active Alerts", "value": "3", "delta": "−2 vs yesterday", "trend": "down"},
    {"label": "System Uptime", "value": "99.98%", "delta": "Stable", "trend": "neutral"},
]

PROJECT_INFO = {
    "eyebrow": "About the Platform",
    "title": "Built for the modern academic campus",
    "body": (
        "AthenaVision unifies camera feeds, presence sensors and behavioral "
        "models into a single intelligence layer for classrooms, libraries "
        "and collaborative learning spaces. Rather than replacing staff "
        "judgment, it surfaces the patterns that matter — occupancy trends, "
        "space utilization, safety anomalies — so academic teams can act on "
        "signal instead of sifting through footage."
    ),
    "facts": [
        {"label": "Version", "value": "2.4.1"},
        {"label": "Coverage", "value": "128 sensors / 6 buildings"},
        {"label": "Model", "value": "AthenaVision Vision-Core v3"},
        {"label": "Status", "value": "Operational"},
    ],
}

SEVERITY_COLOR = {
    "info": "var(--accent-cyan)",
    "success": "#4ade80",
    "warning": "var(--accent-gold)",
    "alert": "var(--accent-rose)",
}


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------
def render_home() -> None:
    """Render the complete AthenaVision homepage."""
    _load_base_styles()
    _inject_page_styles()

    # 1. Full-screen hero — occupies the first screen on its own.
    render_hero()

    # Everything below the hero lives in a centered, max-width column.
    st.markdown('<div class="page-container">', unsafe_allow_html=True)

    _render_workspace_section()
    _render_activity_section()
    _render_stats_section()
    _render_project_section()

    st.markdown('</div>', unsafe_allow_html=True)  # close .page-container

    _render_footer()


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------
def _render_workspace_section() -> None:
    st.markdown('<div class="home-section" id="workspaces">', unsafe_allow_html=True)
    render_cards()

    # Downstream routing hook: read the active workspace here (or in your
    # top-level app/router) and swap views accordingly, e.g.:
    #
    #   active = get_active_view()
    #   if active == "live_monitoring":
    #       switch_to(live_monitoring_view)
    _ = get_active_view()  # noqa: F841 (intentional hook point)

    st.markdown('</div>', unsafe_allow_html=True)


def _render_activity_section() -> None:
    st.markdown(
        """
        <div class="home-section" id="activity">
            <div class="section-header">
                <div class="section-eyebrow">Live Feed</div>
                <div class="section-title">Recent Activity</div>
            </div>
            <div class="activity-list">
        """,
        unsafe_allow_html=True,
    )

    rows = "".join(
        f"""
        <div class="activity-row">
            <span class="activity-dot" style="background:{SEVERITY_COLOR.get(item['severity'], 'var(--accent-cyan)')}"></span>
            <div class="activity-main">
                <div class="activity-event">{item['event']}</div>
                <div class="activity-location">{item['location']}</div>
            </div>
            <div class="activity-time">{item['time']}</div>
        </div>
        """
        for item in RECENT_ACTIVITY
    )

    st.markdown(rows, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)  # close .activity-list, .home-section


def _render_stats_section() -> None:
    st.markdown(
        """
        <div class="home-section" id="statistics">
            <div class="section-header">
                <div class="section-eyebrow">At a Glance</div>
                <div class="section-title">Quick Statistics</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(QUICK_STATS), gap="medium")
    for col, stat in zip(cols, QUICK_STATS):
        trend_class = {
            "up": "stat-card__delta--up",
            "down": "stat-card__delta--down",
            "neutral": "stat-card__delta--neutral",
        }.get(stat["trend"], "")

        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-card__label">{stat['label']}</div>
                    <div class="stat-card__value">{stat['value']}</div>
                    <div class="stat-card__delta {trend_class}">{stat['delta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_project_section() -> None:
    facts_html = "".join(
        f"""
        <div class="project-fact">
            <div class="project-fact__label">{fact['label']}</div>
            <div class="project-fact__value">{fact['value']}</div>
        </div>
        """
        for fact in PROJECT_INFO["facts"]
    )

    st.markdown(
        f"""
        <div class="home-section" id="project-info">
            <div class="project-panel">
                <div class="project-panel__copy">
                    <div class="section-eyebrow">{PROJECT_INFO['eyebrow']}</div>
                    <div class="section-title">{PROJECT_INFO['title']}</div>
                    <p class="project-panel__body">{PROJECT_INFO['body']}</p>
                </div>
                <div class="project-panel__facts">
                    {facts_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_footer() -> None:
    st.markdown(
        f"""
        <footer class="home-footer">
            <div class="home-footer__inner">
                <div class="home-footer__brand">
                    <div class="home-footer__logo">ATHENAVISION</div>
                    <div class="home-footer__tagline">Observe. Understand. Optimize.</div>
                </div>
                <div class="home-footer__links">
                    <div class="home-footer__col">
                        <div class="home-footer__col-title">Product</div>
                        {"".join(f'<div class="home-footer__link">{w["title"]}</div>' for w in WORKSPACES)}
                    </div>
                    <div class="home-footer__col">
                        <div class="home-footer__col-title">Platform</div>
                        <div class="home-footer__link">Documentation</div>
                        <div class="home-footer__link">System Status</div>
                        <div class="home-footer__link">Security</div>
                    </div>
                    <div class="home-footer__col">
                        <div class="home-footer__col-title">Organization</div>
                        <div class="home-footer__link">About</div>
                        <div class="home-footer__link">Support</div>
                        <div class="home-footer__link">Contact</div>
                    </div>
                </div>
            </div>
            <div class="home-footer__bottom">
                <span>© 2026 AthenaVision. All rights reserved.</span>
                <span class="home-footer__status">
                    <span class="status-dot"></span> All systems operational
                </span>
            </div>
        </footer>
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
        /* ---------------------------------------------------------- */
        /* Strip Streamlit's default chrome & spacing                  */
        /* ---------------------------------------------------------- */
        #MainMenu, header[data-testid="stHeader"], footer,
        div[data-testid="stDecoration"], .stDeployButton {
            display: none !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* ---------------------------------------------------------- */
        /* Centered, max-width content column                          */
        /* ---------------------------------------------------------- */
        .page-container {
            max-width: 1180px;
            margin: 0 auto;
            padding: 0 clamp(20px, 5vw, 64px);
        }

        .home-section {
            margin-top: clamp(72px, 10vw, 128px);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .home-section > * { width: 100%; }

        .section-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin-bottom: 40px;
        }
        .section-eyebrow {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--accent-cyan, #4cc9f0);
            margin-bottom: 10px;
        }
        .section-title {
            font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
            font-weight: 600;
            font-size: clamp(1.7rem, 3vw, 2.3rem);
            color: var(--text-primary, #f4f5fb);
        }

        /* ---------------------------------------------------------- */
        /* Recent Activity                                              */
        /* ---------------------------------------------------------- */
        .activity-list {
            width: 100%;
            border-radius: 20px;
            background: var(--glass-fill, rgba(255,255,255,0.045));
            border: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            overflow: hidden;
            text-align: left;
        }
        .activity-row {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 26px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            transition: background 0.25s ease;
        }
        .activity-row:last-child { border-bottom: none; }
        .activity-row:hover { background: rgba(255,255,255,0.035); }

        .activity-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            flex-shrink: 0;
            box-shadow: 0 0 10px currentColor;
        }
        .activity-main { flex: 1; min-width: 0; }
        .activity-event {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--text-primary, #f4f5fb);
        }
        .activity-location {
            font-family: 'Inter', sans-serif;
            font-size: 0.82rem;
            color: var(--text-muted, #7a7f9e);
            margin-top: 2px;
        }
        .activity-time {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.75rem;
            color: var(--text-muted, #7a7f9e);
            white-space: nowrap;
            flex-shrink: 0;
        }

        /* ---------------------------------------------------------- */
        /* Quick Statistics (extends .stat-card from styles.css)       */
        /* ---------------------------------------------------------- */
        .stat-card { text-align: left; }
        .stat-card__delta--neutral { color: var(--text-muted, #7a7f9e); }

        /* ---------------------------------------------------------- */
        /* Project Information                                         */
        /* ---------------------------------------------------------- */
        .project-panel {
            width: 100%;
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 40px;
            padding: clamp(28px, 4vw, 48px);
            border-radius: 24px;
            background: var(--glass-fill, rgba(255,255,255,0.045));
            border: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            text-align: left;
        }
        .project-panel__body {
            margin-top: 14px;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            line-height: 1.75;
            color: var(--text-secondary, #b8bcd4);
            max-width: 52ch;
        }
        .project-panel__facts {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            align-content: start;
        }
        .project-fact {
            padding: 16px 18px;
            border-radius: 14px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
        }
        .project-fact__label {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted, #7a7f9e);
        }
        .project-fact__value {
            margin-top: 6px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary, #f4f5fb);
        }

        /* ---------------------------------------------------------- */
        /* Footer                                                       */
        /* ---------------------------------------------------------- */
        .home-footer {
            margin-top: clamp(80px, 10vw, 140px);
            border-top: 1px solid var(--glass-border, rgba(255,255,255,0.09));
            background: rgba(5, 6, 15, 0.6);
            backdrop-filter: blur(18px);
            padding: 56px clamp(20px, 5vw, 64px) 28px;
        }
        .home-footer__inner {
            max-width: 1180px;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 48px;
            text-align: left;
        }
        .home-footer__logo {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.3rem;
            letter-spacing: 0.02em;
            background: linear-gradient(120deg, #f4f5fb 0%, #7c5cff 60%, #4cc9f0 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .home-footer__tagline {
            margin-top: 8px;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.78rem;
            color: var(--text-muted, #7a7f9e);
        }
        .home-footer__links {
            display: flex;
            gap: 56px;
            flex-wrap: wrap;
        }
        .home-footer__col-title {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.7rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--accent-cyan, #4cc9f0);
            margin-bottom: 14px;
        }
        .home-footer__link {
            font-family: 'Inter', sans-serif;
            font-size: 0.88rem;
            color: var(--text-secondary, #b8bcd4);
            padding: 5px 0;
            cursor: pointer;
            transition: color 0.2s ease;
        }
        .home-footer__link:hover { color: var(--accent-cyan, #4cc9f0); }

        .home-footer__bottom {
            max-width: 1180px;
            margin: 40px auto 0;
            padding-top: 22px;
            border-top: 1px solid rgba(255,255,255,0.06);
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            color: var(--text-muted, #7a7f9e);
        }
        .home-footer__status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 8px #4ade80;
        }

        /* ---------------------------------------------------------- */
        /* Responsive                                                   */
        /* ---------------------------------------------------------- */
        @media (max-width: 860px) {
            .project-panel {
                grid-template-columns: 1fr;
            }
            .home-footer__inner {
                flex-direction: column;
                gap: 32px;
            }
        }

        @media (max-width: 600px) {
            .activity-row {
                padding: 14px 18px;
                flex-wrap: wrap;
            }
            .activity-time { margin-left: 25px; }
            .project-panel__facts {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )