import React, { useState, useEffect } from 'react';
import {
  Layers,
  Zap,
  Activity,
  ShieldCheck,
  RefreshCw,
  AlertCircle,
  Dice5,
  Sliders,
} from 'lucide-react';
import { api } from '../services/api';
import { MultiBitResponse } from '../types';
import { MetricCard } from '../components/shared/MetricCard';
import { BitGrid256 } from '../components/binary/BitGrid256';
import { StatusBadge } from '../components/shared/StatusBadge';

export const MultiBitExperiment: React.FC = () => {
  const [inputText, setInputText] = useState('HashForge Multi-Bit Perturbation 2026');
  const [algorithm, setAlgorithm] = useState<'sha256' | 'sha3_256'>('sha256');
  const [mode, setMode] = useState<'random' | 'manual'>('random');
  const [kBits, setKBits] = useState(4);
  const [seed, setSeed] = useState<number | null>(42);
  const [manualIndices, setManualIndices] = useState('0, 8, 16, 24');
  const [data, setData] = useState<MultiBitResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inputBytes = new TextEncoder().encode(inputText);
  const totalInputBits = Math.max(inputBytes.length * 8, 8);

  const runExperiment = async () => {
    if (!inputText) {
      setError('Input text cannot be empty for multi-bit perturbation.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (mode === 'random') {
        const res = await api.multiBitRandomExperiment(inputText, kBits, seed, algorithm);
        setData(res);
      } else {
        const parsed = manualIndices
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean)
          .map(Number);
        const unique = Array.from(new Set(parsed)).sort((a, b) => a - b);
        for (const idx of unique) {
          if (isNaN(idx) || idx < 0 || idx >= totalInputBits) {
            throw new Error(`Index ${idx} is out of bounds (0 to ${totalInputBits - 1}).`);
          }
        }
        if (unique.length === 0) {
          throw new Error('Please enter at least one valid bit index.');
        }
        const res = await api.multiBitExperiment(inputText, unique, algorithm);
        setData(res);
      }
    } catch (err: any) {
      setError(err?.message || 'Multi-bit experiment execution failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runExperiment();
  }, [algorithm]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Layers className="w-5 h-5 text-accent-cyan" />
            <h1 className="text-xl font-bold text-text-primary">Module 4: Multi-Bit Flip Experiment</h1>
          </div>
          <p className="text-xs text-text-muted">
            Perturb multiple distinct bit positions simultaneously to test diffusion saturation and independence.
          </p>
        </div>

        <StatusBadge variant="cyan" icon="shield">Multi-Point Perturbation</StatusBadge>
      </div>

      {/* Controls */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-5">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 space-y-2">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block">
              1. Baseline Input String (UTF-8)
            </label>
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-4 py-2.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan transition-colors"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block">
              Algorithm Family
            </label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value as any)}
              className="w-full bg-bg-elevated border border-border-subtle rounded-lg px-3 py-2.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            >
              <option value="sha256">SHA-256 (Merkle-Damgård)</option>
              <option value="sha3_256">SHA3-256 (Keccak Sponge)</option>
            </select>
          </div>
        </div>

        {/* Mode Selector */}
        <div className="pt-4 border-t border-border-subtle/50 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              2. Selection Mode:
            </label>
            <div className="inline-flex rounded-lg border border-border-subtle p-0.5 bg-bg-elevated text-xs w-full sm:w-auto">
              <button
                type="button"
                onClick={() => setMode('random')}
                className={`flex-1 sm:flex-none flex items-center justify-center gap-1.5 px-3 py-2 rounded-md font-medium transition-colors min-h-[36px] ${
                  mode === 'random' ? 'bg-bg-card text-accent-cyan font-bold' : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                <Dice5 className="w-3.5 h-3.5" />
                <span>Random Bit Sampling</span>
              </button>
              <button
                type="button"
                onClick={() => setMode('manual')}
                className={`flex-1 sm:flex-none flex items-center justify-center gap-1.5 px-3 py-2 rounded-md font-medium transition-colors min-h-[36px] ${
                  mode === 'manual' ? 'bg-bg-card text-accent-cyan font-bold' : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                <Sliders className="w-3.5 h-3.5" />
                <span>Manual Bit Specification</span>
              </button>
            </div>
          </div>

          {mode === 'random' ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-text-secondary">Number of bits to flip (k):</span>
                  <strong className="text-accent-cyan font-mono-code">{kBits} bits</strong>
                </div>
                <input
                  type="range"
                  min={1}
                  max={Math.min(totalInputBits, 64)}
                  value={kBits}
                  onChange={(e) => setKBits(Number(e.target.value))}
                  className="w-full accent-accent-cyan cursor-pointer"
                />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-text-secondary">Deterministic Seed:</span>
                  <span className="text-text-muted font-mono-code">{seed !== null ? `Seed: ${seed}` : 'Randomized'}</span>
                </div>
                <input
                  type="number"
                  value={seed ?? ''}
                  onChange={(e) => setSeed(e.target.value ? Number(e.target.value) : null)}
                  placeholder="Enter integer seed (or leave blank)..."
                  className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-3 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
                />
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <label className="text-xs text-text-secondary">
                Enter comma-separated bit indices (range: 0 to {totalInputBits - 1}):
              </label>
              <input
                type="text"
                value={manualIndices}
                onChange={(e) => setManualIndices(e.target.value)}
                placeholder="e.g. 0, 8, 16, 24"
                className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-4 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
              />
            </div>
          )}
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
          {data && (
            <div className="text-xs text-text-muted font-mono-code break-all">
              Flipped Indices: <strong className="text-accent-amber">{JSON.stringify(data.flipped_bit_indices)}</strong>
            </div>
          )}
          <button
            type="button"
            onClick={runExperiment}
            disabled={loading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow min-h-[44px]"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Evaluating...' : 'Run Multi-Bit Perturbation'}</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Metrics */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Bits Perturbed"
            value={`${data.flipped_bits_count} Bits`}
            subtitle="Simultaneous input XOR inversions"
            icon={Layers}
            accentColor="amber"
          />
          <MetricCard
            title="Hamming Distance"
            value={`${data.metrics.hamming_distance} / 256`}
            subtitle="Output bits inverted"
            icon={Activity}
            accentColor="cyan"
          />
          <MetricCard
            title="Avalanche Percentage"
            value={`${data.metrics.avalanche_percentage.toFixed(2)}%`}
            subtitle="Expected: ~50.00%"
            icon={Zap}
            accentColor="emerald"
          />
          <MetricCard
            title="Diffusion Stability"
            value={`±${data.metrics.distance_from_ideal.toFixed(2)}%`}
            subtitle="|Actual - 50.00%|"
            icon={ShieldCheck}
            accentColor="default"
          />
        </div>
      )}

      {/* 256-Bit Grid */}
      {data && (
        <BitGrid256
          binaryDigest={data.modified_hash.binary_digest}
          diffMask={data.diff_mask}
          title={`Perturbed ${algorithm.toUpperCase()} 256-Bit Output (${data.flipped_bits_count} Input Bits Flipped)`}
        />
      )}
    </div>
  );
};

