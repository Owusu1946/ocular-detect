import { motion } from 'framer-motion';
import { PredictionResult as PredictionResultType } from '@/types';

interface PredictionResultProps {
  result: PredictionResultType;
}

export const PredictionResult = ({ result }: PredictionResultProps) => {
  const getConfidenceColor = (level: string) => {
    switch (level) {
      case 'High':
        return 'text-green-500';
      case 'Moderate':
        return 'text-yellow-500';
      case 'Low':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto mt-8"
    >
      <h3 className="text-xl font-semibold mb-4">Prediction Results</h3>
      <div className="space-y-4">
        <div>
          <p className="text-gray-600">Condition:</p>
          <p className="text-2xl font-bold text-blue-600">{result.condition}</p>
        </div>
        <div>
          <p className="text-gray-600">Confidence:</p>
          <p className="text-xl">{(result.confidence * 100).toFixed(2)}%</p>
        </div>
        <div>
          <p className="text-gray-600">Confidence Level:</p>
          <p className={`text-xl font-semibold ${getConfidenceColor(result.confidenceLevel)}`}>
            {result.confidenceLevel}
          </p>
        </div>
      </div>
    </motion.div>
  );
};