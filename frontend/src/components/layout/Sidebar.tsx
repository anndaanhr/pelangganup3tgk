import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, UserPlus, UserMinus, LogOut, FileText, BarChart2, ChevronDown, ChevronRight, UserCog } from 'lucide-react';
import plnLogo from '../../img/image.png';

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isCustomerMenuOpen, setIsCustomerMenuOpen] = useState(true);

  // Auto-open menu if current path is a sub-item
  useEffect(() => {
    if (location.pathname.startsWith('/pelanggan')) {
      setIsCustomerMenuOpen(true);
    }
  }, [location.pathname]);


  const handleLogout = () => {
    sessionStorage.removeItem('pln_energy_monitor_logged_in');
    navigate('/login', { replace: true });
  };

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer transition-all duration-200 group ${isActive ? 'bg-blue-600 text-white shadow-md shadow-blue-200' : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
    }`;

  const subNavClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-4 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-sm ml-4 border-l-2 ${isActive ? 'border-blue-600 text-blue-700 bg-blue-50 font-medium' : 'border-transparent text-gray-500 hover:text-gray-900 hover:bg-gray-50'
    }`;

  return (
    <aside className="w-64 bg-white border-r border-gray-100 flex flex-col fixed h-full z-10 transition-all duration-300">
      <div className="p-6 flex items-center gap-4">
        <div className="flex-shrink-0">
          <img src={plnLogo} alt="PLN Logo" className="w-[48px] h-auto object-contain" />
        </div>
        <div>
          <h2 className="font-bold text-gray-800 text-base tracking-tight leading-tight">Energy Monitor</h2>
          <p className="text-[10px] text-gray-400 uppercase tracking-wider font-semibold">Admin Dashboard</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto custom-scrollbar">
        <div className="mb-6">
          <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Main Menu</p>
          <NavLink to="/" end className={navClass}>
            <LayoutDashboard size={20} className="shrink-0" />
            <span className="text-sm font-medium">Dashboard</span>
          </NavLink>
        </div>

        <div>
          {/* Collapsible Customer Menu */}
          <button
            onClick={() => setIsCustomerMenuOpen(!isCustomerMenuOpen)}
            className="w-full flex items-center justify-between px-4 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 hover:text-gray-600 transition-colors"
          >
            <span>Monitoring Pelanggan</span>
            {isCustomerMenuOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </button>

          <div className={`space-y-1 transition-all duration-300 overflow-hidden ${isCustomerMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
            <NavLink to="/pelanggan/baru" className={subNavClass}>
              <UserPlus size={18} className="shrink-0" />
              <span>Pelanggan Baru</span>
            </NavLink>
            <NavLink to="/pelanggan/hilang" className={subNavClass}>
              <UserMinus size={18} className="shrink-0" />
              <span>Pelanggan Hilang</span>
            </NavLink>
            <NavLink to="/pelanggan/semua" className={subNavClass}>
              <UserCog size={18} className="shrink-0" />
              <span>Semua Data</span>
            </NavLink>
          </div>
        </div>

      </nav>

      <div className="p-4 border-t border-gray-100 mb-2">
        <div className="flex items-center gap-3 px-4 py-3 mb-2">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-bold text-xs">A</div>
          <div className="overflow-hidden">
            <h4 className="text-sm font-bold text-gray-700 truncate">Admin PLN</h4>
            <p className="text-xs text-gray-400 truncate">UP3 Tanjung Karang</p>
          </div>
        </div>
        <button
          type="button"
          onClick={handleLogout}
          className="flex items-center gap-3 text-red-500 hover:bg-red-50 px-4 py-2.5 rounded-lg w-full transition-colors group"
        >
          <LogOut size={18} className="group-hover:-translate-x-1 transition-transform" />
          <span className="text-sm font-medium">Log out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
