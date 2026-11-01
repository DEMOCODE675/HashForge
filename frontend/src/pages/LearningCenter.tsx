import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  HelpCircle,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  Award,
  RefreshCw,
} from 'lucide-react';
import { api } from '../services/api';
import { LearningTopic, QuizQuestion } from '../types';
import { StatusBadge } from '../components/shared/StatusBadge';

export const LearningCenter: React.FC = () => {
  const [topics, setTopics] = useState<LearningTopic[]>([]);
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [activeTab, setActiveTab] = useState<'curriculum' | 'quiz'>('curriculum');
  const [expandedTopic, setExpandedTopic] = useState<number | null>(1);

  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [t, q] = await Promise.all([
          api.getLearningTopics(),
          api.getQuizQuestions(),
        ]);
        setTopics(t);
        setQuizQuestions(q);
      } catch (err) {
        console.error('Failed to load learning curriculum:', err);
      }
    };
    fetchData();
  }, []);

  const handleSelectOption = (questionId: number, optionIdx: number) => {
    if (quizSubmitted) return;
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: optionIdx,
    }));
  };

  const handleQuizSubmit = () => {
    let correctCount = 0;
    quizQuestions.forEach((q) => {
      if (selectedAnswers[q.id] === q.correct_index) {
        correctCount += 1;
      }
    });
    setScore(correctCount);
    setQuizSubmitted(true);
  };

  const handleResetQuiz = () => {
    setSelectedAnswers({});
    setQuizSubmitted(false);
    setScore(0);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-5 h-5 text-accent-cyan" />
            <h1 className="text-xl font-bold text-text-primary">Module 7: Cryptographic Learning Center</h1>
          </div>
          <p className="text-xs text-text-muted">
            Master the theoretical principles of one-way hashing, diffusion, and data integrity with interactive evaluation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusBadge variant="cyan" icon="shield">12 Structured Topics</StatusBadge>
          <StatusBadge variant="emerald" icon="check">10-Question Knowledge Check</StatusBadge>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap sm:flex-nowrap items-center gap-2 border-b border-border-subtle pb-2">
        <button
          type="button"
          onClick={() => setActiveTab('curriculum')}
          className={`flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] ${
            activeTab === 'curriculum'
              ? 'bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/40 shadow-cyan-glow'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Curriculum Modules ({topics.length})</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('quiz')}
          className={`flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold transition-all min-h-[40px] ${
            activeTab === 'quiz'
              ? 'bg-accent-emerald/15 text-accent-emerald border border-accent-emerald/40'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
          }`}
        >
          <HelpCircle className="w-4 h-4" />
          <span>Knowledge Check Evaluation</span>
        </button>
      </div>

      {/* Tab 1: Curriculum */}
      {activeTab === 'curriculum' && (
        <div className="space-y-3">
          {topics.map((t) => {
            const isExpanded = expandedTopic === t.id;
            return (
              <div
                key={t.id}
                className="bg-bg-card border border-border-subtle rounded-xl overflow-hidden shadow-card transition-all"
              >
                <button
                  type="button"
                  onClick={() => setExpandedTopic(isExpanded ? null : t.id)}
                  className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-bg-elevated/40 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/30 text-xs font-bold flex items-center justify-center flex-shrink-0">
                      {t.id}
                    </span>
                    <div>
                      <h3 className="text-sm font-bold text-text-primary">{t.title}</h3>
                      <p className="text-xs text-text-muted mt-0.5">{t.summary}</p>
                    </div>
                  </div>

                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-text-muted flex-shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-text-muted flex-shrink-0" />
                  )}
                </button>

                {isExpanded && (
                  <div className="px-5 py-4 border-t border-border-subtle/50 text-xs text-text-secondary leading-relaxed bg-[#070A10]/50 space-y-2">
                    <p>{t.content}</p>
                    {t.id === 12 && (
                      <div className="p-3 rounded-lg bg-accent-amber/10 border border-accent-amber/30 text-accent-amber mt-2">
                        <strong>Security Requirement:</strong> For password storage, always use adaptive, memory-hard algorithms such as <strong>Argon2id</strong>, <strong>bcrypt</strong>, or <strong>scrypt</strong> rather than raw SHA-256.
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Tab 2: Quiz */}
      {activeTab === 'quiz' && (
        <div className="space-y-6">
          {quizSubmitted && (
            <div className="bg-bg-card border border-accent-cyan/40 rounded-xl p-6 shadow-card text-center space-y-3">
              <Award className="w-10 h-10 text-accent-cyan mx-auto" />
              <h2 className="text-xl font-bold text-text-primary">Knowledge Evaluation Result</h2>
              <div className="text-3xl font-extrabold text-accent-cyan font-mono-code">
                {score} / {quizQuestions.length} ({((score / quizQuestions.length) * 100).toFixed(0)}%)
              </div>
              <p className="text-xs text-text-secondary max-w-md mx-auto">
                {score >= 8
                  ? 'Excellent mastery of cryptographic hashing principles, diffusion, and security invariants.'
                  : 'Good effort. Review the technical explanations below to deepen your theoretical understanding.'}
              </p>
              <div>
                <button
                  type="button"
                  onClick={handleResetQuiz}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-bg-elevated hover:bg-bg-card border border-border-subtle text-xs text-text-primary font-semibold transition-colors"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Retake Evaluation</span>
                </button>
              </div>
            </div>
          )}

          <div className="space-y-4">
            {quizQuestions.map((q, qIdx) => {
              const selectedOpt = selectedAnswers[q.id];
              const isCorrect = selectedOpt === q.correct_index;

              return (
                <div
                  key={q.id}
                  className="bg-bg-card border border-border-subtle rounded-xl p-5 shadow-card space-y-3"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-xs font-mono-code font-bold text-accent-cyan flex-shrink-0 mt-0.5">
                      Q{qIdx + 1}.
                    </span>
                    <h3 className="text-sm font-semibold text-text-primary leading-snug">
                      {q.question}
                    </h3>
                  </div>

                  <div className="space-y-2 pt-2">
                    {q.options.map((opt, optIdx) => {
                      const isSelected = selectedOpt === optIdx;
                      let optionStyle = 'bg-bg-elevated/70 border-border-subtle text-text-secondary hover:text-text-primary hover:bg-bg-elevated';

                      if (isSelected) {
                        optionStyle = 'bg-accent-cyan/15 border-accent-cyan text-accent-cyan font-medium';
                      }

                      if (quizSubmitted) {
                        if (optIdx === q.correct_index) {
                          optionStyle = 'bg-accent-emerald/20 border-accent-emerald text-accent-emerald font-bold';
                        } else if (isSelected && !isCorrect) {
                          optionStyle = 'bg-accent-rose/20 border-accent-rose text-accent-rose';
                        }
                      }

                      return (
                        <div
                          key={optIdx}
                          onClick={() => handleSelectOption(q.id, optIdx)}
                          className={`p-3 rounded-lg border text-xs cursor-pointer transition-all flex items-center justify-between gap-3 min-h-[44px] ${optionStyle}`}
                        >
                          <span className="leading-relaxed">{opt}</span>
                          {quizSubmitted && optIdx === q.correct_index && (
                            <CheckCircle2 className="w-4 h-4 text-accent-emerald flex-shrink-0" />
                          )}
                          {quizSubmitted && isSelected && !isCorrect && (
                            <AlertCircle className="w-4 h-4 text-accent-rose flex-shrink-0" />
                          )}
                        </div>
                      );
                    })}
                  </div>

                  {quizSubmitted && (
                    <div className="p-3 rounded-lg bg-[#070A10] border border-border-subtle text-xs text-text-muted mt-3 leading-relaxed">
                      <strong className="text-text-primary">Explanation: </strong>
                      {q.explanation}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {!quizSubmitted && (
            <div className="flex justify-end pt-2">
              <button
                type="button"
                onClick={handleQuizSubmit}
                disabled={Object.keys(selectedAnswers).length < quizQuestions.length}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3 rounded-lg bg-accent-cyan hover:bg-accent-cyan/90 text-bg-primary font-bold text-xs tracking-wider uppercase transition-all shadow-cyan-glow disabled:opacity-50 min-h-[44px]"
              >
                <span>Submit Evaluation ({Object.keys(selectedAnswers).length}/{quizQuestions.length} Answered)</span>
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

