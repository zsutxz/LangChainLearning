# LangDeepAgent API 参考文档

## 概述

LangDeepAgent 是一个基于 DeepSeek API 的智能英语学习助手，提供个性化的英语学习方案和实时辅导。

## 核心类：EnglishLearningAgent

### 初始化

```python
from src.agent import EnglishLearningAgent

agent = EnglishLearningAgent()
```

### 主要方法

#### 1. 创建学习计划

```python
async def create_learning_plan(
    user_id: str,
    current_level: str,
    learning_goals: List[str],
    target_scenario: str = "通用英语",
    study_time_per_day: int = 2,
    study_duration_weeks: int = 12
) -> LearningPlan
```

**参数：**
- `user_id`: 用户唯一标识符
- `current_level`: 当前英语水平 (beginner/intermediate/advanced)
- `learning_goals`: 学习目标列表
- `target_scenario`: 目标语言场景
- `study_time_per_day`: 每日学习时间（小时）
- `study_duration_weeks`: 学习周期（周）

**返回：**
- `LearningPlan`: 个性化学习计划对象

**示例：**
```python
plan = await agent.create_learning_plan(
    user_id="user123",
    current_level="intermediate",
    learning_goals=["商务英语", "日常对话"],
    target_scenario="商务会议",
    study_time_per_day=2,
    study_duration_weeks=8
)
```

#### 2. 英语水平评估

```python
async def assess_level(
    user_id: str,
    current_level: str,
    learning_goals: List[str],
    target_scenario: str = "通用英语"
) -> AssessmentResult
```

**参数：**
- `user_id`: 用户唯一标识符
- `current_level`: 自评当前水平
- `learning_goals`: 学习目标列表
- `target_scenario`: 目标场景

**返回：**
- `AssessmentResult`: 详细的能力评估结果

#### 3. 词汇学习

```python
async def learn_vocabulary(
    user_id: str,
    topic: str,
    count: int = 20,
    difficulty_level: Optional[str] = None
) -> VocabularySession
```

**参数：**
- `user_id`: 用户唯一标识符
- `topic`: 学习主题
- `count`: 学习词汇数量
- `difficulty_level`: 难度级别（可选）

**返回：**
- `VocabularySession`: 词汇学习会话对象

#### 4. 对话练习

```python
async def start_conversation(
    user_id: str,
    scenario: str,
    difficulty_level: Optional[str] = None
) -> ConversationSession
```

**参数：**
- `user_id`: 用户唯一标识符
- `scenario`: 对话场景
- `difficulty_level`: 难度级别（可选）

**返回：**
- `ConversationSession`: 对话练习会话对象

#### 5. 语法练习

```python
async def practice_grammar(
    user_id: str,
    topic: str,
    difficulty_level: Optional[str] = None
) -> GrammarSession
```

**参数：**
- `user_id`: 用户唯一标识符
- `topic`: 语法主题
- `difficulty_level`: 难度级别（可选）

**返回：**
- `GrammarSession`: 语法学习会话对象

#### 6. 进度评估

```python
async def evaluate_progress(user_id: str) -> ProgressReport
```

**参数：**
- `user_id`: 用户唯一标识符

**返回：**
- `ProgressReport`: 学习进度报告

#### 7. 交互式对话

```python
async def interactive_conversation(
    user_id: str,
    session_id: str,
    user_message: str
) -> Dict[str, Any]
```

**参数：**
- `user_id`: 用户唯一标识符
- `session_id`: 对话会话ID
- `user_message`: 用户消息

**返回：**
- `Dict`: 包含AI回复和建议的字典

## 数据模型

### LearningPlan

```python
class LearningPlan(BaseModel):
    plan_id: str
    user_id: str
    current_level: str
    learning_goals: List[str]
    target_scenario: str
    overall_goals: List[str]
    milestones: List[WeeklyPlan]
    daily_schedule: Dict[str, str]
    resources: LearningResources
    created_at: datetime
    updated_at: datetime
```

### VocabularySession

```python
class VocabularySession(BaseModel):
    session_id: str
    topic: str
    words: List[VocabularyWord]
    learning_strategies: List[str]
    practice_exercises: List[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime] = None
```

### ConversationSession

```python
class ConversationSession(BaseModel):
    session_id: str
    scenario: str
    difficulty_level: str
    background: str
    roles: List[Dict[str, str]]
    dialogue: List[DialogueTurn]
    key_vocabulary: List[str]
    useful_phrases: List[str]
    practice_tips: List[str]
    created_at: datetime
```

### AssessmentResult

```python
class AssessmentResult(BaseModel):
    assessment_id: str
    user_id: str
    assessment_date: datetime
    current_level: str
    vocabulary_level: int
    grammar_level: int
    listening_level: int
    speaking_level: int
    reading_level: int
    writing_level: int
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
```

## 配置

### 环境变量

```bash
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-chat
USE_DEEPSEEK=true

# 应用配置
TEMPERATURE=0.7
MAX_TOKENS=2000
TIMEOUT=30

# 学习配置
DEFAULT_LANGUAGE_LEVEL=intermediate
MAX_VOCABULARY_PER_SESSION=50
MAX_CONVERSATION_ROUNDS=10
```

### 配置类

```python
from config import settings

# 获取 LLM 配置
llm_config = settings.get_llm_config()

# 验证配置
is_valid = settings.validate_config()
```

## 错误处理

所有方法都包含完整的错误处理机制：

```python
try:
    plan = await agent.create_learning_plan(
        user_id="user123",
        current_level="intermediate",
        learning_goals=["商务英语"]
    )
except Exception as e:
    print(f"创建学习计划失败: {str(e)}")
```

## 使用示例

### 完整学习流程

```python
import asyncio
from src.agent import EnglishLearningAgent

async def complete_learning_flow():
    agent = EnglishLearningAgent()
    user_id = "student123"

    # 1. 评估水平
    assessment = await agent.assess_level(
        user_id=user_id,
        current_level="intermediate",
        learning_goals=["商务英语"],
        target_scenario="商务会议"
    )

    # 2. 创建学习计划
    plan = await agent.create_learning_plan(
        user_id=user_id,
        current_level=assessment.current_level,
        learning_goals=["商务英语", "日常对话"],
        target_scenario="商务会议"
    )

    # 3. 词汇学习
    vocab_session = await agent.learn_vocabulary(
        user_id=user_id,
        topic="商务词汇",
        count=20
    )

    # 4. 对话练习
    conv_session = await agent.start_conversation(
        user_id=user_id,
        scenario="商务会议讨论",
        difficulty_level="intermediate"
    )

    # 5. 进度评估
    progress = await agent.evaluate_progress(user_id)

    return {
        "assessment": assessment,
        "plan": plan,
        "vocabulary": vocab_session,
        "conversation": conv_session,
        "progress": progress
    }

# 运行示例
result = asyncio.run(complete_learning_flow())
```

## 命令行接口

### 基本用法

```bash
# 创建学习计划
python main.py plan --level intermediate --goals "商务英语,日常对话"

# 水平评估
python main.py assess --level intermediate --goals "提升英语能力"

# 词汇学习
python main.py vocab --topic "商务词汇" --count 20

# 对话练习
python main.py conv --scenario "餐厅点餐"

# 进度查询
python main.py progress

# 交互模式
python main.py --interactive
```

### 参数说明

#### plan 命令
- `--level`: 当前水平 (beginner/intermediate/advanced)
- `--goals`: 学习目标，用逗号分隔
- `--scenario`: 目标场景
- `--time`: 每日学习时间（小时）
- `--duration`: 学习周期（周）

#### vocab 命令
- `--topic`: 学习主题（必需）
- `--count`: 学习词汇数量
- `--level`: 难度级别

#### conv 命令
- `--scenario`: 对话场景（必需）
- `--level`: 难度级别

## 高级功能

### 用户档案管理

```python
# 获取用户档案
profile = agent.get_user_profile(user_id)

# 清除用户数据
agent.clear_user_data(user_id)
```

### 自定义提示词

```python
from config import ENGLISH_LEARNING_PROMPTS

# 修改词汇学习提示词
custom_prompt = """
自定义的词汇学习提示词...
"""
ENGLISH_LEARNING_PROMPTS["vocabulary_learning"] = custom_prompt
```

## 性能优化

### 缓存配置

```python
# 启用缓存
ENABLE_CACHE=true
CACHE_TTL=3600
```

### 异步处理

所有方法都是异步的，支持并发处理：

```python
import asyncio

async def concurrent_learning():
    agent = EnglishLearningAgent()
    user_id = "user123"

    # 并发执行多个学习任务
    tasks = [
        agent.learn_vocabulary(user_id, "商务词汇", 20),
        agent.start_conversation(user_id, "商务会议"),
        agent.practice_grammar(user_id, "现在时态")
    ]

    results = await asyncio.gather(*tasks)
    return results
```

## 扩展开发

### 添加新的学习模块

1. 创建新的 Agent 类
2. 实现相应的方法
3. 添加到主 Agent 中

### 自定义评估标准

```python
class CustomAssessmentAgent:
    def __init__(self):
        self.llm = ChatOpenAI(**settings.get_llm_config())

    async def custom_assessment(self, user_data):
        # 自定义评估逻辑
        pass
```

## 故障排除

### 常见问题

1. **API 密钥错误**
   - 检查 .env 文件中的 DEEPSEEK_API_KEY
   - 确认密钥有效且额度充足

2. **网络连接问题**
   - 检查网络连接
   - 设置代理（如需要）

3. **响应时间过长**
   - 调整 TIMEOUT 参数
   - 减少 MAX_TOKENS 设置

4. **内存使用过高**
   - 启用缓存
   - 定期清理用户数据

### 调试模式

```bash
# 启用调试模式
DEBUG=true python main.py --interactive
```

## 更新日志

### v0.1.0 (2024-12-10)
- 初始版本发布
- 基础英语学习功能
- DeepSeek API 集成
- 命令行界面

---

更多信息请参考 [README.md](../README.md) 和 [用户指南](user_guide.md)。