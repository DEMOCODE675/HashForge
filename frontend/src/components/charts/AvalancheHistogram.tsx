import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ReferenceLine,
  CartesianGrid,
} from 'recharts';
import { TrialRecord } from '../../types';

interface AvalancheHistogramProps {
  trials: TrialRecord[];
  algorithm: string;
  meanPct: number;
  className?: string;
}

export const AvalancheHistogram: React.FC<AvalancheHistogramProps> = ({
  trials,
  algorithm,
  meanPct,
  className,
}) => {
  // Compute histogram bins (e.g. 2% buckets from 30% to 70%)
  const binSize = 2;
  const minBin = 30;
  const maxBin = 70;
  const binsMap: { [key: number]: number } = {};

  for (let b = minBin; b <= maxBin; b += binSize) {
    binsMap[b] = 0;
  }

  trials.forEach((t) => {
    const bucket = Math.floor(t.avalanche_pct / binSize) * binSize;
    if (bucket >= minBin && bucket <= maxBin) {
      binsMap[bucket] = (binsMap[bucket] || 0) + 1;
    }
  });

  const chartData = Object.keys(binsMap)
    .map(Number)
    .sort((a, b) => a - b)
    .map((bucket) => ({
      range: `${bucket}%–${bucket + binSize}%`,
      binCenter: bucket + binSize / 2,
      count: binsMap[bucket],
    }));

  const isSha3 = algorithm.toLowerCase().includes('3');
  const barColor = isSha3 ? '#10B981' : '#00D6C9';

  return (
    <div className={`bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card ${className || ''}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-text-primary">
            Avalanche Percentage Histogram ({algorithm.toUpperCase()})
          </h3>
          <p className="text-xs text-text-muted">
            Frequency distribution across {trials.length} trials compared to the 50% theoretical target
          </p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis
              dataKey="range"
              stroke="#64748B"
              fontSize={10}
              tickLine={false}
              interval={1}
              angle={-25}
              textAnchor="end"
            />
            <YAxis stroke="#64748B" fontSize={11} tickLine={false} allowDecimals={false} />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-bg-elevated border border-border-subtle p-3 rounded-lg shadow-lg text-xs font-mono-code">
                      <div className="text-text-secondary">Range: <strong className="text-text-primary">{data.range}</strong></div>
                      <div className="text-text-secondary mt-1">Trials: <strong className="text-accent-cyan">{data.count}</strong></div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <ReferenceLine
              x="50%–52%"
              stroke="#10B981"
              strokeWidth={2}
              strokeDasharray="4 4"
              label={{
                value: 'Target 50%',
                fill: '#10B981',
                fontSize: 10,
                position: 'top',
              }}
            />
            <Bar dataKey="count" fill={barColor} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-xs text-text-muted mt-2 pt-2 border-t border-border-subtle/50">
        <span>Empirical Mean: <strong className="text-accent-cyan">{meanPct.toFixed(2)}%</strong></span>
        <span>Theoretical Center: <strong className="text-accent-emerald">50.00%</strong></span>
      </div>
    </div>
  );
};

