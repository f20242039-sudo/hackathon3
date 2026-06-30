import streamlit as st


def render_feature_card(icon: str, title: str, description: str, button_label: str, button_action, status: str, primary: bool = False, disabled: bool = False) -> None:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown(f"<div class='feature-icon'>{icon}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0.25rem 0'>{title}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='muted-text'>{description}</p>", unsafe_allow_html=True)
    if st.button(button_label, key=f"{title.lower()}-button", type="primary" if primary else "secondary", disabled=disabled):
        button_action()
    st.markdown(f"<p class='info-pill'>{status}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_info_card(title: str, items: list[str], icon: str) -> None:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown(f"<h4>{icon} {title}</h4>", unsafe_allow_html=True)
    for item in items:
        st.markdown(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)
