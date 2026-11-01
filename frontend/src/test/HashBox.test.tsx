import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { HashBox } from '../components/shared/HashBox';

describe('HashBox Component', () => {
  const hex = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad';
  const chunked = 'ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad';

  it('renders hex digest and algorithm label', () => {
    render(<HashBox algorithm="sha256" hexDigest={hex} formattedHex={chunked} />);
    expect(screen.getByText('SHA256')).toBeInTheDocument();
    expect(screen.getByText(hex)).toBeInTheDocument();
  });

  it('switches to chunked view on toggle', () => {
    render(<HashBox algorithm="sha256" hexDigest={hex} formattedHex={chunked} />);
    const chunkedBtn = screen.getByText('Chunked');
    fireEvent.click(chunkedBtn);
    expect(screen.getByText(chunked)).toBeInTheDocument();
  });
});
