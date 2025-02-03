import { motion } from 'framer-motion';
import { useApp } from '@/context/AppContext';

export function StatisticsPanel() {
  const { state } = useApp();
  
  const stats = {
    totalScans: state.history.length,
    accuracyRate: calculateAccuracyRate(state.history),
    avgConfidence: calculateAverageConfidence(state.history),
    thisMonth: getThisMonthCount(state.history)
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
    >
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Analysis Statistics
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Total Scans" value={stats.totalScans.toString()} />
        <StatCard title="Accuracy Rate" value={`${stats.accuracyRate}%`} />
        <StatCard title="Avg. Confidence" value={`${stats.avgConfidence}%`} />
        <StatCard title="This Month" value={stats.thisMonth.toString()} />
      </div>
    </motion.div>
  );
}

function StatCard({ title, value }: { title: string; value: string }) {
  return (
    <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
      <p className="text-sm text-gray-600 dark:text-gray-300">{title}</p>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
    </div>
  );
}

// Helper functions
function calculateAccuracyRate(history: any[]): number {
  if (history.length === 0) return 0;
  const highConfidencePredictions = history.filter(entry => entry.confidenceLevel === 'High');
  return Math.round((highConfidencePredictions.length / history.length) * 100);
}

function calculateAverageConfidence(history: any[]): number {
  if (history.length === 0) return 0;
  const sum = history.reduce((acc, entry) => acc + entry.confidence, 0);
  return Math.round((sum / history.length));
}

function getThisMonthCount(history: any[]): number {
  const now = new Date();
  const thisMonth = now.getMonth();
  const thisYear = now.getFullYear();
  return history.filter(entry => {
    const entryDate = new Date(entry.date);
    return entryDate.getMonth() === thisMonth && entryDate.getFullYear() === thisYear;
  }).length;
}