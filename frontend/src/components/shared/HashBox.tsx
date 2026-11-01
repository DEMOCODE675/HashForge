import React, { useState } from 'react';
import { Copy, Check, Download, Layers, ShieldCheck } from 'lucide-react';
import { copyToClipboard } from '../../lib/utils';
import { StatusBadge } from './StatusBadge';

interface HashBoxProps {
  algorithm: string;
  hexDigest: string;
  binaryDigest?: string;
  formattedHex?: string;
  executionTimeMs?: number;
  inputLengthBytes?: number;
  label?: string;
}

export const HashBox: React.FC<HashBoxProps> = ({
  algorithm,
  hexDigest,
  binaryDigest,
  formattedHex,
  executionTimeMs,
  inputLengthBytes,
  label = 'Cryptographic Digest',
}) => {
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'hex' | 'chunked' | 'binary'>('hex');

  const handleCopy = async () => {
    const textToCopy =
      viewMode === 'binary' && binaryDigest
        ? binaryDigest
        : viewMode === 'chunked' && formattedHex
        ? formattedHex
        : hexDigest;

    const success = await copyToClipboard(textToCopy);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const content = `HashForge Cryptographic Output\nAlgorithm: ${algorithm.toUpperCase()}\nHex: ${hexDigest}\nBinary: ${binaryDigest || 'N/A'}\nLatency: ${executionTimeMs ?? 'N/A'} ms\n`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `hashforge_${algorithm.toLowerCase()}_digest.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const isSha3 = algorithm.toLowerCase().includes('3');

  return (
    <div className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          <ShieldCheck className={isSha3 ? 'w-5 h-5 text-accent-emerald' : 'w-5 h-5 text-accent-cyan'} />
          <div>
            <h3 className="text-sm font-semibold text-text-primary">{label}</h3>
            <p className="text-xs text-text-muted">256 Bits • 32 Bytes • FIPS Standard</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <StatusBadge variant={isSha3 ? 'emerald' : 'cyan'}>
            {algorithm.toUpperCase()}
          </StatusBadge>

          <div className="inline-flex rounded-lg border border-border-subtle p-0.5 bg-bg-elevated text-xs">
            <button
              type="button"
              onClick={() => setViewMode('hex')}
              className={`px-2.5 py-1.5 rounded-md font-medium transition-colors min-h-[30px] ${
                viewMode === 'hex' ? 'bg-bg-card text-accent-cyan' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Hex
            </button>
            <button
              type="button"
              onClick={() => setViewMode('chunked')}
              className={`px-2.5 py-1.5 rounded-md font-medium transition-colors min-h-[30px] ${
                viewMode === 'chunked' ? 'bg-bg-card text-accent-cyan' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Chunked
            </button>
            {binaryDigest && (
              <button
                type="button"
                onClick={() => setViewMode('binary')}
                className={`px-2.5 py-1.5 rounded-md font-medium transition-colors min-h-[30px] ${
                  viewMode === 'binary' ? 'bg-bg-card text-accent-cyan' : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                Binary
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="relative group bg-[#070A10] border border-border-subtle rounded-lg p-4 font-mono-code text-sm break-all leading-relaxed">
        <div className="text-text-primary select-all">
          {viewMode === 'binary' && binaryDigest ? (
            <span className="text-xs text-accent-cyan/90">{binaryDigest}</span>
          ) : viewMode === 'chunked' && formattedHex ? (
            <span className="text-accent-cyan tracking-wide">{formattedHex}</span>
          ) : (
            <span className="text-text-primary">{hexDigest}</span>
          )}
        </div>

        <div className="flex flex-wrap items-center justify-between sm:justify-end gap-2 mt-3 pt-3 border-t border-border-subtle/50">
          <button
            type="button"
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium text-text-secondary bg-bg-elevated hover:bg-bg-card hover:text-text-primary border border-border-subtle transition-all min-h-[36px]"
            title="Copy digest to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-accent-emerald" />
                <span className="text-accent-emerald">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy</span>
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handleDownload}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium text-text-secondary bg-bg-elevated hover:bg-bg-card hover:text-text-primary border border-border-subtle transition-all min-h-[36px]"
            title="Download digest as text file"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {(executionTimeMs !== undefined || inputLengthBytes !== undefined) && (
        <div className="flex flex-wrap items-center justify-between gap-1 text-xs text-text-muted mt-3 font-mono-code">
          {inputLengthBytes !== undefined && (
            <span>Input Size: <strong className="text-text-secondary">{inputLengthBytes} bytes</strong></span>
          )}
          {executionTimeMs !== undefined && (
            <span>Latency: <strong className="text-accent-cyan">{executionTimeMs.toFixed(4)} ms</strong></span>
          )}
        </div>
      )}
    </div>
  );
};

