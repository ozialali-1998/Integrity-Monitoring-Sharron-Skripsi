import { useMemo, useState } from 'react';
import Layout from './components/Layout.jsx';
import Benchmark from './pages/Benchmark.jsx';
import Dashboard from './pages/Dashboard.jsx';
import DirectoryMonitoring from './pages/DirectoryMonitoring.jsx';
import Logs from './pages/Logs.jsx';
import Settings from './pages/Settings.jsx';
import Verification from './pages/Verification.jsx';

export default function App() {
  const [currentPage, setCurrentPage] = useState('Dashboard');

  const page = useMemo(() => {
    switch (currentPage) {
      case 'Directory Monitoring':
        return <DirectoryMonitoring />;
      case 'Verification':
        return <Verification />;
      case 'Benchmark':
        return <Benchmark />;
      case 'Logs':
        return <Logs />;
      case 'Settings':
        return <Settings />;
      case 'Dashboard':
      default:
        return <Dashboard />;
    }
  }, [currentPage]);

  return (
    <Layout currentPage={currentPage} onNavigate={setCurrentPage}>
      {page}
    </Layout>
  );
}
