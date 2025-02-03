export interface PredictionResult {
    condition: string;
    confidence: number;
    confidenceLevel: 'High' | 'Moderate' | 'Low';
  }
  
  export interface UploadResponse {
    success: boolean;
    prediction?: PredictionResult;
    error?: string;
  }