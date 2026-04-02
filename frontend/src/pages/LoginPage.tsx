import React, { useState } from 'react';
import { User, Lock, Eye, EyeOff } from 'lucide-react';
import logo from '../img/image.png';
import { login } from '../services/authApi';

interface LoginPageProps {
  onLoginSuccess: () => void;
}

const LoginPage = ({ onLoginSuccess }: LoginPageProps) => {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isLoading) return;
    setError('');

    if (!formData.username.trim()) {
      setError('Masukkan username atau email.');
      return;
    }
    if (!formData.password) {
      setError('Masukkan password.');
      return;
    }

    setIsLoading(true);
    try {
      const data = await login(formData.username, formData.password);
      sessionStorage.setItem('access_token', data.access_token);
      sessionStorage.setItem('pln_energy_monitor_logged_in', 'true');
      onLoginSuccess();
    } catch (err: any) {
      console.error("Login failed", err);
      setError('Username atau password salah. Silakan coba lagi.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F0F8F8] flex flex-col items-center justify-center p-4 font-sans">
      {/* Header Section */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-2">
          {/* Logo placeholder - readjust size as needed */}
          <img src={logo} alt="PLN Logo" className="h-12 w-auto object-contain" />
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Energy Monitor</h1>
        </div>
        <p className="text-slate-500 text-sm">Sistem Monitoring Tren Pemakaian Energi Listrik</p>
      </div>

      {/* Login Card */}
      <div className="w-full max-w-md bg-[#475569] rounded-2xl shadow-xl p-8 text-white">
        <div className="mb-6">
          <h2 className="text-xl font-bold mb-1">Masuk ke Dashboard</h2>
          <p className="text-slate-400 text-sm">Silakan masukkan akun Anda untuk melanjutkan</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">

          {/* Username Input */}
          <div className="space-y-1">
            <label className="block text-xs text-slate-300 font-medium ml-1">Email atau Username</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <User size={18} />
              </div>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Masukkan email atau username"
                className="w-full pl-10 pr-4 py-2.5 bg-[#334155] border border-transparent focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-lg text-sm text-white placeholder-slate-500 transition-all outline-none"
              />
            </div>
          </div>

          {/* Password Input */}
          <div className="space-y-1">
            <label className="block text-xs text-slate-300 font-medium ml-1">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <Lock size={18} />
              </div>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Masukkan password"
                className="w-full pl-10 pr-10 py-2.5 bg-[#334155] border border-transparent focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-lg text-sm text-white placeholder-slate-500 transition-all outline-none"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white transition-colors cursor-pointer"
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          {/* Options: Remember Me & Forgot Password */}
          <div className="flex items-center justify-between pt-2">
            <label className="flex items-center space-x-2 cursor-pointer group">
              <div className="relative flex items-center">
                <input
                  type="checkbox"
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleChange}
                  className="peer h-4 w-4 rounded border-slate-500 bg-transparent text-cyan-500 focus:ring-offset-0 focus:ring-0 cursor-pointer"
                />
              </div>
              <span className="text-xs text-slate-400 group-hover:text-slate-300 transition-colors">Ingat saya</span>
            </label>
            <a href="#" className="text-xs text-cyan-500 hover:text-cyan-400 transition-colors">Lupa password?</a>
          </div>

          {error && (
            <p className="text-sm text-red-400 bg-red-900/30 px-3 py-2 rounded-lg">{error}</p>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full text-white font-medium py-2.5 rounded-lg transition-all duration-200 mt-6 shadow-lg flex justify-center items-center ${
              isLoading 
              ? 'bg-slate-500 cursor-not-allowed shadow-none' 
              : 'bg-[#14B8A6] hover:bg-[#0D9488] shadow-teal-900/20'
            }`}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sedang Memuat...
              </>
            ) : (
              'Masuk ke Dashboard'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
