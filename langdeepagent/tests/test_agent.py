"""
英语学习 Agent 测试
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import EnglishLearningAgent
from src.models import VocabularySession, ConversationSession, LearningPlan


class TestEnglishLearningAgent:
    """英语学习 Agent 测试类"""

    @pytest.fixture
    def agent(self):
        """创建 Agent 实例"""
        with patch('src.agent.ChatOpenAI'):
            return EnglishLearningAgent()

    @pytest.mark.asyncio
    async def test_assess_level(self, agent):
        """测试水平评估"""
        # 模拟 LLM 响应
        mock_response = Mock()
        mock_response.content = """
        {
            "current_level": "中级",
            "vocabulary_level": 6,
            "grammar_level": 5,
            "listening_level": 6,
            "speaking_level": 5,
            "reading_level": 7,
            "writing_level": 5,
            "strengths": ["词汇量适中", "阅读能力强"],
            "weaknesses": ["口语表达不够流畅", "语法准确性需提高"],
            "recommendations": ["增加口语练习", "加强语法基础"]
        }
        """

        with patch.object(agent.llm, 'ainvoke', return_value=mock_response):
            assessment = await agent.assess_level(
                user_id="test_user",
                current_level="intermediate",
                learning_goals=["商务英语"],
                target_scenario="商务会议"
            )

            assert assessment is not None
            assert assessment.user_id == "test_user"
            assert assessment.current_level == "中级"
            assert len(assessment.strengths) > 0
            assert len(assessment.recommendations) > 0

    @pytest.mark.asyncio
    async def test_create_learning_plan(self, agent):
        """测试创建学习计划"""
        # 模拟 LLM 响应
        mock_response = Mock()
        mock_response.content = """
        {
            "overall_goals": ["提升商务英语能力", "增强日常对话"],
            "milestones": [
                {
                    "week": 1,
                    "goals": ["学习商务词汇", "练习基本对话"],
                    "vocabulary_focus": "商务问候语",
                    "grammar_focus": "现在时态",
                    "practice_activities": ["角色扮演", "词汇测试"],
                    "estimated_hours": 10
                }
            ],
            "daily_schedule": {
                "vocabulary": "每天30分钟",
                "grammar": "每天20分钟",
                "listening": "每天15分钟",
                "speaking": "每天25分钟",
                "reading": "每天20分钟",
                "writing": "每天10分钟"
            },
            "resources": {
                "textbooks": ["商务英语教程"],
                "websites": ["BBC Learning English"],
                "apps": ["Duolingo"],
                "videos": ["商务英语视频"]
            }
        }
        """

        with patch.object(agent.llm, 'ainvoke', return_value=mock_response):
            plan = await agent.create_learning_plan(
                user_id="test_user",
                current_level="intermediate",
                learning_goals=["商务英语"],
                target_scenario="商务会议",
                study_time_per_day=2,
                study_duration_weeks=8
            )

            assert plan is not None
            assert plan.user_id == "test_user"
            assert plan.current_level == "intermediate"
            assert len(plan.milestones) > 0
            assert len(plan.overall_goals) > 0

    @pytest.mark.asyncio
    async def test_learn_vocabulary(self, agent):
        """测试词汇学习"""
        # 模拟 LLM 响应
        mock_response = Mock()
        mock_response.content = """
        {
            "vocabulary_list": [
                {
                    "word": "meeting",
                    "phonetic": "/ˈmiːtɪŋ/",
                    "part_of_speech": "noun",
                    "definition": "会议，会面",
                    "example_sentence": "We have a meeting at 3 PM.",
                    "synonyms": ["conference", "appointment"],
                    "antonyms": [],
                    "memory_tips": "meet + ing，见面的事就是会议",
                    "difficulty_level": 2
                },
                {
                    "word": "presentation",
                    "phonetic": "/ˌprezənˈteɪʃn/",
                    "part_of_speech": "noun",
                    "definition": "演示，报告",
                    "example_sentence": "She gave a great presentation.",
                    "synonyms": ["demonstration", "report"],
                    "antonyms": [],
                    "memory_tips": "present + ation，呈现出来的东西",
                    "difficulty_level": 3
                }
            ],
            "learning_strategies": ["词根记忆法", "语境记忆法"],
            "practice_exercises": [
                {
                    "type": "填空题",
                    "content": "We have a ___ at 3 PM.",
                    "answer": "meeting"
                }
            ],
            "review_schedule": "每天复习，每周测试"
        }
        """

        with patch.object(agent.llm, 'ainvoke', return_value=mock_response):
            session = await agent.learn_vocabulary(
                user_id="test_user",
                topic="商务词汇",
                count=10
            )

            assert session is not None
            assert session.topic == "商务词汇"
            assert len(session.words) == 2
            assert session.words[0].word == "meeting"
            assert len(session.learning_strategies) > 0

    @pytest.mark.asyncio
    async def test_start_conversation(self, agent):
        """测试对话练习"""
        # 模拟 LLM 响应
        mock_response = Mock()
        mock_response.content = """
        {
            "scenario": "餐厅点餐",
            "background": "顾客在餐厅想要点餐，与服务员交流",
            "roles": [
                {
                    "name": "顾客",
                    "description": "想要点餐的客人",
                    "personality": "礼貌，友好"
                },
                {
                    "name": "服务员",
                    "description": "餐厅服务员",
                    "personality": "专业，热情"
                }
            ],
            "dialogue": [
                {
                    "speaker": "服务员",
                    "text": "Good evening, welcome to our restaurant.",
                    "translation": "晚上好，欢迎来到我们餐厅。",
                    "key_expressions": ["Good evening", "welcome to"],
                    "cultural_notes": "在英语中，服务员通常会很友好地问候客人"
                },
                {
                    "speaker": "顾客",
                    "text": "Good evening. I'd like to see the menu, please.",
                    "translation": "晚上好。我想看看菜单，谢谢。",
                    "key_expressions": ["I'd like to", "see the menu"],
                    "cultural_notes": "使用 'I'd like to' 比 'I want' 更礼貌"
                }
            ],
            "key_vocabulary": ["menu", "order", "dish", "restaurant"],
            "useful_phrases": ["I'd like to order", "What do you recommend?", "Can I have the bill?"],
            "practice_tips": ["注意使用礼貌用语", "学会询问推荐菜品"],
            "extension_activities": ["角色扮演练习", "观看餐厅对话视频"]
        }
        """

        with patch.object(agent.llm, 'ainvoke', return_value=mock_response):
            session = await agent.start_conversation(
                user_id="test_user",
                scenario="餐厅点餐",
                difficulty_level="beginner"
            )

            assert session is not None
            assert session.scenario == "餐厅点餐"
            assert session.difficulty_level == "beginner"
            assert len(session.dialogue) == 2
            assert len(session.roles) == 2
            assert len(session.key_vocabulary) > 0

    def test_user_profile_management(self, agent):
        """测试用户档案管理"""
        # 测试空用户档案
        profile = agent.get_user_profile("non_existent_user")
        assert profile is None

        # 测试清除用户数据
        agent.user_sessions["test_user"] = {"data": "test"}
        agent.clear_user_data("test_user")
        assert agent.get_user_profile("test_user") is None

    @pytest.mark.asyncio
    async def test_error_handling(self, agent):
        """测试错误处理"""
        # 模拟 LLM 调用异常
        with patch.object(agent.llm, 'ainvoke', side_effect=Exception("API 错误")):
            with pytest.raises(Exception) as exc_info:
                await agent.assess_level(
                    user_id="test_user",
                    current_level="intermediate",
                    learning_goals=["英语学习"],
                    target_scenario="通用"
                )

            assert "水平评估失败" in str(exc_info.value)


# 简单的测试运行器
if __name__ == "__main__":
    print("🧪 运行英语学习 Agent 测试")

    # 设置 Windows 兼容性
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # 运行测试
    pytest.main([__file__, "-v"])