import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ReferenceLine,
} from 'recharts';
import { AvalancheSimulationResponse } from '../../types';

interface AlgorithmComparisonBoxProps {
  sha256Result: AvalancheSimulationResponse;
  sha3Result: AvalancheSimulationResponse;
  className?: string;
}

export const AlgorithmComparisonBox: React.FC<AlgorithmComparisonBoxProps> = ({
  sha256Result,
  sha3Result,
  className,
}) => {
  const comparisonData = [
    {
      metric: 'Mean Avalanche',
      'SHA-256': sha256Result.mean_avalanche_pct,
      'SHA3-256': sha3Result.mean_avalanche_pct,
    },
    {
      metric: 'Median Avalanche',
      'SHA-256': sha256Result.median_avalanche_pct,
      'SHA3-256': sha3Result.median_avalanche_pct,
    },
    {
      metric: 'Minimum Recorded',
      'SHA-256': sha256Result.min_avalanche_pct,
      'SHA3-256': sha3Result.min_avalanche_pct,
    },
    {
      metric: 'Maximum Recorded',
      'SHA-256': sha256Result.max_avalanche_pct,
      'SHA3-256': sha3Result.max_avalanche_pct,
    },
  ];

  return (
    <div className={`bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card ${className || ''}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-text-primary">
            Statistical Metric Comparison (SHA-256 vs SHA3-256)
          </h3>
          <p className="text-xs text-text-muted">
            Evaluation of empirical diffusion metrics across identical single-bit perturbation sets
          </p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={comparisonData} margin={{ top: 10, right: 20, left: -10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis dataKey="metric" stroke="#64748B" fontSize={11} tickLine={false} />
            <YAxis domain={[30, 70]} stroke="#64748B" fontSize={11} tickLine={false} unit="%" />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-bg-elevated border border-border-subtle p-3 rounded-lg shadow-lg text-xs font-mono-code space-y-1">
                      <div className="text-text-primary font-bold">{payload[0].payload.metric}</div>
                      <div className="text-accent-cyan">
                        SHA-256: <strong>{Number(payload[0].value).toFixed(2)}%</strong>
                      </div>
                      <div className="text-accent-emerald">
                        SHA3-256: <strong>{Number(payload[1].value).toFixed(2)}%</strong>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }}
              formatter={(value) => <span className="text-text-secondary">{value}</span>}
            />
            <ReferenceLine y={50} stroke="#F59E0B" strokeDasharray="4 4" strokeWidth={1.5} />
            <Bar dataKey="SHA-256" fill="#00D6C9" radius={[4, 4, 0, 0]} />
            <Bar dataKey="SHA3-256" fill="#10B981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

