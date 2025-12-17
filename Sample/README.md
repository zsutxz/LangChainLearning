# 🤖 LangGraph 智能技术学习助手

一个基于 LangGraph 的智能技术学习助手，能够自动收集 IT 技术研究并使用 AI 智能体生成个性化学习方案。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0%2B-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

- 🧠 **智能学习方案生成**: 基于用户经验水平和学习时间，生成个性化技术学习计划
- 🔍 **多源技术研究**: 自动整合 Google 搜索、Arxiv 论文、RSS 订阅等多种信息源
- 🤖 **AI 智能体协作**: 使用 LangGraph 编排多个 AI 智能体协同工作
- 🌐 **异步并发处理**: 高性能异步架构，支持并发数据收集和处理
- 🎯 **个性化定制**: 支持学习偏好设置，生成符合个人习惯的学习方案
- 🔧 **多 LLM 支持**: 集成 OpenAI GPT 和 DeepSeek API，支持模型切换
- 📊 **内容分析**: 智能提取关键概念和技术趋势分析

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenAI API Key (必需)
- 可选: Serper API Key (用于 Google 搜索)、DeepSeek API Key

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-repo/LangChainLearning.git
cd LangChainLearning/Sample
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

5. **验证配置**
```bash
python -c "from config.settings import settings; print('配置有效:', settings.validate_config())"
```

## 🎯 使用方法

### 命令行模式

```bash
# 基本用法 - 生成学习方案
python main.py "Python" --level beginner --hours 30

# 高级用法 - 个性化设置
python main.py "Machine Learning" --level advanced --hours 60 --preferences '{"learning_style": "hands-on"}'

# 保存结果到文件
python main.py "React" --level intermediate --output react_plan.json
```

### 交互模式

```bash
# 启动交互模式 - 为所有输入提供引导式提示
python main.py --interactive
```

### 编程接口

```python
import asyncio
from main import TechLearningAssistant

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

## 🏗️ 项目架构

### 技术栈

- **核心框架**: LangGraph (工作流编排)、LangChain (AI 智能体集成)
- **编程语言**: Python 3.8+ (异步编程支持)
- **LLM 集成**: OpenAI GPT、DeepSeek API
- **数据处理**: pandas、numpy、asyncio、aiohttp
- **网络爬虫**: requests、beautifulsoup4、lxml、feedparser、arxiv
- **配置管理**: python-dotenv

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    用户输入层                                 │
├─────────────────────────────────────────────────────────────┤
│                TechLearningAssistant                         │
│                     (main.py)                               │
├─────────────────────────────────────────────────────────────┤
│                LangGraph 工作流引擎                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ 输入验证     │→ │ 技术研究     │→ │ 生成学习方案         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│           ↓              ↓                    ↓             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ 个性化定制   │→ │ 最终输出     │→ │ 错误处理             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      AI 智能体层                             │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │    ResearchAgent    │      │   LearningAgent     │      │
│  │  (技术研究智能体)    │      │ (学习方案智能体)     │      │
│  └─────────────────────┘      └─────────────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                       工具层                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │WebSearcher  │  │ContentAnalyzer│   │   配置管理           │  │
│  │(网络搜索工具)│  │ (内容分析工具) │   │  (settings.py)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件

#### 📁 目录结构

```
Sample/
├── main.py                    # 程序入口点，CLI 和交互模式
├── requirements.txt           # Python 依赖包列表
├── .env.example              # 环境变量配置模板
├── config/
│   └── settings.py           # 配置管理，API 密钥设置
├── src/
│   ├── assistant.py          # 主要的 TechLearningAssistant 类
│   └── workflow.py           # LangGraph 工作流引擎
├── agents/
│   ├── learning_agent.py     # 学习方案生成智能体
│   └── research_agent.py     # 技术研究智能体
├── tools/
│   ├── web_searcher.py       # 多源网络搜索 (Google, Arxiv, RSS)
│   └── content_analyzer.py   # 内容分析和关键概念提取
└── examples/
    └── basic_usage.py        # 使用示例和演示
```

#### 🔄 LangGraph 状态机工作流

应用程序使用顺序状态机，包含以下节点:

1. **validate_input** - 参数验证和标准化
2. **research_technology** - 多源数据收集和分析
3. **generate_learning_plan** - 使用 LLM 创建基础学习方案
4. **customize_plan** - 基于用户偏好进行个性化(可选)
5. **generate_final_output** - 结果集成和格式化
6. **handle_error** - 全面错误处理和恢复

## ⚙️ 配置说明

### 环境变量

在 `.env` 文件中配置以下变量:

```bash
# 必需配置
OPENAI_API_KEY=your_openai_api_key_here

# 可选配置 - 增强 LLM 支持
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
USE_DEEPSEEK=true

# 可选配置 - 搜索功能
SERPER_API_KEY=your_serper_api_key_here

# 应用配置
DEBUG=false                          # 启用调试日志
MAX_RETRIES=3                        # API 请求重试次数
TIMEOUT=30                           # 请求超时时间(秒)
```

### 个性化选项

```python
preferences = {
    "learning_style": "visual|hands-on|theoretical",  # 学习风格
    "preferred_time": "morning|evening|flexible",    # 偏好学习时间
    "focus": ["specific_topics"],                     # 重点关注领域
    "tools": ["preferred_tools"],                     # 首选工具
    "project_type": "personal|professional|research", # 项目类型
    "background": "user_background_description"       # 用户背景
}
```

## 🧪 开发和测试

### 开发模式

使用快速模式进行开发和测试，避免 API 调用:

```python
# 使用快速模式跳过网络搜索
result = await agent.research_technology("Python", fast_mode=True)
```

### 测试命令

```bash
# 验证配置
python -c "from config.settings import settings; print('配置有效:', settings.validate_config())"

# 测试工作流组件
python -c "
import asyncio
from src.workflow import TechLearningWorkflow
async def test():
    workflow = TechLearningWorkflow()
    result = await workflow.run('Python', 'beginner', 20)
    print('测试结果:', result['status'])
asyncio.run(test())
"

# 测试智能体功能
python -c "
import asyncio
from agents.research_agent import ResearchAgent
async def test():
    agent = ResearchAgent()
    result = await agent.research_technology('Python', fast_mode=True)
    print('研究测试:', result['status'])
asyncio.run(test())
"

# 运行使用示例
python examples/basic_usage.py

# 测试 DeepSeek API 配置
python testdeepseek.py
```

### 调试模式

```bash
# 启用详细日志
export DEBUG=true
python main.py "Python" --level beginner
```

## 📊 API 参考

### TechLearningAssistant

主要的助手类，提供完整的学习方案生成功能。

```python
class TechLearningAssistant:
    async def create_learning_plan(
        self,
        technology: str,
        experience_level: str = "beginner",
        duration_hours: int = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]

    def save_result(self, result: Dict[str, Any], filename: str = None)
```

### TechLearningWorkflow

LangGraph 工作流引擎，管理整个处理流程。

```python
class TechLearningWorkflow:
    async def run(
        self,
        technology: str,
        experience_level: str = "beginner",
        duration_hours: int = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]
```

### ResearchAgent

技术研究智能体，负责数据收集和分析。

```python
class ResearchAgent:
    async def research_technology(
        self,
        technology: str,
        fast_mode: bool = False
    ) -> Dict[str, Any]
```

## 🔧 扩展开发

### 添加新的搜索源

扩展 `WebSearcher` 类:

```python
async def search_new_source(self, query: str) -> List[Dict[str, Any]]:
    """添加新搜索源实现"""
    # 实现新搜索源逻辑
    pass
```

### 自定义学习方案生成

修改 `LearningAgent` 的提示模板和生成逻辑:

```python
def generate_learning_plan(
    self,
    technology: str,
    analysis: Dict[str, Any],
    duration_hours: int = None,
    experience_level: str = "beginner"
):
    """自定义学习方案生成逻辑"""
    # 修改提示模板和生成方法
    pass
```

### 扩展工作流

向 LangGraph 工作流添加新处理节点:

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

## 🐛 故障排除

### 常见问题

1. **配置验证失败**
   - 检查 `.env` 文件中的 API 密钥是否正确设置
   - 确保至少设置了一个 LLM API 密钥 (OpenAI 或 DeepSeek)

2. **搜索结果质量差**
   - 验证 SERPER_API_KEY 是否正确配置
   - 使用快速模式进行测试: `fast_mode=True`

3. **LLM API 错误**
   - 检查 API 密钥有效性
   - 验证网络连接和速率限制
   - 尝试备用 LLM (DeepSeek)

4. **工作流执行失败**
   - 启用调试模式: `DEBUG=True`
   - 检查各个组件的单独测试结果

### 调试技巧

```bash
# 检查 API 密钥配置
python -c "from config.settings import settings;
print('OpenAI:', bool(settings.OPENAI_API_KEY));
print('DeepSeek:', bool(settings.DEEPSEEK_API_KEY));
print('Serper:', bool(settings.SERPER_API_KEY))"

# 测试工作流状态转换
python -c "
import asyncio
from src.workflow import TechLearningWorkflow
async def debug():
    workflow = TechLearningWorkflow()
    result = await workflow.run('Python', 'beginner', 20)
    print('完整状态:', result)
asyncio.run(debug())
"
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤:

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发最佳实践

- 使用类型提示和文档字符串
- 遵循异步编程模式
- 实现适当的错误处理
- 添加单元测试
- 使用快速模式进行开发测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用开发框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 状态机工作流编排
- [OpenAI](https://openai.com/) - GPT API 支持
- [DeepSeek](https://www.deepseek.com/) - 高性能 LLM API

## 📞 联系方式

如有问题或建议，请通过以下方式联系:

- 开启 [Issue](https://github.com/your-repo/LangChainLearning/issues)
- 发送邮件至: your-email@example.com

---

**注意**: 这是一个学习和演示项目，展示了如何使用 LangGraph 和 LangChain 构建智能 AI 应用。欢迎学习和贡献！