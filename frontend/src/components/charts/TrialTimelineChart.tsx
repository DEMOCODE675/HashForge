import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ReferenceLine,
  CartesianGrid,
} from 'recharts';
import { TrialRecord } from '../../types';

interface TrialTimelineChartProps {
  trials: TrialRecord[];
  algorithm: string;
  className?: string;
}

export const TrialTimelineChart: React.FC<TrialTimelineChartProps> = ({
  trials,
  algorithm,
  className,
}) => {
  const isSha3 = algorithm.toLowerCase().includes('3');
  const lineColor = isSha3 ? '#10B981' : '#00D6C9';

  return (
    <div className={`bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card ${className || ''}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-text-primary">
            Trial-by-Trial Avalanche Dispersion ({algorithm.toUpperCase()})
          </h3>
          <p className="text-xs text-text-muted">
            Tracking deviation across consecutive single-bit perturbations
          </p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trials} margin={{ top: 10, right: 20, left: -10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis dataKey="trial" stroke="#64748B" fontSize={11} tickLine={false} />
            <YAxis
              domain={[30, 70]}
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              unit="%"
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload as TrialRecord;
                  return (
                    <div className="bg-bg-elevated border border-border-subtle p-3 rounded-lg shadow-lg text-xs font-mono-code space-y-1">
                      <div className="text-text-primary font-bold">Trial #{data.trial}</div>
                      <div className="text-text-secondary">Flipped Bit: <strong className="text-accent-cyan">{data.bit_index}</strong></div>
                      <div className="text-text-secondary">Hamming Dist: <strong className="text-text-primary">{data.hamming_distance} / 256</strong></div>
                      <div className="text-text-secondary">Avalanche: <strong className="text-accent-amber">{data.avalanche_pct.toFixed(2)}%</strong></div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <ReferenceLine
              y={50}
              stroke="#10B981"
              strokeWidth={2}
              strokeDasharray="4 4"
              label={{
                value: '50% Baseline',
                fill: '#10B981',
                fontSize: 10,
                position: 'right',
              }}
            />
            <Line
              type="monotone"
              dataKey="avalanche_pct"
              stroke={lineColor}
              strokeWidth={2}
              dot={{ r: 2.5, fill: lineColor, stroke: '#0B0F17', strokeWidth: 1 }}
              activeDot={{ r: 5, fill: '#F59E0B' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-xs text-text-muted mt-2 pt-2 border-t border-border-subtle/50">
        <span>Total Experiments: <strong className="text-text-secondary">{trials.length}</strong></span>
        <span>Reference Criterion: <strong className="text-accent-emerald">Strict Avalanche Criterion (SAC)</strong></span>
      </div>
    </div>
  );
};

