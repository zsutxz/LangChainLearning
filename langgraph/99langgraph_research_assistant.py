#!/usr/bin/env python3
"""
LangGraph 1.0 复杂示例：智能研究助手
功能：多步骤研究、分析、验证和报告生成

Converted from Jupyter notebook to Python file.
"""

import os
import json
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from datetime import datetime
import operator

# LangGraph 1.0 导入
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# LangChain 导入
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

try:
    # 尝试使用新版本的导入
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    # 如果新版本不可用，使用旧版本或替代方案
    WIKIPEDIA_AVAILABLE = False
    print("[警告] Wikipedia工具不可用，将仅使用DuckDuckGo搜索")

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("[警告] DuckDuckGo搜索工具不可用")

# ============================================================================
# 1. 配置和初始化
# ============================================================================

class ResearchState(TypedDict):
    # 用户输入字段
    topic: str
    research_depth: str  # e.g., "basic", "standard", "comprehensive"

    # 搜索与研究中间数据
    search_queries: List[str]
    search_results: List[Dict[str, Any]]  # 建议结构：{"title": str, "snippet": str, "url": str, "source_type": str}
    research_notes: List[str]
    key_findings: List[str]
    analysis_summary: str
    research_gaps: List[str]
    improvement_suggestions: List[str]

    # 评估与质量字段
    credibility_scores: Optional[Dict[str, float]]  # e.g., {"overall": 0.85, "source_diversity": 0.8, ...}
    verification_status: bool
    quality_score: float

    # 报告输出字段
    final_report: str
    executive_summary: str

    # 状态控制字段
    current_step: str
    retry_count: int
    max_retries: int
    completed_steps: List[str]

    # 消息历史（用于 LLM 交互）
    messages: List[Dict[str, Any]]  # 或更严格：List[BaseMessage]，但 TypedDict 通常用 dict

def setup_llm() -> ChatOpenAI:
    """
    设置语言模型，支持多种API提供商
    """
    # 设置 DeepSeek 的 API 密钥（LangChain-OpenAI 仍然会查找 OPENAI_API_KEY）
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY') or os.getenv('OPENAI_API_KEY')

    if not deepseek_api_key:
        raise ValueError("请设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY 环境变量")

    # 关键：指定 DeepSeek 的 API 基础 URL
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

    return ChatOpenAI(
        model="deepseek-chat",  # 使用 DeepSeek 的模型名称
        openai_api_base=DEEPSEEK_BASE_URL,  # 指定 DeepSeek 的 URL
        temperature=0.7,
        api_key=deepseek_api_key
    )

def setup_search_tools():
    """
    设置搜索工具
    """
    tools = {}

    # 设置 DuckDuckGo 搜索
    if DDGS_AVAILABLE:
        tools['ddgs'] = DDGS()
        print("[成功] DuckDuckGo 搜索工具已启用")
    else:
        print("[错误] DuckDuckGo 搜索工具不可用")

    # 设置 Wikipedia 搜索
    if WIKIPEDIA_AVAILABLE:
        try:
            api_wrapper = WikipediaAPIWrapper(
                top_k_results=1,          # 只返回1个结果
                doc_content_chars_max=500, # 每篇最多500字符
                lang="zh"                 # 中文维基（可选）
            )
            tools['wikipedia'] = WikipediaQueryRun(api_wrapper=api_wrapper)
            print("[成功] Wikipedia 搜索工具已启用")
        except Exception as e:
            print(f"[警告] Wikipedia 搜索工具设置失败: {e}")

    return tools

# ============================================================================
# 2. 实现节点函数 (Node Functions)
# ============================================================================

def initialize_research(state: ResearchState, llm: ChatOpenAI, tools: Dict[str, Any]) -> ResearchState:
    """
    节点1：初始化研究
    功能：解析研究主题，生成搜索查询，设置研究参数
    """
    print("[启动] 步骤1：初始化研究")

    # 更新当前步骤
    state["current_step"] = "initialization"
    state["completed_steps"] = ["initialization"]

    # 生成搜索查询
    topic = state["topic"]
    depth = state["research_depth"]

    # 根据研究深度生成不同数量的查询
    if depth == "basic":
        query_count = 3
    elif depth == "standard":
        query_count = 5
    else:  # comprehensive
        query_count = 8

    # 使用LLM生成多样化的搜索查询
    query_prompt = ChatPromptTemplate.from_template("""
    为研究主题："{topic}"
    生成 {count} 个不同的搜索查询，涵盖以下角度：
    1. 基础定义和概念
    2. 最新发展和趋势
    3. 关键人物和机构
    4. 争议和挑战
    5. 未来展望
    研究深度：{depth}

    只返回查询列表，每行一个：
    """)

    query_chain = query_prompt | llm
    result = query_chain.invoke({
        "topic": topic,
        "count": query_count,
        "depth": depth
    })

    # 解析查询
    queries = [q.strip() for q in result.content.split('\n') if q.strip()]
    state["search_queries"] = queries[:query_count]  # 确保不超过预期数量

    # 初始化其他字段
    state["search_results"] = []
    state["research_notes"] = []
    state["key_findings"] = []
    state["research_gaps"] = []
    state["improvement_suggestions"] = []
    state["retry_count"] = 0
    state["max_retries"] = 2

    print(f"[成功] 生成了 {len(state['search_queries'])} 个搜索查询")

    return state

def conduct_search(state: ResearchState, tools: Dict[str, Any]) -> ResearchState:
    """
    节点2：执行搜索
    功能：使用生成的查询执行搜索，收集信息
    """
    print("[搜索] 步骤2: 执行搜索")

    state["current_step"] = "searching"
    state["completed_steps"].append("searching")

    search_results = []

    for i, query in enumerate(state["search_queries"]):
        print(f"  执行查询 {i+1}/{len(state['search_queries'])}: {query}")

        ddg_result = ""
        wiki_result = ""

        try:
            # 使用DuckDuckGo搜索
            if 'ddgs' in tools and tools['ddgs']:
                try:
                    results = list(tools['ddgs'].text(query, max_results=5))
                    if results:
                        ddg_result = "\n".join([f"- {result['title']}: {result['body']}" for result in results])
                        print(f"    [成功] DuckDuckGo 搜索成功，找到 {len(results)} 个结果")
                    else:
                        print(f"    [警告] DuckDuckGo 搜索无结果")
                except Exception as e:
                    print(f"    [错误] DuckDuckGo 搜索失败: {str(e)}")

            # 使用Wikipedia搜索
            if 'wikipedia' in tools and tools['wikipedia']:
                try:
                    wiki_result = tools['wikipedia'].invoke(query)
                    # 限制结果长度
                    if len(wiki_result) > 1000:
                        wiki_result = wiki_result[:1000] + "..."
                    print(f"    [成功] Wikipedia 搜索成功")
                except Exception as e:
                    print(f"    [警告] Wikipedia搜索失败: {str(e)}")
                    wiki_result = ""

            # 存储结果
            result_entry = {
                "query": query,
                "ddg_result": ddg_result,
                "wiki_result": wiki_result,
                "timestamp": datetime.now().isoformat(),
                "source_type": "search"
            }
            search_results.append(result_entry)

        except Exception as e:
            print(f"    [错误] 搜索过程发生错误: {str(e)}")
            # 记录失败的搜索
            search_results.append({
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "source_type": "error"
            })

    state["search_results"] = search_results
    print(f"[成功] 完成了 {len(search_results)} 个搜索查询")

    return state

def analyze_findings(state: ResearchState, llm: ChatOpenAI) -> ResearchState:
    """
    节点3：分析发现
    功能：分析搜索结果，提取关键信息，评估可信度
    """
    print("[分析] 步骤3：分析发现")

    state["current_step"] = "analysis"
    state["completed_steps"].append("analysis")

    # 准备分析提示
    analysis_prompt = ChatPromptTemplate.from_template("""
    作为专业研究分析师，请分析以下搜索结果：

    研究主题：{topic}
    研究深度：{depth}

    搜索结果：
    {search_data}

    请提供：
    1. 关键发现（3-5个要点）
    2. 信息可信度评估（0-1评分）
    3. 研究空白或需要进一步调查的领域
    4. 初步分析摘要

    返回格式如下：
    关键发现：
    - 发现1
    - 发现2
    - 发现3

    可信度评估：
    总体评分：X.X
    详细评估：...

    研究空白：
    - 空白1
    - 空白2

    分析摘要：
    [详细的分析摘要]
    """)

    # 准备搜索数据
    search_data = ""
    for i, result in enumerate(state["search_results"]):
        search_data += f"\n=== 查询 {i+1}: {result['query']} ===\n"
        if 'error' in result:
            search_data += f"错误：{result['error']}\n"
        else:
            search_data += f"DuckDuckGo结果：{result.get('ddg_result', '无结果')}\n"
            if result.get('wiki_result'):
                search_data += f"Wikipedia结果：{result['wiki_result']}\n"

    # 执行分析
    analysis_chain = analysis_prompt | llm
    result = analysis_chain.invoke({
        "topic": state["topic"],
        "depth": state["research_depth"],
        "search_data": search_data
    })

    # 解析分析结果
    analysis_text = result.content

    # 提取关键发现
    key_findings = []
    if "关键发现：" in analysis_text:
        findings_section = analysis_text.split("关键发现：")[1].split("可信度评估：")[0]
        for line in findings_section.split('\n'):
            if line.strip().startswith('-'):
                key_findings.append(line.strip()[1:].strip())

    # 提取研究空白
    research_gaps = []
    if "研究空白：" in analysis_text:
        gaps_section = analysis_text.split("研究空白：")[1].split("分析摘要：")[0]
        for line in gaps_section.split('\n'):
            if line.strip().startswith('-'):
                research_gaps.append(line.strip()[1:].strip())

    # 提取分析摘要
    analysis_summary = ""
    if "分析摘要：" in analysis_text:
        analysis_summary = analysis_text.split("分析摘要：")[1].strip()

    # 简单的可信度评分计算（基于结果数量和质量）
    successful_searches = len([r for r in state["search_results"] if 'error' not in r])
    credibility_score = min(successful_searches / len(state["search_results"]), 1.0) if state["search_results"] else 0.0

    # 更新状态
    state["key_findings"] = key_findings[:5]  # 限制为5个关键发现
    state["research_gaps"] = research_gaps[:3]  # 限制为3个研究空白
    state["analysis_summary"] = analysis_summary
    state["credibility_scores"] = {
        "overall": credibility_score,
        "source_diversity": 0.8 if len(set(r.get('source_type', 'unknown') for r in state["search_results"])) > 1 else 0.5,
        "information_depth": 0.7 if len(analysis_summary) > 200 else 0.4
    }

    print(f"[成功] 分析完成，识别了 {len(key_findings)} 个关键发现")

    return state

def verify_quality(state: ResearchState) -> ResearchState:
    """
    节点4：验证质量
    功能：评估研究质量，决定是否需要改进
    """
    print("[成功] 步骤4：验证质量")

    state["current_step"] = "verification"
    state["completed_steps"].append("verification")

    # 计算质量评分
    credibility_scores = state.get("credibility_scores", {})
    quality_factors = [
        credibility_scores.get("overall", 0),
        credibility_scores.get("source_diversity", 0),
        credibility_scores.get("information_depth", 0),
        len(state["key_findings"]) / 5.0,  # 期望至少5个发现
        len(state["research_notes"]) / 10.0  # 期望至少10个笔记
    ]

    quality_score = sum(quality_factors) / len(quality_factors)
    state["quality_score"] = quality_score

    # 生成改进建议
    improvement_suggestions = []

    if quality_score < 0.7:
        if credibility_scores.get("overall", 0) < 0.6:
            improvement_suggestions.append("增加更多可靠的信息源")
        if len(state["key_findings"]) < 3:
            improvement_suggestions.append("扩展搜索范围以获得更多关键发现")
        if len(state["research_notes"]) < 5:
            improvement_suggestions.append("深入研究搜索结果的细节")

        state["improvement_suggestions"] = improvement_suggestions
        state["verification_status"] = False
        print(f"[警告] 质量评分 {quality_score:.2f} 低于阈值，需要改进")
    else:
        state["verification_status"] = True
        print(f"[成功] 质量评分 {quality_score:.2f} 通过验证")

    return state

def generate_report(state: ResearchState, llm: ChatOpenAI) -> ResearchState:
    """
    节点5：生成报告
    功能：基于分析结果生成最终研究报告
    """
    print("[报告] 步骤5：生成报告")

    state["current_step"] = "reporting"
    state["completed_steps"].append("reporting")

    # 生成报告的提示
    report_prompt = ChatPromptTemplate.from_template("""
    基于以下研究数据生成专业的研究报告：

    研究主题：{topic}
    研究深度：{depth}

    关键发现：
    {key_findings}

    分析摘要：
    {analysis_summary}

    研究空白：
    {research_gaps}

    质量评分：{quality_score:.2f}

    请生成包含以下结构的报告：

    # 执行摘要
    [简明扼要的概述，200-300字]

    # 研究方法
    [说明研究方法和数据来源]

    # 主要发现
    [详细展开关键发现]

    # 分析与讨论
    [深入分析和讨论]

    # 研究局限
    [说明研究的局限性]

    # 结论与建议
    [总结结论和建议]

    # 附录
    [数据来源和参考文献]
    """)

    # 准备数据
    key_findings_text = "\n".join([f"- {finding}" for finding in state["key_findings"]])
    research_gaps_text = "\n".join([f"- {gap}" for gap in state["research_gaps"]])

    # 生成报告
    report_chain = report_prompt | llm
    result = report_chain.invoke({
        "topic": state["topic"],
        "depth": state["research_depth"],
        "key_findings": key_findings_text,
        "analysis_summary": state["analysis_summary"],
        "research_gaps": research_gaps_text,
        "quality_score": state["quality_score"]
    })

    # 提取执行摘要
    report_content = result.content
    executive_summary = ""
    if "# 执行摘要" in report_content:
        summary_section = report_content.split("# 执行摘要")[1].split("#")[0]
        executive_summary = summary_section.strip()

    # 更新状态
    state["final_report"] = report_content
    state["executive_summary"] = executive_summary

    print("[成功] 报告生成完成")

    return state

def improve_research(state: ResearchState, llm: ChatOpenAI) -> ResearchState:
    """
    节点6：改进研究
    功能：基于质量验证结果，改进研究质量
    """
    print("[改进] 步骤6：改进研究")

    state["current_step"] = "improvement"
    state["completed_steps"].append("improvement")
    state["retry_count"] += 1

    # 基于改进建议生成新的搜索查询
    suggestions = state["improvement_suggestions"]

    improvement_prompt = ChatPromptTemplate.from_template("""
    原研究主题：{topic}

    当前研究的不足：
    {suggestions}

    已尝试的搜索查询：
    {existing_queries}

    为了改进研究质量，请生成3个新的搜索查询，专注于：
    1. 更可靠的信息源
    2. 更深入的技术细节
    3. 不同的角度和观点

    返回新的查询列表，每行一个：
    """)

    existing_queries = "\n".join(state["search_queries"])
    suggestions_text = "\n".join([f"- {suggestion}" for suggestion in suggestions])

    improvement_chain = improvement_prompt | llm
    result = improvement_chain.invoke({
        "topic": state["topic"],
        "suggestions": suggestions_text,
        "existing_queries": existing_queries
    })

    # 解析新查询并添加到现有查询中
    new_queries = [q.strip() for q in result.content.split('\n') if q.strip()]
    state["search_queries"].extend(new_queries[:3])

    print(f"[成功] 添加了 {len(new_queries)} 个新的搜索查询")

    return state

# ============================================================================
# 3. 条件路由函数 (Conditional Routing Functions)
# ============================================================================

def should_improve_or_continue(state: ResearchState) -> str:
    """
    条件路由：决定是否需要改进研究或继续生成报告
    """
    if not state["verification_status"] and state["retry_count"] < state["max_retries"]:
        return "improve"
    else:
        return "generate_report"

def should_retry_or_finish(state: ResearchState) -> str:
    """
    条件路由：决定是否重试搜索或结束流程
    """
    if state["retry_count"] >= state["max_retries"]:
        return "generate_report"
    else:
        return "search"

# ============================================================================
# 4. 创建工作流图 (Create Workflow Graph)
# ============================================================================

def create_research_graph(llm: ChatOpenAI, tools: Dict[str, Any]) -> StateGraph:
    """
    创建完整的研究工作流图
    """
    # 创建状态图
    workflow = StateGraph(ResearchState)

    # 添加节点
    workflow.add_node("initialize", lambda state: initialize_research(state, llm, tools))
    workflow.add_node("search", lambda state: conduct_search(state, tools))
    workflow.add_node("analyze", lambda state: analyze_findings(state, llm))
    workflow.add_node("verify", verify_quality)
    workflow.add_node("generate_report", lambda state: generate_report(state, llm))
    workflow.add_node("improve", lambda state: improve_research(state, llm))

    # 添加边（定义工作流路径）
    workflow.add_edge(START, "initialize")           # 开始 -> 初始化
    workflow.add_edge("initialize", "search")         # 初始化 -> 搜索
    workflow.add_edge("search", "analyze")            # 搜索 -> 分析
    workflow.add_edge("analyze", "verify")            # 分析 -> 验证

    # 条件边：验证后的分支
    workflow.add_conditional_edges(
        "verify",
        should_improve_or_continue,
        {
            "improve": "improve",           # 需要改进
            "generate_report": "generate_report"  # 继续生成报告
        }
    )

    # 改进后回到搜索
    workflow.add_edge("improve", "search")

    # 结束流程
    workflow.add_edge("generate_report", END)

    return workflow

# ============================================================================
# 5. 主函数和示例使用 (Main Function and Usage Examples)
# ============================================================================

def run_research_assistant(topic: str, research_depth: str = "standard",
                          llm: ChatOpenAI = None, tools: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    运行研究助手

    Args:
        topic: 研究主题
        research_depth: 研究深度 (basic/standard/comprehensive)
        llm: 语言模型实例
        tools: 搜索工具字典

    Returns:
        包含研究结果的字典
    """
    # 设置默认值
    tools = tools if tools is not None else setup_search_tools()
    llm = llm if llm is not None else setup_llm()

    print(f"[目标] 开始研究主题：{topic}")
    print(f"[分析] 研究深度：{research_depth}")
    print("=" * 50)

    # 创建工作流
    research_workflow = create_research_graph(llm, tools)

    # 编译工作流（添加内存保存器以支持检查点）
    app = research_workflow.compile(checkpointer=MemorySaver())

    # 初始化状态
    initial_state = ResearchState(
        topic=topic,
        research_depth=research_depth,
        search_queries=[],
        search_results=[],
        research_notes=[],
        key_findings=[],
        analysis_summary="",
        credibility_scores={},
        research_gaps=[],
        verification_status=False,
        quality_score=0.0,
        improvement_suggestions=[],
        final_report="",
        executive_summary="",
        current_step="",
        retry_count=0,
        max_retries=2,
        completed_steps=[],
        messages=[]
    )

    # 执行工作流
    try:
        # 提供配置参数以支持检查点
        config = {
            "configurable": {
                "thread_id": f"research_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        }
        final_state = app.invoke(initial_state, config=config)

        # 输出结果摘要
        print("\n" + "=" * 50)
        print("[报告] 研究完成摘要")
        print("=" * 50)
        print(f"[目标] 研究主题：{final_state['topic']}")
        print(f"[分析] 质量评分：{final_state['quality_score']:.2f}")
        print(f"[搜索] 执行搜索：{len(final_state['search_results'])} 次")
        print(f"[发现] 关键发现：{len(final_state['key_findings'])} 个")
        print(f"[报告] 完成步骤：{', '.join(final_state['completed_steps'])}")

        if final_state.get('executive_summary'):
            print(f"\n[摘要] 执行摘要：")
            print("-" * 30)
            summary = final_state['executive_summary']
            print(summary[:300] + "..." if len(summary) > 300 else summary)

        return final_state

    except Exception as e:
        print(f"[错误] 研究过程中发生错误：{str(e)}")
        return {"error": str(e)}

def save_results_to_file(results: Dict[str, Any], filename: str = None) -> str:
    """
    保存研究结果到文件

    Args:
        results: 研究结果
        filename: 文件名（可选）

    Returns:
        保存的文件路径
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{timestamp}.md"

    # 创建报告内容
    report_content = results.get('final_report', '无报告内容')

    # 添加元数据
    metadata = f"""---
研究主题：{results.get('topic', '未知')}
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
质量评分：{results.get('quality_score', 0):.2f}
完成步骤：{', '.join(results.get('completed_steps', []))}
---

"""

    full_content = metadata + report_content

    # 保存文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"[文件] 报告已保存到：{filename}")
    return filename

# ============================================================================
# 6. 示例使用 (Usage Examples)
# ============================================================================

def main():
    """
    主函数 - 示例使用
    """
    print("[启动] LangGraph 智能研究助手")
    print("=" * 80)

    # 设置环境
    llm = setup_llm()
    tools = setup_search_tools()

    # 示例研究主题
    examples = [
        {
            "topic": "人工智能在医疗诊断中的最新进展与挑战",
            "depth": "comprehensive",
            "filename": "ai_medical_diagnosis_comprehensive.md"
        },
        {
            "topic": "量子计算对密码学的影响",
            "depth": "standard",
            "filename": "quantum_cryptography_standard.md"
        },
        {
            "topic": "可持续发展与绿色能源技术",
            "depth": "basic",
            "filename": "sustainable_green_energy_basic.md"
        }
    ]

    # 交互式选择
    print("请选择研究主题：")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['topic']} (深度: {example['depth']})")
    print("4. 自定义主题")

    # 默认选择第一个示例，避免交互式输入
    print("使用默认示例进行演示...")
    topic, depth, filename = examples[0]["topic"], examples[0]["depth"], examples[0]["filename"]

# 注释掉交互式输入代码
# try:
#     choice = input("\n请输入选择 (1-4): ").strip()
#
#     if choice == "4":
#         topic = input("请输入研究主题: ").strip()
#         depth_options = ["basic", "standard", "comprehensive"]
#         depth = input("请输入研究深度 (basic/standard/comprehensive): ").strip()
#         if depth not in depth_options:
#             depth = "standard"
#         filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
#     else:
#         choice_idx = int(choice) - 1
#         if 0 <= choice_idx < len(examples):
#             selected = examples[choice_idx]
#             topic, depth, filename = selected["topic"], selected["depth"], selected["filename"]
#         else:
#             print("无效选择，使用默认示例")
#             topic, depth, filename = examples[0]["topic"], examples[0]["depth"], examples[0]["filename"]
# except (ValueError, KeyboardInterrupt):
#     print("无效输入，使用默认示例")
#     topic, depth, filename = examples[0]["topic"], examples[0]["depth"], examples[0]["filename"]

    print("\n" + "=" * 80 + "\n")

    # 执行研究
    results = run_research_assistant(topic, depth, llm, tools)

    if "error" not in results:
        save_results_to_file(results, filename)

    print("\n[完成] 研究完成！")

if __name__ == "__main__":
    # 如果直接运行此脚本，执行主函数
    main()

    # 或者直接运行特定示例（取消注释）
    # llm = setup_llm()
    # tools = setup_search_tools()
    # results = run_research_assistant(
    #     topic="量子计算对密码学的影响",
    #     research_depth="comprehensive",
    #     llm=llm,
    #     tools=tools
    # )
    # save_results_to_file(results, "quantum_cryptography_comprehensive.md")