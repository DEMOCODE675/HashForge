"""Module A: Hash Generator Laboratory."""

import streamlit as st
from components.sidebar import render_sidebar
from components.hash_display import render_hash_card
from core.hash_engine import compute_hash
from core.bit_operations import text_to_bytes

st.set_page_config(
    page_title="Module 1 — Hash Generator | HashForge",
    page_icon="🔬",
    layout="wide",
)

render_sidebar()

st.title("🔬 Module 1: Hash Generator Laboratory")
st.markdown(
    """
    Generate deterministic, collision-resistant cryptographic hash digests using **SHA-256** (FIPS 180-4) 
    and **SHA3-256** (FIPS 202). Inspect byte-level statistics, formatted hex representations, 
    and export cryptographic digests.
    """
)

# Text Input & Controls
col_ctrl1, col_ctrl2 = st.columns([4, 1])

with col_ctrl1:
    default_text = "HashForge Cryptographic Laboratory 2026"
    user_text = st.text_area(
        "Input Plaintext / Data String:",
        value=st.session_state.get("mod1_input", default_text),
        height=120,
        help="Type or paste any text or UTF-8 sequence. Empty strings are cryptographically valid inputs.",
        key="mod1_textarea",
    )

with col_ctrl2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clear Input", use_container_width=True):
        st.session_state["mod1_input"] = ""
        st.rerun()

    if st.button("📋 Sample NIST Vector", use_container_width=True):
        st.session_state["mod1_input"] = "The quick brown fox jumps over the lazy dog"
        st.rerun()

# Input Metrics
input_bytes = text_to_bytes(user_text)
char_count = len(user_text)
byte_count = len(input_bytes)
bit_count = byte_count * 8

st.markdown(
    f"""
    <div style="display: flex; gap: 24px; font-size: 0.85rem; color: #94A3B8; margin: 8px 0 16px 0;">
        <div>Characters: <b style="color: #F8FAFC;">{char_count:,}</b></div>
        <div>Byte Length (UTF-8): <b style="color: #00F0FF;">{byte_count:,} bytes</b></div>
        <div>Total Input Bits: <b style="color: #10B981;">{bit_count:,} bits</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute Hashes
res_sha256 = compute_hash(user_text, algorithm="sha256")
res_sha3 = compute_hash(user_text, algorithm="sha3_256")

# Algorithm Output Tabs
tab_sha256, tab_sha3 = st.tabs(["🔒 SHA-256 Digest (SHA-2 Family)", "🛡️ SHA3-256 Digest (Keccak Family)"])

with tab_sha256:
    render_hash_card(res_sha256, label="SHA-256 Cryptographic Digest")

with tab_sha3:
    render_hash_card(res_sha3, label="SHA3-256 Cryptographic Digest")

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 24px 0;'/>", unsafe_allow_html=True)

# Export Section
st.markdown("### 💾 Export Generated Hashes")
export_content = (
    f"HashForge Cryptographic Hash Digest Export\n"
    f"{'='*50}\n"
    f"Input Text: {user_text}\n"
    f"Byte Length: {byte_count} bytes ({bit_count} bits)\n"
    f"\n"
    f"[SHA-256]\n"
    f"Algorithm: SHA-256 (FIPS 180-4)\n"
    f"Hex Digest: {res_sha256.hex_digest}\n"
    f"Binary:     {res_sha256.binary_digest}\n"
    f"Latency:    {res_sha256.execution_time_ms:.4f} ms\n"
    f"\n"
    f"[SHA3-256]\n"
    f"Algorithm: SHA3-256 (FIPS 202)\n"
    f"Hex Digest: {res_sha3.hex_digest}\n"
    f"Binary:     {res_sha3.binary_digest}\n"
    f"Latency:    {res_sha3.execution_time_ms:.4f} ms\n"
    f"{'='*50}\n"
    f"Generated locally by HashForge Cryptography Platform\n"
)

st.download_button(
    label="📥 Download Cryptographic Digests (.txt)",
    data=export_content,
    file_name="hashforge_digest_output.txt",
    mime="text/plain",
    use_container_width=False,
)

