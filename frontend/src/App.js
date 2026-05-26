import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';
import {
  Shield, Upload, FileCode, AlertTriangle, CheckCircle,
  Database, Eye, Zap, TrendingUp, Lock,
  Sun, Moon, ChevronRight
} from 'lucide-react';

// LIVE BACKEND URL - DO NOT CHANGE
const API_URL = 'https://chainguard-ai-backend.onrender.com';

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [contracts, setContracts] = useState([]);
  const [darkMode, setDarkMode] = useState(true);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { '.sol': [] },
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
      toast.success(`${acceptedFiles[0].name} ready!`);
    },
  });

  const uploadContract = async () => {
    if (!file) {
      toast.error('Please select a .sol file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const res = await axios.post(`${API_URL}/api/upload`, formData);
      toast.success('Contract analyzed!');
      setResult(res.data.analysis);
      fetchContracts();
    } catch (err) {
      toast.error('Upload failed');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const fetchContracts = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/contracts`);
      setContracts(res.data);
    } catch (err) {
      console.error('Failed to fetch contracts');
    }
  };

  useEffect(() => {
    fetchContracts();
  }, []);

  const getRiskColor = (score) => {
    if (score >= 70) return 'text-red-400 border-red-400';
    if (score >= 40) return 'text-yellow-400 border-yellow-400';
    return 'text-green-400 border-green-400';
  };

  const getRiskBg = (score) => {
    if (score >= 70) return 'bg-red-500/20';
    if (score >= 40) return 'bg-yellow-500/20';
    return 'bg-green-500/20';
  };

  const getSeverityColor = (severity) => {
    if (severity === 'High') return 'text-red-400';
    if (severity === 'Medium') return 'text-yellow-400';
    return 'text-blue-400';
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-black' : 'bg-gray-100'} transition-colors duration-300`}>
      <Toaster position="top-right" />

      {/* Navbar */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className={`sticky top-0 z-50 ${darkMode ? 'bg-black/80 border-gray-800' : 'bg-white/80 border-gray-200'} backdrop-blur-xl border-b`}
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center gap-2 cursor-pointer"
            >
              <Shield className={`w-7 h-7 ${darkMode ? 'text-white' : 'text-black'}`} />
              <span className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-black'}`}>
                ChainGuard AI
              </span>
            </motion.div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-lg ${darkMode ? 'bg-gray-800 text-yellow-400' : 'bg-gray-200 text-gray-800'}`}
              >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                AI-Powered Security
              </span>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <Shield className={`w-16 h-16 mx-auto mb-4 ${darkMode ? 'text-white/80' : 'text-gray-800'}`} />
          <h1 className={`text-4xl md:text-6xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Smart Contract Security
          </h1>
          <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-2xl mx-auto`}>
            AI-powered vulnerability detection for Solidity smart contracts.
            Upload your contract and get instant security insights.
          </p>
        </motion.div>

        {/* Stats Row */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12"
        >
          {[
            { icon: <AlertTriangle className="w-5 h-5" />, label: 'Vulnerabilities', value: result?.total_issues || '0', color: 'from-red-500 to-orange-500' },
            { icon: <Zap className="w-5 h-5" />, label: 'Risk Score', value: result?.risk_score || '0', color: 'from-yellow-500 to-orange-500' },
            { icon: <Lock className="w-5 h-5" />, label: 'Issues Found', value: result?.summary ? result.summary.high + result.summary.medium + result.summary.low : '0', color: 'from-green-500 to-emerald-500' },
            { icon: <TrendingUp className="w-5 h-5" />, label: 'Contracts', value: contracts.length, color: 'from-blue-500 to-cyan-500' },
          ].map((stat, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.05, y: -5 }}
              className={`${darkMode ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-200 shadow-lg'} rounded-xl p-4 text-center border`}
            >
              <div className={`flex justify-center mb-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>{stat.icon}</div>
              <div className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{stat.value}</div>
              <div className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all
                ${isDragActive ? 'border-purple-500 bg-purple-500/10' : darkMode ? 'border-gray-700 hover:border-gray-500' : 'border-gray-300 hover:border-gray-400'}
                ${darkMode ? 'bg-gray-900/50' : 'bg-gray-50'}
              `}
            >
              <input {...getInputProps()} />
              <Upload className={`w-12 h-12 mx-auto mb-4 ${isDragActive ? 'text-purple-500' : darkMode ? 'text-gray-500' : 'text-gray-400'}`} />
              {file ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-center gap-2 text-green-500">
                    <FileCode className="w-5 h-5" />
                    <p>{file.name}</p>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); uploadContract(); }}
                    disabled={uploading}
                    className="px-6 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-all disabled:opacity-50"
                  >
                    {uploading ? 'Analyzing...' : 'Analyze Contract'}
                  </button>
                </div>
              ) : (
                <div>
                  <p className={`mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {isDragActive ? 'Drop your .sol file here' : 'Drag & drop .sol file here'}
                  </p>
                  <p className={`text-sm ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>or click to browse</p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Risk Score Gauge */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            className={`${darkMode ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-200 shadow-lg'} rounded-2xl p-6 border`}
          >
            <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Risk Assessment</h3>
            {result ? (
              <div className="text-center">
                <div className="relative w-40 h-40 mx-auto mb-4">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="80" cy="80" r="70" stroke={darkMode ? "#1f2937" : "#e5e7eb"} strokeWidth="12" fill="none" />
                    <circle
                      cx="80" cy="80" r="70"
                      stroke={result.risk_score >= 70 ? '#ef4444' : result.risk_score >= 40 ? '#eab308' : '#22c55e'}
                      strokeWidth="12"
                      fill="none"
                      strokeDasharray={`${(result.risk_score / 100) * 440} 440`}
                      className="transition-all duration-1000"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{result.risk_score}</span>
                    <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>/100</span>
                  </div>
                </div>
                <div className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getRiskBg(result.risk_score)} ${getRiskColor(result.risk_score)} border`}>
                  {result.risk_level} Risk
                </div>
              </div>
            ) : (
              <div className={`text-center py-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                <Eye className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Upload a contract to see risk score</p>
              </div>
            )}
          </motion.div>
        </div>

        {/* Vulnerabilities Section */}
        <AnimatePresence>
          {result && result.vulnerabilities && result.vulnerabilities.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8"
            >
              <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Detected Vulnerabilities ({result.vulnerabilities.length})
              </h3>
              <div className="space-y-4">
                {result.vulnerabilities.map((vuln, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className={`${darkMode ? 'bg-gray-900/50 border-gray-800' : 'bg-white border-gray-200'} rounded-xl p-5 border`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className={`w-5 h-5 ${getSeverityColor(vuln.severity)}`} />
                        <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{vuln.type}</h4>
                        <span className={`text-xs px-2 py-1 rounded-full ${getRiskBg(vuln.severity === 'High' ? 80 : vuln.severity === 'Medium' ? 50 : 10)} ${getRiskColor(vuln.severity === 'High' ? 80 : vuln.severity === 'Medium' ? 50 : 10)} border`}>
                          {vuln.severity}
                        </span>
                      </div>
                    </div>
                    <p className={`text-sm mb-3 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>{vuln.explanation}</p>
                    <div className={`text-sm p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-gray-100'}`}>
                      <p className={`font-mono text-xs ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                        <strong>Fix:</strong> {vuln.fix_example}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Optimization Tips */}
        <AnimatePresence>
          {result && result.optimization_tips && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8"
            >
              <div className={`${darkMode ? 'bg-blue-900/20 border-blue-800' : 'bg-blue-50 border-blue-200'} rounded-xl p-5 border`}>
                <div className="flex items-center gap-2 mb-3">
                  <Zap className="w-5 h-5 text-blue-400" />
                  <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Optimization Tips</h3>
                </div>
                <ul className="space-y-2">
                  {result.optimization_tips.map((tip, idx) => (
                    <li key={idx} className={`text-sm flex items-start gap-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      <ChevronRight className="w-4 h-4 text-blue-400 mt-0.5" />
                      {tip}
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Recent Contracts */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mt-12"
        >
          <div className="flex items-center gap-2 mb-4">
            <Database className="w-5 h-5 text-purple-400" />
            <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Audit History</h3>
          </div>
          <div className="space-y-2">
            {contracts.slice().reverse().map((contract) => (
              <motion.div
                key={contract.id}
                whileHover={{ scale: 1.01 }}
                className={`${darkMode ? 'bg-gray-900/50 border-gray-800' : 'bg-white border-gray-200'} rounded-lg p-3 flex justify-between items-center cursor-pointer border transition-all`}
              >
                <div className="flex items-center gap-3">
                  <FileCode className={`w-4 h-4 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} />
                  <div>
                    <p className={`text-sm font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>{contract.filename}</p>
                    <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                      {new Date(contract.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className={`text-xs px-2 py-1 rounded-full ${getRiskBg(contract.risk_score || 0)} ${getRiskColor(contract.risk_score || 0)} border`}>
                  Score: {contract.risk_score || 'N/A'}
                </div>
              </motion.div>
            ))}
            {contracts.length === 0 && (
              <div className={`text-center py-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                <Eye className="w-8 h-8 mx-auto mb-2 opacity-30" />
                No contracts yet. Upload your first .sol file.
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default App;