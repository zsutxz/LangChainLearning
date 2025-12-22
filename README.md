# LangChain & LangGraph 智能学习仓库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-green.svg)](https://github.com/langchain-ai/langgraph)
[![Claude Skills](https://img.shields.io/badge/Claude_Skills-11+-purple.svg)](https://claude.ai/code)

一个全面的人工智能学习和开发仓库，专注于 LangChain 和 LangGraph 框架，包含智能学习助手、Claude 技能集合以及丰富的学习资源。

## 🎯 项目概览

本项目是一个多功能的 AI 学习和开发平台，包含以下核心组件：

### 🤖 智能学习助手
- **技术学习助手** (`Sample/`) - 基于 LangGraph 的技术学习路径生成
- **英语学习助手** (`langdeepagent/`) - 基于 LangChain 的英语学习系统

### 🛠️ Claude 技能集合 (`.claude/skills/`)
11 个专业化 Claude 技能，扩展 Claude Code 的能力：
- 代码架构分析、AI 新闻聚合、GitHub 项目发现
- 业务开发研究、技能创建、专业翻译
- 算法艺术生成、LangChain 设计、LLM 评估
- 提示工程模式、开发模板

### 🔌 MCP 集成 (`.claude/`)
Model Context Protocol 服务器集成，提供增强的工具能力：
- 文件系统操作、上下文管理、Web 自动化、顺序思维

### 📚 学习资源
- **LangChain 教程** (langchain/) - 7 个 Jupyter 教程
- **LangGraph 教程** (langgraph/) - 7 个 Jupyter 教程

## 🚀 快速开始

### 环境要求
- **Python 3.8+**
- **OpenAI API Key** 或 **DeepSeek API Key** (必需)

### 项目设置

#### 技术学习助手 (Sample/)
```bash
cd Sample/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"
```

#### 英语学习助手 (langdeepagent/)
```bash
cd langdeepagent/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .  # 安装为包，创建 'langdeepagent' 命令
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

## 🎮 使用方法

### 技术学习助手
```bash
cd Sample/

# 基础使用
python main.py "Python" --level beginner --hours 30

# 高级使用
python main.py "React" --level intermediate --hours 40 --preferences '{"learning_style": "hands-on"}'

# 交互模式
python main.py --interactive
```

### 英语学习助手
```bash
cd langdeepagent/

# 生成学习计划
python main.py plan --level intermediate --goals "商务英语,日常对话"

# 练习对话
python main.py conversation --scenario "餐厅点餐" --level intermediate

# 交互模式
python main.py interactive

# Web 界面
streamlit run main.py --server.port 8501
```

### Claude 技能
Claude 技能会自动集成到 Claude Code 中，可以通过自然语言触发：

```bash
# 架构分析
"请分析这个项目的架构和设计模式"

# AI 新闻获取
"获取最新的 AI 行业新闻"

# 翻译服务
"将这篇技术文章翻译成中文"
```

## 🏗️ 项目结构

```
LangChainLearning/
├── Sample/                    # 技术学习助手
│   ├── main.py               # CLI 入口点
│   ├── src/                  # 核心模块
│   ├── agents/               # AI 智能体
│   ├── tools/                # 工具模块
│   └── config/               # 配置文件
├── langdeepagent/            # 英语学习助手
│   ├── main.py               # CLI 和 Streamlit 入口
│   ├── langdeepagent/        # 包代码
│   └── tests/                # 测试套件
├── langchain/                # LangChain 教程
├── langgraph/                # LangGraph 教程
├── .claude/                  # Claude 配置
│   ├── skills/               # 11 个技能
│   ├── commands/             # 自定义命令
│   └── agents/               # 7 个专业代理
└── .vscode/                  # VS Code 配置
```

## 🔧 核心技术

### 框架集成
- **LangGraph** - 工作流编排和状态管理
- **LangChain** - LLM 应用开发框架
- **FastAPI** - 现代 Web 框架 (langdeepagent)
- **Streamlit** - 数据应用界面 (langdeepagent)

### LLM 支持
- **OpenAI GPT** - 默认语言模型
- **DeepSeek API** - 开源大语言模型
- **Anthropic Claude** - 通过 API 集成

### 开发工具
- **异步处理** - 全 asyncio 架构
- **模块化设计** - 清晰的组件分离
- **错误处理** - 全面的异常处理机制
- **调试支持** - 分级日志和性能监控

## 🚨 故障排除

### 常见问题
1. **配置验证失败** - 检查 API 密钥配置
2. **搜索无结果** - 验证 SERPER_API_KEY 或使用 fast_mode
3. **LLM API 错误** - 检查 API 密钥、速率限制
4. **工作流失败** - 启用 DEBUG=True 获取详细日志

### 调试命令
```bash
# 检查配置
cd Sample/
python -c "from config.settings import settings; print('Valid:', settings.validate_config())"

# 启用调试
export DEBUG=True
python main.py "Python" --level beginner
```

## 📝 许可证

本项目采用 **MIT 许可证**。

## 🙏 致谢

感谢以下开源项目：
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排框架
- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用框架
- [Claude Code](https://claude.ai/code) - AI 辅助编程环境
- [OpenAI](https://openai.com/) - GPT 系列模型
- [DeepSeek](https://www.deepseek.com/) - 开源大语言模型

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给我们一个 Star！**

**📚 持续学习，持续创新**

</div>