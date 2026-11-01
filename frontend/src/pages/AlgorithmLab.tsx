import React, { useState, useEffect } from 'react';
import {
  GitCompareArrows,
  Activity,
  Layers,
  Cpu,
  ShieldCheck,
  AlertTriangle,
  Info,
  RefreshCw,
} from 'lucide-react';
import { api } from '../services/api';
import { AlgorithmCompareResponse } from '../types';
import { MetricCard } from '../components/shared/MetricCard';
import { StatusBadge } from '../components/shared/StatusBadge';

export const AlgorithmLab: React.FC = () => {
  const [inputText, setInputText] = useState('HashForge Comparative Algorithm Benchmark 2026');
  const [iterations, setIterations] = useState(1000);
  const [data, setData] = useState<AlgorithmCompareResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runComparison = async (text: string, iters: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.compareAlgorithms(text, iters);
      setData(res);
    } catch (err: any) {
      setError(err?.message || 'Comparison failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runComparison(inputText, iterations);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <GitCompareArrows className="w-5 h-5 text-accent-emerald" />
            <h1 className="text-xl font-bold text-text-primary">Module 2: Algorithm Comparison Lab</h1>
          </div>
          <p className="text-xs text-text-muted">
            Side-by-side architectural analysis of SHA-2 (Merkle-Damgård) vs SHA-3 (Keccak Sponge).
          </p>
        </div>
      </div>

      {/* Input & Benchmark Controls */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
        <div>
          <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
            Baseline Plaintext String
          </label>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-4 py-2.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan transition-colors"
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-border-subtle/50">
          <div className="flex items-center gap-3">
            <label className="text-xs text-text-secondary">Benchmark Iterations:</label>
            <select
              value={iterations}
              onChange={(e) => setIterations(Number(e.target.value))}
              className="bg-bg-elevated border border-border-subtle rounded-lg px-3 py-1.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            >
              <option value={100}>100 Iterations</option>
              <option value={500}>500 Iterations</option>
              <option value={1000}>1,000 Iterations</option>
              <option value={5000}>5,000 Iterations</option>
            </select>
          </div>

          <button
            type="button"
            onClick={() => runComparison(inputText, iterations)}
            disabled={loading}
            className="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-accent-emerald hover:bg-accent-emerald/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Benchmarking...' : 'Execute Comparison & Benchmark'}</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs">
          {error}
        </div>
      )}

      {/* Cross Algorithm Divergence Metrics */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Cross-Divergence"
            value={`${data.cross_divergence_percentage.toFixed(2)}%`}
            subtitle="Target ≈ 50.00% Divergence"
            icon={GitCompareArrows}
            accentColor="amber"
            tooltip="Bit difference between SHA-256 and SHA3-256 on identical input"
          />
          <MetricCard
            title="Hamming Distance"
            value={`${data.cross_hamming_distance} / 256`}
            subtitle="Differing Bit Positions"
            icon={Activity}
            accentColor="cyan"
          />
          {data.sha256_benchmark && (
            <MetricCard
              title="SHA-256 Latency"
              value={`${data.sha256_benchmark.average_latency_us.toFixed(2)} µs`}
              subtitle={`Total: ${data.sha256_benchmark.total_time_ms.toFixed(2)} ms`}
              icon={Cpu}
              accentColor="cyan"
            />
          )}
          {data.sha3_benchmark && (
            <MetricCard
              title="SHA3-256 Latency"
              value={`${data.sha3_benchmark.average_latency_us.toFixed(2)} µs`}
              subtitle={`Total: ${data.sha3_benchmark.total_time_ms.toFixed(2)} ms`}
              icon={Cpu}
              accentColor="emerald"
            />
          )}
        </div>
      )}

      {/* Side-by-Side Algorithm Cards */}
      {data && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* SHA-256 Card */}
          <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-accent-cyan" />
                <h3 className="text-sm font-bold text-text-primary">SHA-256 Architecture</h3>
              </div>
              <StatusBadge variant="cyan">SHA-2 Family</StatusBadge>
            </div>

            <div className="bg-[#070A10] border border-border-subtle rounded-lg p-3 font-mono-code text-xs break-all">
              <div className="text-[11px] text-text-muted mb-1">Hexadecimal Digest (64 Chars):</div>
              <div className="text-accent-cyan">{data.sha256.hex_digest}</div>
            </div>

            <div className="space-y-2 text-xs text-text-secondary leading-relaxed">
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Standard Specification:</span>
                <strong className="text-text-primary">FIPS PUB 180-4 (NIST 2002)</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Internal Construction:</span>
                <strong className="text-text-primary">Merkle-Damgård Iterative Compression</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Block Processing Size:</span>
                <strong className="text-text-primary">512 Bits (64 Bytes)</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Word Size & State:</span>
                <strong className="text-text-primary">32-Bit Words (8 Variables: A–H)</strong>
              </div>
              <div className="flex justify-between py-1">
                <span>Rounds per Block:</span>
                <strong className="text-text-primary">64 Compression Rounds</strong>
              </div>
            </div>
          </div>

          {/* SHA3-256 Card */}
          <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-accent-emerald" />
                <h3 className="text-sm font-bold text-text-primary">SHA3-256 Architecture</h3>
              </div>
              <StatusBadge variant="emerald">SHA-3 Family</StatusBadge>
            </div>

            <div className="bg-[#070A10] border border-border-subtle rounded-lg p-3 font-mono-code text-xs break-all">
              <div className="text-[11px] text-text-muted mb-1">Hexadecimal Digest (64 Chars):</div>
              <div className="text-accent-emerald">{data.sha3_256.hex_digest}</div>
            </div>

            <div className="space-y-2 text-xs text-text-secondary leading-relaxed">
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Standard Specification:</span>
                <strong className="text-text-primary">FIPS PUB 202 (NIST 2015)</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Internal Construction:</span>
                <strong className="text-text-primary">Keccak Permutation-Based Sponge</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Rate / Capacity:</span>
                <strong className="text-text-primary">r = 1088 Bits / c = 512 Bits</strong>
              </div>
              <div className="flex justify-between py-1 border-b border-border-subtle/50">
                <span>Internal State:</span>
                <strong className="text-text-primary">1600 Bits (5x5 Matrix of 64-bit Lanes)</strong>
              </div>
              <div className="flex justify-between py-1">
                <span>Rounds per Block:</span>
                <strong className="text-text-primary">24 Keccak-f[1600] Rounds</strong>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Security Engineering Note */}
      <div className="p-5 rounded-xl bg-bg-card border border-accent-amber/30 text-xs space-y-2">
        <div className="flex items-center gap-2 text-accent-amber font-bold">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>Security Engineering Clarification</span>
        </div>
        <p className="text-text-secondary leading-relaxed">
          Differences in CPU execution latency <strong>do not indicate cryptographic strength</strong>.
          Speed variations arise from hardware instructions (such as Intel/AMD SHA extensions vs 64-bit ALU lanes).
          SHA-3 was intentionally selected with a fundamentally different Sponge design to guarantee that any future mathematical weakness discovered in Merkle-Damgård will not jeopardize global cryptographic infrastructure.
        </p>
      </div>
    </div>
  );
};

