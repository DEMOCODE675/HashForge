import React, { useState } from 'react';
import { AppShell } from './components/layout/AppShell';
import { ActivePage } from './components/layout/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { HashGenerator } from './pages/HashGenerator';
import { AlgorithmLab } from './pages/AlgorithmLab';
import { SingleBitExperiment } from './pages/SingleBitExperiment';
import { MultiBitExperiment } from './pages/MultiBitExperiment';
import { AvalancheAnalyzer } from './pages/AvalancheAnalyzer';
import { FileIntegrity } from './pages/FileIntegrity';
import { LearningCenter } from './pages/LearningCenter';

export const App: React.FC = () => {
  const [activePage, setActivePage] = useState<ActivePage>('dashboard');

  const renderActivePage = () => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard onNavigate={setActivePage} />;
      case 'generator':
        return <HashGenerator />;
      case 'algorithms':
        return <AlgorithmLab />;
      case 'single-bit':
        return <SingleBitExperiment />;
      case 'multi-bit':
        return <MultiBitExperiment />;
      case 'avalanche':
        return <AvalancheAnalyzer />;
      case 'file-integrity':
        return <FileIntegrity />;
      case 'learning':
        return <LearningCenter />;
      default:
        return <Dashboard onNavigate={setActivePage} />;
    }
  };

  return (
    <AppShell activePage={activePage} onSelectPage={setActivePage}>
      {renderActivePage()}
    </AppShell>
  );
};

export default App;
