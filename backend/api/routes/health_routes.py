"""API routes for system health checks and educational content."""

from fastapi import APIRouter

router = APIRouter(tags=["System & Education"])


@router.get("/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "HashForge Cryptographic Backend",
        "version": "2.0.0",
        "algorithms": ["sha256", "sha3_256"],
        "bit_indexing": "Big-Endian (Network Order)",
        "fips_compliant": True,
    }


@router.get("/learning/topics")
def get_learning_topics():
    """Retrieve 12 structured cryptographic curriculum topics."""
    return [
        {
            "id": 1,
            "title": "What is Cryptography?",
            "summary": "The science of secure communication addressing Confidentiality, Integrity, Authentication, and Non-Repudiation (CIA-A).",
            "content": "Cryptography provides mathematical guarantees for data security. Unlike encryption, which provides confidentiality, hash functions focus strictly on Data Integrity and unique identification.",
        },
        {
            "id": 2,
            "title": "What is a Cryptographic Hash Function?",
            "summary": "A one-way mathematical function mapping variable input to a fixed-size digest.",
            "content": "Cryptographic hash functions must satisfy three core properties: Preimage Resistance (one-wayness, O(2^n)), Second Preimage Resistance (weak collision resistance, O(2^n)), and Strong Collision Resistance (O(2^(n/2)) work due to the Birthday Paradox).",
        },
        {
            "id": 3,
            "title": "SHA-256 Explained (FIPS 180-4)",
            "summary": "Merkle-Damgård iterative compression algorithm published by NIST in 2002.",
            "content": "SHA-256 pads input to 512-bit blocks and computes 64 rounds of non-linear operations (Ch, Maj, Sigma, sigma) on eight 32-bit working variables using constants derived from cube roots of primes.",
        },
        {
            "id": 4,
            "title": "SHA3-256 Explained (FIPS 202 & Keccak)",
            "summary": "Permutation-based Sponge construction selected as the winner of the NIST competition.",
            "content": "SHA3-256 operates on a 1600-bit state (5x5 matrix of 64-bit lanes). The state absorbs message blocks across rate r = 1088 bits and isolates capacity c = 512 bits, making it inherently immune to length-extension attacks.",
        },
        {
            "id": 5,
            "title": "What is the Avalanche Effect?",
            "summary": "Claude Shannon's diffusion principle formalized into the Strict Avalanche Criterion.",
            "content": "The Strict Avalanche Criterion (SAC) requires that complementing a single input bit causes each output bit to invert with probability p = 0.5. Without SAC, linear statistical relationships would allow reversing hashes.",
        },
        {
            "id": 6,
            "title": "What is Hamming Distance?",
            "summary": "The count of differing bit positions between two binary strings.",
            "content": "For two 256-bit hashes, Hamming distance D is calculated by XORing the bits and summing the 1s. Ideal cryptographic diffusion produces an expected mean distance of 128 bits (50.0%).",
        },
        {
            "id": 7,
            "title": "Bit Manipulation in Cryptography",
            "summary": "Hardware-level bitwise operations powering non-linear diffusion.",
            "content": "Cryptographic primitives rely on bitwise XOR (inversion without carry), circular rotations (ROTR/ROTL), and modular addition modulo 2^32 (the ARX paradigm) to achieve confusion and diffusion.",
        },
        {
            "id": 8,
            "title": "Data Integrity Verification",
            "summary": "Detecting transmission corruption or tampering using 32-byte fingerprints.",
            "content": "Because collisions are computationally impossible, transmitting or storing a 256-bit hash allows verifying petabyte-scale files bit-for-bit without storing the original file twice.",
        },
        {
            "id": 9,
            "title": "Hashing in Blockchain Networks",
            "summary": "Merkle trees and Proof-of-Work puzzle difficulty.",
            "content": "Blockchains aggregate thousands of transactions into a single 32-byte Merkle root. In Proof-of-Work (PoW), the avalanche effect ensures that incrementing a block nonce by 1 completely scrambles the output unpredictably.",
        },
        {
            "id": 10,
            "title": "Software Verification & Supply Chains",
            "summary": "Preventing man-in-the-middle binary tampering in package distribution.",
            "content": "Modern operating systems and package managers (pip, apt, cargo) verify downloaded binaries by streaming them through SHA-256 and checking against vendor manifests to prevent MitM payloads.",
        },
        {
            "id": 11,
            "title": "Hashing and Digital Signatures",
            "summary": "The Hash-and-Sign paradigm for asymmetric cryptography.",
            "content": "Asymmetric ciphers (RSA, ECDSA, Ed25519) cannot sign large files directly. By hashing the document to 32 bytes and signing only the digest, mathematical authenticity is guaranteed efficiently.",
        },
        {
            "id": 12,
            "title": "Why SHA-256 is NOT for Password Storage",
            "summary": "Critical security principle: High-throughput hashes vs Memory-hard KDFs.",
            "content": "SHA-256 was engineered to be fast; modern GPUs compute over 15 billion hashes/sec, making password cracking trivial. Passwords must be protected using memory-hard Key Derivation Functions: Argon2id, bcrypt, or scrypt.",
        },
    ]


@router.get("/learning/quiz")
def get_quiz_questions():
    """Retrieve 10-question evaluation quiz."""
    return [
        {
            "id": 1,
            "question": "What is the expected Hamming distance between two 256-bit hashes under the Strict Avalanche Criterion (SAC)?",
            "options": ["0 bits (0%)", "64 bits (25%)", "128 bits (50%)", "256 bits (100%)"],
            "correct_index": 2,
            "explanation": "Under ideal diffusion (SAC), each output bit inverts with probability p = 0.5. For a 256-bit digest, E[D] = 256 * 0.5 = 128 bits (50%).",
        },
        {
            "id": 2,
            "question": "What architectural construction powers SHA3-256?",
            "options": ["Merkle-Damgård Compression", "Keccak Sponge Construction", "Feistel Cipher Network", "Davies-Meyer Feedforward"],
            "correct_index": 1,
            "explanation": "SHA-3 utilizes the Keccak Sponge construction (absorbing and squeezing phases over a 1600-bit state), distinct from SHA-2's Merkle-Damgård design.",
        },
        {
            "id": 3,
            "question": "Due to the Birthday Paradox, approximately how many operations are needed to find a collision in a 256-bit hash?",
            "options": ["2^256 operations", "2^128 operations", "2^64 operations", "2^32 operations"],
            "correct_index": 1,
            "explanation": "Collision resistance for an n-bit hash requires work on the order of O(2^(n/2)). For n = 256, 2^(256/2) = 2^128 operations.",
        },
        {
            "id": 4,
            "question": "In HashForge's Big-Endian bit indexing standard, what does bit index 0 represent?",
            "options": ["The Least Significant Bit (LSB) of Byte 0", "The Most Significant Bit (MSB) of Byte 0", "The first bit of the final byte", "A parity check bit"],
            "correct_index": 1,
            "explanation": "In network big-endian order, bit index 0 is strictly the Most Significant Bit (MSB, weight 2^7 = 128) of the first byte.",
        },
        {
            "id": 5,
            "question": "Which bitwise operation is used to flip a bit at offset b without side effects?",
            "options": ["AND with (1 << b)", "OR with (1 << b)", "XOR with (1 << b)", "NOT with (1 << b)"],
            "correct_index": 2,
            "explanation": "Bitwise XOR (^) inverts a bit: 0 ^ 1 = 1, and 1 ^ 1 = 0, leaving all other bit positions unchanged.",
        },
        {
            "id": 6,
            "question": "Why is plain SHA-256 dangerous for storing user passwords?",
            "options": ["It has known collisions", "It produces outputs that are too short", "It is too fast, enabling billions of guesses per second on consumer GPUs", "It requires an internet connection"],
            "correct_index": 2,
            "explanation": "SHA-256 is engineered for maximum throughput. Modern GPUs can compute tens of billions of guesses/sec. Passwords require memory-hard algorithms like Argon2id.",
        },
        {
            "id": 7,
            "question": "What key vulnerability of Merkle-Damgård hashes is solved natively by the Keccak Sponge design?",
            "options": ["Immunity to length-extension attacks without needing HMAC", "Loss of precision", "Memory leaks", "Slow performance on ARM CPUs"],
            "correct_index": 0,
            "explanation": "Because Keccak's capacity portion (512 bits) remains hidden and unexposed during squeezing, SHA-3 is natively immune to length-extension attacks.",
        },
        {
            "id": 8,
            "question": "What does Preimage Resistance guarantee?",
            "options": ["Given input x, finding x' where H(x) = H(x')", "Given digest y, finding any input x such that H(x) = y is computationally infeasible", "Finding any two inputs with identical hashes", "Compressing files without quality loss"],
            "correct_index": 1,
            "explanation": "Preimage resistance (one-way property) guarantees that reversing a hash digest y to find original input x is computationally impossible.",
        },
        {
            "id": 9,
            "question": "If a downloaded file matches the vendor's SHA-256 checksum, what does this mathematically prove?",
            "options": ["The file has zero software bugs", "The file content has not been altered compared to the reference (Data Integrity)", "The vendor's server was never hacked", "The file is an executable binary"],
            "correct_index": 1,
            "explanation": "A hash match guarantees data integrity (the file matches bit-for-bit), but not authenticity unless the distribution channel of the hash itself is trusted.",
        },
        {
            "id": 10,
            "question": "Why does changing a Bitcoin block nonce by just 1 yield a completely unpredictable hash?",
            "options": ["Because Bitcoin uses an unreleased hash", "Because of the cryptographic Avalanche Effect", "Because Bitcoin uses RSA", "Because the difficulty changes every millisecond"],
            "correct_index": 1,
            "explanation": "The avalanche effect ensures that a 1-bit or 1-byte change in the nonce causes an uncorrelated pseudo-random cascade across the entire 256-bit output space.",
        },
    ]

