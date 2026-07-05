import streamlit as st
import pandas as pd
import os

HISTORY_FILE = "datasets/history/activity_history.csv"


def show_history_page():

    st.title("🕒 Activity History")

    st.write(
        """
        Review all AI analysis sessions performed by AthenaVision.
        """
    )

    st.divider()

    if not os.path.exists(HISTORY_FILE):

        st.warning("No activity history found.")

        return

    df = pd.read_csv(HISTORY_FILE)

    if df.empty:

        st.info("No activities recorded yet.")

        return

    st.metric(
        "Total Activities",
        len(df)
    )

    st.write("")

    st.dataframe(
        df.iloc[::-1],
        use_container_width=True,
        hide_index=True
    )