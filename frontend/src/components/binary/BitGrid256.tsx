import React, { useState } from 'react';
import { cn } from '../../lib/utils';
import { Layers, ArrowLeftRight, Eye, EyeOff } from 'lucide-react';

interface BitGrid256Props {
  binaryDigest: string;
  diffMask?: boolean[];
  originalBinaryDigest?: string;
  title?: string;
  className?: string;
}

export const BitGrid256: React.FC<BitGrid256Props> = ({
  binaryDigest,
  diffMask,
  originalBinaryDigest,
  title = '256-Bit Cryptographic Output Grid',
  className,
}) => {
  const [filterMode, setFilterMode] = useState<'all' | 'flipped-only'>('all');
  const [hoveredBit, setHoveredBit] = useState<number | null>(null);

  // Group into 8 rows of 32 bits (4 bytes per row)
  const rows: { rowStart: number; rowEnd: number; bytes: string[] }[] = [];
  const bitsPerRow = 32;
  const bitsPerByte = 8;

  for (let r = 0; r < 256; r += bitsPerRow) {
    const rowEnd = r + bitsPerRow;
    const rowBits = binaryDigest.slice(r, rowEnd);
    const byteGroups: string[] = [];
    for (let b = 0; b < bitsPerRow; b += bitsPerByte) {
      byteGroups.push(rowBits.slice(b, b + bitsPerByte));
    }
    rows.push({ rowStart: r, rowEnd: rowEnd - 1, bytes: byteGroups });
  }

  const changedCount = diffMask ? diffMask.filter(Boolean).length : 0;
  const unchangedCount = 256 - changedCount;
  const avalanchePct = ((changedCount / 256) * 100).toFixed(2);

  return (
    <div className={cn('bg-bg-card border border-border-subtle rounded-xl p-3 sm:p-5 shadow-card', className)}>
      {/* Top Header & Legend */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2.5">
          <Layers className="w-5 h-5 text-accent-cyan flex-shrink-0" />
          <div>
            <h3 className="text-sm font-semibold text-text-primary">{title}</h3>
            <p className="text-xs text-text-muted">8 Rows • 32 Bits per Row • 4 Bytes Grouped</p>
          </div>
        </div>

        {diffMask && (
          <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-accent-amber/30 border border-accent-amber shadow-amber-glow flex-shrink-0" />
              <span className="text-text-secondary">
                Flipped: <strong className="text-accent-amber">{changedCount}</strong> ({avalanchePct}%)
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-bg-elevated border border-border-subtle text-text-muted text-center flex-shrink-0" />
              <span className="text-text-secondary">
                Unchanged: <strong className="text-text-primary">{unchangedCount}</strong>
              </span>
            </div>

            <button
              type="button"
              onClick={() => setFilterMode(filterMode === 'all' ? 'flipped-only' : 'all')}
              className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-bg-elevated hover:bg-bg-card border border-border-subtle text-text-secondary hover:text-text-primary transition-colors text-xs"
            >
              {filterMode === 'all' ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
              <span>{filterMode === 'all' ? 'Focus Flipped' : 'Show All'}</span>
            </button>
          </div>
        )}
      </div>

      {/* Mobile Swipe Hint */}
      <div className="lg:hidden text-[11px] text-accent-cyan/90 bg-accent-cyan/10 border border-accent-cyan/20 px-3 py-1.5 rounded-lg flex items-center gap-2 mb-3">
        <ArrowLeftRight className="w-3.5 h-3.5 flex-shrink-0 text-accent-cyan" />
        <span>Swipe horizontally to view all 32 columns. Tap any bit to inspect.</span>
      </div>

      {/* Bit Grid Matrix */}
      <div className="bg-[#070A10] border border-border-subtle rounded-lg p-2.5 sm:p-4 overflow-x-auto touch-pan-x">
        <div className="min-w-[620px] space-y-2">
          {rows.map((row) => (
            <div key={row.rowStart} className="flex items-center gap-2 sm:gap-3 font-mono-code text-xs">
              <span className="w-20 sm:w-24 text-[10px] sm:text-[11px] text-text-muted select-none flex-shrink-0 sticky left-0 bg-[#070A10] z-10 pr-2 border-r border-border-subtle/50">
                Bits {String(row.rowStart).padStart(3, '0')}–{String(row.rowEnd).padStart(3, '0')}
              </span>

              <div className="flex items-center gap-2 sm:gap-3">
                {row.bytes.map((byteStr, bIdx) => {
                  const byteStartBit = row.rowStart + bIdx * 8;
                  return (
                    <div
                      key={byteStartBit}
                      className="inline-flex items-center p-0.5 rounded bg-bg-card/40 border border-border-subtle/40"
                    >
                      {byteStr.split('').map((bitChar, bitOffset) => {
                        const bitIndex = byteStartBit + bitOffset;
                        const isChanged = diffMask ? diffMask[bitIndex] : false;
                        const isDimmed = filterMode === 'flipped-only' && !isChanged;
                        const isSelected = hoveredBit === bitIndex;

                        return (
                          <div
                            key={bitIndex}
                            onClick={() => setHoveredBit(isSelected ? null : bitIndex)}
                            onMouseEnter={() => setHoveredBit(bitIndex)}
                            className={cn(
                              'w-4 h-5 flex items-center justify-center rounded-[2px] text-[11px] font-semibold cursor-pointer transition-all duration-150 select-none min-w-[15px]',
                              isChanged
                                ? 'bg-accent-amber/25 text-accent-amber border border-accent-amber shadow-amber-glow font-bold scale-105 z-10'
                                : 'bg-bg-elevated/60 text-text-muted hover:text-text-primary hover:bg-bg-elevated',
                              isSelected && 'ring-2 ring-accent-cyan ring-offset-1 ring-offset-[#070A10] z-20 scale-110',
                              isDimmed && 'opacity-15'
                            )}
                            title={`Bit Index ${bitIndex} (Byte ${Math.floor(bitIndex / 8)}, Offset ${7 - (bitIndex % 8)})\nValue: ${bitChar}${
                              diffMask ? (isChanged ? ' [FLIPPED]' : ' [UNCHANGED]') : ''
                            }`}
                          >
                            {bitChar}
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Active Inspector Footer */}
      <div className="mt-3 pt-3 border-t border-border-subtle/50 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-text-muted">
        <div>
          {hoveredBit !== null ? (
            <span className="text-accent-cyan font-mono-code">
              Inspecting Bit <strong className="text-text-primary">#{hoveredBit}</strong> (Byte {Math.floor(hoveredBit / 8)}, Offset {7 - (hoveredBit % 8)}) —{' '}
              {diffMask ? (
                diffMask[hoveredBit] ? (
                  <strong className="text-accent-amber">Inverted via Cascade</strong>
                ) : (
                  <strong className="text-accent-emerald">Unchanged Bit</strong>
                )
              ) : (
                `Current Value: ${binaryDigest[hoveredBit]}`
              )}
            </span>
          ) : (
            <span>Tap or hover over any individual bit in the grid to inspect its byte address and flip status.</span>
          )}
        </div>

        <span className="text-[11px] text-text-muted font-mono-code flex-shrink-0">
          Big-Endian / Network Order
        </span>
      </div>
    </div>
  );
};
