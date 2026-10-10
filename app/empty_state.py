"""Copy and rendering helpers for an empty knowledge graph."""


def empty_graph_content() -> tuple[str, str, str]:
    """Returns the heading, description, and chat destination for an empty graph."""
    return (
        "No knowledge graph yet",
        "Open the Chat tab and start a conversation to create memories and reveal the people, concepts, and relationships that matter to you.",
        "#chat-interface",
    )


def render_empty_graph_state() -> None:
    """Renders a styled empty state that points users toward chatting."""
    import streamlit as st

    heading, description, chat_anchor = empty_graph_content()
    st.markdown(
        f"""
        <div style="border: 1px dashed #4b5563; border-radius: 12px; padding: 48px 24px; text-align: center;">
          <svg aria-hidden="true" width="56" height="56" viewBox="0 0 56 56" fill="none" stroke="#60a5fa" stroke-width="2.5" style="margin-bottom: 8px;">
            <path d="M28 9c-6-7-17-2-16 7C3 17 4 29 11 31c-2 9 8 15 14 10 1 7 10 7 13 1 8 3 14-7 8-13 7-5 2-16-6-15 0-9-7-11-12-5Z"/>
            <path d="M28 9v36M17 20c5 0 6 5 11 5M39 20c-5 0-6 5-11 5M16 33c5 0 7-4 12-3M40 33c-5 0-7-4-12-3"/>
          </svg>
          <h3 style="margin: 12px 0 8px;">{heading}</h3>
          <p style="color: #9ca3af; margin: 0 auto 20px; max-width: 420px;">{description}</p>
          <a href="{chat_anchor}" target="_self" style="background: #2563eb; border-radius: 6px; color: white; display: inline-block; font-weight: 600; padding: 10px 16px; text-decoration: none;">Start chatting</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
