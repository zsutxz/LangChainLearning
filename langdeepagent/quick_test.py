"""
快速测试 LangDeepAgent 功能
"""
import asyncio
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent import EnglishLearningAgent
from config import settings


async def test_basic_functionality():
    """测试基础功能"""
    print("LangDeepAgent 快速测试")
    print("=" * 40)

    # 检查配置
    if not settings.validate_config():
        print("配置验证失败！")
        print("请确保在 .env 文件中设置了有效的 API 密钥")
        return

    print("配置验证通过")

    # 创建 Agent
    agent = EnglishLearningAgent()
    user_id = "test_user"

    try:
        print("\n测试水平评估...")
        assessment = await agent.assess_level(
            user_id=user_id,
            current_level="intermediate",
            learning_goals=["商务英语"],
            target_scenario="商务会议"
        )
        print(f"水平评估完成！当前水平: {assessment.current_level}")

        print("\n测试词汇学习...")
        vocab_session = await agent.learn_vocabulary(
            user_id=user_id,
            topic="商务词汇",
            count=5  # 使用小数量进行快速测试
        )
        print(f"词汇学习完成！学习了 {len(vocab_session.words)} 个单词")

        print("\n测试对话练习...")
        conv_session = await agent.start_conversation(
            user_id=user_id,
            scenario="餐厅点餐",
            difficulty_level="beginner"
        )
        print(f"对话练习完成！场景: {conv_session.scenario}")

        print("\n所有基础功能测试通过！")

        # 显示用户档案摘要
        profile = agent.get_user_profile(user_id)
        if profile:
            print(f"\n用户档案摘要:")
            print(f"   词汇会话: {len(profile.get('vocabulary_sessions', []))}")
            print(f"   对话会话: {len(profile.get('conversation_sessions', []))}")

    except Exception as e:
        print(f"测试失败: {str(e)}")
        if settings.DEBUG:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 设置 Windows 兼容性
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(test_basic_functionality())