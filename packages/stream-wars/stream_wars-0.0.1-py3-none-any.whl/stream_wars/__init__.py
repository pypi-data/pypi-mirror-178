"""Registry of React component to Streamlit."""
from importlib.metadata import version
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent

_RELEASE = st.secrets.get("STREAMLIT_RELEASE", True)

project = Path(__file__).parent
__version__ = version(project.stem)

if _RELEASE:
    build_dir = project / "frontend" / "build"
    _stream_wars = components.declare_component("stream_wars", path=build_dir)
else:
    _stream_wars = components.declare_component(
        "stream_wars",
        url="http://localhost:3000",
    )


def stream_wars(
    button_text: str,
    *,
    intro: str,
    title: str,
    episode_number: str,
    episode_title: str,
    content: str,
    key: str = None,
) -> CustomComponent:
    """
    Star wars crawl component for Streamlit.

    :param button_text: text to include in the button to open the crawl component
    :param intro: intro text (i.e.: "A long time ago, in a galaxy far, far, away...")
    :param title: title (i.e.: "STAR WARS") - case insensitive (always upper cased)
    :param episode_number: episode number text (i.e.: "Episode IV")
    :param episode_title: episode title text (i.e.: "A NEW HOPE") - case sensitive
    :param content: episode content (i.e.: "It is a period of civil war [...]")
    :param key: Streamlit key to distinguish components
    :return: Streamlit-compatible component (component itself returns `None`)
    """
    return _stream_wars(
        button_text=button_text,
        intro=intro,
        title=title,
        episode_number=episode_number,
        episode_title=episode_title,
        content=content,
        key=key,
    )
