import { useState } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { savePlan } from '../services/api';

interface ContentDisplayProps {
  content: any;
  onEdit?: (editedContent: string) => void;
}

const ContentDisplay: React.FC<ContentDisplayProps> = ({ content, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  if (!content) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="card h-full flex items-center justify-center"
      >
        <div className="text-center text-gray-400">
          <svg
            className="w-24 h-24 mx-auto mb-4 opacity-50"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p className="text-lg font-medium">생성된 콘텐츠가 여기에 표시됩니다</p>
          <p className="text-sm mt-2">왼쪽에서 주제를 입력하고 생성 버튼을 클릭하세요</p>
        </div>
      </motion.div>
    );
  }

  const handleCopy = async () => {
    try {
      const textToCopy = `${content.content}\n\n${content.hashtags.join(' ')}`;
      await navigator.clipboard.writeText(textToCopy);
      toast.success('클립보드에 복사되었습니다!');
    } catch (error) {
      toast.error('복사에 실패했습니다');
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await savePlan(content);
      toast.success('콘텐츠가 저장되었습니다!');
    } catch (error) {
      toast.error('저장에 실패했습니다');
    } finally {
      setIsSaving(false);
    }
  };

  const handleEdit = () => {
    setEditedText(content.content);
    setIsEditing(true);
  };

  const handleSaveEdit = () => {
    if (onEdit) {
      onEdit(editedText);
    }
    setIsEditing(false);
    toast.success('콘텐츠가 수정되었습니다!');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="card h-full flex flex-col"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold gradient-text">생성된 콘텐츠</h2>
        <div className="flex gap-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleEdit}
            className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
            title="편집"
          >
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCopy}
            className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
            title="복사"
          >
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSave}
            disabled={isSaving}
            className="p-2 rounded-lg bg-primary-100 hover:bg-primary-200 transition-colors"
            title="저장"
          >
            <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
          </motion.button>
        </div>
      </div>

      {/* Content Display/Edit Area */}
      <div className="flex-1 mb-6">
        {isEditing ? (
          <div className="space-y-4">
            <textarea
              value={editedText}
              onChange={(e) => setEditedText(e.target.value)}
              className="input-field min-h-[400px] font-sans"
              style={{ whiteSpace: 'pre-wrap' }}
            />
            <div className="flex gap-2">
              <button onClick={handleSaveEdit} className="btn-primary flex-1">
                수정 완료
              </button>
              <button onClick={() => setIsEditing(false)} className="btn-secondary flex-1">
                취소
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-gray-50 rounded-lg p-6 min-h-[400px]">
            <pre className="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed">
              {content.content}
            </pre>
          </div>
        )}
      </div>

      {/* Hashtags */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-600 mb-3">해시태그</h3>
        <div className="flex flex-wrap gap-2">
          {content.hashtags.map((tag: string, index: number) => (
            <motion.span
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
            >
              {tag}
            </motion.span>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
        <div className="text-center">
          <p className="text-2xl font-bold text-primary-600">{content.word_count}</p>
          <p className="text-xs text-gray-500">단어 수</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-secondary-600">{content.character_count}</p>
          <p className="text-xs text-gray-500">글자 수</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-green-600">{content.hashtags.length}</p>
          <p className="text-xs text-gray-500">해시태그</p>
        </div>
      </div>
    </motion.div>
  );
};

export default ContentDisplay;

