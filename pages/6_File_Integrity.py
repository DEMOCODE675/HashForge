"""Module F: File Integrity Laboratory."""

import streamlit as st
from components.sidebar import render_sidebar
from core.file_integrity import (
    hash_file_stream,
    compare_file_hashes,
    format_file_size,
)

st.set_page_config(
    page_title="Module 6 — File Integrity Lab | HashForge",
    page_icon="🛡️",
    layout="wide",
)

render_sidebar()

st.title("🛡️ Module 6: File Integrity Laboratory")
st.markdown(
    """
    Experience real-world data integrity verification. Compute cryptographic checksums using 
    memory-efficient **streaming 64KB chunks**, detect single-byte file corruption or tampering,
    and verify downloaded software against official vendor reference hashes.
    """
)

# Mode Selection
verification_mode = st.radio(
    "Select Verification Scenario:",
    options=[
        "Single File Fingerprinting",
        "Two-File Tamper / Parity Comparison",
        "Verify File against Trusted Reference Hash",
    ],
    horizontal=True,
)

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

# ----------------- Scenario 1: Single File Fingerprinting -----------------
if verification_mode == "Single File Fingerprinting":
    uploaded_file = st.file_uploader(
        "Upload a File to Fingerprint (Max 50MB):",
        type=None,
        help="Files are processed strictly in memory/chunks and are never saved to disk.",
    )

    if uploaded_file is not None:
        with st.spinner("Streaming and hashing file..."):
            report = hash_file_stream(uploaded_file, file_name=uploaded_file.name)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("File Name", report.file_name)
        with col_m2:
            st.metric("File Size", report.formatted_size)
        with col_m3:
            st.metric("Chunks (64KB)", f"{report.chunks_processed:,}")
        with col_m4:
            st.metric("Hashing Duration", f"{report.hashing_duration_ms:.2f} ms")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown("**SHA-256 Fingerprint:**")
        st.code(report.sha256_hex, language="text")

        st.markdown("**SHA3-256 Fingerprint:**")
        st.code(report.sha3_256_hex, language="text")

# ----------------- Scenario 2: Two-File Comparison -----------------
elif verification_mode == "Two-File Tamper / Parity Comparison":
    st.markdown("Upload two files (such as an original document and a modified draft) to compare their fingerprints:")

    col_up1, col_up2 = st.columns(2)
    with col_up1:
        file_a = st.file_uploader("Upload File A (Original / Baseline):", key="file_a")
    with col_up2:
        file_b = st.file_uploader("Upload File B (Suspect / Modified):", key="file_b")

    if file_a is not None and file_b is not None:
        with st.spinner("Computing simultaneous streaming checksums..."):
            report_a = hash_file_stream(file_a, file_name=file_a.name)
            report_b = hash_file_stream(file_b, file_name=file_b.name)
            comparison = compare_file_hashes(report_a, report_b)

        if comparison.is_identical:
            st.markdown(
                """
                <div class="hf-callout hf-callout-success">
                    <h4 style="color: #10B981; margin: 0 0 4px 0;">✅ INTEGRITY VERIFIED — IDENTICAL FILES</h4>
                    <div>Both files produce 100% identical SHA-256 and SHA3-256 hashes. Not a single bit differs.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="hf-callout hf-callout-warning">
                    <h4 style="color: #EF4444; margin: 0 0 4px 0;">❌ INTEGRITY MISMATCH DETECTED</h4>
                    <div>Cryptographic fingerprints differ! The file content has been altered, corrupted, or tampered with.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_fa, col_fb = st.columns(2)
        with col_fa:
            st.markdown(f"#### 📄 File A: `{report_a.file_name}` ({report_a.formatted_size})")
            st.markdown("**SHA-256:**")
            st.code(report_a.sha256_hex, language="text")
            st.markdown("**SHA3-256:**")
            st.code(report_a.sha3_256_hex, language="text")

        with col_fb:
            st.markdown(f"#### 📄 File B: `{report_b.file_name}` ({report_b.formatted_size})")
            st.markdown("**SHA-256:**")
            st.code(report_b.sha256_hex, language="text")
            st.markdown("**SHA3-256:**")
            st.code(report_b.sha3_256_hex, language="text")

# ----------------- Scenario 3: Verify Against Reference Hash -----------------
else:
    st.markdown("Upload a downloaded file and enter the official vendor reference hash (e.g., from Ubuntu, Python, or Apache releases):")

    ref_file = st.file_uploader("Upload Downloaded File:", key="ref_file")
    ref_hash = st.text_input(
        "Expected Reference Hash (SHA-256 or SHA3-256 Hex String):",
        placeholder="Paste 64-character hexadecimal checksum here...",
    )

    if ref_file is not None and ref_hash.strip():
        with st.spinner("Streaming file and validating checksum..."):
            report_ref = hash_file_stream(ref_file, file_name=ref_file.name)
            result = compare_file_hashes(report_ref, reference_hash=ref_hash)

        if result.is_identical:
            matched_algo = "SHA-256" if result.sha256_match else "SHA3-256"
            st.markdown(
                f"""
                <div class="hf-callout hf-callout-success">
                    <h4 style="color: #10B981; margin: 0 0 4px 0;">✅ CHECKSUM MATCHED — AUTHENTIC</h4>
                    <div>The file's computed fingerprint matches the reference hash via <b>{matched_algo}</b>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="hf-callout hf-callout-warning">
                    <h4 style="color: #EF4444; margin: 0 0 4px 0;">❌ CHECKSUM MISMATCH — POTENTIAL TAMPERING</h4>
                    <div>The computed file hash does NOT match the vendor reference hash! Do not execute or trust this binary.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"**Computed SHA-256:** `{report_ref.sha256_hex}`")
        st.markdown(f"**Expected Reference:** `{ref_hash.strip().lower()}`")

st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 24px 0;'/>", unsafe_allow_html=True)

# Educational Callout
st.markdown(
    """
    <div class="hf-card">
        <h4 style="color: #00F0FF; margin-top: 0;">🛡️ Cryptographic Security Concept: Authenticity vs Integrity</h4>
        <p style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;">
            A cryptographic hash verifies <b>integrity</b> (proving the file has not changed), but it does not alone prove <b>authenticity</b>.
            If an attacker replaces a downloadable binary on an insecure HTTP mirror <i>and</i> replaces the checksum on the webpage, 
            a user verifying the hash would still see a match!
        </p>
        <p style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 0;">
            True authenticity requires either obtaining the checksum over a secure, authenticated channel (HTTPS / TLS) 
            or verifying a <b>Digital Signature</b> (such as PGP / GPG or Sigstore) created with the vendor's private key.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

