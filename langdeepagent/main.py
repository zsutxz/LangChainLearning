"""
LangDeepAgent 主程序入口
"""
import asyncio
import argparse
import sys
import json
from typing import List, Optional

from src.agent import EnglishLearningAgent
from config import settings


class LangDeepAgentCLI:
    """LangDeepAgent 命令行界面"""

    def __init__(self):
        self.agent = EnglishLearningAgent()

    async def create_plan_command(self, args):
        """创建学习计划命令"""
        try:
            goals = args.goals.split(',') if args.goals else ["日常英语交流"]
            plan = await self.agent.create_learning_plan(
                user_id=args.user_id or "demo_user",
                current_level=args.level,
                learning_goals=goals,
                target_scenario=args.scenario,
                study_time_per_day=args.time,
                study_duration_weeks=args.duration
            )

            print("🎯 学习计划生成成功！")
            print("=" * 60)
            print(f"用户ID: {plan.user_id}")
            print(f"当前水平: {plan.current_level}")
            print(f"学习目标: {', '.join(plan.learning_goals)}")
            print(f"目标场景: {plan.target_scenario}")
            print(f"计划ID: {plan.plan_id}")
            print("=" * 60)

            print("\n📚 总体目标:")
            for i, goal in enumerate(plan.overall_goals, 1):
                print(f"{i}. {goal}")

            print(f"\n📅 学习期限: {len(plan.milestones)} 周")
            print("🌟 推荐资源:")
            resources = plan.resources
            if resources.textbooks:
                print(f"  教材: {', '.join(resources.textbooks)}")
            if resources.websites:
                print(f"  网站: {', '.join(resources.websites)}")
            if resources.apps:
                print(f"  应用: {', '.join(resources.apps)}")

            return plan

        except Exception as e:
            print(f"❌ 创建学习计划失败: {str(e)}")
            return None

    async def assess_command(self, args):
        """水平评估命令"""
        try:
            goals = args.goals.split(',') if args.goals else ["提升英语能力"]
            assessment = await self.agent.assess_level(
                user_id=args.user_id or "demo_user",
                current_level=args.level,
                learning_goals=goals,
                target_scenario=args.scenario
            )

            print("🧠 英语水平评估完成！")
            print("=" * 60)
            print(f"评估ID: {assessment.assessment_id}")
            print(f"评估时间: {assessment.assessment_date}")
            print(f"当前水平: {assessment.current_level}")
            print("=" * 60)

            print("\n📊 能力评分 (1-10分):")
            scores = [
                ("词汇", assessment.vocabulary_level),
                ("语法", assessment.grammar_level),
                ("听力", assessment.listening_level),
                ("口语", assessment.speaking_level),
                ("阅读", assessment.reading_level),
                ("写作", assessment.writing_level)
            ]
            for skill, score in scores:
                bar = "█" * score + "░" * (10 - score)
                print(f"  {skill}: {bar} {score}/10")

            if assessment.strengths:
                print(f"\n💪 优势领域:")
                for strength in assessment.strengths:
                    print(f"  • {strength}")

            if assessment.weaknesses:
                print(f"\n📈 需要提升:")
                for weakness in assessment.weaknesses:
                    print(f"  • {weakness}")

            if assessment.recommendations:
                print(f"\n💡 学习建议:")
                for rec in assessment.recommendations:
                    print(f"  • {rec}")

            return assessment

        except Exception as e:
            print(f"❌ 水平评估失败: {str(e)}")
            return None

    async def vocabulary_command(self, args):
        """词汇学习命令"""
        try:
            session = await self.agent.learn_vocabulary(
                user_id=args.user_id or "demo_user",
                topic=args.topic,
                count=args.count,
                difficulty_level=args.level
            )

            print(f"📚 词汇学习: {session.topic}")
            print("=" * 60)
            print(f"会话ID: {session.session_id}")
            print(f"词汇数量: {len(session.words)}")
            print("=" * 60)

            print(f"\n📖 核心词汇:")
            for i, word in enumerate(session.words[:10], 1):  # 显示前10个
                print(f"{i}. {word.word} [{word.part_of_speech}]")
                print(f"   {word.definition}")
                print(f"   例句: {word.example_sentence}")
                if word.memory_tips:
                    print(f"   💡 记忆技巧: {word.memory_tips}")
                print()

            if len(session.words) > 10:
                print(f"... 还有 {len(session.words) - 10} 个词汇")

            if session.learning_strategies:
                print(f"\n🎯 学习策略:")
                for strategy in session.learning_strategies:
                    print(f"  • {strategy}")

            return session

        except Exception as e:
            print(f"❌ 词汇学习失败: {str(e)}")
            return None

    async def conversation_command(self, args):
        """对话练习命令"""
        try:
            session = await self.agent.start_conversation(
                user_id=args.user_id or "demo_user",
                scenario=args.scenario,
                difficulty_level=args.level
            )

            print(f"💬 对话练习: {session.scenario}")
            print("=" * 60)
            print(f"会话ID: {session.session_id}")
            print(f"难度级别: {session.difficulty_level}")
            print("=" * 60)

            print(f"\n🎭 场景背景:")
            print(f"  {session.background}")

            if session.roles:
                print(f"\n👥 角色设定:")
                for role in session.roles:
                    print(f"  • {role.get('name', '未知')}: {role.get('description', '无描述')}")

            print(f"\n📝 对话示例:")
            for i, turn in enumerate(session.dialogue[:5], 1):  # 显示前5轮
                print(f"{turn.speaker}: {turn.text}")
                if turn.translation:
                    print(f"        {turn.translation}")
                if turn.key_expressions:
                    print(f"        💎 重点表达: {', '.join(turn.key_expressions)}")
                print()

            if session.key_vocabulary:
                print(f"🔑 关键词汇: {', '.join(session.key_vocabulary)}")

            if session.useful_phrases:
                print(f"🌟 实用短语: {', '.join(session.useful_phrases)}")

            return session

        except Exception as e:
            print(f"❌ 对话练习失败: {str(e)}")
            return None

    async def progress_command(self, args):
        """进度查询命令"""
        try:
            report = await self.agent.evaluate_progress(
                user_id=args.user_id or "demo_user"
            )

            print("📊 学习进度报告")
            print("=" * 60)
            print(f"报告ID: {report.report_id}")
            print(f"报告日期: {report.report_date}")
            print("=" * 60)

            print(f"\n📈 总体进度: {report.overall_progress}")
            print(f"⭐ 学习效率评分: {report.study_efficiency_score}/100")

            print(f"\n📚 学习数据:")
            metrics = report.metrics
            print(f"  • 掌握词汇: {metrics.vocabulary_mastered} 个")
            print(f"  • 完成语法: {metrics.grammar_completed} 个主题")
            print(f"  • 对话练习: {metrics.conversations_practiced} 次")
            print(f"  • 学习时长: {metrics.study_hours_total:.1f} 小时")
            print(f"  • 连续学习: {metrics.streak_days} 天")

            if report.achievements:
                print(f"\n🏆 获得成就:")
                for achievement in report.achievements:
                    print(f"  • {achievement.name}")

            if report.areas_for_improvement:
                print(f"\n🎯 下一步重点:")
                for area in report.areas_for_improvement:
                    print(f"  • {area}")

            if report.motivational_feedback:
                print(f"\n💪 激励反馈:")
                print(f"  {report.motivational_feedback}")

            return report

        except Exception as e:
            print(f"❌ 进度查询失败: {str(e)}")
            return None

    async def interactive_mode(self):
        """交互模式"""
        print("🤖 LangDeepAgent 英语学习助手 - 交互模式")
        print("=" * 60)

        user_id = input("请输入用户ID (直接回车使用默认): ").strip() or "demo_user"

        while True:
            try:
                print(f"\n📋 可用命令:")
                print("  1. plan - 创建学习计划")
                print("  2. assess - 水平评估")
                print("  3. vocab - 词汇学习")
                print("  4. conv - 对话练习")
                print("  5. progress - 查看进度")
                print("  6. quit - 退出")

                choice = input("\n请选择功能 (1-6): ").strip()

                if choice == "1":
                    level = input("当前水平 (beginner/intermediate/advanced): ").strip() or "intermediate"
                    goals = input("学习目标 (用逗号分隔): ").strip() or "日常英语交流"
                    scenario = input("目标场景: ").strip() or "通用英语"

                    plan = await self.agent.create_learning_plan(
                        user_id=user_id,
                        current_level=level,
                        learning_goals=goals.split(','),
                        target_scenario=scenario
                    )
                    if plan:
                        print("✅ 学习计划创建成功！")

                elif choice == "2":
                    level = input("当前水平 (beginner/intermediate/advanced): ").strip() or "intermediate"
                    goals = input("学习目标 (用逗号分隔): ").strip() or "提升英语能力"

                    assessment = await self.agent.assess_level(
                        user_id=user_id,
                        current_level=level,
                        learning_goals=goals.split(',')
                    )
                    if assessment:
                        print("✅ 水平评估完成！")

                elif choice == "3":
                    topic = input("学习主题: ").strip() or "日常词汇"
                    count = int(input("学习数量: ").strip() or "20")

                    session = await self.agent.learn_vocabulary(
                        user_id=user_id,
                        topic=topic,
                        count=count
                    )
                    if session:
                        print("✅ 词汇学习会话开始！")

                elif choice == "4":
                    scenario = input("对话场景: ").strip() or "餐厅点餐"

                    session = await self.agent.start_conversation(
                        user_id=user_id,
                        scenario=scenario
                    )
                    if session:
                        print("✅ 对话练习会话创建成功！")

                elif choice == "5":
                    report = await self.agent.evaluate_progress(user_id=user_id)
                    if report:
                        print("✅ 进度报告生成成功！")

                elif choice == "6":
                    print("👋 再见！继续加油学习英语！")
                    break

                else:
                    print("❌ 无效选择，请重新输入。")

            except KeyboardInterrupt:
                print("\n\n👋 用户中断，再见！")
                break
            except Exception as e:
                print(f"❌ 操作失败: {str(e)}")


async def main():
    """主函数"""
    # 验证配置
    if not settings.validate_config():
        print("❌ 配置验证失败，请检查 .env 文件")
        print("确保设置了有效的 DEEPSEEK_API_KEY 或 OPENAI_API_KEY")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="LangDeepAgent - 英语学习 AI 助手")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 学习计划命令
    plan_parser = subparsers.add_parser('plan', help='创建学习计划')
    plan_parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced'],
                            default='intermediate', help='当前水平')
    plan_parser.add_argument('--goals', help='学习目标 (逗号分隔)')
    plan_parser.add_argument('--scenario', default='通用英语', help='目标场景')
    plan_parser.add_argument('--time', type=int, default=2, help='每日学习时间(小时)')
    plan_parser.add_argument('--duration', type=int, default=12, help='学习周期(周)')
    plan_parser.add_argument('--user-id', help='用户ID')

    # 水平评估命令
    assess_parser = subparsers.add_parser('assess', help='英语水平评估')
    assess_parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced'],
                              default='intermediate', help='当前水平')
    assess_parser.add_argument('--goals', help='学习目标 (逗号分隔)')
    assess_parser.add_argument('--scenario', default='通用英语', help='目标场景')
    assess_parser.add_argument('--user-id', help='用户ID')

    # 词汇学习命令
    vocab_parser = subparsers.add_parser('vocab', help='词汇学习')
    vocab_parser.add_argument('--topic', required=True, help='学习主题')
    vocab_parser.add_argument('--count', type=int, default=20, help='学习词汇数量')
    vocab_parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced'],
                             help='难度级别')
    vocab_parser.add_argument('--user-id', help='用户ID')

    # 对话练习命令
    conv_parser = subparsers.add_parser('conv', help='对话练习')
    conv_parser.add_argument('--scenario', required=True, help='对话场景')
    conv_parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced'],
                            help='难度级别')
    conv_parser.add_argument('--user-id', help='用户ID')

    # 进度查询命令
    progress_parser = subparsers.add_parser('progress', help='查看学习进度')
    progress_parser.add_argument('--user-id', help='用户ID')

    # 交互模式
    parser.add_argument('--interactive', action='store_true', help='交互模式')

    args = parser.parse_args()

    cli = LangDeepAgentCLI()

    try:
        if args.interactive or not args.command:
            await cli.interactive_mode()
        elif args.command == 'plan':
            await cli.create_plan_command(args)
        elif args.command == 'assess':
            await cli.assess_command(args)
        elif args.command == 'vocab':
            await cli.vocabulary_command(args)
        elif args.command == 'conv':
            await cli.conversation_command(args)
        elif args.command == 'progress':
            await cli.progress_command(args)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        if settings.DEBUG:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 设置 Windows 兼容性
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(main())