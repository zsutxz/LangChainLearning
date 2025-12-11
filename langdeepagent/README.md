# LangDeepAgent - 英语学习 AI Agent

基于 DeepSeek API 和 LangChain 的智能英语学习助手，提供个性化的英语学习方案和实时辅导。

## 🎯 项目特色

- **智能水平评估**：AI 驱动的英语能力精准评估
- **个性化学习计划**：根据个人目标和水平定制学习路径
- **多维度训练**：词汇、语法、听力、口语、阅读全方位提升
- **实时对话练习**：模拟真实场景的英语对话训练
- **进度跟踪**：智能学习进度监控和成就系统

## 🏗️ 项目结构

```
langdeepagent/
├── src/                    # 核心源码
│   ├── __init__.py
│   ├── agent.py           # 主要的英语学习 Agent
│   ├── workflow.py        # LangGraph 工作流
│   └── models.py          # 数据模型定义
├── agents/                # 专业 Agent
│   ├── __init__.py
│   ├── vocabulary_agent.py    # 词汇学习 Agent
│   ├── grammar_agent.py       # 语法学习 Agent
│   ├── conversation_agent.py  # 对话练习 Agent
│   └── assessment_agent.py    # 水平评估 Agent
├── tools/                 # 学习工具
│   ├── __init__.py
│   ├── vocabulary_tools.py    # 词汇工具
│   ├── grammar_tools.py       # 语法工具
│   ├── conversation_tools.py  # 对话工具
│   └── progress_tools.py      # 进度跟踪工具
├── config/                # 配置文件
│   ├── __init__.py
│   ├── settings.py           # 应用配置
│   └── prompts.py            # 提示词模板
├── tests/                 # 测试文件
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_tools.py
├── examples/              # 使用示例
│   ├── basic_usage.py
│   ├── conversation_practice.py
│   └── vocabulary_learning.py
├── docs/                  # 文档
│   ├── api_reference.md
│   └── user_guide.md
├── requirements.txt       # 依赖包
├── .env.example          # 环境变量示例
├── main.py               # 主程序入口
└── README.md             # 项目说明
```

## 🚀 快速开始

### 1. 环境设置

```bash
# 克隆项目
cd langdeepagent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 DeepSeek API 密钥
```

### 2. 基础使用

```python
from src.agent import EnglishLearningAgent

# 创建英语学习助手
agent = EnglishLearningAgent()

# 生成个性化学习计划
plan = await agent.create_learning_plan(
    current_level="intermediate",
    learning_goals=["商务英语", "日常对话"],
    target_scenario="商务会议"
)

# 开始对话练习
conversation = await agent.start_conversation(
    scenario="餐厅点餐",
    difficulty_level="intermediate"
)

# 词汇学习
vocabulary_session = await agent.learn_vocabulary(
    topic="商务词汇",
    count=20
)
```

### 3. 命令行使用

```bash
# 生成学习计划
python main.py plan --level intermediate --goals "商务英语,日常对话"

# 开始对话练习
python main.py conversation --scenario "餐厅点餐" --level intermediate

# 词汇学习
python main.py vocabulary --topic "商务词汇" --count 20

# 交互模式
python main.py interactive
```

## 🎮 功能模块

### 🧠 智能评估
- 英语水平精准测试
- 学习目标分析
- 个性化建议生成

### 📚 词汇学习
- 智能词汇推荐
- 词根词缀记忆法
- 语境化学习
- 复习计划制定

### 📖 语法训练
- 语法点智能推荐
- 错误诊断和纠正
- 渐进式学习路径
- 实战练习题

### 💬 对话练习
- 场景化对话模拟
- 实时发音纠正
- 流利度评估
- 文化背景讲解

### 📊 进度跟踪
- 学习数据可视化
- 成就徽章系统
- 学习效率分析
- 个性化建议

## 🔧 技术栈

- **DeepSeek API**: 强大的语言模型支持
- **LangChain**: LLM 应用开发框架
- **LangGraph**: 工作流编排
- **FastAPI**: Web API 框架
- **SQLite**: 数据存储
- **Streamlit**: 用户界面

## 📝 API 参考

### EnglishLearningAgent

主要方法：
- `create_learning_plan()`: 创建学习计划
- `start_conversation()`: 开始对话练习
- `learn_vocabulary()`: 词汇学习
- `practice_grammar()`: 语法练习
- `assess_level()`: 水平评估

### 配置选项

```python
# 在 .env 文件中配置
DEEPSEEK_API_KEY=your_api_key_here
DEFAULT_MODEL=deepseek-chat
TEMPERATURE=0.7
MAX_TOKENS=2000
```

## 🎯 使用场景

1. **个人自学**：个性化学习计划，自主提升英语能力
2. **企业培训**：员工英语技能提升计划
3. **学校教学**：辅助教学工具，个性化辅导
4. **语言机构**：智能化教学管理系统

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

感谢 DeepSeek 提供的强大 AI 能力，以及 LangChain 团队的优秀框架。

---

**让 AI 成为你的英语学习伙伴，开启智能学习新体验！** 🚀