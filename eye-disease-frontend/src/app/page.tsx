'use client'

import { useState } from 'react';
import { ImageUpload } from '@/components/ImageUpload';
import { PredictionResult } from '@/components/PredictionResult';
import { StatisticsPanel } from '@/components/StatisticsPanel';
import { HistoryViewer } from '@/components/HistoryViewer';
import type { PredictionResult as PredictionResultType } from '@/types';
import { motion } from 'framer-motion';


export default function Home() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<PredictionResultType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = async (file: File) => {
    setIsProcessing(true);
    setError(null);
    setResult(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        setResult(data.prediction);
      } else {
        setError(data.error || 'An error occurred during prediction');
      }
    } catch (err) {
      setError('Failed to process the image. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto space-y-8"
      >
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4 tracking-tight">
            Eye Disease Detection
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Advanced AI-powered detection of Glaucoma, AMD, and Cataracts
          </p>
        </div>
        <StatisticsPanel />

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
                Upload Image
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                Upload a clear fundus image of the eye for analysis
              </p>
              <ImageUpload onImageSelect={handleImageSelect} isProcessing={isProcessing} />
            </div>
            
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
                Analysis Results
              </h2>
              {error && (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-200 rounded-lg"
                >
                  {error}
                </motion.div>
              )}
              
              {isProcessing && (
                <div className="flex items-center justify-center h-48">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
              )}
              {result && !isProcessing && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <PredictionResult result={result} />
                </motion.div>
              )}
            </div>
          </div>
        </div>
        <HistoryViewer />

        <div className="text-center text-sm text-gray-500 dark:text-gray-400">
          <p>This system is for educational purposes only. Always consult healthcare professionals for medical advice.</p>
        </div>
      </motion.div>
    </main>
  );
}