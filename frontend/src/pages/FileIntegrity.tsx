import React, { useState } from 'react';
import {
  FileCheck,
  Upload,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  FileText,
  RefreshCw,
  Copy,
  Check,
  Download,
} from 'lucide-react';
import { api } from '../services/api';
import { FileHashResponse, FileCompareResponse } from '../types';
import { copyToClipboard } from '../lib/utils';
import { StatusBadge } from '../components/shared/StatusBadge';

export const FileIntegrity: React.FC = () => {
  const [mode, setMode] = useState<'single' | 'two-file' | 'reference'>('single');
  const [fileA, setFileA] = useState<File | null>(null);
  const [fileB, setFileB] = useState<File | null>(null);
  const [referenceHash, setReferenceHash] = useState('');

  const [singleReport, setSingleReport] = useState<FileHashResponse | null>(null);
  const [compareReport, setCompareReport] = useState<FileCompareResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copiedSha256, setCopiedSha256] = useState(false);

  const handleSingleHash = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.hashFile(file);
      setSingleReport(res);
    } catch (err: any) {
      setError(err?.message || 'File hashing failed');
    } finally {
      setLoading(false);
    }
  };

  const handleCompare = async () => {
    if (!fileA) {
      setError('Please select at least the primary file (File A).');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (mode === 'two-file') {
        if (!fileB) {
          setError('Please select a second file to compare.');
          return;
        }
        const res = await api.compareFiles(fileA, fileB, null);
        setCompareReport(res);
      } else if (mode === 'reference') {
        if (!referenceHash.trim()) {
          setError('Please provide a vendor reference hash string.');
          return;
        }
        const res = await api.compareFiles(fileA, null, referenceHash.trim());
        setCompareReport(res);
      }
    } catch (err: any) {
      setError(err?.message || 'File comparison failed');
    } finally {
      setLoading(false);
    }
  };

  const copyDigest = async (text: string) => {
    const ok = await copyToClipboard(text);
    if (ok) {
      setCopiedSha256(true);
      setTimeout(() => setCopiedSha256(false), 2000);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <FileCheck className="w-5 h-5 text-accent-emerald" />
            <h1 className="text-xl font-bold text-text-primary">Module 6: File Integrity Laboratory</h1>
          </div>
          <p className="text-xs text-text-muted">
            Memory-safe 64KB streaming file hashing to detect single-byte corruption and verify vendor checksums.
          </p>
        </div>

        <StatusBadge variant="emerald" icon="shield">Streaming 64KB Buffer</StatusBadge>
      </div>

      {/* Mode Selector Tabs */}
      <div className="flex flex-wrap sm:flex-nowrap items-center gap-2 border-b border-border-subtle pb-2">
        <button
          type="button"
          onClick={() => {
            setMode('single');
            setError(null);
          }}
          className={`flex-1 sm:flex-none justify-center px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] text-center ${
            mode === 'single'
              ? 'bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/40 shadow-cyan-glow'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
          }`}
        >
          Single File Fingerprint
        </button>

        <button
          type="button"
          onClick={() => {
            setMode('two-file');
            setError(null);
          }}
          className={`flex-1 sm:flex-none justify-center px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] text-center ${
            mode === 'two-file'
              ? 'bg-accent-emerald/15 text-accent-emerald border border-accent-emerald/40'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
          }`}
        >
          Two-File Parity Comparison
        </button>

        <button
          type="button"
          onClick={() => {
            setMode('reference');
            setError(null);
          }}
          className={`flex-1 sm:flex-none justify-center px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] text-center ${
            mode === 'reference'
              ? 'bg-accent-amber/15 text-accent-amber border border-accent-amber/40'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
          }`}
        >
          Vendor Reference Hash
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Mode 1: Single File Fingerprinting */}
      {mode === 'single' && (
        <div className="space-y-6">
          <div className="bg-bg-card border-2 border-dashed border-border-subtle hover:border-accent-cyan/50 rounded-xl p-8 text-center transition-all cursor-pointer">
            <input
              type="file"
              id="single-file-input"
              className="hidden"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  const f = e.target.files[0];
                  setFileA(f);
                  handleSingleHash(f);
                }
              }}
            />
            <label htmlFor="single-file-input" className="cursor-pointer block">
              <Upload className="w-8 h-8 text-accent-cyan mx-auto mb-3" />
              <div className="text-sm font-bold text-text-primary mb-1">
                {fileA ? fileA.name : 'Select or drop a file to calculate cryptographic fingerprints'}
              </div>
              <div className="text-xs text-text-muted">
                Max 50MB • Processed purely in volatile memory via 64KB streaming chunks
              </div>
            </label>
          </div>

          {singleReport && (
            <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-border-subtle">
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-accent-cyan" />
                  <div>
                    <h3 className="text-sm font-bold text-text-primary">{singleReport.file_name}</h3>
                    <p className="text-xs text-text-muted">
                      {singleReport.formatted_size} ({singleReport.file_size_bytes.toLocaleString()} bytes) •{' '}
                      {singleReport.chunks_processed} chunks streamed in {singleReport.hashing_duration_ms} ms
                    </p>
                  </div>
                </div>

                <StatusBadge variant="emerald" icon="check">Fingerprints Computed</StatusBadge>
              </div>

              <div className="space-y-3 font-mono-code text-xs">
                <div className="bg-[#070A10] border border-border-subtle rounded-lg p-3">
                  <div className="text-[11px] text-text-muted mb-1 flex items-center justify-between">
                    <span>SHA-256 Fingerprint:</span>
                    <button
                      type="button"
                      onClick={() => copyDigest(singleReport.sha256_hex)}
                      className="text-accent-cyan hover:underline inline-flex items-center gap-1"
                    >
                      {copiedSha256 ? <Check className="w-3 h-3 text-accent-emerald" /> : <Copy className="w-3 h-3" />}
                      <span>{copiedSha256 ? 'Copied' : 'Copy'}</span>
                    </button>
                  </div>
                  <div className="text-accent-cyan break-all">{singleReport.sha256_hex}</div>
                </div>

                <div className="bg-[#070A10] border border-border-subtle rounded-lg p-3">
                  <div className="text-[11px] text-text-muted mb-1">SHA3-256 Fingerprint:</div>
                  <div className="text-accent-emerald break-all">{singleReport.sha3_256_hex}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Mode 2: Two File Parity */}
      {mode === 'two-file' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-bg-card border-2 border-dashed border-border-subtle rounded-xl p-6 text-center cursor-pointer">
              <input
                type="file"
                id="file-a-input"
                className="hidden"
                onChange={(e) => e.target.files && setFileA(e.target.files[0])}
              />
              <label htmlFor="file-a-input" className="cursor-pointer block">
                <Upload className="w-6 h-6 text-accent-cyan mx-auto mb-2" />
                <div className="text-xs font-bold text-text-primary truncate">
                  {fileA ? fileA.name : 'Select File A (Baseline)'}
                </div>
              </label>
            </div>

            <div className="bg-bg-card border-2 border-dashed border-border-subtle rounded-xl p-6 text-center cursor-pointer">
              <input
                type="file"
                id="file-b-input"
                className="hidden"
                onChange={(e) => e.target.files && setFileB(e.target.files[0])}
              />
              <label htmlFor="file-b-input" className="cursor-pointer block">
                <Upload className="w-6 h-6 text-accent-emerald mx-auto mb-2" />
                <div className="text-xs font-bold text-text-primary truncate">
                  {fileB ? fileB.name : 'Select File B (Suspect / Modified)'}
                </div>
              </label>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={handleCompare}
              disabled={loading || !fileA || !fileB}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg bg-accent-emerald hover:bg-accent-emerald/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-cyan-glow disabled:opacity-50 min-h-[44px]"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>{loading ? 'Comparing...' : 'Compare File Fingerprints'}</span>
            </button>
          </div>

          {compareReport && (
            <div className="space-y-4">
              <div
                className={`p-4 rounded-xl border flex items-center gap-3 ${
                  compareReport.is_identical
                    ? 'bg-accent-emerald/10 border-accent-emerald/30 text-accent-emerald'
                    : 'bg-accent-rose/10 border-accent-rose/30 text-accent-rose'
                }`}
              >
                {compareReport.is_identical ? (
                  <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                )}
                <div>
                  <h4 className="text-sm font-bold">
                    {compareReport.is_identical ? 'INTEGRITY VERIFIED — IDENTICAL CONTENT' : 'TAMPERING DETECTED — MISMATCHED CONTENT'}
                  </h4>
                  <p className="text-xs text-text-secondary mt-0.5">{compareReport.details}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div className="bg-bg-card border border-border-subtle rounded-xl p-4 font-mono-code text-xs space-y-2">
                  <div className="text-text-primary font-bold">File A: {compareReport.file_a.file_name}</div>
                  <div className="text-text-muted">Size: {compareReport.file_a.formatted_size}</div>
                  <div className="text-accent-cyan break-all">SHA-256: {compareReport.file_a.sha256_hex}</div>
                </div>

                {compareReport.file_b && (
                  <div className="bg-bg-card border border-border-subtle rounded-xl p-4 font-mono-code text-xs space-y-2">
                    <div className="text-text-primary font-bold">File B: {compareReport.file_b.file_name}</div>
                    <div className="text-text-muted">Size: {compareReport.file_b.formatted_size}</div>
                    <div className="text-accent-emerald break-all">SHA-256: {compareReport.file_b.sha256_hex}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Mode 3: Reference Hash Validation */}
      {mode === 'reference' && (
        <div className="space-y-6">
          <div className="bg-bg-card border-2 border-dashed border-border-subtle rounded-xl p-6 text-center cursor-pointer">
            <input
              type="file"
              id="ref-file-input"
              className="hidden"
              onChange={(e) => e.target.files && setFileA(e.target.files[0])}
            />
            <label htmlFor="ref-file-input" className="cursor-pointer block">
              <Upload className="w-6 h-6 text-accent-cyan mx-auto mb-2" />
              <div className="text-xs font-bold text-text-primary truncate">
                {fileA ? fileA.name : 'Select Downloaded File to Verify'}
              </div>
            </label>
          </div>

          <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-2">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider block">
              Official Vendor Reference Hash (Hexadecimal Checksum)
            </label>
            <input
              type="text"
              value={referenceHash}
              onChange={(e) => setReferenceHash(e.target.value)}
              placeholder="Paste 64-character SHA-256 or SHA3-256 vendor checksum..."
              className="w-full bg-[#070A10] border border-border-subtle rounded-lg px-4 py-2.5 text-xs text-text-primary font-mono-code focus:outline-none focus:border-accent-cyan"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={handleCompare}
              disabled={loading || !fileA || !referenceHash.trim()}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg bg-accent-amber hover:bg-accent-amber/90 text-bg-primary font-semibold text-xs tracking-wider uppercase transition-all shadow-amber-glow disabled:opacity-50 min-h-[44px]"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>{loading ? 'Verifying...' : 'Validate Against Checksum'}</span>
            </button>
          </div>

          {compareReport && (
            <div
              className={`p-4 rounded-xl border flex items-center gap-3 ${
                compareReport.is_identical
                  ? 'bg-accent-emerald/10 border-accent-emerald/30 text-accent-emerald'
                  : 'bg-accent-rose/10 border-accent-rose/30 text-accent-rose'
              }`}
            >
              {compareReport.is_identical ? (
                <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
              ) : (
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
              )}
              <div>
                <h4 className="text-sm font-bold">
                  {compareReport.is_identical ? 'AUTHENTICITY MATCH — CHECKSUM VERIFIED' : 'INTEGRITY MISMATCH — UNVERIFIED FILE'}
                </h4>
                <p className="text-xs text-text-secondary mt-0.5">{compareReport.details}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

