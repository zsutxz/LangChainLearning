"""
主程序入口
"""
import asyncio
import json
import sys

from src.assistant import TechLearningAssistant
from config.settings import settings


async def interactive_mode():
    """交互模式"""
    assistant = TechLearningAssistant()

    print("技术学习助手 - 交互模式")
    print("=" * 40)

    while True:
        try:
            print("\n请输入要学习的技术名称 (输入 'quit' 退出):")
            technology = input("> ").strip()

            if technology.lower() in ['quit', 'exit', 'q']:
                print("再见!")
                break

            if not technology:
                print("请输入有效的技术名称")
                continue

            print("请选择您的经验水平:")
            print("1. beginner (初学者)")
            print("2. intermediate (中级)")
            print("3. advanced (高级)")

            level_choice = input("> ").strip()
            experience_levels = {"1": "beginner", "2": "intermediate", "3": "advanced"}
            experience_level = experience_levels.get(level_choice, "beginner")

            print("请输入计划学习时长(小时，直接回车使用默认值):")
            duration_input = input("> ").strip()
            duration_hours = int(duration_input) if duration_input.isdigit() else None

            print("是否有特殊学习偏好? (可选，直接回车跳过)")
            print("例如: {\"learning_style\": \"visual\", \"preferred_time\": \"evening\"}")
            preferences_input = input("> ").strip()
            preferences = json.loads(preferences_input) if preferences_input else {}

            print("\n开始生成学习方案...")
            result = await assistant.create_learning_plan(
                technology=technology,
                experience_level=experience_level,
                duration_hours=duration_hours,
                preferences=preferences
            )

            if result["status"] == "completed":
                save_choice = input("\n是否保存结果到文件? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    assistant.save_result(result)

        except KeyboardInterrupt:
            print("\n\n用户中断，退出程序")
            break
        except Exception as e:
            print(f"发生错误: {e}")


async def cli_mode():
    """命令行模式"""
    import argparse

    parser = argparse.ArgumentParser(description="技术学习助手")
    parser.add_argument("technology", default="langchain agent",help="要学习的技术名称")
    parser.add_argument("--level",  choices=["beginner", "intermediate", "advanced"],
                       default="beginner", help="经验水平")
    parser.add_argument("--hours", default=30, type=int, help="学习时长(小时)")
    parser.add_argument("--preferences", help="JSON格式的学习偏好")
    parser.add_argument("--output", help="输出文件名")
    parser.add_argument("--interactive", action="store_true", help="交互模式")

    args = parser.parse_args()

    if args.interactive:
        await interactive_mode()
        return

    assistant = TechLearningAssistant()

    preferences = json.loads(args.preferences) if args.preferences else {}

    result = await assistant.create_learning_plan(
        technology=args.technology,
        experience_level=args.level,
        duration_hours=args.hours,
        preferences=preferences
    )

    if args.output and result["status"] == "completed":
        assistant.save_result(result, args.output)


def main():
    """主函数"""
    if not settings.validate_config():
        print("配置验证失败，请检查 .env 文件")
        print("注意: 需要在 .env 文件中设置有效的 OPENAI_API_KEY")
        sys.exit(1)

    try:
        # 设置事件循环策略以改善Windows兼容性
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        # 运行主程序
        asyncio.run(cli_mode())
    except KeyboardInterrupt:
        print("\n用户中断，退出程序")
        sys.exit(0)  # 正常退出码
    except asyncio.CancelledError:
        print("\n异步任务被取消，退出程序")
        sys.exit(0)
    except Exception as e:
        print(f"程序执行失败: {e}")
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理资源
        try:
            # 关闭可能的事件循环
            loop = asyncio.get_event_loop()
            if loop and not loop.is_closed():
                loop.close()
        except:
            pass


if __name__ == "__main__":
    main()