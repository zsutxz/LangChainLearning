# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 🎯 项目概览

这是一个基于 **LangGraph 的智能技术学习助手** - 一个 Python 应用程序，能够自动收集 IT 技术研究并使用 AI 智能体生成个性化学习方案。

## 核心命令

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖项
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

### 运行应用程序
```bash
# 基本用法 - 生成学习方案
python main.py "Python" --level beginner --hours 30

# 高级用法 - 个性化设置
python main.py "Machine Learning" --level advanced --hours 60 --preferences '{"learning_style": "hands-on"}'

# 交互模式 - 为所有输入提供引导式提示
python main.py --interactive

# 保存结果到文件
python main.py "React" --level intermediate --output react_plan.json

# 命令行帮助 - 查看所有可用选项
python main.py --help
```

### 测试和开发
```bash
# 运行综合使用示例
python examples/basic_usage.py

# 测试搜索功能（如果可用）
# python testresearch.py  # 注意：此文件在当前目录中可能不存在

# 测试特定 LLM 配置
python testdeepseek.py

# 验证配置
python -c "from config.settings import settings; print('配置有效:', settings.validate_config())"

# 单独测试各个组件
python -c "
import asyncio
from src.tech_learning_workflow import TechLearningWorkflow

async def test_workflow():
    workflow = TechLearningWorkflow()
    result = await workflow.run('Python', 'beginner', 20)
    print('测试结果:', result['status'])

asyncio.run(test_workflow())
"

# 测试智能体功能
python -c "
import asyncio
from agents.research_agent import ResearchAgent

async def test_research():
    agent = ResearchAgent()
    result = await agent.research_technology('Python', fast_mode=True)
    print('研究测试:', result['status'])

asyncio.run(test_research())
"
```

### 配置管理
```bash
# 验证所需的 API 密钥是否已设置
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"

# 启用调试模式进行故障排除
export DEBUG=True
python main.py "Python" --level beginner
```

## 架构概览

### 技术栈
- **LangGraph**: 使用状态机进行工作流编排
- **LangChain**: 用于 AI 智能体集成的 LLM 框架
- **Python 3.8+**: 支持异步编程，用于并发处理
- **多 LLM 支持**: 集成 OpenAI GPT 和 DeepSeek API

### 核心架构模式

本项目使用**状态机工作流模式**，包含顺序处理节点：

1. **validate_input** - 参数验证和规范化
2. **research_technology** - 多源数据收集和分析
3. **generate_learning_plan** - 使用 LLM 创建基础学习方案
4. **customize_plan** - 基于用户偏好进行个性化（可选）
5. **generate_final_output** - 结果集成和格式化
6. **handle_error** - 全面的错误处理和恢复

### 详细的 LangGraph 状态管理
`WorkflowState` TypedDict 定义了完整的数据契约：
```python
class WorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    technology: str
    experience_level: str
    duration_hours: int
    preferences: Dict[str, Any]
    research_results: Optional[Dict[str, Any]]
    learning_plan: Optional[Dict[str, Any]]
    error: Optional[str]
    status: str
```

### LangGraph 工作流设计
工作流使用条件路由进行个性化：
```python
workflow.add_conditional_edges(
    "generate_learning_plan",
    self._should_customize,  # 根据偏好存在性进行路由
    {
        "customize": "customize_plan",
        "finalize": "generate_final_output"
    }
)
```

### 快速模式实现
研究智能体支持 `fast_mode=True` 参数，跳过网络搜索，为开发/测试提供模拟数据。

### 关键组件

#### TechLearningWorkflow (src/tech_learning_workflow.py:41)
主要的 LangGraph 工作流引擎，通过状态机编排整个学习方案生成过程。使用 StateGraph 管理顺序处理和条件路由。

#### 智能体协作模式
- **ResearchAgent** (agents/research_agent.py): 协调 WebSearcher 和 ContentAnalyzer 进行全面数据收集
- **LearningAgent** (agents/learning_agent.py): 基于研究结果生成个性化学习方案
- **状态管理**: WorkflowState 在智能体之间传递结构化数据

#### 多源研究系统
- **WebSearcher** (tools/web_searcher.py): 并发搜索 Google、ArXiv 论文和 RSS 订阅
- **ContentAnalyzer** (tools/content_analyzer.py): 内容分析和关键概念提取

#### 配置系统 (config/settings.py)
- **多 LLM 支持**: OpenAI GPT 和 DeepSeek API，具有自动回退功能
- **基于环境的配置**: 所有设置通过 .env 变量
- **验证系统**: 配置验证，带有清晰的错误消息

## 开发模式

### 异步处理模式
所有组件使用 asyncio 进行高性能并发操作：
```python
async def research_technology(self, technology: str):
    # 并发网络搜索和内容分析
    results = await self.web_searcher.comprehensive_search(query)
    analysis = self.content_analyzer.analyze_content(results)
```

### 状态管理模式
WorkflowState TypedDict 定义了在工作流节点间传递数据的契约：
```python
class WorkflowState(TypedDict):
    technology: str
    experience_level: str
    duration_hours: int
    preferences: Dict[str, Any]
    research_results: Optional[Dict[str, Any]]
    learning_plan: Optional[Dict[str, Any]]
    # ... 其他字段
```

### 错误处理模式
通过工作流中专用错误处理节点实现全面错误处理和优雅回退。

## 所需环境变量

```bash
# 必需
OPENAI_API_KEY=你的_openai_api_key

# 可选，用于增强功能
SERPER_API_KEY=你的_serper_api_key          # 用于 Google 网络搜索
ANTHROPIC_API_KEY=你的_anthropic_api_key    # 备用 LLM 支持
USE_DEEPSEEK=true                            # 启用 DeepSeek API
DEEPSEEK_API_KEY=你的_deepseek_api_key      # DeepSeek API 密钥
```

## 关键依赖项

- **langgraph>=0.2.0** - 工作流编排和状态管理
- **langchain>=0.2.0** - LLM 框架
- **langchain-openai>=0.1.0** - OpenAI 集成
- **langchain-community>=0.2.0** - 社区工具和集成
- **asyncio, aiohttp** - 用于性能的异步处理
- **requests, beautifulsoup4** - 网络爬虫功能
- **python-dotenv** - 环境变量管理
- **arxiv>=2.0.0** - 学术论文搜索
- **feedparser>=6.0.0** - RSS 订阅处理
- **lxml>=4.9.0** - XML/HTML 解析
- **pandas>=2.0.0** - 数据操作和分析

## 使用示例

### 编程接口
```python
from main import TechLearningAssistant
import asyncio

async def create_learning_plan():
    assistant = TechLearningAssistant()
    result = await assistant.create_learning_plan(
        technology="Python",
        experience_level="beginner",
        duration_hours=30,
        preferences={
            "learning_style": "visual",
            "preferred_time": "evening"
        }
    )

    if result["status"] == "completed":
        assistant.save_result(result)
    return result

# 执行
result = asyncio.run(create_learning_plan())
```

### 自定义选项
```python
preferences = {
    "learning_style": "visual|hands-on|theoretical",
    "preferred_time": "morning|evening|flexible",
    "focus": ["特定主题"],
    "tools": ["首选工具"],
    "project_type": "personal|professional|research",
    "background": "用户背景"
}
```

## 常见开发任务

### 添加新搜索源
用新搜索方法扩展 WebSearcher 类：
```python
async def search_new_source(self, query: str) -> List[Dict[str, Any]]:
    """添加新搜索源实现"""
    # 实现新搜索源逻辑
    pass
```

### 自定义学习方案生成
修改 LearningAgent 提示模板和生成逻辑：
```python
def generate_learning_plan(self, technology: str, analysis: Dict[str, Any],
                         duration_hours: int = None, experience_level: str = "beginner"):
    """自定义学习方案生成逻辑"""
    # 修改提示模板和生成方法
    pass
```

### 扩展 LangGraph 工作流
向工作流添加新处理节点：
```python
def _create_workflow(self) -> StateGraph:
    """用额外处理步骤扩展工作流"""
    workflow = StateGraph(WorkflowState)

    # 添加新节点
    workflow.add_node("new_processing_step", self._new_processing_step)

    # 更新工作流边
    workflow.add_edge("research_technology", "new_processing_step")
    workflow.add_edge("new_processing_step", "generate_learning_plan")

    return workflow.compile()
```

## 调试和故障排除

### 常见问题
1. **API 密钥配置**: 使用 `settings.validate_config()` 验证设置
2. **搜索结果质量**: 检查 SERPER_API_KEY 以获得 Google 搜索功能
3. **LLM 性能**: 使用 testdeepseek.py 测试 OpenAI 和 DeepSeek 配置
4. **异步问题**: 确保所有异步函数都被正确等待

### 调试模式
```bash
export DEBUG=True
python main.py "Python" --level beginner
```

### 单独测试组件
```bash
# 测试研究组件（如果可用）
# python testresearch.py  # 注意：此文件在当前目录中可能不存在

# 测试 LLM 配置
python testdeepseek.py
```

### 高级调试技术

#### 工作流状态检查
```python
# 调试工作流状态转换
python -c "
import asyncio
from src.tech_learning_workflow import TechLearningWorkflow

async def debug_workflow():
    workflow = TechLearningWorkflow()
    # 启用逐步执行
    result = await workflow.run('Python', 'beginner', 20)
    print('完整状态:', result)

asyncio.run(debug_workflow())
"
```

#### 特定智能体测试
```python
# 单独测试研究智能体
python -c "
import asyncio
from agents.research_agent import ResearchAgent

async def debug_research():
    agent = ResearchAgent()
    # 使用快速模式避免网络问题
    result = await agent.research_technology('Python', fast_mode=True)
    print('研究结果键:', list(result.keys()))

asyncio.run(debug_research())
"
```

#### 配置验证
```bash
# 全面配置检查
python -c "
from config.settings import settings
print('OpenAI 密钥:', bool(settings.OPENAI_API_KEY))
print('DeepSeek 密钥:', bool(settings.DEEPSEEK_API_KEY))
print('使用 DeepSeek:', settings.USE_DEEPSEEK)
print('Serper 密钥:', bool(settings.SERPER_API_KEY))
print('配置有效:', settings.validate_config())
"
```

### 性能优化
```bash
# 使用快速模式进行开发测试
python -c "
import asyncio
from main import TechLearningAssistant

async def fast_mode_test():
    assistant = TechLearningAssistant()
    # 使用模拟数据加快开发速度
    result = await assistant.create_learning_plan('Python', 'beginner', 20)
    print('快速模式测试完成')

asyncio.run(fast_mode_test())
"
```

## 开发最佳实践

### 快速模式开发
为快速开发和测试，使用内置的快速模式功能：
- **ResearchAgent.fast_mode=True**: 跳过网络搜索，返回模拟数据
- **工作流测试**: 在没有外部依赖的情况下测试工作流逻辑
- **组件隔离**: 在不执行完整工作流的情况下测试单个智能体

### 环境配置
- **开发**: 设置 `DEBUG=True` 进行详细日志记录
- **测试**: 使用 `fast_mode=True` 避免速率限制和网络依赖
- **生产**: 确保所有 API 密钥都正确配置和验证

### 性能考虑
- **异步处理**: 所有 I/O 操作都是异步的，以提高性能
- **并发搜索**: 多个搜索源并发运行
- **错误恢复**: 当外部服务失败时优雅降级

### Git 配置
注意测试文件被排除在版本控制之外：
```bash
# 测试文件被 .gitignore 忽略
test_*.py
*_test.py
debug_*.py
```

### 开发工作流
1. **设置**: 使用 `settings.validate_config()` 验证配置
2. **开发**: 使用快速模式和调试日志进行快速迭代
3. **测试**: 在集成前单独测试组件
4. **验证**: 在部署前使用真实 API 运行完整工作流