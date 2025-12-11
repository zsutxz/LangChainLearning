"""
英语学习 AI Agent 主类
"""
import json
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing_extensions import Annotated, TypedDict

from ..config import settings, ENGLISH_LEARNING_PROMPTS
from .models import (
    UserProfile,
    LearningPlan,
    VocabularySession,
    ConversationSession,
    ProgressReport,
    AssessmentResult,
    LearningSession
)


class EnglishLearningState(TypedDict):
    """英语学习工作流状态"""
    messages: Annotated[list, add_messages]

    # 输入参数
    user_id: str
    current_level: str
    learning_goals: List[str]
    target_scenario: str
    session_type: str

    # 处理结果
    assessment_result: Optional[Dict[str, Any]]
    learning_plan: Optional[Dict[str, Any]]
    session_data: Optional[Dict[str, Any]]

    # 状态控制
    error: Optional[str]
    status: str


class EnglishLearningAgent:
    """英语学习 AI Agent"""

    def __init__(self):
        self.llm = ChatOpenAI(**settings.get_llm_config())
        self.user_sessions: Dict[str, Dict[str, Any]] = {}

    async def create_learning_plan(
        self,
        user_id: str,
        current_level: str,
        learning_goals: List[str],
        target_scenario: str = "通用英语",
        study_time_per_day: int = 2,
        study_duration_weeks: int = 12
    ) -> LearningPlan:
        """创建个性化学习计划"""
        try:
            # 生成学习计划
            prompt = ENGLISH_LEARNING_PROMPTS["learning_plan"].format(
                current_level=current_level,
                learning_goals=", ".join(learning_goals),
                target_scenario=target_scenario,
                study_time=study_time_per_day,
                duration=study_duration_weeks
            )

            response = await self.llm.ainvoke(prompt)
            plan_data = json.loads(response.content)

            # 创建学习计划对象
            learning_plan = LearningPlan(
                plan_id=str(uuid.uuid4()),
                user_id=user_id,
                current_level=current_level,
                learning_goals=learning_goals,
                target_scenario=target_scenario,
                overall_goals=plan_data.get("overall_goals", []),
                milestones=[
                    WeeklyPlan(**milestone)
                    for milestone in plan_data.get("milestones", [])
                ],
                daily_schedule=plan_data.get("daily_schedule", {}),
                resources=LearningResources(**plan_data.get("resources", {})),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            # 保存到会话中
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            self.user_sessions[user_id]["learning_plan"] = learning_plan.dict()

            return learning_plan

        except Exception as e:
            raise Exception(f"创建学习计划失败: {str(e)}")

    async def assess_level(
        self,
        user_id: str,
        current_level: str,
        learning_goals: List[str],
        target_scenario: str = "通用英语"
    ) -> AssessmentResult:
        """评估英语水平"""
        try:
            prompt = ENGLISH_LEARNING_PROMPTS["level_assessment"].format(
                current_level=current_level,
                learning_goals=", ".join(learning_goals),
                target_scenario=target_scenario
            )

            response = await self.llm.ainvoke(prompt)
            assessment_data = json.loads(response.content)

            assessment = AssessmentResult(
                assessment_id=str(uuid.uuid4()),
                user_id=user_id,
                assessment_date=datetime.now(),
                current_level=assessment_data.get("current_level", current_level),
                vocabulary_level=assessment_data.get("vocabulary_level", 5),
                grammar_level=assessment_data.get("grammar_level", 5),
                listening_level=assessment_data.get("listening_level", 5),
                speaking_level=assessment_data.get("speaking_level", 5),
                reading_level=assessment_data.get("reading_level", 5),
                writing_level=assessment_data.get("writing_level", 5),
                strengths=assessment_data.get("strengths", []),
                weaknesses=assessment_data.get("weaknesses", []),
                recommendations=assessment_data.get("recommendations", [])
            )

            # 保存评估结果
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            self.user_sessions[user_id]["assessment"] = assessment.dict()

            return assessment

        except Exception as e:
            raise Exception(f"水平评估失败: {str(e)}")

    async def learn_vocabulary(
        self,
        user_id: str,
        topic: str,
        count: int = 20,
        difficulty_level: Optional[str] = None
    ) -> VocabularySession:
        """词汇学习"""
        try:
            # 获取用户当前水平
            current_level = difficulty_level
            if not current_level and user_id in self.user_sessions:
                current_level = self.user_sessions[user_id].get("assessment", {}).get("current_level", "intermediate")

            target_scenario = self.user_sessions.get(user_id, {}).get("learning_plan", {}).get("target_scenario", "通用英语")

            prompt = ENGLISH_LEARNING_PROMPTS["vocabulary_learning"].format(
                current_level=current_level or "intermediate",
                topic=topic,
                count=count,
                target_scenario=target_scenario
            )

            response = await self.llm.ainvoke(prompt)
            vocab_data = json.loads(response.content)

            # 创建词汇列表
            words = []
            for word_data in vocab_data.get("vocabulary_list", []):
                from .models import VocabularyWord
                words.append(VocabularyWord(**word_data))

            session = VocabularySession(
                session_id=str(uuid.uuid4()),
                topic=topic,
                words=words,
                learning_strategies=vocab_data.get("learning_strategies", []),
                practice_exercises=vocab_data.get("practice_exercises", []),
                created_at=datetime.now()
            )

            # 保存会话
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            if "vocabulary_sessions" not in self.user_sessions[user_id]:
                self.user_sessions[user_id]["vocabulary_sessions"] = []
            self.user_sessions[user_id]["vocabulary_sessions"].append(session.dict())

            return session

        except Exception as e:
            raise Exception(f"词汇学习失败: {str(e)}")

    async def start_conversation(
        self,
        user_id: str,
        scenario: str,
        difficulty_level: Optional[str] = None
    ) -> ConversationSession:
        """开始对话练习"""
        try:
            # 获取用户信息
            current_level = difficulty_level
            if not current_level and user_id in self.user_sessions:
                current_level = self.user_sessions[user_id].get("assessment", {}).get("current_level", "intermediate")

            learning_goals = self.user_sessions.get(user_id, {}).get("learning_plan", {}).get("learning_goals", [])

            prompt = ENGLISH_LEARNING_PROMPTS["conversation_practice"].format(
                scenario=scenario,
                difficulty_level=current_level or "intermediate",
                current_level=current_level or "intermediate",
                learning_goals=", ".join(learning_goals)
            )

            response = await self.llm.ainvoke(prompt)
            conversation_data = json.loads(response.content)

            # 创建对话回合列表
            dialogue_turns = []
            for turn_data in conversation_data.get("dialogue", []):
                from .models import DialogueTurn
                dialogue_turns.append(DialogueTurn(**turn_data))

            session = ConversationSession(
                session_id=str(uuid.uuid4()),
                scenario=scenario,
                difficulty_level=current_level or "intermediate",
                background=conversation_data.get("background", ""),
                roles=conversation_data.get("roles", []),
                dialogue=dialogue_turns,
                key_vocabulary=conversation_data.get("key_vocabulary", []),
                useful_phrases=conversation_data.get("useful_phrases", []),
                practice_tips=conversation_data.get("practice_tips", []),
                created_at=datetime.now()
            )

            # 保存会话
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            if "conversation_sessions" not in self.user_sessions[user_id]:
                self.user_sessions[user_id]["conversation_sessions"] = []
            self.user_sessions[user_id]["conversation_sessions"].append(session.dict())

            return session

        except Exception as e:
            raise Exception(f"对话练习失败: {str(e)}")

    async def practice_grammar(
        self,
        user_id: str,
        topic: str,
        difficulty_level: Optional[str] = None
    ):
        """语法练习"""
        try:
            from .models import GrammarSession, GrammarRule, CommonError, GrammarExercise

            # 获取用户信息
            current_level = difficulty_level
            if not current_level and user_id in self.user_sessions:
                current_level = self.user_sessions[user_id].get("assessment", {}).get("current_level", "intermediate")

            learning_goals = self.user_sessions.get(user_id, {}).get("learning_plan", {}).get("learning_goals", [])
            common_errors = []  # 可以从用户的练习记录中获取

            prompt = ENGLISH_LEARNING_PROMPTS["grammar_learning"].format(
                current_level=current_level or "intermediate",
                topic=topic,
                learning_goals=", ".join(learning_goals),
                common_errors=", ".join(common_errors)
            )

            response = await self.llm.ainvoke(prompt)
            grammar_data = json.loads(response.content)

            # 创建语法规则列表
            rules = []
            for rule_data in grammar_data.get("rules", []):
                rules.append(GrammarRule(**rule_data))

            # 创建常见错误列表
            errors = []
            for error_data in grammar_data.get("common_errors", []):
                errors.append(CommonError(**error_data))

            # 创建练习题列表
            exercises = []
            for exercise_data in grammar_data.get("practice_exercises", []):
                exercises.append(GrammarExercise(**exercise_data))

            session = GrammarSession(
                session_id=str(uuid.uuid4()),
                topic=topic,
                difficulty_level=current_level or "intermediate",
                explanation=grammar_data.get("explanation", ""),
                rules=rules,
                common_errors=errors,
                practice_exercises=exercises,
                learning_tips=grammar_data.get("learning_tips", []),
                created_at=datetime.now()
            )

            # 保存会话
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            if "grammar_sessions" not in self.user_sessions[user_id]:
                self.user_sessions[user_id]["grammar_sessions"] = []
            self.user_sessions[user_id]["grammar_sessions"].append(session.dict())

            return session

        except Exception as e:
            raise Exception(f"语法练习失败: {str(e)}")

    async def evaluate_progress(self, user_id: str) -> ProgressReport:
        """评估学习进度"""
        try:
            from .models import ProgressMetrics, Achievement

            user_data = self.user_sessions.get(user_id, {})

            # 收集学习数据
            initial_level = user_data.get("assessment", {}).get("current_level", "beginner")
            current_level = user_data.get("assessment", {}).get("current_level", "beginner")
            study_duration = 1  # 计算实际学习周数
            completed_activities = []  # 收集完成的活动
            test_scores = []  # 收集测试成绩

            # 计算进度指标
            vocabulary_mastered = len(user_data.get("vocabulary_sessions", [])) * 20  # 估算
            grammar_completed = len(user_data.get("grammar_sessions", []))
            conversations_practiced = len(user_data.get("conversation_sessions", []))

            prompt = ENGLISH_LEARNING_PROMPTS["progress_evaluation"].format(
                initial_level=initial_level,
                current_level=current_level,
                study_duration=study_duration,
                completed_activities=", ".join(completed_activities),
                test_scores=", ".join(map(str, test_scores))
            )

            response = await self.llm.ainvoke(prompt)
            progress_data = json.loads(response.content)

            # 创建成就列表
            achievements = []
            for achievement_data in progress_data.get("achievements", []):
                achievements.append(Achievement(
                    badge_id=str(uuid.uuid4()),
                    name=achievement_data,
                    description=f"获得成就: {achievement_data}",
                    earned_at=datetime.now()
                ))

            # 创建进度指标
            metrics = ProgressMetrics(
                vocabulary_mastered=vocabulary_mastered,
                grammar_completed=grammar_completed,
                conversations_practiced=conversations_practiced,
                study_hours_total=study_duration * 7 * 2,  # 假设每天2小时
                average_session_length=45.0,  # 平均45分钟
                streak_days=study_duration * 7
            )

            report = ProgressReport(
                report_id=str(uuid.uuid4()),
                user_id=user_id,
                report_date=datetime.now(),
                overall_progress=progress_data.get("overall_progress", ""),
                improvement_areas=progress_data.get("improvement_areas", {}),
                achievements=achievements,
                areas_for_improvement=progress_data.get("areas_for_improvement", []),
                next_steps=progress_data.get("next_steps", []),
                motivational_feedback=progress_data.get("motivational_feedback", ""),
                study_efficiency_score=progress_data.get("study_efficiency_score", 80),
                metrics=metrics
            )

            # 保存进度报告
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            self.user_sessions[user_id]["progress_report"] = report.dict()

            return report

        except Exception as e:
            raise Exception(f"进度评估失败: {str(e)}")

    async def interactive_conversation(
        self,
        user_id: str,
        session_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """交互式对话"""
        try:
            # 获取对话会话
            session_data = None
            for session in self.user_sessions.get(user_id, {}).get("conversation_sessions", []):
                if session.get("session_id") == session_id:
                    session_data = session
                    break

            if not session_data:
                raise Exception("对话会话不存在")

            # 根据用户消息生成AI回复
            conversation_context = f"""
            场景: {session_data.get('scenario')}
            难度级别: {session_data.get('difficulty_level')}
            用户消息: {user_message}

            请作为英语对话伙伴，自然地回应用户的消息，并提供：
            1. 自然的英语回复
            2. 如果用户有语法错误，提供纠正建议
            3. 相关的表达建议
            """

            response = await self.llm.ainvoke(conversation_context)

            return {
                "session_id": session_id,
                "ai_response": response.content,
                "user_message": user_message,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            raise Exception(f"对话交互失败: {str(e)}")

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户档案"""
        return self.user_sessions.get(user_id)

    def clear_user_data(self, user_id: str):
        """清除用户数据"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]