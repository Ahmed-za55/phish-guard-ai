import React, { useState } from 'react';
import axios from 'axios';
import { 
  ShieldAlert, ShieldCheck, Terminal, Cpu, Zap, Activity, 
  Lock, Globe, Database, Network, Eye, Layers 
} from 'lucide-react';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const analyzeThreat = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/analyze', {
        text: inputText
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert('Sovereign Backend Link Error. Ensure backend v53 is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-cyan-400 font-mono p-6 selection:bg-cyan-500 selection:text-black">
      {/* Header */}
      <header className="border-b border-cyan-500/30 pb-4 mb-6 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <Cpu className="w-8 h-8 text-cyan-400 animate-pulse" />
          <div>
            <h1 className="text-2xl font-bold tracking-widest text-cyan-300">PHISHGUARD AI <span className="text-xs bg-cyan-950 border border-cyan-500 px-2 py-0.5 rounded text-cyan-400">v53 GENESIS-SWARM</span></h1>
            <p className="text-xs text-slate-400">100+ Sovereign Cores | Dynamic Genesis & Red-Team Swarm Active</p>
          </div>
        </div>
        <div className="flex items-center space-x-4 text-xs">
          <span className="flex items-center bg-emerald-950 border border-emerald-500/50 text-emerald-400 px-3 py-1 rounded-full">
            <Activity className="w-3 h-3 mr-1.5 animate-spin" /> Mesh Quantum Synced
          </span>
          <span className="flex items-center bg-cyan-950/50 border border-cyan-500/50 text-cyan-300 px-3 py-1 rounded">
            <Lock className="w-3 h-3 mr-1.5" /> ML-DSA / FHE Locked
          </span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Input & Controls */}
        <div className="lg:col-span-1 bg-slate-900/60 border border-cyan-500/30 rounded-xl p-5 backdrop-blur-md flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-cyan-300 mb-3 flex items-center">
              <Terminal className="w-4 h-4 mr-2" /> Threat Telemetry Ingestion
            </h2>
            <textarea
              className="w-full h-44 bg-slate-950 border border-cyan-500/30 rounded-lg p-3 text-cyan-300 text-sm focus:outline-none focus:border-cyan-400 resize-none placeholder-slate-600"
              placeholder="Paste suspicious payload, email body, URL, or adversarial prompt vector here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
          </div>
          <button
            onClick={analyzeThreat}
            disabled={loading}
            className="mt-4 w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center space-x-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50"
          >
            {loading ? (
              <>
                <Activity className="w-5 h-5 animate-spin" />
                <span>Executing 100+ Core Mesh...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>Initialize Sovereign Scan</span>
              </>
            )}
          </button>
        </div>

        {/* Right Columns: Analysis & Telemetry Dashboard */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Quick Metrics Banner */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-slate-900/60 border border-cyan-500/30 p-4 rounded-xl">
              <div className="text-slate-400 text-xs flex items-center"><Network className="w-3.5 h-3.5 mr-1 text-cyan-400" /> Active Cores</div>
              <div className="text-2xl font-bold text-cyan-200 mt-1">100+ <span className="text-xs font-normal text-emerald-400">Gen-Synced</span></div>
            </div>
            <div className="bg-slate-900/60 border border-cyan-500/30 p-4 rounded-xl">
              <div className="text-slate-400 text-xs flex items-center"><ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-400" /> Genesis Status</div>
              <div className="text-2xl font-bold text-emerald-300 mt-1">Autonomous</div>
            </div>
            <div className="bg-slate-900/60 border border-cyan-500/30 p-4 rounded-xl">
              <div className="text-slate-400 text-xs flex items-center"><Layers className="w-3.5 h-3.5 mr-1 text-cyan-400" /> Red-Team Swarm</div>
              <div className="text-2xl font-bold text-cyan-200 mt-1">Hardened</div>
            </div>
          </div>

          {/* Results Display */}
          <div className="bg-slate-900/60 border border-cyan-500/30 rounded-xl p-5 min-h-[320px] flex flex-col justify-between">
            <div>
              <h3 className="text-sm font-semibold text-cyan-300 mb-4 flex items-center">
                <Eye className="w-4 h-4 mr-2" /> Sovereign Intelligence Telemetry
              </h3>

              {!result ? (
                <div className="text-slate-500 text-center py-16 flex flex-col items-center justify-center space-y-2">
                  <Activity className="w-8 h-8 opacity-30 animate-pulse" />
                  <p>Awaiting payload ingestion for multi-dimensional core inspection...</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between bg-slate-950 p-3 rounded-lg border border-cyan-500/20">
                    <span className="text-slate-400 text-xs">Phishing Verdict:</span>
                    <span className={`px-3 py-1 rounded text-xs font-bold ${result.is_phishing ? 'bg-rose-950 text-rose-400 border border-rose-500/50' : 'bg-emerald-950 text-emerald-400 border border-emerald-500/50'}`}>
                      {result.is_phishing ? 'THREAT DETECTED (PHISHING)' : 'SECURE (CLEAN PAYLOAD)'}
                    </span>
                  </div>

                  <div className="bg-slate-950 p-3 rounded-lg border border-cyan-500/20 text-xs space-y-2">
                    <div className="text-cyan-400 font-semibold">Detected Vectors & Evidence:</div>
                    <ul className="list-disc list-inside text-slate-300 space-y-1">
                      {result.threats.map((t, idx) => (
                        <li key={idx} className="text-rose-400">{t}</li>
                      ))}
                      {result.evidence.slice(0, 3).map((e, idx) => (
                        <li key={idx} className="text-slate-400">{e}</li>
                      ))}
                    </ul>
                  </div>

                  {result.cryptographic_warrant && (
                    <div className="bg-slate-950 p-3 rounded-lg border border-cyan-500/20 text-xs space-y-1">
                      <div className="text-cyan-400 font-semibold">Cryptographic Warrant & Genesis Receipt:</div>
                      <div className="text-slate-400 truncate">Signature: {result.cryptographic_warrant.tamper_proof_signature}</div>
                      <div className="text-emerald-400">Status: {result.cryptographic_warrant.status}</div>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="text-right text-[10px] text-slate-600 mt-4 border-t border-slate-800 pt-2">
              PhishGuard AI Apex Sovereign Architecture — 100 Cores Operational
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}