import streamlit as st


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="kicker">🧭 Offline Hyderabad Travel Assistant</div>
            <h1 class="hero-title">Chalo Miya AI</h1>
            <p class="hero-subtitle">Turn travel fragments into a polished Hyderabad plan</p>
            <p class="muted-text">
                Transform travel blogs, PDFs, screenshots, and natural language into structured travel insights using offline AI.
                The experience is designed to feel like a premium travel copilot from the very first interaction.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Get Started", type="primary"):
        st.session_state.hero_completed = True
        st.session_state.current_page = "dashboard"
        st.rerun()
