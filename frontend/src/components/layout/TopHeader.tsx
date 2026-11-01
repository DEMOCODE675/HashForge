import React, { useState, useEffect } from 'react';
import {
  Search,
  SunMoon,
  BookOpen,
  ShieldCheck,
  ChevronRight,
  Wifi,
  WifiOff,
} from 'lucide-react';
import { api } from '../../services/api';
import { ActivePage } from './Sidebar';

interface TopHeaderProps {
  activePage: ActivePage;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  onOpenDocs: () => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({
  activePage,
  theme,
  onToggleTheme,
  onOpenDocs,
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
    <header className="h-16 px-6 bg-bg-primary/80 backdrop-blur-md border-b border-border-subtle flex items-center justify-between sticky top-0 z-20">
      {/* Breadcrumb Trail */}
      <div className="flex items-center gap-2 text-xs">
        <span className="text-text-muted font-medium">HashForge</span>
        <ChevronRight className="w-3.5 h-3.5 text-text-muted" />
        <span className="text-text-secondary font-medium">{current.category}</span>
        <ChevronRight className="w-3.5 h-3.5 text-text-muted" />
        <span className="text-text-primary font-semibold">{current.title}</span>
      </div>

      {/* Right Action Icons */}
      <div className="flex items-center gap-3">
        {/* Backend Status */}
        <div
          title={backendOnline ? 'Backend service online at 127.0.0.1:8000' : 'Backend service offline or unreachable'}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-bg-card border border-border-subtle text-xs"
        >
          {backendOnline ? (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
              <span className="text-text-secondary text-[11px] font-mono-code">Core API Ready</span>
            </>
          ) : backendOnline === false ? (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-rose" />
              <span className="text-accent-rose text-[11px] font-mono-code">API Offline</span>
            </>
          ) : (
            <>
              <span className="w-2 h-2 rounded-full bg-accent-amber animate-pulse" />
              <span className="text-text-muted text-[11px] font-mono-code">Connecting...</span>
            </>
          )}
        </div>

        {/* Learning / Docs shortcut */}
        <button
          type="button"
          onClick={onOpenDocs}
          className="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-transparent hover:border-border-subtle transition-colors"
          title="Open Documentation & Learning Center"
          aria-label="Documentation"
        >
          <BookOpen className="w-4 h-4" />
        </button>

        {/* Theme Toggle */}
        <button
          type="button"
          onClick={onToggleTheme}
          className="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-transparent hover:border-border-subtle transition-colors"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Theme`}
          aria-label="Toggle theme"
        >
          <SunMoon className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};

