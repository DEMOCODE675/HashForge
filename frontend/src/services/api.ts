import {
  HashResponse,
  AlgorithmCompareResponse,
  SingleBitResponse,
  MultiBitResponse,
  AvalancheSimulationResponse,
  ComparativeSimulationResponse,
  FileHashResponse,
  FileCompareResponse,
  LearningTopic,
  QuizQuestion,
} from '../types';

const rawBase = import.meta.env.VITE_API_BASE_URL;
const API_BASE = rawBase
  ? rawBase.replace(/\/$/, '').endsWith('/api')
    ? rawBase.replace(/\/$/, '')
    : `${rawBase.replace(/\/$/, '')}/api`
  : '/api';

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      let errorMsg = `Server error (${res.status})`;
      try {
        const errorJson = await res.json();
        if (errorJson.detail) {
          errorMsg = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail);
        }
      } catch {
        // Fallback to text
      }
      throw new ApiError(errorMsg, res.status);
    }
    return (await res.json()) as T;
  } catch (err: any) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(err?.message || 'Network communication error', 0);
  }
}

export const api = {
  getHealth: () => request<{ status: string; service: string; version: string; algorithms: string[] }>('/health'),

  generateHash: (text: string, algorithm: string = 'sha256') =>
    request<HashResponse>('/hash/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, algorithm }),
    }),

  compareAlgorithms: (text: string, benchmarkIterations: number = 1000) =>
    request<AlgorithmCompareResponse>('/hash/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, benchmark_iterations: benchmarkIterations }),
    }),

  singleBitExperiment: (text: string, bitIndex: number, algorithm: string = 'sha256') =>
    request<SingleBitResponse>('/experiments/single-bit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, bit_index: bitIndex, algorithm }),
    }),

  multiBitExperiment: (text: string, bitIndices: number[], algorithm: string = 'sha256') =>
    request<MultiBitResponse>('/experiments/multi-bit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, bit_indices: bitIndices, algorithm }),
    }),

  multiBitRandomExperiment: (text: string, kBits: number, seed: number | null = null, algorithm: string = 'sha256') =>
    request<MultiBitResponse>('/experiments/multi-bit/random', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, k_bits: kBits, seed, algorithm }),
    }),

  avalancheSimulation: (
    text: string,
    trials: number = 50,
    algorithm: string = 'sha256',
    seed: number | null = null,
    mode: string = 'single_bit',
    comparative: boolean = false
  ) =>
    request<AvalancheSimulationResponse | ComparativeSimulationResponse>('/experiments/avalanche', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, trials, algorithm, seed, mode, comparative }),
    }),

  hashFile: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return request<FileHashResponse>('/files/hash', {
      method: 'POST',
      body: formData,
    });
  },

  compareFiles: (fileA: File, fileB?: File | null, referenceHash?: string | null) => {
    const formData = new FormData();
    formData.append('file_a', fileA);
    if (fileB) formData.append('file_b', fileB);
    if (referenceHash) formData.append('reference_hash', referenceHash);
    return request<FileCompareResponse>('/files/compare', {
      method: 'POST',
      body: formData,
    });
  },

  getLearningTopics: () => request<LearningTopic[]>('/learning/topics'),

  getQuizQuestions: () => request<QuizQuestion[]>('/learning/quiz'),
};

