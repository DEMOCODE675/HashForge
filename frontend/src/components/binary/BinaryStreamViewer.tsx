import React from 'react';
import { cn } from '../../lib/utils';
import { Binary, ArrowRight } from 'lucide-react';

interface BinaryStreamViewerProps {
  originalBytesHex: string;
  modifiedBytesHex?: string;
  originalBinary: string;
  modifiedBinary?: string;
  flippedIndices?: number[];
  className?: string;
}

export const BinaryStreamViewer: React.FC<BinaryStreamViewerProps> = ({
  originalBytesHex,
  modifiedBytesHex,
  originalBinary,
  modifiedBinary,
  flippedIndices = [],
  className,
}) => {
  // Break binary into 8-bit groups (bytes)
  const groupBits = (bin: string) => {
    const groups: string[] = [];
    for (let i = 0; i < bin.length; i += 8) {
      groups.push(bin.slice(i, i + 8));
    }
    return groups;
  };

  const origGroups = groupBits(originalBinary);
  const modGroups = modifiedBinary ? groupBits(modifiedBinary) : [];

  return (
    <div className={cn('bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card', className)}>
      <div className="flex items-center gap-2 mb-4">
        <Binary className="w-5 h-5 text-accent-cyan" />
        <h3 className="text-sm font-semibold text-text-primary">Input Bitstream & Byte Representation</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Original Input */}
        <div className="bg-[#070A10] border border-border-subtle rounded-lg p-4 font-mono-code text-xs">
          <div className="text-text-secondary font-semibold mb-2 flex items-center justify-between">
            <span>Original Input Bytes</span>
            <span className="text-[11px] text-accent-cyan font-normal">{originalBinary.length} Bits</span>
          </div>

          <div className="text-text-muted mb-2 break-all">
            Hex: <span className="text-text-primary font-bold">{originalBytesHex}</span>
          </div>

          <div className="flex flex-wrap gap-1.5 leading-relaxed">
            {origGroups.map((byteStr, bIdx) => (
              <span
                key={bIdx}
                className="px-1.5 py-0.5 rounded bg-bg-elevated/80 border border-border-subtle text-text-primary"
                title={`Byte #${bIdx}`}
              >
                {byteStr}
              </span>
            ))}
          </div>
        </div>

        {/* Modified Input (if present) */}
        {modifiedBinary && (
          <div className="bg-[#070A10] border border-border-subtle rounded-lg p-4 font-mono-code text-xs">
            <div className="text-text-secondary font-semibold mb-2 flex items-center justify-between">
              <span>Modified Input (After XOR Flip)</span>
              <span className="text-[11px] text-accent-amber font-normal">
                {flippedIndices.length} Flipped {flippedIndices.length === 1 ? 'Bit' : 'Bits'}
              </span>
            </div>

            <div className="text-text-muted mb-2 break-all">
              Hex: <span className="text-accent-amber font-bold">{modifiedBytesHex}</span>
            </div>

            <div className="flex flex-wrap gap-1.5 leading-relaxed">
              {modGroups.map((byteStr, bIdx) => {
                const byteStart = bIdx * 8;
                const hasFlippedBit = flippedIndices.some(
                  (idx) => idx >= byteStart && idx < byteStart + 8
                );

                return (
                  <span
                    key={bIdx}
                    className={cn(
                      'px-1.5 py-0.5 rounded border',
                      hasFlippedBit
                        ? 'bg-accent-amber/20 border-accent-amber text-accent-amber font-bold'
                        : 'bg-bg-elevated/80 border-border-subtle text-text-primary'
                    )}
                    title={`Byte #${bIdx}${hasFlippedBit ? ' (Contains Inverted Bit)' : ''}`}
                  >
                    {byteStr}
                  </span>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

