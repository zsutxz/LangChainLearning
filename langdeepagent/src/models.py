"""
数据模型定义
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class UserProfile(BaseModel):
    """用户档案"""
    user_id: str
    current_level: str  # beginner, intermediate, advanced
    learning_goals: List[str]
    target_scenario: str
    study_time_per_day: int
    study_duration_weeks: int
    created_at: datetime
    updated_at: datetime


class VocabularyWord(BaseModel):
    """词汇条目"""
    word: str
    phonetic: Optional[str] = None
    part_of_speech: str
    definition: str
    example_sentence: str
    synonyms: List[str] = []
    antonyms: List[str] = []
    memory_tips: Optional[str] = None
    difficulty_level: int  # 1-5
    mastery_level: int = 0  # 0-5


class VocabularySession(BaseModel):
    """词汇学习会话"""
    session_id: str
    topic: str
    words: List[VocabularyWord]
    learning_strategies: List[str]
    practice_exercises: List[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime] = None


class DialogueTurn(BaseModel):
    """对话回合"""
    speaker: str
    text: str
    translation: Optional[str] = None
    key_expressions: List[str] = []
    cultural_notes: Optional[str] = None


class ConversationSession(BaseModel):
    """对话练习会话"""
    session_id: str
    scenario: str
    difficulty_level: str
    background: str
    roles: List[Dict[str, str]]
    dialogue: List[DialogueTurn]
    key_vocabulary: List[str]
    useful_phrases: List[str]
    practice_tips: List[str]
    created_at: datetime


class GrammarRule(BaseModel):
    """语法规则"""
    rule: str
    formula: Optional[str] = None
    examples: List[str]
    exceptions: List[str] = []


class CommonError(BaseModel):
    """常见错误"""
    error: str
    correction: str
    explanation: str
    tip: str


class GrammarExercise(BaseModel):
    """语法练习题"""
    type: str
    question: str
    options: Optional[List[str]] = None
    answer: str
    explanation: str


class GrammarSession(BaseModel):
    """语法学习会话"""
    session_id: str
    topic: str
    difficulty_level: str
    explanation: str
    rules: List[GrammarRule]
    common_errors: List[CommonError]
    practice_exercises: List[GrammarExercise]
    learning_tips: List[str]
    created_at: datetime


class WeeklyPlan(BaseModel):
    """周计划"""
    week: int
    goals: List[str]
    vocabulary_focus: str
    grammar_focus: str
    practice_activities: List[str]
    estimated_hours: int


class LearningResources(BaseModel):
    """学习资源"""
    textbooks: List[str]
    websites: List[str]
    apps: List[str]
    videos: List[str]


class LearningPlan(BaseModel):
    """学习计划"""
    plan_id: str
    user_id: str
    current_level: str
    learning_goals: List[str]
    target_scenario: str
    overall_goals: List[str]
    milestones: List[WeeklyPlan]
    daily_schedule: Dict[str, str]
    resources: LearningResources
    created_at: datetime
    updated_at: datetime


class ProgressMetrics(BaseModel):
    """进度指标"""
    vocabulary_mastered: int
    grammar_completed: int
    conversations_practiced: int
    study_hours_total: float
    average_session_length: float
    streak_days: int


class Achievement(BaseModel):
    """成就徽章"""
    badge_id: str
    name: str
    description: str
    earned_at: datetime


class ProgressReport(BaseModel):
    """进度报告"""
    report_id: str
    user_id: str
    report_date: datetime
    overall_progress: str
    improvement_areas: Dict[str, str]
    achievements: List[Achievement]
    areas_for_improvement: List[str]
    next_steps: List[str]
    motivational_feedback: str
    study_efficiency_score: int
    metrics: ProgressMetrics


class AssessmentResult(BaseModel):
    """评估结果"""
    assessment_id: str
    user_id: str
    assessment_date: datetime
    current_level: str
    vocabulary_level: int
    grammar_level: int
    listening_level: int
    speaking_level: int
    reading_level: int
    writing_level: int
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


class LearningSession(BaseModel):
    """学习会话"""
    session_id: str
    user_id: str
    session_type: str  # vocabulary, grammar, conversation, assessment
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    content: Dict[str, Any]
    performance_score: Optional[float] = None
    notes: Optional[str] = None


# API 响应模型
class APIResponse(BaseModel):
    """API 响应基类"""
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: datetime


class ConversationResponse(APIResponse):
    """对话响应"""
    session_id: str
    ai_response: str
    suggested_replies: List[str] = []
    corrections: List[Dict[str, str]] = []


class VocabularyResponse(APIResponse):
    """词汇学习响应"""
    words: List[VocabularyWord]
    next_review_date: datetime
    review_count: int


class PlanResponse(APIResponse):
    """学习计划响应"""
    learning_plan: LearningPlan
    estimated_completion_date: datetime


class ErrorResponse(APIResponse):
    """错误响应"""
    error_code: str
    error_details: Optional[Dict[str, Any]] = None
    suggestions: List[str] = []