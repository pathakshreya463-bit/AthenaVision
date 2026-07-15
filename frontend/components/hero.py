import streamlit as st


def hero():

    st.markdown(
        """
        <section class="hero">

            <div class="hero-eyebrow">
                AI-Powered Academic Analytics Platform
            </div>

            <h1 class="hero-title">
                ATHENAVISION
            </h1>

            <h3 class="hero-subtitle">
                Observe. Understand. Optimize.
            </h3>

            <div style="height:22px;"></div>

            <p style="
                max-width:760px;
                margin:auto;
                text-align:center;
                font-size:1.12rem;
                color:var(--text-secondary);
                line-height:1.9;
            ">
                AthenaVision transforms classrooms, libraries and collaborative
                learning spaces through intelligent computer vision analytics.
                Monitor occupancy, analyze images, generate insights and make
                data-driven decisions from one unified platform.
            </p>

            <div style="height:45px;"></div>

            <div style="
                display:flex;
                justify-content:center;
                gap:20px;
                flex-wrap:wrap;
            ">

                <div class="stat-card">

                    <div class="stat-card__value">
                        AI
                    </div>

                    <div class="stat-card__label">
                        Vision Powered
                    </div>

                </div>

                <div class="stat-card">

                    <div class="stat-card__value">
                        YOLOv8
                    </div>

                    <div class="stat-card__label">
                        Detection Engine
                    </div>

                </div>

                <div class="stat-card">

                    <div class="stat-card__value">
                        Flask
                    </div>

                    <div class="stat-card__label">
                        Backend API
                    </div>

                </div>

                <div class="stat-card">

                    <div class="stat-card__value">
                        Live
                    </div>

                    <div class="stat-card__label">
                        Monitoring
                    </div>

                </div>

            </div>

            <div style="height:60px;"></div>

            <div style="
                text-align:center;
                color:var(--text-muted);
                font-family:var(--font-mono);
                letter-spacing:.12em;
                font-size:.82rem;
                text-transform:uppercase;
            ">

                Scroll to explore workspaces

            </div>

            <div style="
                text-align:center;
                font-size:28px;
                color:var(--accent-cyan);
                margin-top:8px;
                animation:bounce 2.5s infinite;
            ">

                ↓

            </div>

        </section>
        """,
        unsafe_allow_html=True,
    )