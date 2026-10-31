"""HashForge: Cryptographic Hashing & Avalanche Effect Visualization Laboratory.

Home Dashboard and Platform Overview.
"""

import os
import streamlit as st
from components.sidebar import render_sidebar, load_css

st.set_page_config(
    page_title="HashForge — Cryptography Laboratory",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ingest Design System & Sidebar
render_sidebar()

# Hero Section
col_hero, col_stat = st.columns([2.5, 1.2])

with col_hero:
    # Render SVG Logo
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")
    if os.path.exists(logo_path):
        with open(logo_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        st.markdown(
            f'<div style="max-width: 460px; margin-bottom: 8px;">{svg_content}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("# 🛡️ HASHFORGE")

    st.markdown(
        """
        ### An Interactive Cryptographic Hashing & Avalanche Effect Visualization Laboratory
        **HashForge** bridges the gap between theoretical cryptographic principles and empirical understanding.
        Explore how small input perturbations cascade through **SHA-256** and **SHA3-256** compression networks to yield
        statistically uncorrelated, pseudo-random outputs.
        """
    )

with col_stat:
    st.markdown(
        """
        <div class="hf-card hf-card-accent" style="margin-top: 10px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #00F0FF; text-transform: uppercase; letter-spacing: 1px;">
                Platform Specs
            </div>
            <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 8px; line-height: 1.6;">
                <div>⚡ <b>Target Avalanche:</b> 50.00%</div>
                <div>🔒 <b>Digest Bit-Length:</b> 256 Bits</div>
                <div>📐 <b>Distance Metric:</b> Hamming Distance</div>
                <div>🏛️ <b>Standards:</b> FIPS 180-4 / FIPS 202</div>
                <div>💻 <b>Runtime:</b> 100% Local / Zero Cloud</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Laboratory Modules Grid
st.markdown("## 🔬 Interactive Laboratory Modules")
st.markdown("Select a module from the sidebar or jump directly into an experiment below:")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🔬</span>
                <span class="hf-badge hf-badge-cyan">Module 1</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">Hash Generator</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Compute SHA-256 and SHA3-256 hashes with real-time byte counters, chunked hex breakdowns, and file export.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🔀</span>
                <span class="hf-badge hf-badge-cyan">Module 4</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">Multi-Bit Experiment</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Perturb multiple distinct bit positions simultaneously and investigate if multi-bit changes yield proportional output shifts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_m2:
    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">⚖️</span>
                <span class="hf-badge hf-badge-emerald">Module 2</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">Algorithm Lab</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Compare SHA-2 Merkle-Damgård vs SHA-3 Keccak Sponge architectures, execution latency benchmarks, and padding dynamics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">📊</span>
                <span class="hf-badge hf-badge-emerald">Module 5</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">Avalanche Analyzer</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Execute automated 10 to 500-trial Monte Carlo simulations with interactive Plotly histograms, standard deviation, and mean tracking.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_m3:
    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">⚡</span>
                <span class="hf-badge hf-badge-amber">Module 3</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">Single-Bit Flip Lab</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Invert exactly one input bit via XOR and visualize every altered bit across the 256-bit output grid with color-coded highlighting.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🛡️</span>
                <span class="hf-badge hf-badge-amber">Module 6</span>
            </div>
            <h4 style="margin: 0 0 6px 0;">File Integrity Lab</h4>
            <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                Demonstrate streaming chunked hashing for files, detect single-byte tampering, and verify against reference distribution checksums.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hf-card" style="margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.6rem;">📚</span>
                <div>
                    <h4 style="margin: 0;">Learning Center &amp; Cryptography Quiz</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8; margin: 2px 0 0 0;">
                        12 foundational educational topics with real-world applications and an interactive 10-question knowledge evaluation.
                    </p>
                </div>
            </div>
            <span class="hf-badge hf-badge-cyan">Module 7</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 24px 0;'/>", unsafe_allow_html=True)

# Core Concepts Briefing
st.markdown("### 🔑 Core Mathematical Foundations")
col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.markdown(
        """
        <div class="hf-card">
            <h5 style="color: #00F0FF; margin-top:0;">The Avalanche Effect</h5>
            <p style="font-size: 0.82rem; color: #94A3B8;">
                First formalized by Horst Feistel and Claude Shannon (diffusion), a cryptographic hash exhibits the <b>Strict Avalanche Criterion (SAC)</b>
                if each output bit changes with a probability of $p \\approx 0.5$ whenever a single input bit is complemented.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c2:
    st.markdown(
        """
        <div class="hf-card">
            <h5 style="color: #10B981; margin-top:0;">Hamming Distance</h5>
            <p style="font-size: 0.82rem; color: #94A3B8;">
                The Hamming distance $D(H_1, H_2)$ between two binary sequences is the number of positions where corresponding bits differ.
                For a 256-bit digest, ideal diffusion produces:
                $$\\mathbb{E}[D] = 128 \\text{ bits} \\quad (50.0\\%)$$
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c3:
    st.markdown(
        """
        <div class="hf-card">
            <h5 style="color: #F59E0B; margin-top:0;">Bit Indexing Standard</h5>
            <p style="font-size: 0.82rem; color: #94A3B8;">
                HashForge implements <b>Big-Endian Network Indexing</b>:
                $$i = \\lfloor k / 8 \\rfloor, \\quad b = 7 - (k \\bmod 8)$$
                Bit 0 is the MSB of Byte 0, inverted via exact bitwise XOR: <code>byte ^ (1 &lt;&lt; b)</code>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hf-callout">
        <b>Academic &amp; Research Note:</b> HashForge is an interactive educational laboratory built for university demonstrations,
        cryptography coursework, and student visualization. It relies strictly on standard, verified FIPS implementations via Python's <code>hashlib</code>.
    </div>
    """,
    unsafe_allow_html=True,
)

