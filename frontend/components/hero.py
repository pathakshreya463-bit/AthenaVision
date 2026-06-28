import streamlit as st


def hero():

    st.markdown(
        """
        <div class="hero">

            <div class="hero-glow"></div>

            <div class="hero-title">
                ATHENAVISION
            </div>

            <div class="hero-subtitle">
                Observe. Understand. Optimize.
            </div>

            <div class="hero-description">

                Transforming Academic Spaces Through Intelligent Vision Analytics
                for Classrooms, Libraries and Collaborative Learning Spaces.

            </div>

            <div class="hero-scroll">

                ↓ Explore

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )