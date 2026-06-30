import streamlit as st

from services.api import mock_recommendations_response


def render_recommendations() -> None:
    st.markdown("<h2 style='margin-bottom:0.3rem;'>Recommendations</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>These picks are shaped around your extracted interests and travel context.</p>", unsafe_allow_html=True)

    if not st.session_state.extracted_data:
        st.info("Complete extraction first to unlock tailored recommendations.")
        return

    recommendations = st.session_state.recommendations or mock_recommendations_response()
    st.session_state.recommendations = recommendations
    st.session_state.planner_unlocked = True

    for item in recommendations:
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='margin-bottom:0.2rem;'>{item['name']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p class='info-pill'>{item['category']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='muted-text'>{item['description']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Reason:</strong> {item['reason']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Trip", type="primary"):
        st.session_state.current_page = "planner"
        st.rerun()
