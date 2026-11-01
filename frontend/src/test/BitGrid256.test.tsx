import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { BitGrid256 } from '../components/binary/BitGrid256';

describe('BitGrid256 Component', () => {
  const sample256 = '01'.repeat(128); // 256 bits
  const sampleDiffMask = Array.from({ length: 256 }, (_, i) => i % 2 === 1); // 128 changed

  it('renders the 256-bit grid with row labels', () => {
    render(<BitGrid256 binaryDigest={sample256} diffMask={sampleDiffMask} />);
    expect(screen.getByText('Bits 000–031')).toBeInTheDocument();
    expect(screen.getByText('Bits 224–255')).toBeInTheDocument();
  });

  it('accurately reports flipped and unchanged bit counts', () => {
    render(<BitGrid256 binaryDigest={sample256} diffMask={sampleDiffMask} />);
    expect(screen.getByText(/Flipped:/i)).toBeInTheDocument();
    expect(screen.getAllByText('128').length).toBe(2);
    expect(screen.getByText(/50\.00%/)).toBeInTheDocument();
  });
});
