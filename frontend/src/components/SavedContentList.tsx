import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { getSavedPlans, deleteSavedPlan } from '../services/api';

interface SavedContent {
  id: string;
  topic: string;
  content_type: string;
  plan: any;
  created_at: string;
}

interface SavedContentListProps {
  onSelect?: (content: SavedContent) => void;
  refreshTrigger?: number;
}

const SavedContentList: React.FC<SavedContentListProps> = ({ onSelect, refreshTrigger }) => {
  const [savedContent, setSavedContent] = useState<SavedContent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSavedContent();
  }, [refreshTrigger]);

  const loadSavedContent = async () => {
    setIsLoading(true);
    try {
      const response = await getSavedPlans();
      setSavedContent(response.saved_plans || []);
    } catch (error) {
      toast.error('저장된 콘텐츠를 불러오는데 실패했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (window.confirm('이 콘텐츠를 삭제하시겠습니까?')) {
      try {
        await deleteSavedPlan(id);
        setSavedContent(savedContent.filter(item => item.id !== id));
        toast.success('콘텐츠가 삭제되었습니다');
      } catch (error) {
        toast.error('삭제에 실패했습니다');
      }
    }
  };

  const handleCopy = async (content: SavedContent, e: React.MouseEvent) => {
    e.stopPropagation();
    
    try {
      const textToCopy = JSON.stringify(content.plan, null, 2);
      await navigator.clipboard.writeText(textToCopy);
      toast.success('클립보드에 복사되었습니다!');
    } catch (error) {
      toast.error('복사에 실패했습니다');
    }
  };

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    );
  }

  if (savedContent.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="card text-center py-8"
      >
        <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p className="text-gray-500">저장된 콘텐츠가 없습니다</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="card"
    >
      <h3 className="text-xl font-bold mb-4 gradient-text">저장된 콘텐츠</h3>
      
      <div className="space-y-3 max-h-[600px] overflow-y-auto">
        <AnimatePresence>
          {savedContent.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: index * 0.05 }}
              onClick={() => onSelect?.(item)}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer border border-gray-200 hover:border-primary-300"
            >
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-semibold text-gray-800 flex-1">{item.topic}</h4>
                <div className="flex gap-2 ml-2">
                  <button
                    onClick={(e) => handleCopy(item, e)}
                    className="p-1 rounded hover:bg-gray-200 transition-colors"
                    title="복사"
                  >
                    <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    className="p-1 rounded hover:bg-red-100 transition-colors"
                    title="삭제"
                  >
                    <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                {item.topic}
              </p>
              
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded">
                  {item.content_type}
                </span>
                <span>
                  {new Date(item.created_at).toLocaleDateString('ko-KR')}
                </span>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default SavedContentList;

