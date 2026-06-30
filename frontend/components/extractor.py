import time
import streamlit as st

from components.cards import render_info_card
from services.api import mock_extract_response


def render_extractor() -> None:
    st.markdown("<h2 style='margin-bottom:0.3rem;'>AI Extractor</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Paste travel context or upload a file, then let the offline AI structure the information.</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        travel_text = st.text_area(
            "Travel information",
            placeholder="I want to visit Charminar, eat biryani and shop for bangles.",
            height=140,
        )
        st.markdown("<div style='text-align:center; margin:0.8rem 0;'>OR</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload travel material", type=["pdf", "png", "jpg", "jpeg"])
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Extract Information", type="primary"):
            if not travel_text.strip() and uploaded_file is None:
                st.warning("Please enter some travel context or upload a file to continue.")
                return

            progress = st.progress(0)
            status = st.empty()
            steps = [
                "Reading travel information...",
                "Finding places...",
                "Finding restaurants...",
                "Finding activities...",
                "Understanding preferences...",
            ]

            for index, message in enumerate(steps, start=1):
                status.text(message)
                progress.progress(index / len(steps))
                time.sleep(0.45)

            extracted = mock_extract_response()
            st.session_state.extracted_data = extracted
            st.session_state.recommendations_unlocked = True
            st.session_state.current_page = "extractor"
            st.session_state.hero_completed = True
            st.success("Extraction complete. Your structured travel profile is ready.")

            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(2)
            with cols[0]:
                render_info_card("Places", extracted["places"], "📍")
            with cols[1]:
                render_info_card("Food", extracted["food"], "🍛")
            cols = st.columns(2)
            with cols[0]:
                render_info_card("Activities", extracted["activities"], "🛍")
            with cols[1]:
                render_info_card("Budget", [extracted["budget"]], "💰")
            cols = st.columns(2)
            with cols[0]:
                render_info_card("Duration", [extracted["duration"]], "📅")
            with cols[1]:
                render_info_card("Group", [extracted["group"]], "👨‍👩‍👧")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continue to Recommendations", type="primary"):
                st.session_state.current_page = "recommendations"
                st.rerun()
