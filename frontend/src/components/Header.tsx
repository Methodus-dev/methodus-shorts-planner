import { motion } from 'framer-motion';

interface HeaderProps {
  showSaved: boolean;
  onToggleSaved: () => void;
}

const Header: React.FC<HeaderProps> = ({ showSaved, onToggleSaved }) => {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text">
              ✨ Content Creator AI
            </h1>
            <p className="text-gray-600 mt-1">
              AI 기반 LinkedIn 콘텐츠 자동 생성 플랫폼
            </p>
          </div>
          
          <div className="flex gap-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onToggleSaved}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                showSaved
                  ? 'bg-primary-500 text-white'
                  : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-primary-400'
              }`}
            >
              📚 저장된 콘텐츠
            </motion.button>
            
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 rounded-lg font-semibold bg-white text-gray-700 border-2 border-gray-200 hover:border-secondary-400 transition-all"
            >
              📖 API Docs
            </motion.a>
          </div>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;

