import streamlit as st
from pathlib import Path

from components.hero import render_hero
from components.dashboard import render_dashboard
from components.extractor import render_extractor
from components.recommendations import render_recommendations
from components.planner import render_planner
from components.sidebar import render_sidebar


def init_session_state() -> None:
    defaults = {
        "hero_completed": False,
        "current_page": "hero",
        "extracted_data": None,
        "recommendations": None,
        "trip": None,
        "recommendations_unlocked": False,
        "planner_unlocked": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_css() -> None:
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="Chalo Miya AI", page_icon="🧭", layout="wide")
    init_session_state()
    load_css()

    st.markdown('<div class="main-shell">', unsafe_allow_html=True)

    with st.sidebar:
        render_sidebar(
            current_page=st.session_state.current_page,
            hero_completed=st.session_state.hero_completed,
            recommendations_unlocked=st.session_state.recommendations_unlocked,
            planner_unlocked=st.session_state.planner_unlocked,
        )

    if not st.session_state.hero_completed:
        render_hero()
    else:
        page = st.session_state.current_page
        if page == "dashboard":
            render_dashboard()
        elif page == "extractor":
            render_extractor()
        elif page == "recommendations":
            render_recommendations()
        elif page == "planner":
            render_planner()
        else:
            render_dashboard()

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
