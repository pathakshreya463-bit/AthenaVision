from pathlib import Path
import streamlit as st


def load_theme():

    css = Path("frontend/assets/styles.css").read_text()

    st.markdown(

        f"<style>{css}</style>",

        unsafe_allow_html=True

    )