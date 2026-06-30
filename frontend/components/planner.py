import streamlit as st

from services.api import mock_trip_response


def render_planner() -> None:
    st.markdown("<h2 style='margin-bottom:0.3rem;'>Trip Planner</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>A premium, step-by-step itinerary that mirrors the flow from extracted interests to a complete day plan.</p>", unsafe_allow_html=True)

    trip = st.session_state.trip or mock_trip_response()
    st.session_state.trip = trip

    st.markdown('<div class="timeline-card">', unsafe_allow_html=True)
    for index, step in enumerate(trip):
        if index > 0:
            st.markdown("<div style='margin:0.35rem 0 0.35rem 1rem;'>↓</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='timeline-node'><strong>{step['time']}</strong><br>{step['title']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
