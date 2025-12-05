# LangChain & LangGraph 智能学习仓库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-green.svg)](https://github.com/langchain-ai/langgraph)
[![Claude Skills](https://img.shields.io/badge/Claude_Skills-11+-purple.svg)](https://claude.ai/code)

一个全面的人工智能学习和开发仓库，专注于 LangChain 和 LangGraph 框架，包含智能学习助手、Claude 技能集合以及丰富的学习资源。

## 🎯 项目概览

本项目是一个多功能的 AI 学习和开发平台，包含三个核心组件：

### 🤖 智能技术学习助手 (`Sample/`)
基于 LangGraph 构建的智能学习系统，具备以下核心能力：
- **多源数据收集**：Google 搜索、ArXiv 论文、RSS 订阅的并发搜索
- **个性化学习方案**：根据用户偏好和经验水平生成定制化学习路径
- **智能工作流引擎**：使用 LangGraph 状态机模式实现复杂的多步骤 AI 处理
- **多 LLM 支持**：OpenAI GPT、DeepSeek、Anthropic Claude 的灵活切换
- **高性能异步架构**：全异步处理实现高并发和资源优化
- **企业级错误处理**：全面的异常处理和优雅降级机制

### 🛠️ Claude 技能集合 (`.claude/skills/`)
11 个专业化 Claude 技能，扩展 Claude Code 的能力：
- **代码架构分析器** (`code-architecture-analyzer/`) - 多语言项目架构识别和设计模式分析
- **AI 新闻聚合器** (`ai-news-aggregator/`) - 最新 AI 行业动态收集和总结
- **GitHub AI 项目** (`github-ai-projects/`) - GitHub AI 项目发现和分析
- **业务开发研究助手** (`lead-research-assistant/`) - 业务开发研究自动化
- **技能创建器** (`skill-creator/`) - 元技能，用于创建新的 Claude 技能
- **翻译专家** (`translate-it-article/`) - 专业 IT 文章翻译
- **算法艺术生成器** (`algorithmic-art/`) - 基于 p5.js 的生成艺术创作
- **LangChain 架构设计** (`langchain-architecture/`) - LangChain 应用设计模式和最佳实践
- **LLM 评估策略** (`llm-evaluation/`) - 大语言模型应用评估框架
- **提示工程模式** (`prompt-engineering-patterns/`) - 高级提示工程技术
- **模板技能** (`template-skill/`) - 新技能开发模板

### 🔌 MCP 集成 (`.claude/settings.json`)
Model Context Protocol 服务器集成，提供增强的工具能力：
- **文件系统操作** (`filesystem`) - 文件监控和操作
- **上下文管理** (`context7`) - 智能上下文检索和管理
- **Web 自动化** (`playwright`) - 基于 Playwright 的网页自动化
- **顺序思维** (`sequential-thinking`) - 增强的推理和分析能力

## 🚀 快速开始

### 环境要求
- **Python 3.8+** (需要 async/await 支持)
- **OpenAI API Key** (必需)
- **可选**: Serper API Key (用于 Google 搜索)、DeepSeek API Key、Anthropic API Key

### 快速开发设置

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/LangChainLearning.git
cd LangChainLearning

# 2. 进入主项目目录 (推荐使用 Sample/ 目录的最新版本)
cd Sample/

# 3. 创建并激活虚拟环境
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 4. 安装项目依赖
pip install -r requirements.txt

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥

# 6. 验证配置
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"
```

### 完整环境变量配置

```bash
# === 核心大语言模型配置 ===
OPENAI_API_KEY=sk-...                    # 必需：OpenAI API 密钥
ANTHROPIC_API_KEY=sk-ant-...             # 可选：Anthropic Claude API
USE_DEEPSEEK=true                        # 可选：启用 DeepSeek API
DEEPSEEK_API_KEY=sk-...                  # 启用 DeepSeek 时必需

# === 搜索 API 配置 ===
SERPER_API_KEY=your_serper_key           # 可选：Google 搜索 via Serper

# === 应用配置 ===
DEBUG=False                              # 调试模式开关
MAX_RETRIES=3                            # API 请求重试次数
TIMEOUT=30                               # 请求超时时间（秒）

# === 模型配置 ===
DEFAULT_MODEL=gpt-4o-mini                # 默认 OpenAI 模型
TEMPERATURE=0.1                          # LLM 响应随机性 (0-1)
MAX_TOKENS=4000                          # 最大响应 token 数

# === 搜索配置 ===
MAX_SEARCH_RESULTS=10                    # 每个源的最大搜索结果数
SEARCH_LANGUAGES=["zh", "en"]            # 搜索结果语言

# === 学习计划配置 ===
MIN_COURSE_DURATION=1                    # 最短课程时长（小时）
MAX_COURSE_DURATION=100                  # 最长课程时长（小时）
DEFAULT_COURSE_DURATION=20               # 默认课程时长（小时）
```

## 🎮 使用方法

### 智能技术学习助手

#### 命令行模式 (推荐使用 Sample/ 目录)
```bash
# 进入项目目录
cd Sample/

# 基础使用
python main.py "Python" --level beginner --hours 30

# 高级使用
python main.py "React" --level intermediate --hours 40 --preferences '{"learning_style": "hands-on"}'

# 保存结果到文件
python main.py "Machine Learning" --level advanced --output ml_plan.json

# 交互模式
python main.py --interactive

# 启用调试模式
export DEBUG=True
python main.py "LangChain" --level intermediate
```

#### 编程接口
```python
from main import TechLearningAssistant
import asyncio

async def create_learning_plan():
    assistant = TechLearningAssistant()

    result = await assistant.create_learning_plan(
        technology="LangChain",
        experience_level="intermediate",
        duration_hours=50,
        preferences={
            "learning_style": "project-based",
            "preferred_time": "evening",
            "focus": ["rag", "agents", "workflows"]
        }
    )

    if result["status"] == "completed":
        assistant.save_result(result)
        print("学习方案生成成功！")

    return result

# 运行
result = asyncio.run(create_learning_plan())
```

### 🧪 测试和开发策略

#### 组件测试
```bash
# 验证配置
cd Sample/
python -c "from config.settings import settings; print('配置有效:', settings.validate_config())"

# 测试工作流组件
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

#### 集成测试
```bash
# 运行综合使用示例
cd Sample/
python examples/basic_usage.py

# 测试不同 LLM 配置
export USE_DEEPSEEK=true
python main.py "Python" --level beginner

# 运行独立测试脚本
cd Sample/
python testresearch.py
python testdeepseek.py
```

#### 调试模式测试
```bash
# 启用详细日志记录
export DEBUG=True
cd Sample/
python main.py "React" --level intermediate --hours 30
```

#### 开发模式测试
```bash
# 开发环境快速测试
cd Sample/
python -c "
import asyncio
from main import TechLearningAssistant

async def dev_test():
    assistant = TechLearningAssistant()
    result = await assistant.create_learning_plan(
        technology='FastAPI',
        experience_level='intermediate',
        duration_hours=25,
        preferences={'learning_style': 'hands-on'}
    )
    print('状态:', result['status'])
    if result['status'] == 'completed':
        assistant.save_result(result, 'dev_test.json')

asyncio.run(dev_test())
"
```

### Claude 技能使用

Claude 技能会自动集成到 Claude Code 中，可以通过自然语言触发：

```bash
# 架构分析
skill: "code-architecture-analyzer"
"请分析这个项目的架构和设计模式"

# AI 新闻获取
skill: "ai-news-aggregator"
"获取最新的 AI 行业新闻和发展趋势"

# GitHub 项目发现
skill: "github-ai-projects"
"帮我找一些有趣的 GitHub AI 项目"

# 技能创建
skill: "skill-creator"
"帮我创建一个新的 Claude 技能来处理 X 任务"

# 翻译服务
skill: "translate-it-article"
"将这篇技术文章翻译成中文"

# 算法艺术
skill: "algorithmic-art"
"使用 p5.js 创建一些算法艺术作品"
```

### MCP 服务器使用
MCP 服务器会自动启动，提供以下能力：
- **文件系统监控**: 自动检测文件变化
- **智能上下文**: 增强的对话记忆和检索
- **Web 自动化**: 复杂的网页操作和测试
- **推理增强**: 逐步分析和问题解决

## 🏗️ 项目架构

### 核心目录结构

```
LangChainLearning/
├── Sample/                         # 🆕 最新版本项目目录 (推荐使用)
│   ├── main.py                     # 程序入口 - TechLearningAssistant 类
│   ├── src/                        # 核心模块
│   │   └── tech_learning_workflow.py  # LangGraph 工作流引擎
│   ├── agents/                     # AI 智能体模块
│   │   ├── research_agent.py       # 研究智能体 - 技术数据收集分析
│   │   └── learning_agent.py       # 学习智能体 - 个性化学习方案生成
│   ├── tools/                      # 工具模块
│   │   ├── web_searcher.py         # 网络搜索 - Google、ArXiv、RSS
│   │   └── content_analyzer.py     # 内容分析 - 关键概念提取、趋势分析
│   ├── config/                     # 配置文件
│   │   └── settings.py             # 应用配置 - API密钥、模型设置、DeepSeek支持
│   ├── examples/                   # 使用示例
│   │   └── basic_usage.py          # 基础、高级、批量、个性化使用场景
│   ├── requirements.txt            # Python 依赖
│   ├── .env.example                # 环境变量模板
│   └── CLAUDE.md                   # Claude Code 项目指南
├── .claude/                        # Claude 配置和技能
│   ├── skills/                     # Claude 技能集合 (11个技能)
│   │   ├── code-architecture-analyzer/  # 多语言项目架构分析
│   │   ├── ai-news-aggregator/          # AI新闻收集总结
│   │   ├── github-ai-projects/          # GitHub AI项目发现分析
│   │   ├── lead-research-assistant/     # 业务开发研究自动化
│   │   ├── skill-creator/               # 元技能-创建新技能
│   │   ├── translate-it-article/        # 专业IT文章翻译
│   │   ├── algorithmic-art/             # p5.js生成艺术
│   │   ├── langchain-architecture/      # LangChain设计模式
│   │   ├── llm-evaluation/              # LLM应用评估
│   │   ├── prompt-engineering-patterns/ # 高级提示工程
│   │   └── template-skill/              # 开发模板
│   └── settings.json               # MCP 服务器配置
├── langchain/                      # LangChain 学习资源
├── langgraph/                      # LangGraph 学习资源
├── testresearch.py                 # 搜索功能测试脚本 (在Sample/目录)
├── testdeepseek.py                 # DeepSeek API配置测试 (在Sample/目录)
├── CLAUDE.md                       # 仓库级 Claude Code 指南
└── README.md                       # 项目文档
```

### LangGraph 工作流架构 (Sample/src/tech_learning_workflow.py)

智能学习助手采用状态机模式，包含以下处理节点：

1. **输入验证** (`validate_input`) - 参数验证和标准化
2. **技术研究** (`research_technology`) - 多源数据收集和分析
   - 并发搜索：Google、ArXiv 论文、RSS 订阅
   - 内容分析：关键概念提取、趋势分析、难度评估
3. **方案生成** (`generate_learning_plan`) - 基础学习计划创建
   - 使用 LLM 生成结构化学习路径
   - 包含时间安排、资源推荐、成功指标
4. **个性化定制** (`customize_plan`) - 基于用户偏好定制 (可选)
   - 学习风格适配：视觉、实践、理论
   - 时间安排：晨间、晚间、灵活
5. **输出生成** (`generate_final_output`) - 结果整合和格式化
6. **错误处理** (`handle_error`) - 全面的错误处理和恢复

### 智能体协作模式

- **ResearchAgent** (`agents/research_agent.py`):
  - 协调 WebSearcher 和 ContentAnalyzer
  - 提供全面的数据收集和分析
  - 生成技术研究报告

- **LearningAgent** (`agents/learning_agent.py`):
  - 基于研究结果生成个性化学习计划
  - 匹配用户偏好和经验水平
  - 提供资源推荐和进度跟踪建议

- **状态管理**: WorkflowState 在智能体间传递结构化数据

### 技术栈

#### 核心框架
- **langgraph>=0.2.0** - 工作流编排和状态管理
- **langchain>=0.2.0** - LLM 应用框架
- **langchain-openai>=0.1.0** - OpenAI 集成
- **langchain-community>=0.2.0** - 社区工具和集成

#### LLM 集成
- **OpenAI GPT** - 默认语言模型 (gpt-4o-mini)
- **DeepSeek API** - 可选的替代 LLM (deepseek-chat)
- **Anthropic Claude** - 通过 API 集成支持

#### 异步和网络
- **asyncio, aiohttp** - 高性能异步处理
- **requests>=2.31.0** - HTTP 请求处理
- **beautifulsoup4>=4.12.0** - 网页内容解析

#### 数据采集和处理
- **arxiv>=2.0.0** - 学术论文搜索
- **feedparser>=6.0.0** - RSS 订阅处理
- **lxml>=4.9.0** - XML/HTML 解析
- **pandas>=2.0.0** - 数据分析和处理
- **numpy>=1.24.0** - 数值计算

#### 配置和工具
- **python-dotenv>=1.0.0** - 环境变量管理
- **pydantic>=2.0.0** - 数据验证和设置

#### MCP 集成
- **playwright** - Web 自动化测试
- **filesystem** - 文件系统操作
- **context7** - 智能上下文管理
- **sequential-thinking** - 增强推理能力

## 📊 功能特性

### 🔍 智能研究能力 (Sample/tools/)
- **多源并发搜索**: Google 搜索、ArXiv 学术论文、RSS 订阅源
- **智能内容分析**: 关键概念提取、技术趋势分析、难度等级评估
- **实时数据获取**: 获取最新技术动态、教程和官方文档
- **学术资源整合**: 自动筛选高质量的学术论文和技术报告

### 🎯 个性化学习 (Sample/agents/)
- **经验水平智能适配**: 初学者、中级、专家三级学习路径
- **多学习风格支持**: 视觉型、实践型、理论型学习方式
- **灵活时间安排**: 自定义学习时长、每日时间分配偏好
- **智能进度跟踪**: 成功指标设定、里程碑规划、学习效果评估

### 🛠️ 企业级开发特性
- **高性能异步架构**: 全面使用 asyncio 实现并发处理
- **模块化设计**: 清晰的组件分离，易于扩展和定制
- **完整错误处理**: 全面的异常处理机制和优雅降级
- **详细调试支持**: 分级日志、调试模式、性能监控

### 🔌 Claude 生态深度集成
- **11个专业技能**: 涵盖代码分析、新闻聚合、项目管理等
- **MCP 协议支持**: 先进的 Model Context Protocol 工具集成
- **技能开发框架**: 使用内置技能创建器快速开发新功能
- **自动化工作流**: 复杂多步骤任务的端到端自动化

### 🌐 多语言和多平台支持
- **中英文双语**: 完整的中文文档和英文技术支持
- **跨平台兼容**: Windows、macOS、Linux 全平台支持
- **多 LLM 提供商**: OpenAI、DeepSeek、Anthropic Claude 灵活切换

## 🎨 使用场景

### 个人学习
- 制定技术学习计划
- 获取最新学习资源
- 跟踪技术发展趋势

### 团队培训
- 统一技术栈学习路径
- 个性化培训方案
- 进度跟踪和评估

### 项目开发
- 技术选型研究
- 架构设计和分析
- 最佳实践指导

### 教育教学
- 课程设计和优化
- 教学资源整理
- 学习路径规划

## 🚨 故障排除指南

### 常见问题和解决方案

#### 1. 配置验证失败
**问题**: `settings.validate_config()` 返回 False
```bash
# 检查 API 密钥配置
cd Sample/
python -c "from config.settings import settings; print('OpenAI Key:', bool(settings.OPENAI_API_KEY)); print('DeepSeek Key:', bool(settings.DEEPSEEK_API_KEY)); print('Use DeepSeek:', settings.USE_DEEPSEEK)"

# 解决方案：确保至少配置一个有效的 LLM 提供商
# 编辑 .env 文件，添加有效的 API 密钥
```

#### 2. 搜索返回无结果
**问题**: "未找到关于 X 的相关资料"
```bash
# 测试搜索功能
cd Sample/
python -c "
import asyncio
from tools.web_searcher import WebSearcher

async def test_search():
    searcher = WebSearcher()
    async with searcher:
        results = await searcher.comprehensive_search('Python tutorial')
        print('搜索结果数量:', len(results))

asyncio.run(test_search())
"

# 解决方案：检查 SERPER_API_KEY 配置或使用 fast_mode
```

#### 3. LLM API 错误
**问题**: API 速率限制或认证失败
```bash
# 测试 LLM 配置
cd Sample/
python -c "
from langchain_openai import ChatOpenAI
from config.settings import settings

try:
    llm = ChatOpenAI(**settings.get_llm_config())
    response = llm.invoke('Hello')
    print('LLM 测试成功')
except Exception as e:
    print('LLM 测试失败:', e)
"

# 解决方案：验证 API 密钥，检查速率限制，尝试备用 LLM
```

#### 4. 工作流状态错误
**问题**: 工作流在特定节点失败
```bash
# 启用调试模式获取详细日志
export DEBUG=True
cd Sample/
python main.py "Python" --level beginner
```

#### 5. 批处理内存问题
**问题**: 批处理操作时内存使用过高
```bash
# 使用较小批次或使用 fast_mode 进行开发
cd Sample/
python -c "
import asyncio
from main import TechLearningAssistant

async def memory_efficient_batch():
    assistant = TechLearningAssistant()
    technologies = ['Python', 'JavaScript', 'TypeScript']

    # 逐个处理以限制内存使用
    for tech in technologies:
        try:
            result = await assistant.create_learning_plan(tech, 'beginner', 20)
            if result['status'] == 'completed':
                assistant.save_result(result, f'memory_{tech.lower()}.json')
            print(f'已完成: {tech}')
        except Exception as e:
            print(f'{tech} 处理错误: {e}')

asyncio.run(memory_efficient_batch())
"
```

### 调试模式功能
当 `DEBUG=True` 时，系统提供：
- 详细的 API 请求/响应日志
- 工作流状态转换跟踪
- 性能计时信息
- 带上下文的错误堆栈跟踪

### 获取帮助
1. 在调试模式下检查错误消息
2. 使用 `settings.validate_config()` 验证配置
3. 在运行完整工作流前测试单个组件
4. 使用 fast_mode 进行开发以隔离网络问题

## 🔧 高级配置

### 学习偏好配置
```json
{
  "learning_style": "visual|hands-on|theoretical",
  "preferred_time": "morning|evening|flexible",
  "focus": ["specific_topics"],
  "tools": ["preferred_tools"],
  "project_type": "personal|professional|research",
  "background": "user_background"
}
```

### MCP 服务器配置
项目默认集成以下 MCP 服务器：
- **filesystem**: 文件系统操作
- **context7**: 上下文管理
- **playwright**: Web 自动化
- **sequential-thinking**: 增强推理

### 自定义技能开发
使用内置的技能创建器开发新的 Claude 技能：
```bash
# Claude 会自动引导你创建新技能
"帮我创建一个新的技能来处理 X 任务"
```

## 📈 性能优化

### 异步处理
- 所有 I/O 操作使用 asyncio
- 并发搜索和内容分析
- 高效的资源利用

### 缓存机制
- 搜索结果缓存
- API 响应缓存
- 减少重复请求

### 错误恢复
- 自动重试机制
- 优雅降级处理
- 详细的错误日志

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. **Fork** 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 **Pull Request**

### 开发规范
- 遵循 PEP 8 代码风格
- 添加适当的文档和注释
- 确保所有测试通过
- 更新相关文档

## 📝 更新日志

### v2.2.0 (最新) - 2024年12月
- 📚 **文档全面升级**: 增强 CLAUDE.md 和 README.md，包含完整的开发指南和故障排除
- 🧪 **测试策略完善**: 新增组件测试、集成测试、调试模式测试的详细指南
- 🚨 **故障排除指南**: 新增全面的问题诊断和解决方案文档
- ⚙️ **环境变量扩展**: 从 5 个基础配置扩展到 17 个完整配置选项
- 🏗️ **架构文档深化**: 新增 LangGraph 状态管理、条件路由逻辑详细说明
- 🔧 **开发工作流优化**: 完善的快速开发设置和最佳实践指南

### v2.1.0 - 2024年12月
- 🆕 **新增 Sample/ 目录**: 包含最新版本的项目架构和功能，移除旧的 test/ 目录
- 🔄 **架构优化**: 重构工作流引擎，提升性能和稳定性
- 🛠️ **增强配置系统**: 改进的多 LLM 支持，自动故障转移
- 📚 **完善文档**: 新增详细的 CLAUDE.md 指南和使用示例
- 🐛 **错误处理优化**: 更全面的异常处理和恢复机制
- 📁 **目录结构调整**: 项目主目录从 test/ 迁移至 Sample/，所有文档已更新

### v2.0.0
- ✨ **11 个 Claude 技能**: 完整的技能生态系统
- 🔌 **MCP 协议集成**: Model Context Protocol 先进工具支持
- 🤖 **DeepSeek API 支持**: 新增 DeepSeek 大语言模型集成
- 📊 **增强分析**: 改进的内容分析和学习计划生成
- 🌐 **多语言支持**: 完整的中英文双语界面

### v1.5.0
- ⚡ **性能优化**: 异步处理和并发搜索
- 🎯 **个性化增强**: 更精细的学习偏好配置
- 📈 **进度跟踪**: 新增学习进度和成功指标
- 🔧 **调试模式**: 开发者友好的调试和日志系统

### v1.0.0
- 🚀 **初始版本发布**: 基础的 LangGraph 工作流
- 🤖 **智能学习助手**: 核心功能实现
- 🔍 **多源搜索**: Google、ArXiv、RSS 数据源
- 📋 **内容分析**: 自动化的技术内容分析

## 📄 许可证

本项目采用 **MIT 许可证** - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目和服务：

### 核心框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排和状态管理框架
- [LangChain](https://github.com/langchain-ai/langchain) - 大语言模型应用开发框架

### 语言模型提供商
- [OpenAI](https://openai.com/) - GPT 系列语言模型 API
- [Anthropic](https://anthropic.com/) - Claude 系列模型
- [DeepSeek](https://www.deepseek.com/) - 开源大语言模型和 API 服务

### 工具和服务
- [Serper](https://serper.dev/) - 高性能 Google 搜索 API 服务
- [ArXiv](https://arxiv.org/) - 开放获取的学术论文库
- [Playwright](https://playwright.dev/) - 现代化的 Web 自动化测试框架

### 开发工具
- [Claude Code](https://claude.ai/code) - AI 辅助编程环境
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI 应用工具集成标准

## 📞 联系我们

- **问题报告**: [GitHub Issues](https://github.com/your-username/LangChainLearning/issues)
- **功能建议**: [GitHub Discussions](https://github.com/your-username/LangChainLearning/discussions)
- **邮件联系**: your-email@example.com

### 社区资源

- **中文社区**: 欢迎中文用户参与讨论和贡献
- **技术交流**: 定期举办 LangChain 和 LangGraph 相关技术分享
- **案例分享**: 收集和分享用户的使用案例和最佳实践

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给我们一个 Star！**

**📚 持续学习，持续创新**

Made with ❤️ by the LangChainLearning Team

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/LangChainLearning&type=Date)](https://star-history.com/#your-username/LangChainLearning&Date)

</div>