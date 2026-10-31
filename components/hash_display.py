"""Formatted hash displays, copy utilities, and digest inspect widgets."""

import streamlit as st
from core.hash_engine import HashResult


def render_hash_card(result: HashResult, label: str = "Digest Output") -> None:
    """Render a comprehensive hash result card with hex, binary, and metadata.

    Args:
        result: Computed HashResult.
        label: Custom section label.
    """
    algo_name = result.algorithm.upper()
    badge_class = "hf-badge-cyan" if "3" not in result.algorithm else "hf-badge-emerald"

    st.markdown(
        f"""
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC;">{label}</div>
                <div>
                    <span class="hf-badge {badge_class}">{algo_name}</span>
                    <span class="hf-badge hf-badge-cyan" style="margin-left: 6px;">{result.digest_bits} BITS</span>
                </div>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                Hexadecimal Digest (64 Chars / 32 Bytes)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Use native st.code for effortless one-click copying
    st.code(result.hex_digest, language="text")

    # Expandable binary and timing inspection
    with st.expander("🔍 View Formatted Hex & Raw Binary Digest", expanded=False):
        st.markdown("**Chunked Hex (8-Char Blocks):**")
        st.code(result.formatted_hex, language="text")

        st.markdown("**Raw Binary String (256 Bits):**")
        st.code(result.binary_digest, language="text")

        st.markdown(
            f"""
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 8px;">
                Computation Latency: <b style="color: #00F0FF;">{result.execution_time_ms:.4f} ms</b> |
                Input Length: <b>{result.input_length_bytes} bytes</b>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_copyable_hash(hex_digest: str, label: str = "Hash Digest") -> None:
    """Render a compact copyable hash row."""
    st.markdown(f"**{label}:**")
    st.code(hex_digest, language="text")

