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
  X,
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
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activePage,
  onSelectPage,
  collapsed,
  onToggleCollapsed,
  mobileOpen = false,
  onCloseMobile,
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
    <>
      {/* Mobile Drawer Backdrop */}
      <div
        className={cn(
          'fixed inset-0 bg-black/70 backdrop-blur-sm z-40 transition-opacity duration-300 lg:hidden',
          mobileOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        )}
        onClick={onCloseMobile}
        aria-hidden="true"
      />

      {/* Main Sidebar Element */}
      <aside
        className={cn(
          'bg-bg-sidebar border-r border-border-subtle flex flex-col justify-between select-none flex-shrink-0 min-h-screen transition-all duration-300 ease-in-out',
          // Mobile Drawer styling
          'fixed inset-y-0 left-0 z-50 w-72 max-w-[85vw] shadow-2xl lg:shadow-none',
          mobileOpen ? 'translate-x-0' : '-translate-x-full',
          // Desktop flow styling
          'lg:static lg:translate-x-0 lg:z-30',
          collapsed ? 'lg:w-20' : 'lg:w-64'
        )}
      >
        {/* Top Header / Branding */}
        <div>
          <div className="h-16 px-4 border-b border-border-subtle flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-accent-cyan/15 border border-accent-cyan/40 flex items-center justify-center text-accent-cyan flex-shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              {(!collapsed || mobileOpen) && (
                <div>
                  <div className="text-sm font-bold tracking-wider text-text-primary flex items-center gap-1.5">
                    HASH<span className="text-accent-cyan">FORGE</span>
                  </div>
                  <div className="text-[10px] text-text-muted font-medium tracking-wide">
                    CRYPTOGRAPHY LAB
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Close Button */}
            <button
              type="button"
              onClick={onCloseMobile}
              aria-label="Close navigation menu"
              className="lg:hidden p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-bg-elevated transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Desktop Collapse Toggle */}
            <button
              type="button"
              onClick={onToggleCollapsed}
              aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
              className="hidden lg:flex p-1.5 rounded-lg text-text-muted hover:text-text-primary hover:bg-bg-elevated transition-colors"
            >
              {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          {/* Navigation Items */}
          <nav className="p-3 space-y-6 overflow-y-auto max-h-[calc(100vh-140px)]">
            {navSections.map((sec) => (
              <div key={sec.group}>
                {(!collapsed || mobileOpen) && (
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
                        onClick={() => {
                          onSelectPage(item.id as ActivePage);
                          if (onCloseMobile) onCloseMobile();
                        }}
                        title={collapsed && !mobileOpen ? item.label : undefined}
                        className={cn(
                          'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group min-h-[40px]',
                          isActive
                            ? 'bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30 shadow-cyan-glow'
                            : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated/70'
                        )}
                      >
                        <Icon className={cn('w-4 h-4 flex-shrink-0', isActive ? 'text-accent-cyan' : 'text-text-muted group-hover:text-text-primary')} />
                        {(!collapsed || mobileOpen) && <span className="truncate">{item.label}</span>}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>
        </div>

        {/* Bottom Status Box */}
        <div className="p-3 border-t border-border-subtle bg-bg-sidebar">
          {(!collapsed || mobileOpen) ? (
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
            <div className="flex justify-center py-2" title="FIPS Core Active">
              <div className="w-3 h-3 rounded-full bg-accent-emerald animate-pulse" />
            </div>
          )}
        </div>
      </aside>
    </>
  );
};
