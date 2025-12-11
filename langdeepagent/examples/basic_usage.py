"""
LangDeepAgent 基础使用示例
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import EnglishLearningAgent


async def basic_example():
    """基础使用示例"""
    print("🤖 LangDeepAgent 基础使用示例")
    print("=" * 50)

    # 创建英语学习助手
    agent = EnglishLearningAgent()
    user_id = "example_user"

    try:
        # 1. 水平评估
        print("\n🧠 1. 英语水平评估...")
        assessment = await agent.assess_level(
            user_id=user_id,
            current_level="intermediate",
            learning_goals=["商务英语", "日常对话"],
            target_scenario="商务会议"
        )
        print(f"✅ 评估完成！当前水平: {assessment.current_level}")

        # 2. 创建学习计划
        print("\n📋 2. 创建个性化学习计划...")
        plan = await agent.create_learning_plan(
            user_id=user_id,
            current_level="intermediate",
            learning_goals=["商务英语", "日常对话"],
            target_scenario="商务会议",
            study_time_per_day=2,
            study_duration_weeks=8
        )
        print(f"✅ 学习计划创建成功！包含 {len(plan.milestones)} 周计划")

        # 3. 词汇学习
        print("\n📚 3. 词汇学习...")
        vocab_session = await agent.learn_vocabulary(
            user_id=user_id,
            topic="商务词汇",
            count=15
        )
        print(f"✅ 词汇学习完成！学习了 {len(vocab_session.words)} 个单词")

        # 显示部分词汇
        print("\n📖 学习的词汇示例:")
        for i, word in enumerate(vocab_session.words[:5], 1):
            print(f"{i}. {word.word} - {word.definition}")
            print(f"   例句: {word.example_sentence}")

        # 4. 对话练习
        print("\n💬 4. 对话练习...")
        conv_session = await agent.start_conversation(
            user_id=user_id,
            scenario="商务会议讨论",
            difficulty_level="intermediate"
        )
        print(f"✅ 对话练习场景创建成功！")

        # 显示对话示例
        print("\n📝 对话示例:")
        for i, turn in enumerate(conv_session.dialogue[:3], 1):
            print(f"{turn.speaker}: {turn.text}")
            if turn.key_expressions:
                print(f"   💎 重点表达: {', '.join(turn.key_expressions)}")

        # 5. 进度评估
        print("\n📊 5. 学习进度评估...")
        progress = await agent.evaluate_progress(user_id)
        print(f"✅ 进度报告生成成功！")
        print(f"   总体进度: {progress.overall_progress}")
        print(f"   学习效率评分: {progress.study_efficiency_score}/100")

        print("\n🎉 基础使用示例完成！")

        # 6. 显示用户档案摘要
        user_profile = agent.get_user_profile(user_id)
        if user_profile:
            print("\n📋 用户学习档案摘要:")
            print(f"   词汇会话: {len(user_profile.get('vocabulary_sessions', []))}")
            print(f"   对话会话: {len(user_profile.get('conversation_sessions', []))}")
            print(f"   语法会话: {len(user_profile.get('grammar_sessions', []))}")

    except Exception as e:
        print(f"❌ 示例执行失败: {str(e)}")


async def conversation_example():
    """对话练习示例"""
    print("\n💬 对话练习详细示例")
    print("=" * 50)

    agent = EnglishLearningAgent()
    user_id = "conversation_example"

    try:
        # 创建多个场景的对话练习
        scenarios = [
            ("餐厅点餐", "beginner"),
            ("机场问询", "intermediate"),
            ("工作面试", "advanced"),
            ("商务谈判", "advanced")
        ]

        for scenario, level in scenarios:
            print(f"\n🎭 场景: {scenario} ({level})")
            session = await agent.start_conversation(
                user_id=user_id,
                scenario=scenario,
                difficulty_level=level
            )

            print(f"   背景描述: {session.background}")
            print(f"   关键词汇: {', '.join(session.key_vocabulary[:5])}")

    except Exception as e:
        print(f"❌ 对话示例失败: {str(e)}")


async def vocabulary_example():
    """词汇学习详细示例"""
    print("\n📚 词汇学习详细示例")
    print("=" * 50)

    agent = EnglishLearningAgent()
    user_id = "vocabulary_example"

    try:
        # 不同主题的词汇学习
        topics = [
            "日常用品",
            "商务英语",
            "旅游词汇",
            "科技词汇"
        ]

        for topic in topics:
            print(f"\n📖 主题: {topic}")
            session = await agent.learn_vocabulary(
                user_id=user_id,
                topic=topic,
                count=10
            )

            print(f"   学习了 {len(session.words)} 个单词")
            if session.learning_strategies:
                print(f"   学习策略: {session.learning_strategies[0]}")

            # 显示第一个单词的详细信息
            if session.words:
                word = session.words[0]
                print(f"   示例单词: {word.word}")
                print(f"   词义: {word.definition}")
                print(f"   难度: {word.difficulty_level}/5")

    except Exception as e:
        print(f"❌ 词汇示例失败: {str(e)}")


async def main():
    """主函数"""
    print("🚀 LangDeepAgent 使用示例集")
    print("=" * 60)

    try:
        # 运行基础示例
        await basic_example()

        # 运行对话示例
        await conversation_example()

        # 运行词汇示例
        await vocabulary_example()

        print("\n✅ 所有示例执行完成！")
        print("\n💡 提示:")
        print("1. 确保 .env 文件中配置了有效的 API 密钥")
        print("2. 可以修改示例中的参数来尝试不同场景")
        print("3. 查看 README.md 了解更多功能")

    except Exception as e:
        print(f"❌ 示例执行失败: {str(e)}")
        if os.getenv("DEBUG", "false").lower() == "true":
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 设置 Windows 兼容性
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(main())