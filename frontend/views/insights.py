import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/analytics"


def show_insights_page():

    st.markdown(
        """
        <div class="hero" style="padding:40px;margin-bottom:35px;">

            <div class="hero-eyebrow">
                ANALYTICS DASHBOARD
            </div>

            <h2 style="margin-bottom:10px;">
                Occupancy Insights
            </h2>

            <p style="color:var(--text-secondary);max-width:700px;">
                Analyze occupancy statistics generated from image analysis
                and live monitoring sessions using AthenaVision.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    try:

        response = requests.get(API_URL)

        if response.status_code != 200:

            st.error("Unable to load analytics.")
            return

        data = response.json()

    except Exception as e:

        st.error(f"Server Error: {e}")
        return

    webcam = data["webcam"]
    image = data["image"]

    # ---------------------------------------------------
    # IMAGE ANALYSIS
    # ---------------------------------------------------

    st.subheader("📷 Image Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Records", image["records"])

    with col2:
        st.metric("Average", image["average"])

    with col3:
        st.metric("Maximum", image["maximum"])

    with col4:
        st.metric("Minimum", image["minimum"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # LIVE MONITORING
    # ---------------------------------------------------

    st.subheader("🎥 Live Monitoring")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Records", webcam["records"])

    with col2:
        st.metric("Average", webcam["average"])

    with col3:
        st.metric("Maximum", webcam["maximum"])

    with col4:
        st.metric("Minimum", webcam["minimum"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------

    st.markdown(
        """
        <div class="glass-card">

            <h3>Summary</h3>

            <p>

            AthenaVision combines image analysis and live monitoring
            to provide intelligent occupancy analytics for academic
            environments. The statistics shown above are generated
            from the cleaned datasets and updated automatically after
            every analysis session.

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # QUICK COMPARISON
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="glass-card">

                <h4>Image Analysis</h4>

                <ul>
                    <li>Static image processing</li>
                    <li>Fast occupancy estimation</li>
                    <li>Ideal for classrooms and libraries</li>
                </ul>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="glass-card">

                <h4>Live Monitoring</h4>

                <ul>
                    <li>Real-time webcam analysis</li>
                    <li>Continuous occupancy tracking</li>
                    <li>Automatic CSV logging</li>
                </ul>

            </div>
            """,
            unsafe_allow_html=True,
        )