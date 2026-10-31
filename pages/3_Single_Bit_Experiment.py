"""Module C: Single-Bit Flip Experiment."""

import streamlit as st
from components.sidebar import render_sidebar
from components.bit_visualizer import render_bit_grid
from components.comparison import render_comparison_summary
from core.bit_operations import (
    text_to_bytes,
    bytes_to_bits,
    BIT_INDEXING_EXPLANATION,
    format_binary_grouped,
)
from core.experiments import run_single_bit_trial

st.set_page_config(
    page_title="Module 3 — Single-Bit Experiment | HashForge",
    page_icon="⚡",
    layout="wide",
)

render_sidebar()

st.title("⚡ Module 3: Single-Bit Flip Experiment")
st.markdown(
    """
    Explore the **Strict Avalanche Criterion (SAC)** in action. Invert exactly **one bit** of your input
    data using bitwise XOR, and watch how that microscopic 1-bit perturbation cascades through the cryptographic
    compression function to flip approximately **50% of the output digest bits**.
    """
)

# Text Input
default_text = "HashForge"
input_text = st.text_input(
    "1. Enter Baseline Input Text (UTF-8):",
    value=st.session_state.get("mod3_text", default_text),
    help="Enter text with at least 1 character.",
)

if not input_text:
    st.warning("⚠️ Please enter at least 1 character to run the single-bit flip experiment.")
    st.stop()

# Convert to bytes
raw_bytes = text_to_bytes(input_text)
total_input_bits = len(raw_bytes) * 8

# Algorithm Selection
col_cfg1, col_cfg2 = st.columns([1, 2])
with col_cfg1:
    selected_algo = st.selectbox(
        "2. Select Cryptographic Algorithm:",
        options=["sha256", "sha3_256"],
        format_func=lambda x: "SHA-256 (FIPS 180-4)" if x == "sha256" else "SHA3-256 (FIPS 202)",
    )

with col_cfg2:
    st.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 10px 14px; margin-top: 18px;">
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Input Byte Length: <b style="color: #00F0FF;">{len(raw_bytes)} bytes</b> |
                Addressable Bit Space: <b style="color: #10B981;">0 to {total_input_bits - 1} ({total_input_bits} bits)</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# Bit Selection Section
st.markdown("### 🎯 3. Select Target Bit to Invert")

bit_select_col1, bit_select_col2 = st.columns([2, 1])

with bit_select_col1:
    selected_bit = st.slider(
        f"Select Bit Index (0 to {total_input_bits - 1}):",
        min_value=0,
        max_value=total_input_bits - 1,
        value=min(0, total_input_bits - 1),
        step=1,
        help="0 is the Most Significant Bit (MSB) of Byte 0.",
    )

target_byte_idx = selected_bit // 8
target_bit_offset = 7 - (selected_bit % 8)
target_char = input_text[target_byte_idx] if target_byte_idx < len(input_text) else "?"

with bit_select_col2:
    st.markdown(
        f"""
        <div class="hf-card" style="padding: 12px 16px; margin: 0;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Target Bit Address</div>
            <div style="font-size: 0.88rem; color: #F8FAFC; margin-top: 4px; line-height: 1.5;">
                • Byte Index: <b style="color: #00F0FF;">{target_byte_idx}</b> (Char: '<code>{target_char}</code>')<br>
                • Bit in Byte: <b style="color: #10B981;">{target_bit_offset}</b> (Weight: 2<sup>{target_bit_offset}</sup> = {1 << target_bit_offset})<br>
                • Operation: <code>byte ^ 0x{1 << target_bit_offset:02X}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Educational note on bit indexing
with st.expander("ℹ️ Bit Indexing & Endianness Specification"):
    st.info(BIT_INDEXING_EXPLANATION)

# Run Trial
trial = run_single_bit_trial(input_text, bit_index=selected_bit, algorithm=selected_algo)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# 4. Input Binary Inspection
st.markdown("### 🔠 4. Input Byte & Bit Inspection")
in_col1, in_col2 = st.columns(2)

orig_bits = bytes_to_bits(trial.original_bytes)
mod_bits = bytes_to_bits(trial.modified_bytes)

with in_col1:
    st.markdown("**Original Input Bytes:**")
    st.code(f"Raw Bytes: {trial.original_bytes!r}\nHex:       {trial.original_bytes.hex(' ')}\nBinary:    {' '.join(format_binary_grouped(orig_bits, 8, 32))}")

with in_col2:
    st.markdown("**Modified Input Bytes (After XOR Flip):**")
    st.code(f"Raw Bytes: {trial.modified_bytes!r}\nHex:       {trial.modified_bytes.hex(' ')}\nBinary:    {' '.join(format_binary_grouped(mod_bits, 8, 32))}")

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# 5. Avalanche Results Summary
render_comparison_summary(
    orig_hash=trial.original_hash,
    mod_hash=trial.modified_hash,
    metrics=trial.metrics,
    title="5. Cryptographic Avalanche Quantification",
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# 6. Interactive 256-Bit Visualizer
st.markdown("### 👁️ 6. 256-Bit Output Diffusion Visualizer")
st.markdown(
    """
    Every output bit is rendered below across 8 rows of 32 bits (4 bytes per row).
    <span style="color: #FBBF24; font-weight: bold;">Glowing amber bits</span> represent positions where the output bit 
    inverted as a result of that single 1-bit input perturbation:
    """,
    unsafe_allow_html=True,
)

diff_mask = [i in trial.metrics.changed_indices for i in range(256)]

render_bit_grid(
    binary_str=trial.modified_hash.binary_digest,
    diff_mask=diff_mask,
    title=f"Perturbed {selected_algo.upper()} Output Bitstream (Changed Bits Highlighted)",
)

