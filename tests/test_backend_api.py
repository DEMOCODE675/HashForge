"""Integration tests for HashForge FastAPI endpoints."""

import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthAndMetaAPI:
    def test_root_endpoint(self):
        res = client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "HashForge API"

    def test_health_check(self):
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "sha256" in data["algorithms"]
        assert "sha3_256" in data["algorithms"]

    def test_learning_topics(self):
        res = client.get("/api/learning/topics")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 12

    def test_learning_quiz(self):
        res = client.get("/api/learning/quiz")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 10


class TestHashEndpoints:
    def test_generate_sha256_nist(self):
        res = client.post("/api/hash/generate", json={"text": "abc", "algorithm": "sha256"})
        assert res.status_code == 200
        data = res.json()
        assert data["hex_digest"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        assert data["digest_bits"] == 256
        assert len(data["binary_digest"]) == 256

    def test_generate_sha3_256_nist(self):
        res = client.post("/api/hash/generate", json={"text": "abc", "algorithm": "sha3_256"})
        assert res.status_code == 200
        data = res.json()
        assert data["hex_digest"] == "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"

    def test_invalid_algorithm_returns_400(self):
        res = client.post("/api/hash/generate", json={"text": "abc", "algorithm": "md5"})
        assert res.status_code == 400
        assert "Unsupported algorithm" in res.json()["detail"]

    def test_compare_algorithms(self):
        res = client.post("/api/hash/compare", json={"text": "HashForge 2026", "benchmark_iterations": 50})
        assert res.status_code == 200
        data = res.json()
        assert "sha256" in data
        assert "sha3_256" in data
        assert data["cross_hamming_distance"] > 50
        assert data["sha256_benchmark"] is not None


class TestExperimentEndpoints:
    def test_single_bit_experiment(self):
        res = client.post("/api/experiments/single-bit", json={"text": "HashForge", "bit_index": 0, "algorithm": "sha256"})
        assert res.status_code == 200
        data = res.json()
        assert data["bit_index"] == 0
        assert len(data["diff_mask"]) == 256
        assert data["metrics"]["hamming_distance"] == sum(data["diff_mask"])
        assert data["metrics"]["hamming_distance"] > 50

    def test_single_bit_out_of_bounds_returns_400(self):
        res = client.post("/api/experiments/single-bit", json={"text": "A", "bit_index": 999, "algorithm": "sha256"})
        assert res.status_code == 400

    def test_multi_bit_experiment(self):
        res = client.post("/api/experiments/multi-bit", json={"text": "HashForge", "bit_indices": [0, 8, 16], "algorithm": "sha256"})
        assert res.status_code == 200
        data = res.json()
        assert data["flipped_bits_count"] == 3
        assert len(data["diff_mask"]) == 256

    def test_multi_bit_random_experiment(self):
        res = client.post("/api/experiments/multi-bit/random", json={"text": "HashForge", "k_bits": 5, "seed": 42, "algorithm": "sha256"})
        assert res.status_code == 200
        data = res.json()
        assert data["flipped_bits_count"] == 5

    def test_avalanche_simulation_single(self):
        res = client.post("/api/experiments/avalanche", json={"text": "HashForge", "trials": 10, "algorithm": "sha256", "seed": 123})
        assert res.status_code == 200
        data = res.json()
        assert data["trials_count"] == 10
        assert len(data["trials"]) == 10
        assert 30 <= data["mean_avalanche_pct"] <= 70

    def test_avalanche_simulation_comparative(self):
        res = client.post("/api/experiments/avalanche", json={"text": "HashForge", "trials": 10, "comparative": True, "seed": 456})
        assert res.status_code == 200
        data = res.json()
        assert "sha256_result" in data
        assert "sha3_256_result" in data


class TestFileEndpoints:
    def test_hash_file(self):
        file_content = b"HashForge secure streaming test content"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        res = client.post("/api/files/hash", files=files)
        assert res.status_code == 200
        data = res.json()
        assert data["file_name"] == "test.txt"
        assert len(data["sha256_hex"]) == 64
        assert len(data["sha3_256_hex"]) == 64

    def test_compare_identical_files(self):
        content = b"Same content file"
        files = {
            "file_a": ("file_a.txt", io.BytesIO(content), "text/plain"),
            "file_b": ("file_b.txt", io.BytesIO(content), "text/plain"),
        }
        res = client.post("/api/files/compare", files=files)
        assert res.status_code == 200
        data = res.json()
        assert data["is_identical"] is True
        assert data["sha256_match"] is True

    def test_compare_file_with_reference(self):
        content = b"NIST ABC test payload"
        files = {"file_a": ("doc.txt", io.BytesIO(content), "text/plain")}
        data = {"reference_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
        res = client.post("/api/files/compare", files=files, data=data)
        assert res.status_code == 200
        resp_data = res.json()
        assert resp_data["is_identical"] is False

