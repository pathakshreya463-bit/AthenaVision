
import streamlit as st
import requests


API_URL = "http://127.0.0.1:5000/image"


def show_image_page():

    st.title("📷 Visual Analysis")

    st.write(
        "Analyze all images inside the datasets/images folder using the AthenaVision AI engine."
    )

    st.write("")

    if st.button(
        "🚀 Start Image Analysis",
        use_container_width=True
    ):

        with st.spinner("Analyzing images..."):

            try:

                response = requests.post(API_URL)

                if response.status_code == 200:

                    result = response.json()

                    st.success(result["message"])

                    st.metric(
                        "Images Analyzed",
                        result["data"]["total_images"]
                    )

                    st.metric(
                        "Total People",
                        result["data"]["total_people"]
                    )

                    st.metric(
                        "Average People",
                        result["data"]["average_people"]
                    )

                    st.write("### Individual Results")

                    st.dataframe(
                        result["data"]["results"],
                        use_container_width=True
                    )

                else:

                    st.error("Image analysis failed.")

            except Exception as e:

                st.error(f"Server Error: {e}")

