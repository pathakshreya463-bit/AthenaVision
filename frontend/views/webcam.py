import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:5000/webcam"


def show_webcam_page():

    st.title("🎥 Live Monitoring")

    st.write(
        """
        Monitor classrooms, libraries and study spaces in real time using
        AthenaVision's AI-powered occupancy detection.
        """
    )

    st.divider()

    # --------------------------
    # Session State
    # --------------------------

    if "monitoring" not in st.session_state:
        st.session_state.monitoring = False

    # --------------------------
    # Metrics
    # --------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        status = "🟢 Running" if st.session_state.monitoring else "⚪ Ready"
        st.metric("Status", status)

    with col2:
        st.metric("People", "--")

    with col3:
        st.metric("Average", "--")

    st.divider()

    # --------------------------
    # Camera Placeholder
    # --------------------------

    camera_placeholder = st.empty()

    if not st.session_state.monitoring:

        camera_placeholder.info(
            "Camera preview will appear here when monitoring starts."
        )

    st.write("")

    # --------------------------
    # Buttons
    # --------------------------

    left, right = st.columns(2)

    with left:

        if st.button(
            "▶ Start Monitoring",
            use_container_width=True,
            disabled=st.session_state.monitoring
        ):

            st.session_state.monitoring = True

            with st.spinner("Starting AthenaVision AI Engine..."):

                try:

                    response = requests.post(API_URL)

                    if response.status_code == 200:

                        result = response.json()

                        st.success(result["message"])

                        st.rerun()

                    else:

                        st.error("Unable to start monitoring.")

                except Exception as e:

                    st.error(f"Server Error: {e}")

                    st.session_state.monitoring = False

    with right:

        if st.button(
            "■ Stop Monitoring",
            use_container_width=True,
            disabled=not st.session_state.monitoring
        ):

            st.session_state.monitoring = False

            st.success("Monitoring stopped.")

            st.rerun()

    st.divider()

    st.subheader("Live Session")

    st.info(
        """
        🚧 Live video streaming inside AthenaVision will be connected to the backend
        in the next step. The backend communication is already implemented.
        """
    )