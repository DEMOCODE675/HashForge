"""Module D: Multi-Bit Flip Experiment."""

import random
import streamlit as st
from components.sidebar import render_sidebar
from components.bit_visualizer import render_bit_grid
from components.comparison import render_comparison_summary
from core.bit_operations import text_to_bytes, bytes_to_bits, format_binary_grouped
from core.experiments import run_multi_bit_trial

st.set_page_config(
    page_title="Module 4 — Multi-Bit Experiment | HashForge",
    page_icon="🔀",
    layout="wide",
)

render_sidebar()

st.title("🔀 Module 4: Multi-Bit Flip Experiment")
st.markdown(
    """
    Test non-linear diffusion under multi-bit input perturbations.
    Select $k$ input bits to invert simultaneously, choose between deterministic pseudo-random 
    sampling or manual index selection, and verify whether flipping multiple bits increases or stabilizes the avalanche percentage.
    """
)

# Text Input
default_text = "HashForge Multi-Bit Cryptography 2026"
input_text = st.text_input(
    "1. Enter Baseline Input Text (UTF-8):",
    value=st.session_state.get("mod4_text", default_text),
)

if not input_text:
    st.warning("⚠️ Please enter at least 1 character for multi-bit experimentation.")
    st.stop()

raw_bytes = text_to_bytes(input_text)
total_input_bits = len(raw_bytes) * 8

# Algorithm and Selection Mode
col_a, col_b = st.columns(2)
with col_a:
    selected_algo = st.selectbox(
        "2. Select Algorithm:",
        options=["sha256", "sha3_256"],
        format_func=lambda x: "SHA-256 (FIPS 180-4)" if x == "sha256" else "SHA3-256 (FIPS 202)",
    )

with col_b:
    selection_mode = st.radio(
        "3. Bit Selection Mode:",
        options=["Random Bit Sampling", "Manual Bit Specification"],
        horizontal=True,
    )

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# Bit selection logic
chosen_bit_indices = []

if selection_mode == "Random Bit Sampling":
    col_k, col_seed = st.columns([2, 1])
    with col_k:
        k_bits = st.slider(
            f"Number of distinct bits to flip (1 to {total_input_bits}):",
            min_value=1,
            max_value=total_input_bits,
            value=min(4, total_input_bits),
            step=1,
        )
    with col_seed:
        use_seed = st.checkbox("Deterministic RNG Seed", value=True)
        seed_val = st.number_input("Seed Value:", value=42, step=1) if use_seed else None

    rng = random.Random(seed_val)
    chosen_bit_indices = sorted(rng.sample(range(total_input_bits), k_bits))

else:
    st.markdown(f"Enter comma-separated bit indices within range `0` to `{total_input_bits - 1}`:")
    default_indices_str = "0, 8, 16, 24" if total_input_bits >= 32 else "0, 1"
    indices_str = st.text_input("Bit Indices (e.g. 0, 7, 15):", value=default_indices_str)

    try:
        parsed = [int(x.strip()) for x in indices_str.split(",") if x.strip()]
        unique_parsed = sorted(set(parsed))
        for idx in unique_parsed:
            if idx < 0 or idx >= total_input_bits:
                st.error(f"❌ Index {idx} is out of bounds (valid range: 0 to {total_input_bits - 1}).")
                st.stop()
        if not unique_parsed:
            st.error("❌ At least one valid bit index must be provided.")
            st.stop()
        chosen_bit_indices = unique_parsed
    except ValueError:
        st.error("❌ Invalid format. Please enter integers separated by commas.")
        st.stop()

# Display active selection
st.markdown(
    f"""
    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 12px 16px; margin: 12px 0;">
        <span style="font-size: 0.85rem; color: #94A3B8;">Selected Flipped Bit Positions ({len(chosen_bit_indices)} bits):</span><br>
        <code style="color: #00F0FF; font-size: 0.9rem;">{chosen_bit_indices}</code>
    </div>
    """,
    unsafe_allow_html=True,
)

# Run Trial
trial = run_multi_bit_trial(input_text, bit_indices=chosen_bit_indices, algorithm=selected_algo)

# Input Bytes Comparison
in_col1, in_col2 = st.columns(2)
orig_bits = bytes_to_bits(trial.original_bytes)
mod_bits = bytes_to_bits(trial.modified_bytes)

with in_col1:
    st.markdown("**Original Input:**")
    st.code(f"Bytes:  {trial.original_bytes!r}\nBinary: {' '.join(format_binary_grouped(orig_bits, 8, 32))}")

with in_col2:
    st.markdown(f"**Modified Input ({len(chosen_bit_indices)} Bits Flipped):**")
    st.code(f"Bytes:  {trial.modified_bytes!r}\nBinary: {' '.join(format_binary_grouped(mod_bits, 8, 32))}")

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# Avalanche Summary
render_comparison_summary(
    orig_hash=trial.original_hash,
    mod_hash=trial.modified_hash,
    metrics=trial.metrics,
    title=f"Avalanche Quantification ({len(chosen_bit_indices)} Input Bits Flipped)",
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# 256-Bit Visualizer
diff_mask = [i in trial.metrics.changed_indices for i in range(256)]
render_bit_grid(
    binary_str=trial.modified_hash.binary_digest,
    diff_mask=diff_mask,
    title=f"Perturbed Output Bitstream ({selected_algo.upper()})",
)

