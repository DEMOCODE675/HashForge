"""Metric display cards for HashForge visual summaries."""

from typing import List, Tuple
import streamlit as st


def render_metric_card(
    title: str,
    value: str,
    subtitle: str = "",
    color_accent: str = "cyan",
    help_text: str = "",
) -> None:
    """Render a styled metric card.

    Args:
        title: Metric title.
        value: Main numeric or text value.
        subtitle: Secondary descriptive text.
        color_accent: 'cyan', 'emerald', 'amber', or 'rose'.
        help_text: Optional tooltip text.
    """
    accent_class = f"hf-metric-{color_accent}"

    tooltip_attr = f'title="{help_text}"' if help_text else ""
    st.markdown(
        f"""
        <div class="hf-metric-card" {tooltip_attr}>
            <div class="hf-metric-title">{title}</div>
            <div class="hf-metric-value {accent_class}">{value}</div>
            {"<div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>" + subtitle + "</div>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_row(metrics: List[Tuple[str, str, str, str]]) -> None:
    """Render a row of metric cards using Streamlit columns.

    Args:
        metrics: List of (title, value, subtitle, color_accent) tuples.
    """
    cols = st.columns(len(metrics))
    for col, (title, val, sub, acc) in zip(cols, metrics):
        with col:
            render_metric_card(title, val, sub, acc)

