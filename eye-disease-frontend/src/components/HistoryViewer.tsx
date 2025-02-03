'use client'
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { useApp } from '@/context/AppContext';
import Image from 'next/image';
import { useState } from 'react';

export function HistoryViewer() {
  const { state } = useApp();
  const [selectedEntry, setSelectedEntry] = useState<string | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Analysis History
        </h3>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {state.history.length} total scans
        </span>
      </div>
      
      <div className="space-y-4">
        <AnimatePresence>
          {state.history.map((entry) => (
            <motion.div
              key={entry.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="group cursor-pointer"
              onClick={() => setSelectedEntry(selectedEntry === entry.id ? null : entry.id)}
            >
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="relative w-12 h-12 rounded-lg overflow-hidden">
                    <Image
                      src={entry.imageUrl}
                      alt={entry.condition}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {entry.condition}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {format(new Date(entry.date), 'PPP')}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-blue-600 dark:text-blue-400">
                    {(entry.confidence * 100).toFixed(1)}%
                  </p>
                  <p className={`text-sm ${getConfidenceLevelColor(entry.confidenceLevel)}`}>
                    {entry.confidenceLevel}
                  </p>
                </div>
              </div>
              
              {selectedEntry === entry.id && (
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: 'auto' }}
                  exit={{ height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-4 bg-gray-100 dark:bg-gray-600 rounded-b-lg">
                    <div className="relative aspect-video w-full rounded-lg overflow-hidden">
                      <Image
                        src={entry.imageUrl}
                        alt={entry.condition}
                        fill
                        className="object-contain"
                      />
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}

function getConfidenceLevelColor(level: string) {
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
}