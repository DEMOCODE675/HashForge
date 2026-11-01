import React, { useState, useEffect } from 'react';
import {
  ChartNoAxesCombined,
  Zap,
  Activity,
  Layers,
  Download,
  RefreshCw,
  AlertCircle,
  FileSpreadsheet,
} from 'lucide-react';
import { api } from '../services/api';
import {
  AvalancheSimulationResponse,
  ComparativeSimulationResponse,
} from '../types';
import { MetricCard } from '../components/shared/MetricCard';
import { AvalancheHistogram } from '../components/charts/AvalancheHistogram';
import { TrialTimelineChart } from '../components/charts/TrialTimelineChart';
import { AlgorithmComparisonBox } from '../components/charts/AlgorithmComparisonBox';
import { StatusBadge } from '../components/shared/StatusBadge';

export const AvalancheAnalyzer: React.FC = () => {
  const [inputText, setInputText] = useState('HashForge Cryptographic Avalanche Statistical Evaluation 2026');
  const [trialsCount, setTrialsCount] = useState(50);
  const [algorithm, setAlgorithm] = useState<'sha256' | 'sha3_256'>('sha256');
  const [comparative, setComparative] = useState(true);
  const [mode, setMode] = useState<'single_bit' | 'cumulative'>('single_bit');
  const [seed, setSeed] = useState<number | null>(101);

  const [simData, setSimData] = useState<AvalancheSimulationResponse | null>(null);
  const [compData, setCompData] = useState<ComparativeSimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tableAlgo, setTableAlgo] = useState<'sha256' | 'sha3_256'>('sha256');

  const runSimulation = async () => {
    if (!inputText) {
      setError('Baseline input text cannot be empty.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.avalancheSimulation(
        inputText,
        trialsCount,
        algorithm,
        seed,
        mode,
        comparative
      );
      if (comparative) {
        setCompData(res as ComparativeSimulationResponse);
        setSimData(null);
      } else {
        setSimData(res as AvalancheSimulationResponse);
        setCompData(null);
      }
    } catch (err: any) {
      setError(err?.message || 'Simulation execution failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, []);

  const exportCSV = (trials: any[], algoName: string) => {
    const headers = 'Trial,Bit Index,Byte Index,Hamming Distance,Avalanche %,Original Hex,Modified Hex,Latency (ms)\n';
    const rows = trials
      .map(
        (t) =>
          `${t.trial},${t.bit_index},${t.byte_index},${t.hamming_distance},${t.avalanche_pct},"${t.original_hex}","${t.modified_hex}",${t.time_ms}`
      )
      .join('\n');
    const blob = new Blob([headers + rows], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `hashforge_${algoName}_simulation_${trials.length}_trials.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const activeResult = comparative && compData
    ? tableAlgo === 'sha256'
      ? compData.sha256_result
      : compData.sha3_256_result
    : simData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <ChartNoAxesCombined className="w-5 h-5 text-accent-cyan" />
            <h1 className="text-xl font-bold text-text-primary">Module 5: Avalanche Statistical Analyzer</h1>
          </div>
          <p className="text-xs text-text-muted">
            High-sample Monte Carlo simulations to statistically evaluate binomial diffusion against the 50% target.
          </p>
        </div>

        <StatusBadge variant="cyan" icon="shield">Monte Carlo Engine</StatusBadge>
      </div>

      {/* Experiment Controls */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
        <div className="space-y-2">
          <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block">
            Baseline Plaintext String (Reset Every Trial)
          </label>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-4 py-2.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan transition-colors"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-3 border-t border-border-subtle/50">
          <div>
            <label className="text-xs text-text-secondary block mb-1">Sample Count:</label>
            <select
              value={trialsCount}
              onChange={(e) => setTrialsCount(Number(e.target.value))}
              className="w-full bg-bg-elevated border border-border-subtle rounded-lg px-3 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            >
              <option value={10}>10 Trials</option>
              <option value={50}>50 Trials</option>
              <option value={100}>100 Trials</option>
              <option value={200}>200 Trials</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-text-secondary block mb-1">Execution Mode:</label>
            <select
              value={comparative ? 'comp' : 'single'}
              onChange={(e) => setComparative(e.target.value === 'comp')}
              className="w-full bg-bg-elevated border border-border-subtle rounded-lg px-3 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            >
              <option value="comp">Compare SHA-2 & SHA-3</option>
              <option value="single">Single Algorithm</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-text-secondary block mb-1">Trial Methodology:</label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value as any)}
              className="w-full bg-bg-elevated border border-border-subtle rounded-lg px-3 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            >
              <option value="single_bit">Independent Flips (SAC)</option>
              <option value="cumulative">Cumulative Mutation</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-text-secondary block mb-1">Deterministic Seed:</label>
            <input
              type="number"
              value={seed ?? ''}
              onChange={(e) => setSeed(e.target.value ? Number(e.target.value) : null)}
              placeholder="e.g. 101"
              className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-3 py-2 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="button"
            onClick={runSimulation}
            disabled={loading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow min-h-[44px]"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Simulating...' : 'Execute Monte Carlo Simulation'}</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Statistical Summary KPIs */}
      {activeResult && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <MetricCard
            title="Mean Avalanche"
            value={`${activeResult.mean_avalanche_pct.toFixed(2)}%`}
            subtitle="Target: 50.00%"
            icon={Zap}
            accentColor="cyan"
          />
          <MetricCard
            title="Standard Dev"
            value={`±${activeResult.std_avalanche_pct.toFixed(2)}%`}
            subtitle="Dispersion from Mean"
            icon={Activity}
            accentColor="emerald"
          />
          <MetricCard
            title="Min Avalanche"
            value={`${activeResult.min_avalanche_pct.toFixed(2)}%`}
            subtitle="Minimum recorded trial"
            icon={ChartNoAxesCombined}
            accentColor="default"
          />
          <MetricCard
            title="Max Avalanche"
            value={`${activeResult.max_avalanche_pct.toFixed(2)}%`}
            subtitle="Maximum recorded trial"
            icon={ChartNoAxesCombined}
            accentColor="default"
          />
          <MetricCard
            title="Median"
            value={`${activeResult.median_avalanche_pct.toFixed(2)}%`}
            subtitle="50th Percentile"
            icon={Layers}
            accentColor="amber"
          />
        </div>
      )}

      {/* Visual Charts */}
      {comparative && compData ? (
        <div className="space-y-6">
          <AlgorithmComparisonBox
            sha256Result={compData.sha256_result}
            sha3Result={compData.sha3_256_result}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AvalancheHistogram
              trials={compData.sha256_result.trials}
              algorithm="sha256"
              meanPct={compData.sha256_result.mean_avalanche_pct}
            />
            <AvalancheHistogram
              trials={compData.sha3_256_result.trials}
              algorithm="sha3_256"
              meanPct={compData.sha3_256_result.mean_avalanche_pct}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <TrialTimelineChart
              trials={compData.sha256_result.trials}
              algorithm="sha256"
            />
            <TrialTimelineChart
              trials={compData.sha3_256_result.trials}
              algorithm="sha3_256"
            />
          </div>
        </div>
      ) : (
        simData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AvalancheHistogram
              trials={simData.trials}
              algorithm={simData.algorithm}
              meanPct={simData.mean_avalanche_pct}
            />
            <TrialTimelineChart
              trials={simData.trials}
              algorithm={simData.algorithm}
            />
          </div>
        )
      )}

      {/* Trial Execution Log & CSV Export */}
      {activeResult && (
        <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <FileSpreadsheet className="w-5 h-5 text-accent-cyan" />
              <div>
                <h3 className="text-sm font-semibold text-text-primary">Trial Execution Records</h3>
                <p className="text-xs text-text-muted">{activeResult.trials.length} verified trial records</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {comparative && (
                <div className="inline-flex rounded-lg border border-border-subtle p-0.5 bg-bg-elevated text-xs">
                  <button
                    type="button"
                    onClick={() => setTableAlgo('sha256')}
                    className={`px-3 py-1 rounded-md font-medium transition-colors ${
                      tableAlgo === 'sha256' ? 'bg-bg-card text-accent-cyan font-bold' : 'text-text-secondary'
                    }`}
                  >
                    SHA-256
                  </button>
                  <button
                    type="button"
                    onClick={() => setTableAlgo('sha3_256')}
                    className={`px-3 py-1 rounded-md font-medium transition-colors ${
                      tableAlgo === 'sha3_256' ? 'bg-bg-card text-accent-emerald font-bold' : 'text-text-secondary'
                    }`}
                  >
                    SHA3-256
                  </button>
                </div>
              )}

              <button
                type="button"
                onClick={() => exportCSV(activeResult.trials, activeResult.algorithm)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-bg-elevated hover:bg-bg-card border border-border-subtle text-xs text-text-secondary hover:text-text-primary transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export CSV</span>
              </button>
            </div>
          </div>

          <div className="overflow-x-auto touch-pan-x max-h-72 border border-border-subtle rounded-lg">
            <table className="w-full min-w-[520px] text-left font-mono-code text-xs">
              <thead className="bg-[#070A10] text-text-muted text-[11px] uppercase sticky top-0 border-b border-border-subtle">
                <tr>
                  <th className="px-3 py-2">Trial #</th>
                  <th className="px-3 py-2">Flipped Bit</th>
                  <th className="px-3 py-2">Byte Address</th>
                  <th className="px-3 py-2">Hamming Dist</th>
                  <th className="px-3 py-2">Avalanche %</th>
                  <th className="px-3 py-2">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/50 text-text-secondary">
                {activeResult.trials.map((t) => (
                  <tr key={t.trial} className="hover:bg-bg-elevated/40 transition-colors">
                    <td className="px-3 py-2 text-text-primary font-bold">{t.trial}</td>
                    <td className="px-3 py-2 text-accent-cyan">#{t.bit_index}</td>
                    <td className="px-3 py-2">Byte {t.byte_index}</td>
                    <td className="px-3 py-2 text-text-primary">{t.hamming_distance} / 256</td>
                    <td className="px-3 py-2">
                      <span className="font-bold text-accent-amber">{t.avalanche_pct.toFixed(2)}%</span>
                    </td>
                    <td className="px-3 py-2 text-text-muted">{t.time_ms.toFixed(4)} ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

