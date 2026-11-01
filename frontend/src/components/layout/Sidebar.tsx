import React from 'react';
import {
  LayoutDashboard,
  Fingerprint,
  GitCompareArrows,
  Binary,
  Layers,
  ChartNoAxesCombined,
  FileCheck,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { StatusBadge } from '../shared/StatusBadge';

export type ActivePage =
  | 'dashboard'
  | 'generator'
  | 'algorithms'
  | 'single-bit'
  | 'multi-bit'
  | 'avalanche'
  | 'file-integrity'
  | 'learning';

interface SidebarProps {
  activePage: ActivePage;
  onSelectPage: (page: ActivePage) => void;
  collapsed: boolean;
  onToggleCollapsed: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activePage,
  onSelectPage,
  collapsed,
  onToggleCollapsed,
}) => {
  const navSections = [
    {
      group: 'Overview',
      items: [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
      ],
    },
    {
      group: 'Cryptography Lab',
      items: [
        { id: 'generator', label: 'Hash Generator', icon: Fingerprint },
        { id: 'algorithms', label: 'Algorithm Lab', icon: GitCompareArrows },
        { id: 'single-bit', label: 'Single-Bit Experiment', icon: Binary },
        { id: 'multi-bit', label: 'Multi-Bit Experiment', icon: Layers },
        { id: 'avalanche', label: 'Avalanche Analyzer', icon: ChartNoAxesCombined },
        { id: 'file-integrity', label: 'File Integrity Lab', icon: FileCheck },
      ],
    },
    {
      group: 'Education',
      items: [
        { id: 'learning', label: 'Learning Center', icon: BookOpen },
      ],
    },
  ];

  return (
    <aside
      className={cn(
        'bg-bg-sidebar border-r border-border-subtle flex flex-col justify-between transition-all duration-300 z-30 select-none flex-shrink-0 min-h-screen',
        collapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* Top Header / Branding */}
      <div>
        <div className="h-16 px-4 border-b border-border-subtle flex items-center justify-between">
          {!collapsed ? (
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-accent-cyan/15 border border-accent-cyan/40 flex items-center justify-center text-accent-cyan">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <div className="text-sm font-bold tracking-wider text-text-primary flex items-center gap-1.5">
                  HASH<span className="text-accent-cyan">FORGE</span>
                </div>
                <div className="text-[10px] text-text-muted font-medium tracking-wide">
                  CRYPTOGRAPHY LAB
                </div>
              </div>
            </div>
          ) : (
            <div className="mx-auto w-8 h-8 rounded-lg bg-accent-cyan/15 border border-accent-cyan/40 flex items-center justify-center text-accent-cyan">
              <ShieldCheck className="w-5 h-5" />
            </div>
          )}

          <button
            type="button"
            onClick={onToggleCollapsed}
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            className="p-1.5 rounded-lg text-text-muted hover:text-text-primary hover:bg-bg-elevated transition-colors"
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-6">
          {navSections.map((sec) => (
            <div key={sec.group}>
              {!collapsed && (
                <div className="px-3 mb-2 text-[11px] font-semibold tracking-wider text-text-muted uppercase">
                  {sec.group}
                </div>
              )}

              <div className="space-y-1">
                {sec.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activePage === item.id;

                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => onSelectPage(item.id as ActivePage)}
                      title={collapsed ? item.label : undefined}
                      className={cn(
                        'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all group',
                        isActive
                          ? 'bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30 shadow-cyan-glow'
                          : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated/70'
                      )}
                    >
                      <Icon className={cn('w-4 h-4 flex-shrink-0', isActive ? 'text-accent-cyan' : 'text-text-muted group-hover:text-text-primary')} />
                      {!collapsed && <span className="truncate">{item.label}</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>
      </div>

      {/* Bottom Status Box */}
      <div className="p-3 border-t border-border-subtle">
        {!collapsed ? (
          <div className="bg-bg-card border border-border-subtle rounded-lg p-3">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] text-text-muted">Core Engine</span>
              <StatusBadge variant="emerald" icon="shield">FIPS Active</StatusBadge>
            </div>
            <div className="text-[11px] text-text-secondary">
              SHA-256 / SHA3-256
            </div>
            <div className="text-[10px] text-text-muted mt-1 font-mono-code">
              Big-Endian MSB Order
            </div>
          </div>
        ) : (
          <div className="flex justify-center" title="FIPS Core Active">
            <div className="w-3 h-3 rounded-full bg-accent-emerald animate-pulse" />
          </div>
        )}
      </div>
    </aside>
  );
};

