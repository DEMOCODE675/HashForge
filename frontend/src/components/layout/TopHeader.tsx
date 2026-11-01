import React, { useState, useEffect } from 'react';
import {
  Menu,
  SunMoon,
  BookOpen,
  ChevronRight,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../../services/api';
import { ActivePage } from './Sidebar';

interface TopHeaderProps {
  activePage: ActivePage;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  onOpenDocs: () => void;
  onToggleMobileMenu?: () => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({
  activePage,
  theme,
  onToggleTheme,
  onOpenDocs,
  onToggleMobileMenu,
}) => {
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let isMounted = true;
    const checkHealth = async () => {
      try {
        await api.getHealth();
        if (isMounted) setBackendOnline(true);
      } catch {
        if (isMounted) setBackendOnline(false);
      }
    };
    checkHealth();
    const timer = setInterval(checkHealth, 15000);
    return () => {
      isMounted = false;
      clearInterval(timer);
    };
  }, []);

  const pageTitles: Record<ActivePage, { title: string; category: string }> = {
    dashboard: { title: 'Dashboard Overview', category: 'Platform' },
    generator: { title: 'Hash Generator Laboratory', category: 'Module 1' },
    algorithms: { title: 'Algorithm Comparison Lab', category: 'Module 2' },
    'single-bit': { title: 'Single-Bit Flip Experiment', category: 'Module 3' },
    'multi-bit': { title: 'Multi-Bit Flip Experiment', category: 'Module 4' },
    avalanche: { title: 'Avalanche Statistical Analyzer', category: 'Module 5' },
    'file-integrity': { title: 'File Integrity Laboratory', category: 'Module 6' },
    learning: { title: 'Learning Center & Knowledge Quiz', category: 'Module 7' },
  };

  const current = pageTitles[activePage] || { title: 'Dashboard', category: 'Overview' };

  return (
    <header className="h-16 px-3 sm:px-6 bg-bg-primary/90 backdrop-blur-md border-b border-border-subtle flex items-center justify-between sticky top-0 z-20">
      {/* Left: Mobile Menu Trigger + Breadcrumb Trail */}
      <div className="flex items-center gap-2 sm:gap-2.5 min-w-0">
        <button
          type="button"
          onClick={onToggleMobileMenu}
          aria-label="Open navigation menu"
          className="lg:hidden p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-border-subtle/50 transition-colors flex-shrink-0"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Mobile Logo Brand Icon */}
        <div className="lg:hidden flex items-center gap-1.5 flex-shrink-0">
          <div className="w-7 h-7 rounded-lg bg-accent-cyan/15 border border-accent-cyan/40 flex items-center justify-center text-accent-cyan">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>

        {/* Breadcrumb Trail */}
        <div className="flex items-center gap-1.5 sm:gap-2 text-xs min-w-0 truncate">
          <span className="hidden sm:inline text-text-muted font-medium">HashForge</span>
          <ChevronRight className="hidden sm:inline w-3.5 h-3.5 text-text-muted flex-shrink-0" />
          <span className="hidden md:inline text-text-secondary font-medium">{current.category}</span>
          <ChevronRight className="hidden md:inline w-3.5 h-3.5 text-text-muted flex-shrink-0" />
          <span className="text-text-primary font-semibold truncate max-w-[150px] sm:max-w-none">
            {current.title}
          </span>
        </div>
      </div>

      {/* Right Action Icons */}
      <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
        {/* Backend Status */}
        <div
          title={backendOnline ? 'Backend service online at /api/health' : 'Backend service offline or unreachable'}
          className="flex items-center gap-1.5 px-2 sm:px-2.5 py-1 rounded-full bg-bg-card border border-border-subtle text-xs"
        >
          {backendOnline ? (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse flex-shrink-0" />
              <span className="hidden sm:inline text-text-secondary text-[11px] font-mono-code">Core API Ready</span>
              <span className="sm:hidden text-accent-emerald text-[10px] font-mono-code">Ready</span>
            </>
          ) : backendOnline === false ? (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-rose flex-shrink-0" />
              <span className="hidden sm:inline text-accent-rose text-[11px] font-mono-code">API Offline</span>
              <span className="sm:hidden text-accent-rose text-[10px] font-mono-code">Offline</span>
            </>
          ) : (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-amber animate-pulse flex-shrink-0" />
              <span className="hidden sm:inline text-text-muted text-[11px] font-mono-code">Connecting...</span>
              <span className="sm:hidden text-text-muted text-[10px] font-mono-code">...</span>
            </>
          )}
        </div>

        {/* Learning / Docs shortcut */}
        <button
          type="button"
          onClick={onOpenDocs}
          className="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-transparent hover:border-border-subtle transition-colors min-h-[38px] min-w-[38px] flex items-center justify-center"
          title="Open documentation"
          aria-label="Open documentation"
        >
          <BookOpen className="w-4 h-4" />
        </button>

        {/* Dark / Light Theme Toggle */}
        <button
          type="button"
          onClick={onToggleTheme}
          className="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-transparent hover:border-border-subtle transition-colors min-h-[38px] min-w-[38px] flex items-center justify-center"
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          aria-label="Toggle theme"
        >
          <SunMoon className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
