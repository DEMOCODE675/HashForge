export interface HashResponse {
  algorithm: string;
  hex_digest: string;
  binary_digest: string;
  digest_bits: number;
  digest_bytes: number;
  input_length_bytes: number;
  execution_time_ms: number;
  formatted_hex: string;
}

export interface AlgorithmBenchmarkInfo {
  iterations: number;
  total_time_ms: number;
  average_latency_us: number;
}

export interface AlgorithmCompareResponse {
  original_text: string;
  input_bytes_count: number;
  input_bits_count: number;
  sha256: HashResponse;
  sha3_256: HashResponse;
  cross_hamming_distance: number;
  cross_divergence_percentage: number;
  sha256_benchmark?: AlgorithmBenchmarkInfo;
  sha3_benchmark?: AlgorithmBenchmarkInfo;
}

export interface AvalancheMetrics {
  hamming_distance: number;
  total_bits: number;
  avalanche_percentage: number;
  changed_indices: number[];
  unchanged_count: number;
  distance_from_ideal: number;
}

export interface SingleBitResponse {
  original_text: string;
  total_input_bits: number;
  bit_index: number;
  byte_index: number;
  bit_offset_in_byte: number;
  original_bit_value: number;
  modified_bit_value: number;
  original_bytes_hex: string;
  modified_bytes_hex: string;
  original_binary_input: string;
  modified_binary_input: string;
  algorithm: string;
  original_hash: HashResponse;
  modified_hash: HashResponse;
  metrics: AvalancheMetrics;
  diff_mask: boolean[];
}

export interface MultiBitResponse {
  original_text: string;
  total_input_bits: number;
  flipped_bit_indices: number[];
  flipped_bits_count: number;
  original_bytes_hex: string;
  modified_bytes_hex: string;
  algorithm: string;
  original_hash: HashResponse;
  modified_hash: HashResponse;
  metrics: AvalancheMetrics;
  diff_mask: boolean[];
}

export interface TrialRecord {
  trial: number;
  bit_index: number;
  byte_index: number;
  hamming_distance: number;
  avalanche_pct: number;
  original_hex: string;
  modified_hex: string;
  time_ms: number;
}

export interface AvalancheSimulationResponse {
  original_text: string;
  algorithm: string;
  total_input_bits: number;
  trials_count: number;
  mean_avalanche_pct: number;
  std_avalanche_pct: number;
  min_avalanche_pct: number;
  max_avalanche_pct: number;
  median_avalanche_pct: number;
  ideal_avalanche_pct: number;
  trials: TrialRecord[];
}

export interface ComparativeSimulationResponse {
  original_text: string;
  trials_count: number;
  sha256_result: AvalancheSimulationResponse;
  sha3_256_result: AvalancheSimulationResponse;
}

export interface FileHashResponse {
  file_name: string;
  file_size_bytes: number;
  formatted_size: string;
  sha256_hex: string;
  sha3_256_hex: string;
  chunks_processed: number;
  hashing_duration_ms: number;
}

export interface FileCompareResponse {
  file_a: FileHashResponse;
  file_b?: FileHashResponse;
  reference_hash?: string;
  is_identical: boolean;
  sha256_match: boolean;
  sha3_256_match: boolean;
  size_match: boolean;
  details: string;
}

export interface LearningTopic {
  id: number;
  title: string;
  summary: string;
  content: string;
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}
