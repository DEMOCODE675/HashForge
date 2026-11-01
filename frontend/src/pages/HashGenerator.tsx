import React, { useState, useEffect } from 'react';
import {
  Fingerprint,
  RefreshCw,
  Trash2,
  FileText,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
} from 'lucide-react';
import { api } from '../services/api';
import { HashResponse } from '../types';
import { HashBox } from '../components/shared/HashBox';
import { StatusBadge } from '../components/shared/StatusBadge';

export const HashGenerator: React.FC = () => {
  const [inputText, setInputText] = useState('HashForge Cryptographic Laboratory 2026');
  const [activeTab, setActiveTab] = useState<'sha256' | 'sha3_256'>('sha256');
  const [sha256Result, setSha256Result] = useState<HashResponse | null>(null);
  const [sha3Result, setSha3Result] = useState<HashResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const computeHashes = async (text: string) => {
    setLoading(true);
    setError(null);
    try {
      const [res2, res3] = await Promise.all([
        api.generateHash(text, 'sha256'),
        api.generateHash(text, 'sha3_256'),
      ]);
      setSha256Result(res2);
      setSha3Result(res3);
    } catch (err: any) {
      setError(err?.message || 'Failed to compute hash');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    computeHashes(inputText);
  }, []);

  const handleClear = () => {
    setInputText('');
    computeHashes('');
  };

  const handleLoadSample = () => {
    const sample = 'The quick brown fox jumps over the lazy dog';
    setInputText(sample);
    computeHashes(sample);
  };

  const byteLength = new TextEncoder().encode(inputText).length;
  const bitLength = byteLength * 8;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Fingerprint className="w-5 h-5 text-accent-cyan" />
            <h1 className="text-xl font-bold text-text-primary">Module 1: Hash Generator Laboratory</h1>
          </div>
          <p className="text-xs text-text-muted">
            Compute deterministic SHA-256 and SHA3-256 cryptographic digests with byte inspection.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleLoadSample}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-bg-card hover:bg-bg-elevated border border-border-subtle text-xs text-text-secondary hover:text-text-primary transition-colors"
          >
            <FileText className="w-3.5 h-3.5 text-accent-cyan" />
            <span>NIST Fox Vector</span>
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-bg-card hover:bg-bg-elevated border border-border-subtle text-xs text-text-secondary hover:text-accent-rose transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Input</span>
          </button>
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
            Plaintext / UTF-8 Input String
          </label>
          <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs text-text-muted font-mono-code">
            <span>Length: <strong className="text-text-primary">{inputText.length}</strong> chars</span>
            <span>Bytes: <strong className="text-accent-cyan">{byteLength}</strong></span>
            <span>Bits: <strong className="text-accent-emerald">{bitLength}</strong></span>
          </div>
        </div>

        <textarea
          rows={4}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type or paste input data here (empty string is a cryptographically valid test vector)..."
          className="w-full bg-[#070A10] border border-border-subtle rounded-lg p-3 text-xs text-text-primary font-mono-code placeholder:text-text-muted focus:outline-none focus:border-accent-cyan transition-colors resize-y leading-relaxed"
        />

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1">
          <span className="text-[11px] text-text-muted">
            UTF-8 encoded • FIPS 180-4 / FIPS 202 standards
          </span>
          <button
            type="button"
            onClick={() => computeHashes(inputText)}
            disabled={loading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow min-h-[44px]"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Computing...' : 'Recalculate Digests'}</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Algorithm Output Tabs */}
      <div className="space-y-4">
        <div className="flex flex-wrap sm:flex-nowrap items-center gap-2 border-b border-border-subtle pb-2">
          <button
            type="button"
            onClick={() => setActiveTab('sha256')}
            className={`flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] ${
              activeTab === 'sha256'
                ? 'bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/40 shadow-cyan-glow'
                : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>SHA-256 (SHA-2 Family)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('sha3_256')}
            className={`flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] ${
              activeTab === 'sha3_256'
                ? 'bg-accent-emerald/15 text-accent-emerald border border-accent-emerald/40'
                : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>SHA3-256 (Keccak Family)</span>
          </button>
        </div>

        {activeTab === 'sha256' && sha256Result && (
          <HashBox
            algorithm="sha256"
            hexDigest={sha256Result.hex_digest}
            binaryDigest={sha256Result.binary_digest}
            formattedHex={sha256Result.formatted_hex}
            executionTimeMs={sha256Result.execution_time_ms}
            inputLengthBytes={sha256Result.input_length_bytes}
            label="SHA-256 Cryptographic Digest (FIPS 180-4)"
          />
        )}

        {activeTab === 'sha3_256' && sha3Result && (
          <HashBox
            algorithm="sha3_256"
            hexDigest={sha3Result.hex_digest}
            binaryDigest={sha3Result.binary_digest}
            formattedHex={sha3Result.formatted_hex}
            executionTimeMs={sha3Result.execution_time_ms}
            inputLengthBytes={sha3Result.input_length_bytes}
            label="SHA3-256 Cryptographic Digest (FIPS 202)"
          />
        )}
      </div>
    </div>
  );
};

