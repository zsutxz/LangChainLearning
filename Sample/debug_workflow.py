"""
调试工作流的独立脚本
"""
import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tech_learning_workflow import TechLearningWorkflow
from config.settings import settings


async def debug_workflow():
    """调试工作流"""
    print("开始调试工作流...")

    # 验证配置
    if not settings.validate_config():
        print("配置验证失败！")
        print("请确保在 .env 文件中设置了有效的 OPENAI_API_KEY")
        return

    print("配置验证通过")

    # 创建工作流实例
    workflow = TechLearningWorkflow()

    # 测试参数
    technology = "Python"
    experience_level = "beginner"
    duration_hours = 20

    print(f"测试参数: {technology}, {experience_level}, {duration_hours}小时")
    print("-" * 50)

    try:
        # 运行工作流
        result = await workflow.run(
            technology=technology,
            experience_level=experience_level,
            duration_hours=duration_hours
        )

        print("工作流执行完成!")
        print(f"状态: {result.get('status')}")
        print(f"数据键: {list(result.get('data', {}).keys()) if result.get('data') else 'None'}")

        if result.get('status') == 'completed':
            print("✅ 工作流成功完成")
        else:
            print(f"❌ 工作流失败: {result.get('error', '未知错误')}")

    except Exception as e:
        print(f"❌ 调试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 设置事件循环策略以改善Windows兼容性
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(debug_workflow())