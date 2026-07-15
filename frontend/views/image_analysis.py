import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/image"


def show_image_page():

    st.markdown(
        """
        <div class="hero" style="padding:40px;margin-bottom:35px;">

            <div class="hero-eyebrow">
                COMPUTER VISION
            </div>

            <h2 style="margin-bottom:10px;">
                Image Analysis
            </h2>

            <p style="color:var(--text-secondary);max-width:700px;">
                Upload classroom, laboratory or library images and let
                AthenaVision detect occupancy using artificial intelligence.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(

        "Upload Image",

        type=["jpg", "jpeg", "png", "webp"]

    )

    if uploaded_file:

        st.markdown("### Image Preview")

        st.image(
            uploaded_file,
            use_container_width=True,
        )

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Status", "Ready")

        with col2:
            st.metric("AI Model", "YOLOv8")

        with col3:
            st.metric("Source", "Uploaded")

        st.write("")

        if st.button(
            "Analyze Image",
            use_container_width=True,
            type="primary",
        ):

            with st.spinner("AthenaVision AI is analyzing the image..."):

                try:
                    files = {
                        "image": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }

                    response = requests.post(
                        API_URL,
                        files=files
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.success("Analysis completed successfully.")
                        st.divider()
                        st.subheader("Detection Results")
                        st.json(result)
                    else:
                        st.error("Image analysis failed.")

                except Exception as e:
                    st.error(f"Server Error: {e}")

    else:

        st.info(
            "Upload an image to begin AI-powered occupancy analysis."
        )