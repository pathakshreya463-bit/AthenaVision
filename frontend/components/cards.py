"""
components/cards.py

Workspace navigation cards for AthenaVision.

These cards *replace* traditional buttons as the primary navigation surface:
each entire card (icon, title, description) is clickable — there is no
separate "Open" button. Clicking a card updates st.session_state and
triggers a rerun, so the rest of the app can read the active workspace via
`get_active_view()`.

Implementation note:
Streamlit only fires Python-side callbacks from real widgets, so each card
pairs a purely visual glass "card" div (rendered via st.markdown) with an
invisible st.button of matching size, layered exactly on top of it with a
negative CSS margin. Hover/active state on that invisible button is relayed
back to the visual card underneath using the CSS `:has()` selector, so the
glow / lift / scale / shadow react as if the card itself were hovered.

Usage:
    from components.cards import render_cards, get_active_view

    render_cards()
    active = get_active_view()   # None, or one of the WORKSPACES[i]["key"]
"""

import streamlit as st


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
NAV_STATE_KEY = "active_view"      # st.session_state key holding the active workspace
CARD_HEIGHT_PX = 224                # fixed card height (keeps the overlay button aligned)
COLUMNS_PER_ROW = 3                 # cards per row before wrapping to a new row

WORKSPACES = [
    {
        "key": "image_analysis",
        "icon": "🖼️",
        "title": "Image Analysis",
        "description": "Deep visual inspection of captured frames across every monitored space.",
    },
    {
        "key": "live_monitoring",
        "icon": "📡",
        "title": "Live Monitoring",
        "description": "Real-time camera feeds with instant anomaly and occupancy detection.",
    },
    {
        "key": "insights",
        "icon": "📊",
        "title": "Insights",
        "description": "Aggregated analytics that turn raw footage into actionable intelligence.",
    },
    {
        "key": "activity_history",
        "icon": "🕘",
        "title": "Activity History",
        "description": "A searchable timeline of every detected event, session and trend.",
    },
    {
        "key": "video_intelligence",
        "icon": "🎥",
        "title": "Video Intelligence",
        "description": "AI-driven recognition that understands behavior, not just motion.",
    },
]


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def get_active_view():
    """Return the currently active workspace key, or None if nothing selected."""
    return st.session_state.get(NAV_STATE_KEY)


def render_cards(columns_per_row: int = COLUMNS_PER_ROW) -> None:
    """
    Render the workspace card grid.

    Entire cards are clickable and act as navigation — no "Open" buttons.
    Selecting a card sets st.session_state[NAV_STATE_KEY] and reruns the app.
    """
    if NAV_STATE_KEY not in st.session_state:
        st.session_state[NAV_STATE_KEY] = None

    _inject_card_styles()

    st.markdown(
        """
        <div class="workspace-grid-header">
            <div class="workspace-grid-eyebrow">Workspaces</div>
            <div class="workspace-grid-title">Choose where to begin</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    workspaces = WORKSPACES
    index = 0
    while index < len(workspaces):
        row_items = workspaces[index: index + columns_per_row]
        cols = st.columns(len(row_items), gap="medium")
        for col, workspace in zip(cols, row_items):
            with col:
                _render_card(workspace)
        index += columns_per_row


# --------------------------------------------------------------------------
# Internals
# --------------------------------------------------------------------------
def _navigate_to(view_key: str) -> None:
    st.session_state[NAV_STATE_KEY] = view_key
    st.rerun()


def _render_card(workspace: dict) -> None:
    """Render one visual card plus its invisible overlay button."""
    is_active = get_active_view() == workspace["key"]
    active_class = " workspace-card--active" if is_active else ""

    # 1) visual card (purely decorative, not itself interactive)
    st.markdown(
        f"""
        <div class="workspace-card{active_class}">
            <div class="workspace-card__icon">{workspace['icon']}</div>
            <div class="workspace-card__title">{workspace['title']}</div>
            <div class="workspace-card__desc">{workspace['description']}</div>
            <div class="workspace-card__edge"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2) invisible button, layered exactly over the card via CSS (see
    #    _inject_card_styles). This is what actually receives the click.
    clicked = st.button(
        workspace["title"],
        key=f"nav_btn_{workspace['key']}",
        help=f"Open {workspace['title']}",
        use_container_width=True,
    )
    if clicked:
        _navigate_to(workspace["key"])


def _inject_card_styles() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --card-accent-violet: #7c5cff;
            --card-accent-cyan: #4cc9f0;
        }}

        /* ---------------------------------------------------------- */
        /* Section header                                              */
        /* ---------------------------------------------------------- */
        .workspace-grid-header {{
            margin: 8px 0 28px 0;
        }}
        .workspace-grid-eyebrow {{
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.72rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--card-accent-cyan);
            margin-bottom: 6px;
        }}
        .workspace-grid-title {{
            font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: #f4f5fb;
        }}

        /* ---------------------------------------------------------- */
        /* Row / column spacing — premium breathing room               */
        /* ---------------------------------------------------------- */
        div[data-testid="stHorizontalBlock"] {{
            gap: 24px;
            margin-bottom: 28px;
        }}

        /* ---------------------------------------------------------- */
        /* Visual card                                                  */
        /* ---------------------------------------------------------- */
        div.workspace-card {{
            position: relative;
            height: {CARD_HEIGHT_PX}px;
            padding: 28px 26px 24px 26px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.09);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow: hidden;
            transition: transform 0.38s cubic-bezier(0.16, 1, 0.3, 1),
                        box-shadow 0.38s ease,
                        border-color 0.38s ease,
                        background 0.38s ease;
        }}

        div.workspace-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(124, 92, 255, 0.14), rgba(76, 201, 240, 0.08));
            opacity: 0;
            transition: opacity 0.38s ease;
            pointer-events: none;
        }}

        div.workspace-card__edge {{
            position: absolute;
            left: 0; right: 0; bottom: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--card-accent-violet), var(--card-accent-cyan));
            transform: scaleX(0);
            transform-origin: left center;
            transition: transform 0.4s ease;
        }}

        div.workspace-card__icon {{
            font-size: 2rem;
            line-height: 1;
            filter: drop-shadow(0 0 12px rgba(124, 92, 255, 0.45));
        }}

        div.workspace-card__title {{
            font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: #f4f5fb;
        }}

        div.workspace-card__desc {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 0.88rem;
            line-height: 1.55;
            color: #b8bcd4;
        }}

        /* persistent highlight for the currently active workspace */
        div.workspace-card--active {{
            border-color: rgba(124, 92, 255, 0.55);
            box-shadow: 0 0 0 1px rgba(124, 92, 255, 0.25), 0 0 30px rgba(124, 92, 255, 0.2);
        }}
        div.workspace-card--active .workspace-card__edge {{
            transform: scaleX(1);
        }}

        /* ---------------------------------------------------------- */
        /* Overlay button — invisible, exactly covers the card above   */
        /* ---------------------------------------------------------- */
        div[data-testid="element-container"]:has(> div.workspace-card)
            + div[data-testid="element-container"] {{
            margin-top: -{CARD_HEIGHT_PX}px;
            position: relative;
            z-index: 5;
        }}

        div[data-testid="element-container"]:has(> div.workspace-card)
            + div[data-testid="element-container"] div[data-testid="stButton"] button {{
            width: 100%;
            height: {CARD_HEIGHT_PX}px;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: transparent !important;
            font-size: 0 !important;
            opacity: 0;
            cursor: pointer;
            margin: 0;
            padding: 0;
            border-radius: 20px !important;
            transition: transform 0.12s ease;
        }}

        /* keyboard accessibility: show a visible ring on focus */
        div[data-testid="element-container"]:has(> div.workspace-card)
            + div[data-testid="element-container"] div[data-testid="stButton"] button:focus-visible {{
            opacity: 1;
            background: rgba(124, 92, 255, 0.06) !important;
            outline: 2px solid var(--card-accent-cyan);
            outline-offset: -4px;
        }}

        /* ---------------------------------------------------------- */
        /* Hover: lift + glow + scale + smooth shadow, relayed from     */
        /* the invisible overlay button to the visual card via :has()   */
        /* ---------------------------------------------------------- */
        div[data-testid="element-container"]:has(> div.workspace-card):has(
            + div[data-testid="element-container"] button:hover
        ) > div.workspace-card {{
            transform: translateY(-10px) scale(1.015);
            border-color: rgba(124, 92, 255, 0.5);
            background: rgba(255, 255, 255, 0.07);
            box-shadow:
                0 24px 60px rgba(0, 0, 0, 0.5),
                0 0 30px rgba(124, 92, 255, 0.35),
                0 0 70px rgba(76, 201, 240, 0.15);
        }}
        div[data-testid="element-container"]:has(> div.workspace-card):has(
            + div[data-testid="element-container"] button:hover
        ) > div.workspace-card::before {{
            opacity: 1;
        }}
        div[data-testid="element-container"]:has(> div.workspace-card):has(
            + div[data-testid="element-container"] button:hover
        ) > div.workspace-card .workspace-card__edge {{
            transform: scaleX(1);
        }}
        div[data-testid="element-container"]:has(> div.workspace-card):has(
            + div[data-testid="element-container"] button:hover
        ) > div.workspace-card .workspace-card__icon {{
            filter: drop-shadow(0 0 18px rgba(124, 92, 255, 0.75));
        }}

        /* ---------------------------------------------------------- */
        /* Click / active state: quick, snappy scale-down                */
        /* ---------------------------------------------------------- */
        div[data-testid="element-container"]:has(> div.workspace-card):has(
            + div[data-testid="element-container"] button:active
        ) > div.workspace-card {{
            transform: translateY(-4px) scale(0.97);
            transition: transform 0.12s ease;
        }}

        /* ---------------------------------------------------------- */
        /* Responsive                                                    */
        /* ---------------------------------------------------------- */
        @media (max-width: 768px) {{
            div.workspace-card {{
                height: auto;
                min-height: 180px;
                padding: 22px 20px;
            }}
            div[data-testid="element-container"]:has(> div.workspace-card)
                + div[data-testid="element-container"] {{
                margin-top: -180px;
            }}
            div[data-testid="element-container"]:has(> div.workspace-card)
                + div[data-testid="element-container"] div[data-testid="stButton"] button {{
                height: 180px;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            div.workspace-card,
            div.workspace-card::before,
            div.workspace-card__edge {{
                transition: none !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )