import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/analytics"


def show_insights_page():

    st.title("📊 AthenaVision Insights")

    st.write(
        "View occupancy statistics generated from image analysis and live monitoring."
    )

    st.divider()

    try:

        response = requests.get(API_URL)

        if response.status_code == 200:

            result = response.json()

            if result["status"] == "success":

                data = result["data"]

                st.subheader("📷 Image Analysis")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Records", data["image"]["records"])

                with col2:
                    st.metric("Average", data["image"]["average"])

                with col3:
                    st.metric("Maximum", data["image"]["maximum"])

                with col4:
                    st.metric("Minimum", data["image"]["minimum"])

                st.divider()

                st.subheader("🎥 Live Monitoring")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Records", data["webcam"]["records"])

                with col2:
                    st.metric("Average", data["webcam"]["average"])

                with col3:
                    st.metric("Maximum", data["webcam"]["maximum"])

                with col4:
                    st.metric("Minimum", data["webcam"]["minimum"])

        else:

            st.error("Unable to retrieve analytics.")

    except Exception as e:

        st.error(f"Server Error: {e}")