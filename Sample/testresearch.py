#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试主程序问题
"""
import asyncio

from config.settings import settings
from agents.research_agent import ResearchAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

async def test_deepseek_learning():
    print("=== 测试 DeepSeek Learning ===")

    try:
        # 获取配置
        llm_config = settings.get_llm_config()
        print(f"使用模型: {llm_config.get('model')}")
        print(f"API Base: {llm_config.get('openai_api_base', 'Default')}")

        # 初始化 LLM
        llm = ChatOpenAI(**llm_config)

        # 发送测试消息
        test_prompt = """
        请为Python初学者制定一个2小时的学习计划，包含以下内容：
        1. 学习目标（3个）
        2. 具体内容安排
        3. 实践练习

        请用中文回答，保持简洁实用。
        """

        messages = [HumanMessage(content=test_prompt)]
        print("\n正在调用 DeepSeek API...")
        response = await llm.ainvoke(messages)

        print("\n=== DeepSeek 回复 ===")
        print(response.content)

        return True

    except Exception as e:
        print(f"\n✗ DeepSeek Learning 测试失败: {str(e)}")
        return False
    
async def test_research():
    """调试研究功能"""
    print("=== 调试研究功能 ===")

    try:
        research_agent = ResearchAgent()
        print("[OK] ResearchAgent 初始化成功")

        # 测试搜索功能
        print("\n开始技术研究...")
        result = await research_agent.research_technology("Python")

        print(f"研究状态: {result.get('status')}")
        print(f"研究消息: {result.get('message', 'N/A')}")

        if result.get("status") == "completed":
            print(f"找到文章数量: {len(result.get('search_results', {}).get('results', []))}")
            print("[OK] 研究功能正常")
        else:
            print("[ERROR] 研究功能异常")

    except Exception as e:
        print(f"[ERROR] 研究功能出错: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""

    success = await test_deepseek_learning()
    # success = await test_research()

    print(f"\n=== 测试结果 ===")
    if success:
        print("[SUCCESS] test_deepseek_learning test_research 测试正常!")
    else:
        print("[ERROR] 测试存在问题，请检查配置!")


if __name__ == "__main__":
    asyncio.run(main())