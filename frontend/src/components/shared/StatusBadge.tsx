import React from 'react';
import { cn } from '../../lib/utils';
import { ShieldCheck, CheckCircle2, AlertCircle, AlertTriangle, Info } from 'lucide-react';

interface StatusBadgeProps {
  variant?: 'cyan' | 'emerald' | 'amber' | 'rose' | 'default';
  children: React.ReactNode;
  icon?: 'shield' | 'check' | 'alert' | 'warning' | 'info' | 'none';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  variant = 'cyan',
  children,
  icon = 'none',
  className,
}) => {
  const variantStyles = {
    cyan: 'bg-accent-cyan/10 text-accent-cyan border-accent-cyan/30',
    emerald: 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/30',
    amber: 'bg-accent-amber/10 text-accent-amber border-accent-amber/30',
    rose: 'bg-accent-rose/10 text-accent-rose border-accent-rose/30',
    default: 'bg-bg-elevated text-text-secondary border-border-subtle',
  };

  const renderIcon = () => {
    switch (icon) {
      case 'shield':
        return <ShieldCheck className="w-3.5 h-3.5 mr-1" />;
      case 'check':
        return <CheckCircle2 className="w-3.5 h-3.5 mr-1" />;
      case 'alert':
        return <AlertCircle className="w-3.5 h-3.5 mr-1" />;
      case 'warning':
        return <AlertTriangle className="w-3.5 h-3.5 mr-1" />;
      case 'info':
        return <Info className="w-3.5 h-3.5 mr-1" />;
      default:
        return null;
    }
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider border',
        variantStyles[variant],
        className
      )}
    >
      {renderIcon()}
      {children}
    </span>
  );
};

