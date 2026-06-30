import streamlit as st


def render_sidebar(current_page: str, hero_completed: bool, recommendations_unlocked: bool, planner_unlocked: bool) -> None:
    st.markdown("<h3 style='margin-bottom:0.3rem;'>Chalo Miya AI</h3>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Offline travel assistant</p>", unsafe_allow_html=True)

    pages = [
        ("hero", "🏠 Hero", True),
        ("dashboard", "📊 Dashboard", hero_completed),
        ("extractor", "🤖 AI Extractor", hero_completed),
        ("recommendations", "✨ Recommendations", recommendations_unlocked),
        ("planner", "📅 Trip Planner", planner_unlocked),
    ]

    for page_key, label, enabled in pages:
        if page_key == current_page:
            st.markdown(f"<div class='info-pill' style='display:inline-flex; margin-bottom:0.45rem;'>● {label}</div>", unsafe_allow_html=True)
        elif enabled:
            if st.button(label, key=f"sidebar-{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        else:
            st.button(label, key=f"sidebar-disabled-{page_key}", use_container_width=True, disabled=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset Flow", use_container_width=True):
        st.session_state.hero_completed = False
        st.session_state.current_page = "hero"
        st.session_state.extracted_data = None
        st.session_state.recommendations = None
        st.session_state.trip = None
        st.session_state.recommendations_unlocked = False
        st.session_state.planner_unlocked = False
        st.rerun()
