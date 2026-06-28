
import streamlit as st

from components.hero import hero
from components.cards import workspace_card


def show_home():

    # ---------------- HERO ---------------- #

    hero()

    # Space before workspace section
    st.markdown(
        """
        <div style="height:140px;"></div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- WORKSPACE TITLE ---------------- #

    st.markdown(
        """
        <div class="workspace-section">

            <div class="workspace-heading">
                Choose Your Workspace
            </div>

            <div class="workspace-subheading">
                Select a module to begin exploring your academic environment.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- FIRST ROW ---------------- #

    col1, col2 = st.columns(2, gap="large")

    with col1:

        workspace_card(
            icon="👁",
            title="Vision",
            description="""
            Analyze classrooms, libraries and study spaces
            using Artificial Intelligence.
            """,
            key="vision_card",
            page="📷 Visual Analysis",
        )

    with col2:

        workspace_card(
            icon="📹",
            title="Monitor",
            description="""
            Observe occupancy in real time through
            intelligent webcam monitoring.
            """,
            key="monitor_card",
            page="📹 Live Monitoring",
        )

    st.write("")
    st.write("")

    # ---------------- SECOND ROW ---------------- #

    col3, col4 = st.columns(2, gap="large")

    with col3:

        workspace_card(
            icon="📊",
            title="Insights",
            description="""
            Explore occupancy trends,
            reports and visual analytics.
            """,
            key="insights_card",
            page="📊 Insights",
        )

    with col4:

        workspace_card(
            icon="🎥",
            title="Video",
            description="""
            Analyze recorded videos and
            generate intelligent observations.
            """,
            key="video_card",
            page="🎥 Video Intelligence",
        )

    # ---------------- FOOTER SPACE ---------------- #

    st.markdown(
        """
        <div style="height:80px;"></div>
        """,
        unsafe_allow_html=True,
    )

