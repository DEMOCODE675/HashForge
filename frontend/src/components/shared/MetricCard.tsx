import React from 'react';
import { cn } from '../../lib/utils';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  accentColor?: 'cyan' | 'emerald' | 'amber' | 'rose' | 'default';
  tooltip?: string;
  badge?: string;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  accentColor = 'cyan',
  tooltip,
  badge,
  className,
}) => {
  const valueColorStyles = {
    cyan: 'text-accent-cyan',
    emerald: 'text-accent-emerald',
    amber: 'text-accent-amber',
    rose: 'text-accent-rose',
    default: 'text-text-primary',
  };

  const iconBgStyles = {
    cyan: 'bg-accent-cyan/10 text-accent-cyan',
    emerald: 'bg-accent-emerald/10 text-accent-emerald',
    amber: 'bg-accent-amber/10 text-accent-amber',
    rose: 'bg-accent-rose/10 text-accent-rose',
    default: 'bg-bg-elevated text-text-secondary',
  };

  return (
    <div
      title={tooltip}
      className={cn(
        'bg-bg-card border border-border-subtle rounded-xl p-5 hover:border-border-active/40 transition-all duration-200 shadow-card flex flex-col justify-between',
        className
      )}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
          {title}
        </span>
        {Icon && (
          <div className={cn('p-2 rounded-lg', iconBgStyles[accentColor])}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2">
        <div className={cn('text-2xl font-bold font-mono-code tracking-tight', valueColorStyles[accentColor])}>
          {value}
        </div>
        {badge && (
          <span className="text-xs px-2 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border-subtle">
            {badge}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="text-xs text-text-muted mt-2">
          {subtitle}
        </p>
      )}
    </div>
  );
};

