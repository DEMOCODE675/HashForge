import React, { useState, useEffect } from 'react';
import {
  Binary,
  Zap,
  Activity,
  Layers,
  ShieldCheck,
  Info,
  RefreshCw,
  AlertCircle,
  HelpCircle,
} from 'lucide-react';
import { api } from '../services/api';
import { SingleBitResponse } from '../types';
import { MetricCard } from '../components/shared/MetricCard';
import { BitGrid256 } from '../components/binary/BitGrid256';
import { BinaryStreamViewer } from '../components/binary/BinaryStreamViewer';
import { StatusBadge } from '../components/shared/StatusBadge';

export const SingleBitExperiment: React.FC = () => {
  const [inputText, setInputText] = useState('HashForge');
  const [bitIndex, setBitIndex] = useState(0);
  const [algorithm, setAlgorithm] = useState<'sha256' | 'sha3_256'>('sha256');
  const [data, setData] = useState<SingleBitResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inputBytes = new TextEncoder().encode(inputText);
  const totalInputBits = Math.max(inputBytes.length * 8, 8);

  const runExperiment = async (text: string, index: number, algo: string) => {
    if (!text) {
      setError('Input text cannot be empty for single-bit perturbation experiments.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.singleBitExperiment(text, index, algo);
      setData(res);
    } catch (err: any) {
      setError(err?.message || 'Experiment execution failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runExperiment(inputText, bitIndex, algorithm);
  }, [algorithm]);

  const targetByteIdx = Math.floor(bitIndex / 8);
  const targetBitOffset = 7 - (bitIndex % 8);
  const targetChar = targetByteIdx < inputText.length ? inputText[targetByteIdx] : '?';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Binary className="w-5 h-5 text-accent-cyan" />
            <h1 className="text-xl font-bold text-text-primary">Module 3: Single-Bit Flip Experiment</h1>
          </div>
          <p className="text-xs text-text-muted">
            Invert exactly one input bit via XOR and visualize non-linear output diffusion across 256 bits.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusBadge variant="cyan" icon="shield">Strict Avalanche Criterion (SAC)</StatusBadge>
        </div>
      </div>

      {/* Input & Bit Selection Controls */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-5">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 space-y-2">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block">
              1. Baseline Input String (UTF-8)
            </label>
            <input
              type="text"
              value={inputText}
              onChange={(e) => {
                const next = e.target.value;
                setInputText(next);
                const nextBits = Math.max(new TextEncoder().encode(next).length * 8, 8);
                if (bitIndex >= nextBits) setBitIndex(0);
              }}
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

        {/* Bit Selection Slider & Info */}
        <div className="pt-4 border-t border-border-subtle/50 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
                2. Target Bit Index to Invert:
              </label>
              <span className="text-xs font-mono-code text-accent-cyan font-bold">
                Bit #{bitIndex}
              </span>
            </div>

            <div className="text-xs font-mono-code text-text-muted">
              Byte: <strong className="text-text-primary">{targetByteIdx}</strong> ('{targetChar}') • Offset:{' '}
              <strong className="text-accent-amber">{targetBitOffset}</strong> (Weight 2<sup>{targetBitOffset}</sup> = {1 << targetBitOffset})
            </div>
          </div>

          <input
            type="range"
            min={0}
            max={Math.max(totalInputBits - 1, 0)}
            value={bitIndex}
            onChange={(e) => setBitIndex(Number(e.target.value))}
            className="w-full accent-accent-cyan cursor-pointer"
          />

          <div className="flex items-center justify-between text-[11px] text-text-muted font-mono-code">
            <span>Bit 0 (MSB of Byte 0)</span>
            <span>Bit {totalInputBits - 1} (LSB of Byte {Math.floor((totalInputBits - 1) / 8)})</span>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="button"
            onClick={() => runExperiment(inputText, bitIndex, algorithm)}
            disabled={loading}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Evaluating...' : 'Run Single-Bit Inversion'}</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Metrics Row */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Hamming Distance"
            value={`${data.metrics.hamming_distance} / 256`}
            subtitle="Output bits inverted by 1-bit input flip"
            icon={Activity}
            accentColor="amber"
          />
          <MetricCard
            title="Avalanche Percentage"
            value={`${data.metrics.avalanche_percentage.toFixed(2)}%`}
            subtitle="Theoretical Ideal: 50.00%"
            icon={Zap}
            accentColor="cyan"
          />
          <MetricCard
            title="Unchanged Bits"
            value={data.metrics.unchanged_count}
            subtitle="Identical output bit positions"
            icon={ShieldCheck}
            accentColor="default"
          />
          <MetricCard
            title="Deviation from 50%"
            value={`±${data.metrics.distance_from_ideal.toFixed(2)}%`}
            subtitle="|Actual - Ideal|"
            icon={Info}
            accentColor="emerald"
          />
        </div>
      )}

      {/* Input Stream Viewer */}
      {data && (
        <BinaryStreamViewer
          originalBytesHex={data.original_bytes_hex}
          modifiedBytesHex={data.modified_bytes_hex}
          originalBinary={data.original_binary_input}
          modifiedBinary={data.modified_binary_input}
          flippedIndices={[data.bit_index]}
        />
      )}

      {/* 256-Bit Visualizer */}
      {data && (
        <BitGrid256
          binaryDigest={data.modified_hash.binary_digest}
          diffMask={data.diff_mask}
          title={`Modified ${algorithm.toUpperCase()} 256-Bit Output (Flipped Bits Glowing)`}
        />
      )}
    </div>
  );
};

