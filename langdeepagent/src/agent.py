"""
英语学习 AI Agent 主类
"""
import json
import asyncio
import uuid
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from config import settings, ENGLISH_LEARNING_PROMPTS
from src.models import (
    UserProfile,
    LearningPlan,
    VocabularySession,
    ConversationSession,
    ProgressReport,
    AssessmentResult,
    LearningSession,
    VocabularyWord,
    DialogueTurn,
    GrammarSession,
    GrammarRule,
    CommonError,
    GrammarExercise,
    WeeklyPlan,
    LearningResources,
    ProgressMetrics,
    Achievement
)


async def safe_api_call(llm, prompt: str, timeout: int = 60) -> Optional[Any]:
    """
    安全的API调用，带有超时和取消处理

    Args:
        llm: 语言模型实例
        prompt: 提示词
        timeout: 超时时间（秒）

    Returns:
        API响应或None（如果被取消或超时）
    """
    try:
        # 使用asyncio.wait_for添加超时
        response = await asyncio.wait_for(
            llm.ainvoke(prompt),
            timeout=timeout
        )
        return response
    except asyncio.TimeoutError:
        try:
            print("⚠️ API调用超时，请稍后重试")
        except UnicodeEncodeError:
            print("API调用超时，请稍后重试")
        return None
    except asyncio.CancelledError:
        # 用户取消操作，静默处理
        return None
    except Exception as e:
        try:
            print(f"⚠️ API调用失败: {str(e)}")
        except UnicodeEncodeError:
            print("API调用失败: " + str(e).encode('ascii', 'ignore').decode('ascii'))
        return None


def safe_json_parse(response_content: str, fallback_data: dict = None) -> dict:
    """
    安全解析JSON响应，带有回退机制

    Args:
        response_content: LLM响应内容
        fallback_data: 解析失败时的默认数据

    Returns:
        解析后的字典或回退数据
    """
    if fallback_data is None:
        fallback_data = {}

    # 首先尝试直接解析
    try:
        return json.loads(response_content.strip())
    except json.JSONDecodeError:
        pass

    # 尝试提取JSON代码块
    try:
        # 查找 ```json...``` 代码块
        json_match = re.search(r'```json\s*\n(.*?)\n```', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1).strip())
    except json.JSONDecodeError:
        pass

    try:
        # 查找 ```...``` 代码块
        json_match = re.search(r'```\s*\n(.*?)\n```', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1).strip())
    except json.JSONDecodeError:
        pass

    # 尝试查找花括号包围的JSON
    try:
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except json.JSONDecodeError:
        pass

    # 最后尝试清理文本并解析
    try:
        # 移除markdown标记和多余空白
        cleaned = re.sub(r'```json\s*|```|\*\*|\*|#', '', response_content)
        cleaned = cleaned.strip()
        if cleaned.startswith('{') and cleaned.endswith('}'):
            return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 所有尝试都失败，记录警告并返回回退数据
    print(f"⚠️ JSON解析失败，使用默认数据。响应内容: {response_content[:200]}...")
    return fallback_data


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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                plan_data = {
                    "overall_goals": [f"提升{target_scenario}英语能力"],
                    "milestones": [],
                    "daily_schedule": {
                        "vocabulary": "每日学习30分钟",
                        "grammar": "每日学习30分钟",
                        "listening": "每日练习15分钟",
                        "speaking": "每日练习15分钟",
                        "reading": "每日阅读30分钟",
                        "writing": "每日写作15分钟"
                    },
                    "resources": {
                        "textbooks": ["新概念英语", "剑桥商务英语"],
                        "websites": ["BBC Learning English", "VOA Learning English"],
                        "apps": ["Duolingo", "多邻国"],
                        "videos": ["YouTube英语频道"]
                    }
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "overall_goals": [f"提升{target_scenario}英语能力"],
                    "milestones": [],
                    "daily_schedule": {
                        "vocabulary": "每日学习30分钟",
                        "grammar": "每日学习30分钟",
                        "listening": "每日练习15分钟",
                        "speaking": "每日练习15分钟",
                        "reading": "每日阅读30分钟",
                        "writing": "每日写作15分钟"
                    },
                    "resources": {
                        "textbooks": ["新概念英语", "剑桥商务英语"],
                        "websites": ["BBC Learning English", "VOA Learning English"],
                        "apps": ["Duolingo", "多邻国"],
                        "videos": ["YouTube英语频道"]
                    }
                }
                plan_data = safe_json_parse(response.content, fallback_data)

            # 创建学习计划对象
            milestones = []
            for milestone in plan_data.get("milestones", []):
                # 确保 milestone 有所有必需的字段
                milestone_data = milestone.copy()
                if 'estimated_hours' not in milestone_data:
                    milestone_data['estimated_hours'] = study_time_per_day * 7  # 每周估算学习时间
                milestones.append(WeeklyPlan(**milestone_data))

            learning_plan = LearningPlan(
                plan_id=str(uuid.uuid4()),
                user_id=user_id,
                current_level=current_level,
                learning_goals=learning_goals,
                target_scenario=target_scenario,
                overall_goals=plan_data.get("overall_goals", []),
                milestones=milestones,
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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                assessment_data = {
                    "current_level": current_level,
                    "vocabulary_level": 5,
                    "grammar_level": 5,
                    "listening_level": 5,
                    "speaking_level": 5,
                    "reading_level": 5,
                    "writing_level": 5,
                    "strengths": ["学习热情高", "有明确目标"],
                    "weaknesses": ["需要更多练习"],
                    "recommendations": ["坚持每日学习", "多进行听说练习"]
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "current_level": current_level,
                    "vocabulary_level": 5,
                    "grammar_level": 5,
                    "listening_level": 5,
                    "speaking_level": 5,
                    "reading_level": 5,
                    "writing_level": 5,
                    "strengths": ["学习热情高", "有明确目标"],
                    "weaknesses": ["需要更多练习"],
                    "recommendations": ["坚持每日学习", "多进行听说练习"]
                }
                assessment_data = safe_json_parse(response.content, fallback_data)

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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                vocab_data = {
                    "vocabulary_list": [],
                    "learning_strategies": [
                        "使用闪卡记忆单词",
                        "在语境中学习单词",
                        "定期复习已学词汇"
                    ],
                    "practice_exercises": [],
                    "review_schedule": "每日复习前一天的词汇"
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "vocabulary_list": [],
                    "learning_strategies": [
                        "使用闪卡记忆单词",
                        "在语境中学习单词",
                        "定期复习已学词汇"
                    ],
                    "practice_exercises": [],
                    "review_schedule": "每日复习前一天的词汇"
                }
                vocab_data = safe_json_parse(response.content, fallback_data)

            # 创建词汇列表
            words = []
            for word_data in vocab_data.get("vocabulary_list", []):
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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                conversation_data = {
                    "scenario": scenario,
                    "background": f"这是一个关于{scenario}的对话练习场景",
                    "roles": [
                        {
                            "name": "用户",
                            "description": "想要练习英语对话的学习者"
                        },
                        {
                            "name": "助手",
                            "description": "帮助用户练习英语对话的AI助手"
                        }
                    ],
                    "dialogue": [],
                    "key_vocabulary": [],
                    "useful_phrases": [],
                    "practice_tips": [
                        "尽量用完整的句子回答",
                        "不要害怕犯错",
                        "可以请求对方重复或澄清"
                    ]
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "scenario": scenario,
                    "background": f"这是一个关于{scenario}的对话练习场景",
                    "roles": [
                        {
                            "name": "用户",
                            "description": "想要练习英语对话的学习者"
                        },
                        {
                            "name": "助手",
                            "description": "帮助用户练习英语对话的AI助手"
                        }
                    ],
                    "dialogue": [],
                    "key_vocabulary": [],
                    "useful_phrases": [],
                    "practice_tips": [
                        "尽量用完整的句子回答",
                        "不要害怕犯错",
                        "可以请求对方重复或澄清"
                    ]
                }
                conversation_data = safe_json_parse(response.content, fallback_data)

            # 创建对话回合列表
            dialogue_turns = []
            for turn_data in conversation_data.get("dialogue", []):
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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                grammar_data = {
                    "grammar_topic": topic,
                    "difficulty_level": current_level or "intermediate",
                    "explanation": f"这是关于{topic}的语法学习内容",
                    "rules": [],
                    "common_errors": [],
                    "practice_exercises": [],
                    "learning_tips": [
                        "理解语法规则是基础",
                        "多练习加深印象",
                        "在真实语境中运用"
                    ]
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "grammar_topic": topic,
                    "difficulty_level": current_level or "intermediate",
                    "explanation": f"这是关于{topic}的语法学习内容",
                    "rules": [],
                    "common_errors": [],
                    "practice_exercises": [],
                    "learning_tips": [
                        "理解语法规则是基础",
                        "多练习加深印象",
                        "在真实语境中运用"
                    ]
                }
                grammar_data = safe_json_parse(response.content, fallback_data)

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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, prompt, timeout=settings.TIMEOUT)
            if response is None:
                # API调用被取消或失败，使用回退数据
                progress_data = {
                    "overall_progress": "学习进度良好，继续保持",
                    "improvement_areas": {
                        "vocabulary": "词汇量有所提升",
                        "grammar": "语法掌握程度中等",
                        "listening": "听力理解能力逐步提高",
                        "speaking": "口语表达能力需要更多练习",
                        "reading": "阅读理解能力稳定",
                        "writing": "写作基础技能正在发展"
                    },
                    "achievements": ["坚持学习", "完成学习计划"],
                    "areas_for_improvement": ["加强口语练习", "扩大词汇量"],
                    "next_steps": ["继续按计划学习", "增加实践机会"],
                    "motivational_feedback": "你的学习态度很好，继续保持这种势头！",
                    "study_efficiency_score": 75
                }
            else:
                # 安全解析JSON响应，提供回退数据
                fallback_data = {
                    "overall_progress": "学习进度良好，继续保持",
                    "improvement_areas": {
                        "vocabulary": "词汇量有所提升",
                        "grammar": "语法掌握程度中等",
                        "listening": "听力理解能力逐步提高",
                        "speaking": "口语表达能力需要更多练习",
                        "reading": "阅读理解能力稳定",
                        "writing": "写作基础技能正在发展"
                    },
                    "achievements": ["坚持学习", "完成学习计划"],
                    "areas_for_improvement": ["加强口语练习", "扩大词汇量"],
                    "next_steps": ["继续按计划学习", "增加实践机会"],
                    "motivational_feedback": "你的学习态度很好，继续保持这种势头！",
                    "study_efficiency_score": 75
                }
                progress_data = safe_json_parse(response.content, fallback_data)

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

            # 使用安全的API调用
            response = await safe_api_call(self.llm, conversation_context, timeout=30)
            if response is None:
                return {
                    "session_id": session_id,
                    "ai_response": "抱歉，当前无法处理您的请求，请稍后再试。",
                    "user_message": user_message,
                    "timestamp": datetime.now().isoformat(),
                    "error": True
                }

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