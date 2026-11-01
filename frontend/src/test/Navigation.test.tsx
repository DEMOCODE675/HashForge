import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { App } from '../App';

describe('App Navigation and Layout', () => {
  it('renders Dashboard by default', () => {
    render(<App />);
    expect(screen.getByText('An Interactive Cryptographic Hashing and Avalanche Effect Laboratory')).toBeInTheDocument();
  });

  it('navigates to Hash Generator when sidebar button is clicked', () => {
    render(<App />);
    const genButton = screen.getByRole('button', { name: /Hash Generator/i });
    fireEvent.click(genButton);
    expect(screen.getByText('Module 1: Hash Generator Laboratory')).toBeInTheDocument();
  });

  it('navigates to Algorithm Lab', () => {
    render(<App />);
    const algoButton = screen.getByRole('button', { name: /Algorithm Lab/i });
    fireEvent.click(algoButton);
    expect(screen.getByText('Module 2: Algorithm Comparison Lab')).toBeInTheDocument();
  });

  it('navigates to Single-Bit Experiment', () => {
    render(<App />);
    const singleButton = screen.getByRole('button', { name: /Single-Bit Experiment/i });
    fireEvent.click(singleButton);
    expect(screen.getByText('Module 3: Single-Bit Flip Experiment')).toBeInTheDocument();
  });

  it('navigates to Learning Center', () => {
    render(<App />);
    const learnButton = screen.getByRole('button', { name: /Learning Center/i });
    fireEvent.click(learnButton);
    expect(screen.getByText('Module 7: Cryptographic Learning Center')).toBeInTheDocument();
  });

  it('contains no emoji characters in navigation buttons', () => {
    const { container } = render(<App />);
    const navText = container.querySelector('nav')?.textContent || '';
    // Check common emoji code ranges
    const emojiRegex = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
    expect(emojiRegex.test(navText)).toBe(false);
  });
});

