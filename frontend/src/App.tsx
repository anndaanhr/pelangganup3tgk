import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import CustomerTable from './components/customers/CustomerTable';
import CustomerDetail from './pages/CustomerDetail';
import AnalyticsPage from './pages/AnalyticsPage';

import LoginPage from './pages/LoginPage';
import InfrastructurePage from './pages/analysis/InfrastructurePage';
import ParetoPage from './pages/analysis/ParetoPage';
import PowerPage from './pages/analysis/PowerPage';
import ComparisonPage from './pages/analysis/ComparisonPage';

const LOGIN_KEY = 'pln_energy_monitor_logged_in';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const loggedIn = sessionStorage.getItem(LOGIN_KEY) === 'true';
  if (!loggedIn) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function App() {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    sessionStorage.setItem(LOGIN_KEY, 'true');
    navigate('/', { replace: true });
  };

  const handleShowDetail = (data: any) => {
    const idpel = data?.idpel || data?.['2025']?.idpel || data?.['2024']?.idpel;
    if (idpel) navigate(`/pelanggan/${idpel}`);
  };

  return (
    <Routes>
      <Route path="/login" element={<LoginPage onLoginSuccess={handleLoginSuccess} />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard setActiveTab={(tab) => navigate(tab === 'new' ? '/pelanggan/baru' : tab === 'lost' ? '/pelanggan/hilang' : '/pelanggan/semua')} onShowDetail={handleShowDetail} />} />
        <Route path="pelanggan/semua" element={<CustomerTable mode="all" onShowDetail={handleShowDetail} />} />
        <Route path="pelanggan/baru" element={<CustomerTable mode="new" onShowDetail={handleShowDetail} />} />
        <Route path="pelanggan/hilang" element={<CustomerTable mode="lost" onShowDetail={handleShowDetail} />} />
        <Route path="pelanggan/:idpel" element={<CustomerDetail />} />


        {/* Deep Dive Routes */}
        <Route path="analysis/infrastructure" element={<InfrastructurePage />} />
        <Route path="analysis/pareto" element={<ParetoPage />} />
        <Route path="analysis/power" element={<PowerPage />} />
        <Route path="analysis/comparison" element={<ComparisonPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
