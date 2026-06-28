
import streamlit as st


def workspace_card(icon, title, description, key, page):

    st.markdown(
        f"""
        <div class="glass-card">

            <div class="card-icon">
                {icon}
            </div>

            <div class="card-title">
                {title}
            </div>

            <div class="card-text">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"Open {title} →",
        key=key,
        use_container_width=True
    ):
        st.session_state.page = page
        st.rerun()
