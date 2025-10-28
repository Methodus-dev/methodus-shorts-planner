import { motion } from 'framer-motion';

const QuickTips = () => {
  const tips = [
    {
      icon: '🎯',
      text: '구체적인 주제를 입력할수록 더 정확한 콘텐츠가 생성됩니다'
    },
    {
      icon: '👥',
      text: '타겟 오디언스를 지정하면 맞춤형 콘텐츠를 얻을 수 있습니다'
    },
    {
      icon: '✏️',
      text: '생성된 콘텐츠는 편집 버튼으로 수정 가능합니다'
    },
    {
      icon: '💾',
      text: '마음에 드는 콘텐츠는 저장하여 나중에 다시 사용하세요'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="mt-6 card bg-gradient-to-br from-primary-50 to-secondary-50"
    >
      <h3 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
        <span>💡</span>
        <span>작성 팁</span>
      </h3>
      <ul className="space-y-2">
        {tips.map((tip, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + index * 0.1 }}
            className="flex items-start text-sm text-gray-700"
          >
            <span className="mr-2">{tip.icon}</span>
            <span>{tip.text}</span>
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
};

export default QuickTips;

