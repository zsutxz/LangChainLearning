"""
LangDeepAgent - 英语学习 AI Agent
基于 DeepSeek API 的智能英语学习助手
"""

__version__ = "0.1.0"
__author__ = "LangDeepAgent Team"
__description__ = "基于 DeepSeek 的智能英语学习助手"

# 导出主要类
from src.agent import EnglishLearningAgent
from src.models import (
    LearningPlan,
    VocabularySession,
    ConversationSession,
    ProgressReport,
    AssessmentResult
)

__all__ = [
    'EnglishLearningAgent',
    'LearningPlan',
    'VocabularySession',
    'ConversationSession',
    'ProgressReport',
    'AssessmentResult'
]