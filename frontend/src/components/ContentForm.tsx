import React, { useState, useEffect } from 'react';
import { getTopics } from '../services/api';
import { motion } from 'framer-motion';

interface ContentFormProps {
  onGenerate: (data: FormData) => void;
  isLoading: boolean;
}

export interface FormData {
  topic: string;
  structure: string;
  content_type: string;
  target_audience: string;
  tone: string;
}

const ContentForm: React.FC<ContentFormProps> = ({ onGenerate, isLoading }) => {
  const [formData, setFormData] = useState<FormData>({
    topic: '',
    structure: 'Trailer-Meat-Summary-CTC',
    content_type: 'Actionable',
    target_audience: '',
    tone: 'professional',
  });

  const [suggestedTopics, setSuggestedTopics] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    loadFormOptions();
  }, []);

  const loadFormOptions = async () => {
    try {
      const topicsData = await getTopics();
      setSuggestedTopics(topicsData);
    } catch (error) {
      console.error('Failed to load form options:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.topic.trim()) {
      onGenerate(formData);
    }
  };

  const handleTopicChange = (value: string) => {
    setFormData({ ...formData, topic: value });
    setShowSuggestions(value.length > 0);
  };

  const selectSuggestedTopic = (topic: string) => {
    setFormData({ ...formData, topic });
    setShowSuggestions(false);
  };

  const filteredSuggestions = suggestedTopics.filter((topic) =>
    topic.toLowerCase().includes(formData.topic.toLowerCase())
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="card"
    >
      <h2 className="text-2xl font-bold mb-6 gradient-text">
        콘텐츠 생성 설정
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Topic Input */}
        <div className="relative">
          <label className="label">주제 *</label>
          <input
            type="text"
            value={formData.topic}
            onChange={(e) => handleTopicChange(e.target.value)}
            onFocus={() => setShowSuggestions(true)}
            placeholder="예: 마케팅, 창업, 개발, 투자, 부업, 성장"
            className="input-field"
            required
          />
          
          {/* Topic Suggestions */}
          {showSuggestions && filteredSuggestions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="absolute z-10 w-full mt-2 bg-white border-2 border-gray-200 rounded-lg shadow-xl max-h-48 overflow-y-auto"
            >
              {filteredSuggestions.slice(0, 8).map((topic, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => selectSuggestedTopic(topic)}
                  className="w-full text-left px-4 py-2 hover:bg-primary-50 transition-colors duration-150 text-sm"
                >
                  {topic}
                </button>
              ))}
            </motion.div>
          )}
        </div>

        {/* Structure Select */}
        <div>
          <label className="label">콘텐츠 구조</label>
          <select
            value={formData.structure}
            onChange={(e) => setFormData({ ...formData, structure: e.target.value })}
            className="input-field"
          >
            <option value="Trailer-Meat-Summary-CTC">훅-핵심-요약-행동유도</option>
            <option value="Story-Based">스토리 기반</option>
            <option value="Listicle">리스트 형식</option>
          </select>
        </div>

        {/* Content Type Select */}
        <div>
          <label className="label">콘텐츠 타입</label>
          <select
            value={formData.content_type}
            onChange={(e) => setFormData({ ...formData, content_type: e.target.value })}
            className="input-field"
          >
            <option value="Actionable">실행 가능한 가이드</option>
            <option value="Motivational">동기부여 스토리</option>
            <option value="Analytical">분석 및 해부</option>
            <option value="Contrarian">반대 의견</option>
            <option value="Observation">관찰 및 인사이트</option>
            <option value="X vs. Y">비교 분석</option>
            <option value="Present/Future">현재와 미래</option>
            <option value="Listicle">목록형</option>
          </select>
        </div>

        {/* Target Audience */}
        <div>
          <label className="label">타겟 오디언스 (선택)</label>
          <input
            type="text"
            value={formData.target_audience}
            onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
            placeholder="예: 마케터, 창업가, 개발자"
            className="input-field"
          />
        </div>

        {/* Tone Select */}
        <div>
          <label className="label">톤앤매너</label>
          <select
            value={formData.tone}
            onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
            className="input-field"
          >
            <option value="professional">전문적</option>
            <option value="casual">친근한</option>
            <option value="motivational">동기부여</option>
            <option value="educational">교육적</option>
          </select>
        </div>

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={isLoading || !formData.topic.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`btn-primary w-full ${
            isLoading || !formData.topic.trim() ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              생성 중...
            </span>
          ) : (
            '✨ 콘텐츠 생성하기'
          )}
        </motion.button>
      </form>
    </motion.div>
  );
};

export default ContentForm;

