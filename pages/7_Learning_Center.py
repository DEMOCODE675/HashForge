"""Module G: Learning Center and Interactive Cryptography Quiz."""

import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Module 7 — Learning Center | HashForge",
    page_icon="📚",
    layout="wide",
)

render_sidebar()

st.title("📚 Module 7: Cryptographic Learning Center")
st.markdown(
    """
    Master the theoretical foundations of modern hashing, diffusion mechanics, and data integrity.
    Review the **12 core curriculum topics** below, then test your understanding with the interactive **Knowledge Evaluation Quiz**.
    """
)

tab_learn, tab_quiz = st.tabs(["📖 Cryptography Curriculum (12 Topics)", "🧠 Interactive Knowledge Check Quiz"])

with tab_learn:
    st.markdown("### 🏛️ Foundations of Modern Cryptographic Hashing")

    # Topic 1 & 2
    with st.expander("1. What is Cryptography?", expanded=False):
        st.markdown(
            """
            **Cryptography** is the science of secure communication in the presence of adversarial third parties.
            It encompasses four fundamental security objectives (often abbreviated **CIA-A**):
            - **Confidentiality:** Ensuring unauthorized entities cannot read sensitive information.
            - **Integrity:** Ensuring information cannot be modified or tampered with undetected.
            - **Authentication:** Confirming the true identity of the originator or communicating party.
            - **Non-repudiation:** Preventing an entity from denying the authenticity of a previously sent message.
            """
        )

    with st.expander("2. What is a Cryptographic Hash Function?", expanded=False):
        st.markdown(
            """
            A **cryptographic hash function** $H: \\{0, 1\\}^* \\to \\{0, 1\\}^n$ is a deterministic mathematical algorithm 
            that maps an arbitrary-length input byte stream to a fixed-length output digest (e.g. 256 bits).
            
            To be considered cryptographically secure, it must satisfy three core properties:
            1. **Preimage Resistance (One-Wayness):** Given a digest $y$, it is computationally infeasible to find any input $x$ such that $H(x) = y$. Required computational work: $\\mathcal{O}(2^n)$.
            2. **Second Preimage Resistance (Weak Collision Resistance):** Given an input $x_1$, it is computationally infeasible to find a distinct input $x_2 \\neq x_1$ such that $H(x_1) = H(x_2)$. Required work: $\\mathcal{O}(2^n)$.
            3. **Collision Resistance (Strong Collision Resistance):** It is computationally infeasible to find *any* two arbitrary distinct inputs $x_1 \\neq x_2$ such that $H(x_1) = H(x_2)$. Due to the **Birthday Paradox**, required work is $\\mathcal{O}(2^{n/2})$ (for 256 bits: $2^{128}$ operations).
            """
        )

    with st.expander("3. SHA-256 Explained (FIPS 180-4)", expanded=False):
        st.markdown(
            """
            **SHA-256** (Secure Hash Algorithm 2) was designed by the US National Security Agency (NSA) and published by NIST in 2002.
            
            **Internal Mechanics:**
            - **Merkle-Damgård Construction:** Iteratively processes 512-bit message blocks.
            - **Padding:** Appends a '1' bit, followed by '0' bits, and terminates with a 64-bit big-endian integer representing the original message bit-length.
            - **Compression Function:** 64 rounds of non-linear bitwise operations ($Ch$, $Maj$, $\\Sigma_0$, $\\Sigma_1$, $\\sigma_0$, $\\sigma_1$) operating on eight 32-bit working variables ($A, B, C, D, E, F, G, H$).
            - **Constants:** 64 round constants derived from the fractional parts of the cube roots of the first 64 prime numbers.
            """
        )

    with st.expander("4. SHA3-256 Explained (FIPS 202 & Keccak)", expanded=False):
        st.markdown(
            """
            **SHA3-256** was selected as the winner of the 5-year public NIST Cryptographic Hash Competition in 2012 (created by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche) and standardized in 2015.
            
            **The Sponge Construction:**
            - Does not use Merkle-Damgård or Davies-Meyer compression functions.
            - Operates on a large 1600-bit internal state arranged as a $5 \\times 5$ array of 64-bit words.
            - **Rate ($r = 1088$ bits):** The portion of state that is directly XORed with input message chunks during the *Absorbing* phase.
            - **Capacity ($c = 512$ bits):** The hidden portion of the state that remains insulated from direct external manipulation, providing the cryptographic security margin ($c/2 = 256$ bits of security).
            - **Permutation:** 24 rounds of $\\theta, \\rho, \\pi, \\chi, \\iota$ step mappings.
            """
        )

    with st.expander("5. What is the Avalanche Effect?", expanded=False):
        st.markdown(
            """
            The **Avalanche Effect** (first coined by Horst Feistel in 1973 and closely tied to Claude Shannon's concept of **Diffusion**) 
            dictates that a microscopic modification to the input (even complementing a single bit) must cause a non-linear cascade, 
            resulting in an output where each bit has an independent 50% probability of changing.
            
            **Strict Avalanche Criterion (SAC):**
            Formally defined by Webster and Tavares (1985): whenever a single input bit $i$ is inverted, each output bit $j$ must complement with probability $P(\\Delta y_j = 1) = 0.5$.
            If a function fails SAC, attackers can exploit correlation linearities to reverse hashes or find collisions.
            """
        )

    with st.expander("6. What is Hamming Distance?", expanded=False):
        st.markdown(
            """
            Named after Richard Hamming, the **Hamming Distance** $D(x, y)$ between two binary strings of equal length $n$ 
            is the number of positions at which the corresponding symbols differ:
            
            $$D(x, y) = \\sum_{i=0}^{n-1} (x_i \\oplus y_i)$$
            
            For a cryptographic hash with an output length of $n = 256$ bits:
            - **Minimum Distance:** $0$ (identical inputs)
            - **Maximum Distance:** $256$ (completely inverted)
            - **Expected Value (SAC):** $\\mathbb{E}[D] = n \\times 0.5 = 128$ bits
            - **Avalanche Percentage:** $\\frac{D}{n} \\times 100\\%$
            """
        )

    with st.expander("7. Bit Manipulation in Cryptography", expanded=False):
        st.markdown(
            """
            Cryptographic primitives rely on fast, deterministic CPU-level bitwise operations:
            - **XOR ($\\oplus$):** $0 \\oplus 0 = 0$, $0 \\oplus 1 = 1$, $1 \\oplus 0 = 1$, $1 \\oplus 1 = 0$. Inverts bits without carrying, forming the basis of perturbation and one-time pads.
            - **Bit Rotations (ROTR / ROTL):** Circular shifts that disperse bit positions across word boundaries without destroying bit count.
            - **Modular Addition ($\\boxplus$):** Addition modulo $2^{32}$ introduces non-linearity when combined with bitwise XOR (the ARX paradigm: Addition-Rotation-XOR).
            """
        )

    with st.expander("8. Data Integrity Verification", expanded=False):
        st.markdown(
            """
            **Data Integrity** guarantees that digital information has remained unaltered from transmission to storage.
            
            Because cryptographic hashes are computationally infeasible to invert or collide, storing or transmitting a 256-bit hash (32 bytes)
            serves as an immutable fingerprint for files of any size (terabytes or petabytes). If even a single flipped bit occurs due to cosmic rays,
            disk degradation (bit rot), or malicious alteration, the recomputed hash will completely diverge.
            """
        )

    with st.expander("9. Cryptographic Hashing in Blockchain", expanded=False):
        st.markdown(
            """
            Blockchains use cryptographic hashes for two pivotal architectural mechanisms:
            1. **Merkle Trees:** Efficiently summarizes thousands of transactions in a block into a single 32-byte **Merkle Root**. Any transaction tampering invalidates the root.
            2. **Proof-of-Work (PoW):** In Bitcoin, miners repeatedly compute $\\text{SHA-256}(\\text{SHA-256}(\\text{BlockHeader} \\,|\\, \\text{nonce}))$ searching for a hash with a specific number of leading zero bits. The avalanche effect guarantees that incrementing the nonce by 1 completely scrambles the output unpredictably.
            """
        )

    with st.expander("10. Hashing in Software Verification & Supply Chains", expanded=False):
        st.markdown(
            """
            Operating systems, package managers (e.g. `pip`, `apt`, `cargo`), and software vendors distribute cryptographic checksums alongside software releases.
            
            When downloading binaries, the package manager streams the downloaded file through SHA-256 and compares the result against a known vendor manifest.
            This prevents man-in-the-middle (MitM) payload substitution and corrupted partial downloads.
            """
        )

    with st.expander("11. Hashing and Digital Signatures", expanded=False):
        st.markdown(
            """
            Asymmetric cryptosystems (RSA, ECDSA, Ed25519) cannot efficiently encrypt large multi-gigabyte files directly.
            
            Instead, modern systems use the **Hash-and-Sign paradigm**:
            1. The message $M$ is hashed to a fixed 256-bit digest $h = H(M)$.
            2. The private key signs only the 32-byte digest $h$, producing signature $\\sigma$.
            3. The recipient hashes $M$ independently and verifies $\\sigma$ against the sender's public key.
            Because $H$ is collision-resistant, signing the hash is mathematically equivalent to signing the entire document.
            """
        )

    with st.expander("12. Why General Hashes (SHA-256) Are NOT for Password Storage", expanded=False):
        st.markdown(
            """
            <div class="hf-callout hf-callout-warning">
                <b>CRITICAL SECURITY RULE: Never store passwords using raw SHA-256 or SHA3-256!</b>
            </div>
            
            **Why?**
            SHA-256 was deliberately engineered to be **extremely fast and computationally cheap**.
            A modern consumer GPU (e.g. NVIDIA RTX 4090) can calculate over **15 billion SHA-256 hashes per second**.
            An attacker who steals a database of salted SHA-256 hashes can brute-force 8-character passwords in minutes.
            
            **The Solution: Key Derivation Functions (KDFs)**
            Passwords must be protected using deliberately **slow, memory-hard** algorithms:
            - **Argon2id** (Winner of Password Hashing Competition, RFC 9106)
            - **bcrypt** (Blowfish-based adaptive key derivation)
            - **scrypt** (Memory-hard sequential memory scheme)
            - **PBKDF2** (NIST SP 800-132 with >600,000 iterations)
            
            These algorithms require massive amounts of RAM and millions of rounds, rendering GPU and ASIC brute-force attacks economically impossible.
            """,
            unsafe_allow_html=True,
        )

with tab_quiz:
    st.markdown("### 🧠 Cryptography Knowledge Evaluation")
    st.markdown("Answer the 10 questions below to test your mastery. Submit when complete to review your score and detailed explanations.")

    questions = [
        {
            "q": "1. What is the expected Hamming distance between two 256-bit hashes when an algorithm satisfies the Strict Avalanche Criterion (SAC)?",
            "options": [
                "0 bits (0%)",
                "64 bits (25%)",
                "128 bits (50%)",
                "256 bits (100%)",
            ],
            "correct": 2,
            "exp": "Under ideal diffusion (SAC), each output bit inverts with probability p = 0.5. For a 256-bit digest, E[D] = 256 * 0.5 = 128 bits (50%).",
        },
        {
            "q": "2. What is the fundamental architectural construction underlying SHA3-256?",
            "options": [
                "Merkle-Damgård Compression",
                "Keccak Sponge Construction",
                "Feistel Cipher Network",
                "Davies-Meyer Feedforward",
            ],
            "correct": 1,
            "exp": "SHA-3 uses the Keccak Sponge construction (absorbing and squeezing phases over a 1600-bit state), distinct from SHA-2's Merkle-Damgård design.",
        },
        {
            "q": "3. Due to the Birthday Paradox, how many operations are required to find a collision in a 256-bit hash function?",
            "options": [
                "2^256 operations",
                "2^128 operations",
                "2^64 operations",
                "2^32 operations",
            ],
            "correct": 1,
            "exp": "Collision resistance for an n-bit hash requires work on the order of O(2^(n/2)). For n = 256, 2^(256/2) = 2^128 operations.",
        },
        {
            "q": "4. In HashForge's Big-Endian bit indexing standard, which bit does index 0 refer to?",
            "options": [
                "The Least Significant Bit (LSB) of Byte 0",
                "The Most Significant Bit (MSB) of Byte 0",
                "The first bit of the final byte",
                "A random parity bit",
            ],
            "correct": 1,
            "exp": "In network big-endian order, bit index 0 is the Most Significant Bit (MSB, weight 2^7) of the very first byte.",
        },
        {
            "q": "5. Which bitwise operation is used to flip a bit at offset b without affecting other bits?",
            "options": [
                "AND with 1 << b",
                "OR with 1 << b",
                "XOR with 1 << b",
                "NOT with 1 << b",
            ],
            "correct": 2,
            "exp": "Bitwise XOR (^) inverts a bit: 0 ^ 1 = 1, and 1 ^ 1 = 0, leaving all other bits unaffected where mask has 0.",
        },
        {
            "q": "6. Why is raw SHA-256 dangerous for storing user passwords?",
            "options": [
                "It has known mathematical collisions.",
                "It produces outputs that are too short.",
                "It is too fast, enabling billions of guesses per second on GPUs.",
                "It requires an internet connection to compute.",
            ],
            "correct": 2,
            "exp": "SHA-256 was designed for high throughput. Modern GPUs can calculate tens of billions of hashes/sec, making password brute-forcing trivial.",
        },
        {
            "q": "7. What security advantage does the Sponge construction offer over basic Merkle-Damgård?",
            "options": [
                "It is immune to length-extension attacks without needing HMAC.",
                "It makes hashes shorter.",
                "It allows reversing the hash backwards.",
                "It eliminates the need for prime numbers.",
            ],
            "correct": 0,
            "exp": "Because the sponge capacity portion remains secret and is not directly output, Keccak/SHA-3 is inherently immune to length extension attacks.",
        },
        {
            "q": "8. What does Preimage Resistance mean?",
            "options": [
                "Given input x, finding another x' where H(x) = H(x').",
                "Given output y, finding any input x such that H(x) = y is infeasible.",
                "Finding any two inputs with identical hashes.",
                "Compressing a file to 50% size.",
            ],
            "correct": 1,
            "exp": "Preimage resistance (one-way property) ensures that given hash digest y, discovering original input x is computationally impossible.",
        },
        {
            "q": "9. If a file's SHA-256 hash matches the vendor checksum, what does this guarantee?",
            "options": [
                "The file is definitely free of all software bugs.",
                "The file's content has not changed compared to the checksum reference (Integrity).",
                "The author's computer was not infected.",
                "The file cannot be deleted.",
            ],
            "correct": 1,
            "exp": "A hash match guarantees data integrity (the file matches the reference bit-for-bit), but not necessarily vendor authenticity unless the hash source is trusted.",
        },
        {
            "q": "10. In Bitcoin mining, why does changing the nonce by 1 completely scramble the hash?",
            "options": [
                "Bitcoin uses an unreleased custom hash.",
                "Because of the cryptographic Avalanche Effect.",
                "Because Bitcoin uses RSA encryption.",
                "Because the timestamp changes every second.",
            ],
            "correct": 1,
            "exp": "The avalanche effect ensures that even a 1-bit or 1-byte change in the nonce causes a pseudo-random, uncorrelated hash output.",
        },
    ]

    user_answers = {}
    for i, q_item in enumerate(questions):
        st.markdown(f"**{q_item['q']}**")
        ans = st.radio(
            label=f"q_{i}",
            options=range(len(q_item["options"])),
            format_func=lambda idx, q=q_item: q["options"][idx],
            key=f"quiz_q_{i}",
            label_visibility="collapsed",
        )
        user_answers[i] = ans
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    if st.button("📝 Submit Quiz & Calculate Score", use_container_width=True):
        score = 0
        st.markdown("<hr style='border: 0; border-top: 1px solid #1F2937; margin: 16px 0;'/>", unsafe_allow_html=True)

        for i, q_item in enumerate(questions):
            is_correct = user_answers[i] == q_item["correct"]
            if is_correct:
                score += 1
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                        <b style="color: #10B981;">Question {i+1}: Correct!</b><br>
                        <span style="font-size: 0.85rem; color: #D1D5DB;">{q_item['exp']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                correct_text = q_item["options"][q_item["correct"]]
                st.markdown(
                    f"""
                    <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #EF4444; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                        <b style="color: #EF4444;">Question {i+1}: Incorrect.</b><br>
                        <span style="font-size: 0.85rem; color: #D1D5DB;"><b>Correct Answer:</b> {correct_text}</span><br>
                        <span style="font-size: 0.85rem; color: #94A3B8;">{q_item['exp']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        pct_score = (score / len(questions)) * 100
        badge_cls = "hf-badge-emerald" if pct_score >= 80 else ("hf-badge-amber" if pct_score >= 60 else "hf-badge-rose")

        st.markdown(
            f"""
            <div class="hf-card hf-card-accent" style="text-align: center; margin-top: 16px;">
                <h3 style="margin: 0;">Evaluation Result</h3>
                <div style="font-size: 2.2rem; font-weight: 800; color: #00F0FF; margin: 8px 0;">
                    {score} / {len(questions)} ({pct_score:.0f}%)
                </div>
                <div><span class="hf-badge {badge_cls}">{'EXCELLENT' if pct_score >= 80 else ('GOOD EFFORT' if pct_score >= 60 else 'REVIEW RECOMMENDED')}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

