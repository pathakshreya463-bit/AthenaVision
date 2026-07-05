
import streamlit as st

from views.home import show_home
from views.image_analysis import show_image_page
from views.webcam import show_webcam_page
from views.insights import show_insights_page
from views.video import show_video_page

from components.theme import load_theme
from views.history import show_history_page

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AthenaVision",
    page_icon="🎓",
    layout="wide"
)

load_theme()

st.markdown("""
<style>

.block-container{
    padding-top:0rem;
    padding-left:4rem;
    padding-right:4rem;
    padding-bottom:0rem;
    max-width:100%;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

PAGES = [
    "🏠 Home",
    "📷 Visual Analysis",
    "📹 Live Monitoring",
    "📊 Insights",
    "🎥 Video Intelligence",
    "🕒 Activity History",
]

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎓 AthenaVision")

selected = st.sidebar.radio(
    "Mission Control",
    PAGES,
    index=PAGES.index(st.session_state.page)
)

# If the user changed the sidebar,
# update the current page.

if selected != st.session_state.page:
    st.session_state.page = selected

# This is the page used everywhere.
page = st.session_state.page

# --------------------------------------------------
# ROUTER
# --------------------------------------------------

if page == "🏠 Home":

    show_home()

elif page == "📷 Visual Analysis":

    show_image_page()

elif page == "📹 Live Monitoring":

    show_webcam_page()

elif page == "📊 Insights":

    show_insights_page()

elif page == "🕒 Activity History":

    show_history_page()
    
elif page == "🎥 Video Intelligence":

    show_video_page()
