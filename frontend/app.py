import streamlit as st

# --------------------------------------------------
# THEME
# --------------------------------------------------

from components.theme import load_theme

# --------------------------------------------------
# PAGES
# --------------------------------------------------

from views.home import show_home
from views.image_analysis import show_image_page
from views.webcam import show_webcam_page
from views.insights import show_insights_page
from views.history import show_history_page
from views.video import show_video_page

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AthenaVision",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_theme()

# --------------------------------------------------
# CUSTOM LAYOUT
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container{

        padding-top:0rem;
        padding-left:3rem;
        padding-right:3rem;
        padding-bottom:2rem;

        max-width:1600px;

    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

PAGES = {
    "🏠 Home": show_home,
    "📷 Visual Analysis": show_image_page,
    "📹 Live Monitoring": show_webcam_page,
    "📊 Insights": show_insights_page,
    "🕒 Activity History": show_history_page,
    "🎥 Video Intelligence": show_video_page,
}
# Safety check
if (
    "page" not in st.session_state
    or st.session_state.page not in PAGES
):
    st.session_state.page = "🏠 Home"

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding-top:20px;">

            <h2 style="margin-bottom:0;">
                AthenaVision
            </h2>

            <p style="
                color:var(--text-secondary);
                font-size:.9rem;
            ">

            AI Academic Analytics

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    selected = st.radio(

        "Mission Control",

        list(PAGES.keys()),

        index=list(PAGES.keys()).index(
            st.session_state.page
        ),

    )

    st.session_state.page = selected

    st.markdown("---")

    st.caption("Version 1.0")

    st.caption("Built with ❤️ using Streamlit + Flask")

# --------------------------------------------------
# PAGE ROUTER
# --------------------------------------------------

PAGES[st.session_state.page]()