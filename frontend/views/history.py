import os
import pandas as pd
import streamlit as st

HISTORY_FILE = "datasets/history/activity_history.csv"


def show_history_page():

    st.markdown(
        """
        <div class="hero" style="padding:40px;margin-bottom:35px;">

            <div class="hero-eyebrow">
                ACTIVITY TIMELINE
            </div>

            <h2 style="margin-bottom:10px;">
                Activity History
            </h2>

            <p style="color:var(--text-secondary);max-width:700px;">
                View all image analyses, live monitoring sessions and
                analytics activities performed by AthenaVision.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # CHECK FILE
    # --------------------------------------

    if not os.path.exists(HISTORY_FILE):

        st.warning("No activity history found.")
        return

    df = pd.read_csv(HISTORY_FILE)

    if df.empty:

        st.info("No activities have been recorded yet.")
        return

    # --------------------------------------
    # SEARCH
    # --------------------------------------

    search = st.text_input(
        "🔍 Search Module or Source",
        placeholder="Image Analysis, Webcam..."
    )

    if search:

        df = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]

    # --------------------------------------
    # SUMMARY CARDS
    # --------------------------------------

    st.markdown("### Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Activities", len(df))

    with c2:
        st.metric("Modules", df["Module"].nunique())

    with c3:
        st.metric("Status", "Active")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # RECENT ACTIVITY
    # --------------------------------------

    st.markdown("### Recent Activity")

    history = df.iloc[::-1]

    for _, row in history.iterrows():

        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom:18px;">

                <h4 style="margin-bottom:6px;">
                    {row["Module"]}
                </h4>

                <p style="color:var(--text-secondary);">

                    <b>Time:</b> {row["Time"]}<br>

                    <b>Source:</b> {row["Source"]}<br>

                    <b>People:</b> {row["People"]}<br>

                    <b>Status:</b> {row["Status"]}

                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # FULL TABLE
    # --------------------------------------

    st.markdown("### Complete History")

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------
    # DOWNLOAD
    # --------------------------------------

    st.download_button(
        "⬇ Download Activity History",
        df.to_csv(index=False),
        file_name="activity_history.csv",
        mime="text/csv",
        use_container_width=True,
    )