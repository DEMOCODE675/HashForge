"""Unified sidebar navigation and CSS injector for HashForge."""

import os
import streamlit as st


def load_css() -> None:
    """Inject custom CSS stylesheet into the Streamlit session."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render unified HashForge sidebar branding and status widgets."""
    load_css()

    with st.sidebar:
        # Brand Header
        st.markdown(
            """
            <div style="text-align: center; padding: 12px 0 18px 0; border-bottom: 1px solid #1F2937;">
                <h2 style="margin: 0; font-size: 1.6rem; letter-spacing: 2px;">
                    HASH<span style="color: #00F0FF;">FORGE</span>
                </h2>
                <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px; letter-spacing: 1.5px;">
                    CRYPTOGRAPHIC AVALANCHE LAB
                </div>
                <div style="margin-top: 10px;">
                    <span class="hf-badge hf-badge-emerald">v2.0 • FIPS Active</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Laboratory Modules Index
        st.markdown(
            """
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748B; font-weight: 700; margin-bottom: 8px; letter-spacing: 1px;">
                Laboratory Modules
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8;">
                <div>🔬 <b>1. Hash Generator</b></div>
                <div>⚖️ <b>2. Algorithm Lab</b></div>
                <div>⚡ <b>3. Single-Bit Experiment</b></div>
                <div>🔀 <b>4. Multi-Bit Experiment</b></div>
                <div>📊 <b>5. Avalanche Analyzer</b></div>
                <div>🛡️ <b>6. File Integrity Lab</b></div>
                <div>📚 <b>7. Learning Center</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

        # Cryptographic Engine Spec
        st.markdown(
            """
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748B; font-weight: 700; margin-bottom: 8px; letter-spacing: 1px;">
                Engine Architecture
            </div>
            <div style="font-size: 0.8rem; color: #94A3B8;">
                <div>• <b>SHA-256</b> (FIPS 180-4, Merkle-Damgård)</div>
                <div>• <b>SHA3-256</b> (FIPS 202, Keccak Sponge)</div>
                <div>• <b>Bit Indexing</b>: Big-Endian / Network</div>
                <div>• <b>Backend</b>: Python C-hashlib (Offline)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

        # Educational Disclaimer
        st.markdown(
            """
            <div style="background-color: rgba(245, 158, 11, 0.08); border-left: 3px solid #F59E0B; padding: 10px 12px; border-radius: 0 6px 6px 0;">
                <div style="font-size: 0.72rem; color: #F59E0B; font-weight: 700; margin-bottom: 3px;">
                    EDUCATIONAL PLATFORM
                </div>
                <div style="font-size: 0.75rem; color: #D1D5DB; line-height: 1.4;">
                    Designed for interactive classroom visualization &amp; research demonstration. No proprietary hashes invented.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

