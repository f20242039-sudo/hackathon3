import streamlit as st

from components.cards import render_feature_card


def render_dashboard() -> None:
    st.markdown("<h2 style='margin-bottom:0.3rem;'>Your travel workflow</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Follow the guided flow from extraction to itinerary in a few focused steps.</p>", unsafe_allow_html=True)

    extractor_status = "✅ Completed" if st.session_state.extracted_data else "✅ Available"
    recommendations_status = "✅ Available" if st.session_state.recommendations_unlocked else "🔒 Locked"
    planner_status = "✅ Available" if st.session_state.planner_unlocked else "🔒 Locked"

    cols = st.columns(3)
    with cols[0]:
        render_feature_card(
            icon="🤖",
            title="AI Extractor",
            description="Convert travel blogs, PDFs and screenshots into structured travel data.",
            button_label="Open",
            button_action=lambda: setattr(st.session_state, "current_page", "extractor") or st.rerun(),
            status=extractor_status,
            primary=True,
        )

    with cols[1]:
        render_feature_card(
            icon="✨",
            title="Recommendations",
            description="Receive personalized recommendations based on extracted travel insights.",
            button_label="Open",
            button_action=lambda: setattr(st.session_state, "current_page", "recommendations") or st.rerun(),
            status=recommendations_status,
            disabled=not st.session_state.recommendations_unlocked,
        )

    with cols[2]:
        render_feature_card(
            icon="📅",
            title="Trip Planner",
            description="Generate a complete Hyderabad itinerary tailored to your journey.",
            button_label="Open",
            button_action=lambda: setattr(st.session_state, "current_page", "planner") or st.rerun(),
            status=planner_status,
            disabled=not st.session_state.planner_unlocked,
        )

    if st.session_state.extracted_data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Extraction complete. You can now explore recommendations and start planning your trip.")
