import React, { useState } from 'react';
import { Sidebar, ActivePage } from './Sidebar';
import { TopHeader } from './TopHeader';

interface AppShellProps {
  activePage: ActivePage;
  onSelectPage: (page: ActivePage) => void;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({
  activePage,
  onSelectPage,
  children,
}) => {
  const [collapsed, setCollapsed] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    if (nextTheme === 'light') {
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
    }
  };

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary flex antialiased">
      <Sidebar
        activePage={activePage}
        onSelectPage={onSelectPage}
        collapsed={collapsed}
        onToggleCollapsed={() => setCollapsed(!collapsed)}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <TopHeader
          activePage={activePage}
          theme={theme}
          onToggleTheme={toggleTheme}
          onOpenDocs={() => onSelectPage('learning')}
        />

        <main className="flex-1 p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
};

