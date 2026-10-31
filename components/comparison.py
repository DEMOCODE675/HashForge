"""Side-by-side comparison tables and diff indicators for HashForge."""

import streamlit as st
from core.avalanche import AvalancheMetrics
from core.hash_engine import HashResult


def render_comparison_summary(
    orig_hash: HashResult,
    mod_hash: HashResult,
    metrics: AvalancheMetrics,
    title: str = "Cryptographic Avalanche Comparison",
) -> None:
    """Render a side-by-side comparison of original and perturbed hashes.

    Args:
        orig_hash: Original HashResult.
        mod_hash: Perturbed HashResult.
        metrics: AvalancheMetrics.
        title: Header text.
    """
    st.markdown(f"### {title}")

    # Top Metric Banner
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">Hamming Distance</div>
                <div class="hf-metric-value hf-metric-amber">{metrics.hamming_distance}</div>
                <div style="font-size:0.75rem; color:#94A3B8;">out of 256 output bits</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">Avalanche Effect</div>
                <div class="hf-metric-value hf-metric-cyan">{metrics.avalanche_percentage:.2f}%</div>
                <div style="font-size:0.75rem; color:#94A3B8;">Target ≈ 50.00%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">Unchanged Bits</div>
                <div class="hf-metric-value">{metrics.unchanged_count}</div>
                <div style="font-size:0.75rem; color:#94A3B8;">Identical positions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">Deviation from Ideal</div>
                <div class="hf-metric-value hf-metric-emerald">{metrics.distance_from_ideal:.2f}%</div>
                <div style="font-size:0.75rem; color:#94A3B8;">|Actual - 50.00%|</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Side-by-side Hex comparison
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Original Hash (SHA-256):**")
        st.code(orig_hash.hex_digest, language="text")
    with col_b:
        st.markdown("**Modified Hash (Perturbed Output):**")
        st.code(mod_hash.hex_digest, language="text")

