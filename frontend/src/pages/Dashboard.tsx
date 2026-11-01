import React, { useState } from 'react';
import {
  ShieldCheck,
  Fingerprint,
  GitCompareArrows,
  Binary,
  Layers,
  ChartNoAxesCombined,
  FileCheck,
  BookOpen,
  ArrowRight,
  Zap,
  Activity,
  Cpu,
} from 'lucide-react';
import { MetricCard } from '../components/shared/MetricCard';
import { StatusBadge } from '../components/shared/StatusBadge';
import { api } from '../services/api';
import { HashResponse } from '../types';
import { ActivePage } from '../components/layout/Sidebar';

interface DashboardProps {
  onNavigate: (page: ActivePage) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [quickInput, setQuickInput] = useState('HashForge Cryptography 2026');
  const [quickResult, setQuickResult] = useState<HashResponse | null>(null);
  const [isHashing, setIsHashing] = useState(false);

  const handleQuickHash = async () => {
    if (!quickInput.trim()) return;
    setIsHashing(true);
    try {
      const res = await api.generateHash(quickInput, 'sha256');
      setQuickResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsHashing(false);
    }
  };

  const featureCards = [
    {
      id: 'generator',
      title: 'Hash Generator',
      category: 'Module 1',
      description: 'Compute SHA-256 and SHA3-256 digests with live byte statistics, chunked hex breakdowns, and file export.',
      icon: Fingerprint,
      accent: 'cyan' as const,
    },
    {
      id: 'algorithms',
      title: 'Algorithm Lab',
      category: 'Module 2',
      description: 'Compare Merkle-Damgård vs Keccak Sponge architectures, execution latency benchmarks, and cross-divergence.',
      icon: GitCompareArrows,
      accent: 'emerald' as const,
    },
    {
      id: 'single-bit',
      title: 'Single-Bit Experiment',
      category: 'Module 3',
      description: 'Invert exactly one input bit via XOR and visualize output diffusion across an organized 256-bit grid.',
      icon: Binary,
      accent: 'amber' as const,
    },
    {
      id: 'multi-bit',
      title: 'Multi-Bit Experiment',
      category: 'Module 4',
      description: 'Perturb multiple distinct bits simultaneously using random sampling or manual indices to study diffusion saturation.',
      icon: Layers,
      accent: 'cyan' as const,
    },
    {
      id: 'avalanche',
      title: 'Avalanche Analyzer',
      category: 'Module 5',
      description: 'Execute automated 10 to 500-trial Monte Carlo simulations with histograms, scatter lines, and CSV export.',
      icon: ChartNoAxesCombined,
      accent: 'emerald' as const,
    },
    {
      id: 'file-integrity',
      title: 'File Integrity Lab',
      category: 'Module 6',
      description: 'Stream files in memory-safe 64KB buffers to detect single-byte corruption and verify vendor checksums.',
      icon: FileCheck,
      accent: 'amber' as const,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Welcome Banner */}
      <div className="bg-bg-card border border-border-subtle rounded-2xl p-6 lg:p-8 shadow-card relative overflow-hidden">
        <div className="max-w-3xl space-y-4">
          <div className="flex items-center gap-2">
            <StatusBadge variant="cyan" icon="shield">FIPS Compliant Architecture</StatusBadge>
            <StatusBadge variant="emerald">Local Computation</StatusBadge>
          </div>

          <h1 className="text-2xl lg:text-3xl font-bold tracking-tight text-text-primary">
            An Interactive Cryptographic Hashing and Avalanche Effect Laboratory
          </h1>

          <p className="text-sm lg:text-base text-text-secondary leading-relaxed">
            HashForge bridges the gap between abstract cryptography theory and empirical understanding.
            Investigate how microscopic 1-bit input perturbations cascade non-linearly through <strong>SHA-256</strong> (Merkle-Damgård)
            and <strong>SHA3-256</strong> (Keccak Sponge) to achieve the Strict Avalanche Criterion.
          </p>
        </div>
      </div>

      {/* Top Level Metric KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Avalanche Target"
          value="50.00%"
          subtitle="Strict Avalanche Criterion (SAC)"
          icon={Zap}
          accentColor="cyan"
          tooltip="Ideal theoretical diffusion rate for non-linear hash compression"
        />
        <MetricCard
          title="Digest Size"
          value="256 Bits"
          subtitle="32 Bytes (64 Hex Characters)"
          icon={Cpu}
          accentColor="emerald"
          tooltip="Standard cryptographic digest bit-length"
        />
        <MetricCard
          title="Distance Metric"
          value="Hamming"
          subtitle="Bit-by-Bit XOR Inversion Count"
          icon={Activity}
          accentColor="amber"
          tooltip="Counts differing bit positions between original and modified hashes"
        />
        <MetricCard
          title="FIPS Standards"
          value="180-4 / 202"
          subtitle="SHA-2 & SHA-3 Family Specifications"
          icon={ShieldCheck}
          accentColor="default"
          tooltip="NIST standard specifications implemented via hashlib C-bindings"
        />
      </div>

      {/* Quick Hash Widget */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Fingerprint className="w-4 h-4 text-accent-cyan" />
            <h3 className="text-sm font-semibold text-text-primary">Quick Hash Engine Test</h3>
          </div>
          <span className="text-xs text-text-muted">Instant SHA-256 verification</span>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={quickInput}
            onChange={(e) => setQuickInput(e.target.value)}
            placeholder="Type any plaintext to compute instant digest..."
            className="flex-1 bg-bg-elevated border border-border-subtle rounded-lg px-4 py-2.5 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-cyan transition-colors font-mono-code"
          />
          <button
            type="button"
            onClick={handleQuickHash}
            disabled={isHashing}
            className="px-5 py-2.5 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow flex items-center justify-center gap-2"
          >
            {isHashing ? 'Computing...' : 'Compute SHA-256'}
          </button>
        </div>

        {quickResult && (
          <div className="mt-3 p-3 bg-[#070A10] border border-border-subtle rounded-lg font-mono-code text-xs break-all">
            <div className="text-text-muted text-[11px] mb-1">SHA-256 Digest:</div>
            <div className="text-accent-cyan">{quickResult.hex_digest}</div>
            <div className="text-[10px] text-text-muted mt-2">
              Latency: {quickResult.execution_time_ms.toFixed(4)} ms • Length: {quickResult.input_length_bytes} bytes
            </div>
          </div>
        )}
      </div>

      {/* Module Navigation Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-text-primary">Laboratory Modules</h2>
          <span className="text-xs text-text-muted">Select an experiment to begin testing</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {featureCards.map((feat) => {
            const Icon = feat.icon;
            return (
              <div
                key={feat.id}
                onClick={() => onNavigate(feat.id as ActivePage)}
                className="bg-bg-card border border-border-subtle hover:border-accent-cyan/40 rounded-xl p-5 shadow-card transition-all duration-200 cursor-pointer group flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="p-2.5 rounded-lg bg-bg-elevated text-accent-cyan group-hover:bg-accent-cyan/10 transition-colors">
                      <Icon className="w-5 h-5" />
                    </div>
                    <StatusBadge variant={feat.accent}>{feat.category}</StatusBadge>
                  </div>

                  <h3 className="text-sm font-bold text-text-primary mb-1.5 group-hover:text-accent-cyan transition-colors">
                    {feat.title}
                  </h3>

                  <p className="text-xs text-text-secondary leading-relaxed">
                    {feat.description}
                  </p>
                </div>

                <div className="flex items-center gap-1.5 text-xs font-semibold text-accent-cyan mt-4 pt-3 border-t border-border-subtle/50 group-hover:translate-x-1 transition-transform">
                  <span>Open Laboratory</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Learning Center Banner */}
      <div
        onClick={() => onNavigate('learning')}
        className="bg-gradient-to-r from-bg-card to-bg-elevated border border-border-subtle hover:border-accent-cyan/40 rounded-xl p-5 shadow-card cursor-pointer transition-all flex items-center justify-between group"
      >
        <div className="flex items-center gap-4">
          <div className="p-3 rounded-xl bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-text-primary group-hover:text-accent-cyan transition-colors">
              Module 7: Cryptographic Learning Center & Knowledge Quiz
            </h3>
            <p className="text-xs text-text-secondary mt-0.5">
              12 curriculum topics covering hash mechanics, blockchain Merkle trees, and a 10-question evaluation quiz.
            </p>
          </div>
        </div>

        <ArrowRight className="w-5 h-5 text-accent-cyan group-hover:translate-x-1.5 transition-transform" />
      </div>
    </div>
  );
};

