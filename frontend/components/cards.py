import streamlit as st


def workspace_card(icon, title, description, key, page):

    with st.container():

        st.markdown(
            f"""
            <div class="workspace-card">

                <div style="font-size:58px;text-align:center;margin-bottom:18px;">
                    {icon}
                </div>

                <div class="workspace-card__title"
                     style="text-align:center;font-size:1.5rem;margin-bottom:12px;">

                    {title}

                </div>

                <div style="
                    text-align:center;
                    color:var(--text-secondary);
                    line-height:1.7;
                    min-height:72px;
                    margin-bottom:20px;
                ">

                    {description}

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"Launch {title}",
            key=key,
            use_container_width=True,
        ):
            st.session_state.page = page
            st.rerun()