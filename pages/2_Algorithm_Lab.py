"""Module B: Algorithm Comparison Lab (SHA-256 vs SHA3-256)."""

import time
import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from core.hash_engine import compute_hash
from core.avalanche import hamming_distance, avalanche_percentage

st.set_page_config(
    page_title="Module 2 — Algorithm Lab | HashForge",
    page_icon="⚖️",
    layout="wide",
)

render_sidebar()

st.title("⚖️ Module 2: Algorithm Comparison Lab")
st.markdown(
    """
    Compare **SHA-256** (Merkle-Damgård) and **SHA3-256** (Keccak Sponge) on identical inputs.
    Examine structural design differences, padding mechanics, and local execution benchmarks.
    """
)

# Input
input_text = st.text_input(
    "Enter Comparison Plaintext:",
    value="Cryptographic Hash Function Comparison 2026",
    help="Enter text to analyze across both hashing families.",
)

# Run computations
res_sha256 = compute_hash(input_text, "sha256")
res_sha3 = compute_hash(input_text, "sha3_256")

# Calculate inter-algorithm Hamming distance (how different are the two algorithms' digests for the SAME input)
inter_dist = hamming_distance(res_sha256.binary_digest, res_sha3.binary_digest)
inter_pct = avalanche_percentage(inter_dist, 256)

# Side-by-Side Comparison Columns
col_sha2, col_sha3 = st.columns(2)

with col_sha2:
    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #00F0FF;">SHA-256</h4>
                <span class="hf-badge hf-badge-cyan">SHA-2 Family</span>
            </div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 12px;">
                FIPS 180-4 standard • Published by NIST (2002) • Merkle-Damgård construction
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**Hexadecimal Output:**")
    st.code(res_sha256.hex_digest, language="text")

    st.markdown(
        f"""
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8; margin-top: 8px;">
            <div>• Digest Bit Length: <b>256 bits (32 bytes)</b></div>
            <div>• Hex Length: <b>64 characters</b></div>
            <div>• Block Size: <b>512 bits (64 bytes)</b></div>
            <div>• Word Size: <b>32 bits</b></div>
            <div>• Internal State: <b>8 × 32-bit words (256 bits)</b></div>
            <div>• Latency (Single Pass): <b>{res_sha256.execution_time_ms:.4f} ms</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_sha3:
    st.markdown(
        """
        <div class="hf-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #10B981;">SHA3-256</h4>
                <span class="hf-badge hf-badge-emerald">SHA-3 Family</span>
            </div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 12px;">
                FIPS 202 standard • NIST Competition Winner (Keccak, 2015) • Sponge construction
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**Hexadecimal Output:**")
    st.code(res_sha3.hex_digest, language="text")

    st.markdown(
        f"""
        <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8; margin-top: 8px;">
            <div>• Digest Bit Length: <b>256 bits (32 bytes)</b></div>
            <div>• Hex Length: <b>64 characters</b></div>
            <div>• Rate ($r$): <b>1088 bits (136 bytes)</b></div>
            <div>• Capacity ($c$): <b>512 bits (security parameter)</b></div>
            <div>• Internal State: <b>1600 bits (5×5 matrix of 64-bit lanes)</b></div>
            <div>• Latency (Single Pass): <b>{res_sha3.execution_time_ms:.4f} ms</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Mutual Correlation / Cross-Algorithm Diversity
st.markdown("### 🔀 Cross-Algorithm Divergence")
st.markdown(
    f"""
    Even though both algorithms process the identical input string, their distinct mathematical constructions
    produce completely independent, uncorrelated outputs:
    """
)

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.markdown(
        f"""
        <div class="hf-metric-card">
            <div class="hf-metric-title">Cross-Algorithm Hamming Distance</div>
            <div class="hf-metric-value hf-metric-amber">{inter_dist} / 256 bits</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Difference between SHA-256 and SHA3-256 outputs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_d2:
    st.markdown(
        f"""
        <div class="hf-metric-card">
            <div class="hf-metric-title">Cross-Algorithm Divergence Rate</div>
            <div class="hf-metric-value hf-metric-cyan">{inter_pct:.2f}%</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Expected statistical divergence ≈ 50.00%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Benchmark Suite
st.markdown("### ⏱️ Local Execution Benchmark")
st.markdown(
    "Benchmark hashing latency across multiple iterations on this machine to observe local throughput differences:"
)

benchmark_iterations = st.slider("Benchmark Iterations:", min_value=100, max_value=5000, value=1000, step=100)

if st.button("🚀 Run Local Latency Benchmark", use_container_width=False):
    byte_input = input_text.encode("utf-8")

    # Benchmark SHA-256
    t0_sha2 = time.perf_counter_ns()
    for _ in range(benchmark_iterations):
        compute_hash(byte_input, "sha256")
    t1_sha2 = time.perf_counter_ns()
    total_time_sha2_ms = (t1_sha2 - t0_sha2) / 1_000_000.0
    avg_sha2_us = (total_time_sha2_ms / benchmark_iterations) * 1000.0

    # Benchmark SHA3-256
    t0_sha3 = time.perf_counter_ns()
    for _ in range(benchmark_iterations):
        compute_hash(byte_input, "sha3_256")
    t1_sha3 = time.perf_counter_ns()
    total_time_sha3_ms = (t1_sha3 - t0_sha3) / 1_000_000.0
    avg_sha3_us = (total_time_sha3_ms / benchmark_iterations) * 1000.0

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">SHA-256 Average Latency</div>
                <div class="hf-metric-value hf-metric-cyan">{avg_sha2_us:.2f} µs</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Total for {benchmark_iterations:,} runs: {total_time_sha2_ms:.2f} ms</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with bcol2:
        st.markdown(
            f"""
            <div class="hf-metric-card">
                <div class="hf-metric-title">SHA3-256 Average Latency</div>
                <div class="hf-metric-value hf-metric-emerald">{avg_sha3_us:.2f} µs</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Total for {benchmark_iterations:,} runs: {total_time_sha3_ms:.2f} ms</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="hf-callout hf-callout-warning" style="margin-top: 16px;">
        <b>⚠️ Cryptographic Engineering Clarification:</b><br>
        Execution time differences <b>DO NOT</b> imply that one algorithm is "more secure" or "weaker" than the other.
        Execution speed is governed by CPU instruction architecture (such as hardware SHA extensions, vector registers, and cache layout).
        SHA3-256 was purposefully designed with a completely different cryptographic architecture (Sponge construction) 
        specifically to ensure that if any mathematical vulnerability were ever discovered in Merkle-Damgård designs, 
        the global security ecosystem would have an entirely independent cryptographic backup.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Architecture Breakdown
st.markdown("### 🏛️ Architectural Comparison: Merkle-Damgård vs Keccak Sponge")

arch_col1, arch_col2 = st.columns(2)

with arch_col1:
    st.markdown(
        """
        <div class="hf-card">
            <h4 style="color: #00F0FF; margin-top: 0;">Merkle-Damgård (SHA-256)</h4>
            <p style="font-size: 0.82rem; color: #CBD5E1;">
                <b>Iterative Compression:</b> The input message is padded and split into fixed 512-bit blocks.
                Each block is passed into a one-way compression function $f$:
            </p>
            <div style="font-family: monospace; font-size: 0.8rem; background: #080C13; padding: 10px; border-radius: 6px; margin: 8px 0;">
                H_i = f(H_{i-1}, M_i)
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8;">
                <b>Length-Extension Vulnerability:</b> Because the final output is directly the internal state $H_k$,
                unkeyed Merkle-Damgård constructions are susceptible to length extension attacks if used incorrectly for message authentication (why HMAC is mandatory).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with arch_col2:
    st.markdown(
        """
        <div class="hf-card">
            <h4 style="color: #10B981; margin-top: 0;">Keccak Sponge (SHA3-256)</h4>
            <p style="font-size: 0.82rem; color: #CBD5E1;">
                <b>Absorbing &amp; Squeezing:</b> Operates on a large 1600-bit state $b = r + c$, where $r$ is the rate (1088 bits)
                and $c$ is the capacity (512 bits):
            </p>
            <div style="font-family: monospace; font-size: 0.8rem; background: #080C13; padding: 10px; border-radius: 6px; margin: 8px 0;">
                State = Keccak-f[1600](State ⊕ (P_i || 0^c))
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8;">
                <b>Inherent Immunity:</b> Because the output is squeezed from only the rate portion while the capacity $c$ remains secret,
                SHA-3 is inherently immune to length extension attacks without needing HMAC wrappers.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

