'use client'
import { createContext, useContext, useReducer, ReactNode } from 'react';

export interface HistoryEntry {
  id: string;
  date: Date;
  condition: string;
  confidence: number;
  confidenceLevel: 'High' | 'Moderate' | 'Low';
  imageUrl: string;
}

interface AppState {
  history: HistoryEntry[];
  statistics: {
    totalScans: number;
    accuracyRate: number;
    avgConfidence: number;
    monthlyScans: number;
  };
}

type AppAction = 
  | { type: 'ADD_PREDICTION'; payload: HistoryEntry }
  | { type: 'UPDATE_STATISTICS' };

const initialState: AppState = {
  history: [],
  statistics: {
    totalScans: 0,
    accuracyRate: 0,
    avgConfidence: 0,
    monthlyScans: 0,
  }
};

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | undefined>(undefined);

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'ADD_PREDICTION':
      const newHistory = [action.payload, ...state.history];
      return {
        ...state,
        history: newHistory,
        statistics: calculateStatistics(newHistory)
      };
    default:
      return state;
  }
}

function calculateStatistics(history: HistoryEntry[]) {
  const totalScans = history.length;
  const avgConfidence = history.reduce((acc, curr) => acc + curr.confidence, 0) / totalScans;
  const thisMonth = new Date().getMonth();
  const monthlyScans = history.filter(entry => 
    new Date(entry.date).getMonth() === thisMonth
  ).length;

  return {
    totalScans,
    accuracyRate: 97, // This would come from model metrics in real app
    avgConfidence: avgConfidence * 100,
    monthlyScans,
  };
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
} 