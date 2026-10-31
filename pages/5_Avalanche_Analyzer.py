"""Module E: Avalanche Effect Statistical Analyzer."""

import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from components.charts import (
    create_avalanche_histogram,
    create_trial_timeline_chart,
    create_algorithm_comparison_chart,
)
from core.bit_operations import text_to_bytes
from core.experiments import run_avalanche_simulation, run_comparative_simulation

st.set_page_config(
    page_title="Module 5 — Avalanche Analyzer | HashForge",
    page_icon="📊",
    layout="wide",
)

render_sidebar()

st.title("📊 Module 5: Avalanche Effect Statistical Analyzer")
st.markdown(
    """
    Execute high-sample Monte Carlo simulations to statistically evaluate the **Strict Avalanche Criterion (SAC)**.
    Measure empirical mean, standard deviation, and distribution dispersion against the theoretical **50.00%** baseline.
    """
)

# Baseline Text
default_text = "HashForge Cryptographic Avalanche Statistical Evaluation 2026"
input_text = st.text_input(
    "Baseline Plaintext Input:",
    value=st.session_state.get("mod5_text", default_text),
    help="Each trial will start strictly from this identical baseline input.",
)

if not input_text:
    st.warning("⚠️ Please provide input text to execute statistical simulations.")
    st.stop()

raw_bytes = text_to_bytes(input_text)
total_input_bits = len(raw_bytes) * 8

# Experiment Controls
col_preset, col_custom, col_mode, col_seed = st.columns([1.5, 1.2, 1.5, 1.2])

with col_preset:
    preset_choice = st.selectbox(
        "Experiment Sample Size:",
        options=["10 Trials", "50 Trials", "100 Trials", "Custom Count"],
        index=1,
    )

with col_custom:
    if preset_choice == "Custom Count":
        trials_count = st.number_input("Custom Trials (1 to 500):", min_value=1, max_value=500, value=75, step=5)
    else:
        trials_count = int(preset_choice.split()[0])

with col_mode:
    exp_mode = st.radio(
        "Trial Methodology:",
        options=["Independent Flips (Standard SAC)", "Cumulative Mutation"],
        help="Independent: each trial inverts 1 bit from baseline. Cumulative: perturbations accumulate.",
    )
    sim_mode = "single_bit" if "Independent" in exp_mode else "cumulative"

with col_seed:
    use_fixed_seed = st.checkbox("Fix Seed (Reproducible)", value=True)
    seed_value = st.number_input("RNG Seed:", value=101, step=1) if use_fixed_seed else None

# Run Simulation
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
run_clicked = st.button("🚀 Run Monte Carlo Avalanche Simulation", use_container_width=True)

# Run comparative analysis when button clicked or initial load
if run_clicked or "sim_result_sha256" not in st.session_state:
    with st.spinner(f"Computing {trials_count} cryptographic trials across SHA-256 and SHA3-256..."):
        sim_sha256 = run_avalanche_simulation(
            text=input_text,
            trials=trials_count,
            algorithm="sha256",
            seed=seed_value,
            mode=sim_mode,
        )
        sim_sha3 = run_avalanche_simulation(
            text=input_text,
            trials=trials_count,
            algorithm="sha3_256",
            seed=seed_value,
            mode=sim_mode,
        )
        st.session_state["sim_result_sha256"] = sim_sha256
        st.session_state["sim_result_sha3"] = sim_sha3

sim_sha256 = st.session_state["sim_result_sha256"]
sim_sha3 = st.session_state["sim_result_sha3"]

df_sha256 = pd.DataFrame(sim_sha256.trials)
df_sha3 = pd.DataFrame(sim_sha3.trials)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Statistical Summary Cards
st.markdown("### 📈 Statistical Summary Metrics")

stat_col1, stat_col2 = st.columns(2)

with stat_col1:
    st.markdown(
        f"""
        <div class="hf-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#00F0FF;">SHA-256 Statistics</h4>
                <span class="hf-badge hf-badge-cyan">{sim_sha256.trials_count} TRIALS</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:14px;">
                <div>Mean Avalanche: <b style="color:#00F0FF; font-size:1.2rem;">{sim_sha256.mean_avalanche_pct:.2f}%</b></div>
                <div>Standard Deviation: <b style="color:#F8FAFC; font-size:1.2rem;">±{sim_sha256.std_avalanche_pct:.2f}%</b></div>
                <div>Minimum Avalanche: <b style="color:#94A3B8;">{sim_sha256.min_avalanche_pct:.2f}%</b></div>
                <div>Maximum Avalanche: <b style="color:#94A3B8;">{sim_sha256.max_avalanche_pct:.2f}%</b></div>
                <div>Median Avalanche: <b style="color:#94A3B8;">{sim_sha256.median_avalanche_pct:.2f}%</b></div>
                <div>Theoretical Target: <b style="color:#10B981;">50.00%</b></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat_col2:
    st.markdown(
        f"""
        <div class="hf-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#10B981;">SHA3-256 Statistics</h4>
                <span class="hf-badge hf-badge-emerald">{sim_sha3.trials_count} TRIALS</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:14px;">
                <div>Mean Avalanche: <b style="color:#10B981; font-size:1.2rem;">{sim_sha3.mean_avalanche_pct:.2f}%</b></div>
                <div>Standard Deviation: <b style="color:#F8FAFC; font-size:1.2rem;">±{sim_sha3.std_avalanche_pct:.2f}%</b></div>
                <div>Minimum Avalanche: <b style="color:#94A3B8;">{sim_sha3.min_avalanche_pct:.2f}%</b></div>
                <div>Maximum Avalanche: <b style="color:#94A3B8;">{sim_sha3.max_avalanche_pct:.2f}%</b></div>
                <div>Median Avalanche: <b style="color:#94A3B8;">{sim_sha3.median_avalanche_pct:.2f}%</b></div>
                <div>Theoretical Target: <b style="color:#10B981;">50.00%</b></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Interactive Visualizations
st.markdown("### 📊 Interactive Visualizations")

tab_hist, tab_line, tab_box = st.tabs([
    "📉 Avalanche Histograms",
    "📈 Trial-by-Trial Dispersion",
    "📦 Algorithm Boxplot Comparison",
])

with tab_hist:
    hcol1, hcol2 = st.columns(2)
    with hcol1:
        st.plotly_chart(create_avalanche_histogram(df_sha256, "SHA-256"), use_container_width=True)
    with hcol2:
        st.plotly_chart(create_avalanche_histogram(df_sha3, "SHA3-256"), use_container_width=True)

with tab_line:
    lcol1, lcol2 = st.columns(2)
    with lcol1:
        st.plotly_chart(create_trial_timeline_chart(df_sha256, "SHA-256"), use_container_width=True)
    with lcol2:
        st.plotly_chart(create_trial_timeline_chart(df_sha3, "SHA3-256"), use_container_width=True)

with tab_box:
    st.plotly_chart(create_algorithm_comparison_chart(df_sha256, df_sha3), use_container_width=True)

st.markdown(
    """
    <div class="hf-callout">
        <b>💡 Statistical Interpretation:</b><br>
        Notice that individual trials do not output exactly 50.00% every single run — some trials may yield 48.44% or 52.34%.
        This is expected binomial behavior: each of the 256 output bits acts like an independent fair coin toss ($p = 0.5$).
        The theoretical distribution of Hamming distance follows a binomial distribution $B(n=256, p=0.5)$ with mean $\\mu = 128$ 
        and standard deviation $\\sigma = \\sqrt{256 \\times 0.5 \\times 0.5} = 8$ bits ($\\approx 3.125\\%$).
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 20px 0;'/>", unsafe_allow_html=True)

# Data Table and Export
st.markdown("### 📋 Trial Execution Log & CSV Export")

col_tbl1, col_tbl2 = st.columns([3, 1])
with col_tbl1:
    display_algo = st.radio("Display Records For:", options=["SHA-256", "SHA3-256"], horizontal=True)

active_df = df_sha256 if display_algo == "SHA-256" else df_sha3

st.dataframe(
    active_df[[
        "trial", "bit_index", "byte_index", "hamming_distance", 
        "avalanche_pct", "original_hex", "modified_hex", "time_ms"
    ]],
    use_container_width=True,
    height=260,
)

csv_data = active_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"📥 Download {display_algo} Trial Data (.csv)",
    data=csv_data,
    file_name=f"hashforge_{display_algo.lower().replace('-', '')}_trials.csv",
    mime="text/csv",
)

