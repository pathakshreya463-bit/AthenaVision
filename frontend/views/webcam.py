import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/webcam"


def show_webcam_page():

    st.markdown(
        """
        <div class="hero" style="padding:40px;margin-bottom:35px;">

            <div class="hero-eyebrow">
                LIVE AI MONITORING
            </div>

            <h2 style="margin-bottom:10px;">
                Live Occupancy Monitoring
            </h2>

            <p style="color:var(--text-secondary);max-width:700px;">
                Observe classrooms and learning spaces in real time using
                AthenaVision's intelligent computer vision engine.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # STATUS CARDS
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Status", "Ready")

    with col2:
        st.metric("AI Model", "YOLOv8")

    with col3:
        st.metric("Mode", "Live")

    with col4:
        st.metric("Camera", "Webcam")

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # CAMERA + SIDE PANEL
    # -----------------------------

    left, right = st.columns([3, 1])

    with left:

        st.markdown(
            """
            <div class="glass-card"
                 style="
                    height:430px;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    text-align:center;
                 ">

                <div>

                    <div style="
                        font-size:72px;
                        margin-bottom:20px;
                    ">
                        🎥
                    </div>

                    <h3 style="margin-bottom:12px;">
                        Live Camera Feed
                    </h3>

                    <p style="
                        color:var(--text-secondary);
                    ">
                        Your live AI monitoring session
                        will appear here.
                    </p>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            """
            <div class="glass-card">

                <h4>Session</h4>

                <hr>

                <p><b>Status</b><br>Ready</p>

                <p><b>People</b><br>--</p>

                <p><b>Average</b><br>--</p>

                <p><b>Maximum</b><br>--</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # BUTTONS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ Start Monitoring",
            use_container_width=True,
            type="primary",
        ):

            with st.spinner("Launching AthenaVision AI..."):

                try:

                    response = requests.get(API_URL)

                    if response.status_code == 200:

                        data = response.json()

                        st.success(data["message"])

                        st.divider()

                        st.subheader("Monitoring Summary")

                        colA, colB, colC = st.columns(3)

                        with colA:
                            st.metric(
                                "Frames Processed",
                                data["frames_processed"]
                            )

                        with colB:
                            st.metric(
                                "Average People",
                                data["average_people"]
                            )

                        with colC:
                            st.metric(
                                "Maximum People",
                                data["maximum_people"]
                            )

                    else:

                        st.error("Unable to start monitoring.")

                except Exception as e:

                    st.error(f"Server Error: {e}")

    with col2:

        st.button(
            "■ Stop Monitoring",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # INFORMATION
    # -----------------------------

    st.markdown(
        """
        <div class="glass-card">

            <h3>Monitoring Information</h3>

            <p>

            • Real-time occupancy detection using YOLOv8.<br>

            • Automatic CSV logging every five seconds.<br>

            • Automatic data cleaning after monitoring.<br>

            • Activity history updated after every session.<br>

            • Results available instantly in the Insights dashboard.

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )