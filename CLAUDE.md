# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## 🎯 Repository Overview

This is a **multi-project AI learning repository** with two main applications and extensive Claude Code integrations:

### Main Projects
1. **Tech Learning Assistant** (`Sample/`) - LangGraph-based technical learning path generator
2. **English Learning Assistant** (`langdeepagent/`) - LangChain-based English learning system

### Claude Code Extensions
- **11 Skills** (`.claude/skills/`) - Specialized capabilities for different domains
- **4 Commands** (`.claude/commands/`) - Custom slash commands
- **7 Agents** (`.claude/agents/`) - Specialized AI agents
- **4 MCP Servers** (`.claude/settings.json`) - Enhanced tool integration

## 🚀 Working with Multiple Projects

### Project Navigation
```bash
# Repository root - overview and configuration
cd /path/to/LangChainLearning/

# Tech Learning Assistant - technical learning paths
cd Sample/

# English Learning Assistant - language learning system
cd langdeepagent/
```

### Environment Setup per Project
Each project has its own virtual environment and requirements:

```bash
# For Tech Learning Assistant
cd Sample/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# For English Learning Assistant
cd langdeepagent/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .  # Install as package
```

## 🏗️ Repository Architecture

### High-Level Structure
```
LangChainLearning/             # Repository root
├── Sample/                    # Tech Learning Assistant (LangGraph)
├── langdeepagent/            # English Learning Assistant (LangChain)
├── langchain/                # LangChain tutorials (7 notebooks)
├── langgraph/                # LangGraph tutorials (7 notebooks)
├── .claude/                  # Claude Code extensions
│   ├── skills/               # 11 specialized skills
│   ├── commands/             # Custom slash commands
│   ├── agents/               # Specialized AI agents
│   └── settings.json         # MCP server configuration
├── .vscode/                  # VS Code configuration
└── README.md                 # Repository overview
```

### When to Use Each Project

**Use Sample/ for:**
- Technical skill learning plans
- Programming language tutorials
- Technology research and roadmap generation
- DevOps and architecture learning paths

**Use langdeepagent/ for:**
- English language learning
- Conversation practice
- Vocabulary and grammar training
- Personalized English learning plans

## 🔧 Claude Code Integration

### Available Skills
Use natural language to trigger specialized capabilities:

```bash
# Code analysis
"Analyze the architecture of this project"

# AI news aggregation
"Get the latest AI industry news"

# Learning assistance
"Create a learning plan for React development"

# Translation
"Translate this technical article to Chinese"
```

### MCP Servers
4 Model Context Protocol servers provide enhanced capabilities:
- **filesystem** - File system operations and monitoring
- **context7** - Intelligent context management
- **playwright** - Web automation and testing
- **sequential-thinking** - Enhanced reasoning capabilities

### Custom Commands
Available slash commands in `.claude/commands/`:
- `/ai-assistant` - Comprehensive AI development assistant
- `/langchain-agent` - LangChain-specific guidance
- `/prompt-optimize` - Prompt optimization tools
- `/texttomd` - Text to Markdown conversion

## ⚙️ Development Configuration

### VS Code Setup
`.vscode/` contains pre-configured development environment:
- Debug configurations for both projects
- Python interpreter settings
- Integrated terminal configuration
- Testing and linting setup

### Environment Variables
Each project requires its own `.env` file:
- `Sample/.env` - Tech learning assistant configuration
- `langdeepagent/.env` - English learning assistant configuration

Required API keys (at least one per project):
- `OPENAI_API_KEY` - OpenAI GPT models
- `DEEPSEEK_API_KEY` - DeepSeek open-source models
- `ANTHROPIC_API_KEY` - Anthropic Claude models

## 🧪 Testing Strategy

### Project-Specific Testing
```bash
# Tech Learning Assistant tests
cd Sample/
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"
python examples/basic_usage.py

# English Learning Assistant tests
cd langdeepagent/
pytest tests/
python -c "
from langdeepagent.agents.learning_agent import LearningAgent
import asyncio
async def test():
    agent = LearningAgent()
    result = await agent.create_learning_plan('intermediate', 'business', fast_mode=True)
    print('Test:', result.get('status'))
asyncio.run(test())
"
```

### Development Mode Testing
Both projects support `fast_mode=True` for development without API calls.

## 📚 Learning Resources

### Tutorial Notebooks
- `langchain/` - 7 Jupyter notebooks covering LangChain fundamentals
- `langgraph/` - 7 Jupyter notebooks covering LangGraph workflows

### Project Documentation
- `Sample/CLAUDE.md` - Detailed tech learning assistant guide
- `langdeepagent/README.md` - English learning assistant documentation

## 🚨 Common Issues

### Multi-Project Conflicts
- Use separate virtual environments for each project
- Ensure correct working directory when running commands
- Validate configuration per project before running

### API Key Management
- Each project needs at least one valid LLM API key
- Check `.env` files in respective project directories
- Use `settings.validate_config()` to verify setup

### Claude Skills Not Working
- Ensure `.claude/` directory is in repository root
- Check Claude Code is properly configured
- Verify MCP servers are running in settings

## 📍 Best Practices

### Development Workflow
1. Choose appropriate project directory for your task
2. Set up project-specific virtual environment
3. Configure environment variables
4. Validate configuration before running
5. Use project-specific CLAUDE.md for detailed guidance

### When to Use Repository vs Project CLAUDE.md
- **Repository CLAUDE.md** (this file) - High-level overview, project selection, Claude extensions
- **Project CLAUDE.md** - Detailed implementation guides, project-specific commands, architecture

### Claude Code Usage
- Skills work across the entire repository
- Commands are available from any directory
- MCP servers provide cross-project functionality
- Each project can leverage all Claude extensions