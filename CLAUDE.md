# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

This is a **LangChain and LangGraph learning repository** focused on building intelligent agents and workflows. The repository contains:

1. **Main Project**: An intelligent technical learning assistant built with LangGraph (in `Sample/` directory)
2. **Claude Skills**: Multiple specialized skills for extending Claude's capabilities (in `.claude/skills/`)
3. **Learning Resources**: Research documents and case studies for AI/ML development (in `langchain/`, `langgraph/` directories)
4. **MCP Integration**: Model Context Protocol servers for enhanced tool integration (in `.claude/settings.json`)

## 🏗️ Repository Structure

### Core Technical Learning Assistant (`Sample/`)
The main project demonstrates LangGraph workflow capabilities:

```
Sample/                       # Main LangGraph project directory
├── main.py                    # Entry point - TechLearningAssistant class with CLI interface
├── config/settings.py         # Configuration management - API keys, model settings, DeepSeek support
├── src/tech_learning_workflow.py  # LangGraph workflow engine - state management and process orchestration
├── agents/                    # AI agent modules
│   ├── research_agent.py      # Research agent - technology data collection and analysis
│   └── learning_agent.py      # Learning agent - personalized learning plan generation
├── tools/                     # Utility tools
│   ├── web_searcher.py        # Web search - Google search, Arxiv papers, RSS feeds
│   └── content_analyzer.py    # Content analysis - key concept extraction, trend analysis
├── examples/basic_usage.py    # Usage examples - basic, advanced, batch, personalized scenarios
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── CLAUDE.md                  # Project-specific Claude Code guide
```

### Claude Skills (`.claude/skills/`)
Multiple specialized skills for extending Claude's capabilities:
- `ai-news-aggregator/` - AI news collection and summarization
- `github-ai-projects/` - GitHub AI project discovery and analysis
- `lead-research-assistant/` - Research automation for business development
- `skill-creator/` - Meta-skill for creating new Claude skills
- `template-skill/` - Development template for new skills
- `translate-it-article/` - Professional IT article translation
- `code-architecture-analyzer/` - Multi-language project architecture analysis
- `algorithmic-art/` - Generative art creation using p5.js
- `langchain-architecture/` - LangChain application design patterns
- `llm-evaluation/` - LLM application evaluation strategies
- `prompt-engineering-patterns/` - Advanced prompt engineering techniques

### MCP Integration (`.claude/settings.json`)
Model Context Protocol servers for enhanced capabilities:
- **context7**: Advanced context management and retrieval
- **filesystem**: File system operations and monitoring
- **playwright**: Web automation and testing capabilities
- **sequential-thinking**: Enhanced reasoning and step-by-step analysis

## ⚙️ Development Environment Setup

### Prerequisites
- **Python 3.8+** (async/await support required)
- **API Keys**: OpenAI (required), Serper (optional for web search)

### Installation Commands
```bash
# Navigate to the main project directory
cd Sample/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Complete Environment Variables Reference
```bash
# === Core LLM Configuration ===
OPENAI_API_KEY=sk-...                    # Required: OpenAI API key
ANTHROPIC_API_KEY=sk-ant-...             # Optional: Anthropic Claude API key
USE_DEEPSEEK=true                        # Optional: Enable DeepSeek API
DEEPSEEK_API_KEY=sk-...                  # Required if USE_DEEPSEEK=true

# === Search APIs (Optional) ===
SERPER_API_KEY=your_serper_key           # Google search via Serper

# === Application Configuration ===
DEBUG=False                              # Enable debug logging
MAX_RETRIES=3                            # API request retry attempts
TIMEOUT=30                               # Request timeout in seconds

# === Model Configuration ===
DEFAULT_MODEL=gpt-4o-mini                # Default OpenAI model
TEMPERATURE=0.1                          # LLM response randomness (0-1)
MAX_TOKENS=4000                          # Maximum response tokens

# === DeepSeek Configuration ===
DEEPSEEK_MODEL=deepseek-chat             # DeepSeek model name
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1  # DeepSeek API endpoint

# === Search Configuration ===
MAX_SEARCH_RESULTS=10                    # Maximum search results per source
SEARCH_LANGUAGES=["zh", "en"]            # Search result languages

# === Learning Plan Configuration ===
MIN_COURSE_DURATION=1                    # Minimum course duration (hours)
MAX_COURSE_DURATION=100                  # Maximum course duration (hours)
DEFAULT_COURSE_DURATION=20               # Default course duration (hours)
```

### Key Dependencies
- **langgraph>=0.2.0** - Workflow orchestration and state management
- **langchain>=0.2.0** - LLM framework
- **langchain-openai>=0.1.0** - OpenAI integration
- **langchain-community>=0.2.0** - Community tools and integrations
- **asyncio, aiohttp** - Async processing for performance
- **requests, beautifulsoup4** - Web scraping capabilities
- **python-dotenv** - Environment variable management
- **arxiv>=2.0.0** - Academic paper search
- **feedparser>=6.0.0** - RSS feed processing
- **lxml>=4.9.0** - XML/HTML parsing
- **pandas>=2.0.0** - Data manipulation and analysis

## 🚀 Development Workflow

### Quick Development Setup
```bash
# 1. Navigate to project directory
cd Sample/

# 2. Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your API keys

# 5. Validate configuration
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"
```

### Running the Technical Learning Assistant
```bash
# Navigate to project directory first
cd Sample/

# Basic usage - generate learning plan
python main.py "Python" --level beginner --hours 30

# Advanced usage with personalization
python main.py "Machine Learning" --level advanced --hours 60 --preferences '{"learning_style": "hands-on"}'

# Interactive mode
python main.py --interactive

# Save results to file
python main.py "React" --level intermediate --output react_plan.json
```

### 🧪 Testing Strategy

#### Component Testing
```bash
# Test configuration validation
cd Sample/
python -c "from config.settings import settings; print('Valid:', settings.validate_config())"

# Test workflow components
python -c "
import asyncio
from src.tech_learning_workflow import TechLearningWorkflow

async def test_workflow():
    workflow = TechLearningWorkflow()
    result = await workflow.run('Python', 'beginner', 20)
    print('Test result:', result['status'])

asyncio.run(test_workflow())
"

# Test agent functionality
python -c "
import asyncio
from agents.research_agent import ResearchAgent

async def test_research():
    agent = ResearchAgent()
    result = await agent.research_technology('Python', fast_mode=True)
    print('Research test:', result['status'])

asyncio.run(test_research())
"
```

#### Integration Testing
```bash
# Run comprehensive usage examples
cd Sample/
python examples/basic_usage.py

# Test different LLM configurations
export USE_DEEPSEEK=true
python main.py "Python" --level beginner

# Run standalone test scripts
python testresearch.py
python testdeepseek.py
```

#### Debug Mode Testing
```bash
# Enable comprehensive logging
export DEBUG=True
cd Sample/
python main.py "React" --level intermediate --hours 30
```

### Configuration Management
```bash
# Verify required API keys are set
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"

# Test DeepSeek API configuration
python testdeepseek.py

# Enable debug mode for troubleshooting
export DEBUG=True
python main.py "Python" --level beginner

# Test search functionality
python testresearch.py
```

## 🏛️ Core Architecture Patterns

### Detailed LangGraph State Management
The `WorkflowState` TypedDict defines the complete data contract:
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

### LangGraph Workflow Design
The project uses a **state machine pattern** with these sequential nodes:
1. **validate_input** - Parameter validation and normalization
2. **research_technology** - Multi-source data collection and analysis
3. **generate_learning_plan** - Base learning plan creation using LLM
4. **customize_plan** - Personalization based on user preferences (optional)
5. **generate_final_output** - Result integration and formatting
6. **handle_error** - Comprehensive error handling and recovery

### Conditional Routing Logic
The workflow uses conditional routing for personalization:
```python
workflow.add_conditional_edges(
    "generate_learning_plan",
    self._should_customize,  # Routes based on preferences existence
    {
        "customize": "customize_plan",
        "finalize": "generate_final_output"
    }
)
```

### Fast Mode Implementation
The research agent supports a `fast_mode=True` parameter that skips network searches and provides mock data for development/testing.

### Agent Collaboration Pattern
- **ResearchAgent**: Coordinates WebSearcher and ContentAnalyzer for comprehensive data collection
- **LearningAgent**: Generates personalized learning plans based on research results
- **State Management**: WorkflowState passes structured data between agents

### Async Processing Pattern
All components use asyncio for high-performance concurrent operations:
```python
async def research_technology(self, technology: str):
    # Concurrent web search and content analysis
    results = await self.web_searcher.comprehensive_search(query)
    analysis = self.content_analyzer.analyze_content(results)
```

## 📊 Key Components and Usage

### 1. TechLearningAssistant (Sample/main.py:13)
Primary user interface class providing complete learning plan generation.

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

# Execute
result = asyncio.run(create_learning_plan())
```

### 2. TechLearningWorkflow (Sample/src/tech_learning_workflow.py:41)
LangGraph workflow engine managing the entire learning plan generation process.

```python
from src.tech_learning_workflow import TechLearningWorkflow

workflow = TechLearningWorkflow()
result = await workflow.run(
    technology="React",
    experience_level="intermediate",
    duration_hours=40,
    preferences={"learning_style": "hands-on"}
)
```

### 3. ResearchAgent (Sample/agents/research_agent.py:14)
Research agent responsible for comprehensive technology data collection and analysis.

```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
research_results = await agent.search_technology_info("Docker")
```

### 4. WebSearcher (Sample/tools/web_searcher.py:16)
Multi-source web search tool supporting Google Search, Arxiv papers, and RSS feeds.

```python
from tools.web_searcher import WebSearcher

async with WebSearcher() as searcher:
    google_results = await searcher.search_google("Python tutorial")
    arxiv_papers = await searcher.search_arxiv("machine learning")
    rss_content = await searcher.search_rss_feeds("AI news")
```

## 🔧 Development Patterns

### Adding New Search Sources
Extend the WebSearcher class with new search methods:
```python
async def search_new_source(self, query: str) -> List[Dict[str, Any]]:
    """Add new search source implementation"""
    # Implement new search source logic
    pass
```

### Customizing Learning Plan Generation
Modify the LearningAgent prompt templates and generation logic:
```python
def generate_learning_plan(self, technology: str, analysis: Dict[str, Any],
                         duration_hours: int = None, experience_level: str = "beginner"):
    """Customize learning plan generation logic"""
    # Modify prompt templates and generation approach
    pass
```

### Extending the LangGraph Workflow
Add new processing nodes to the workflow:
```python
def _create_workflow(self) -> StateGraph:
    """Extend workflow with additional processing steps"""
    workflow = StateGraph(WorkflowState)

    # Add new node
    workflow.add_node("new_processing_step", self._new_processing_step)

    # Update workflow edges
    workflow.add_edge("research_technology", "new_processing_step")
    workflow.add_edge("new_processing_step", "generate_learning_plan")

    return workflow.compile()
```

## 🎨 Claude Skills Integration

### Available Skills
The repository includes 11 specialized Claude skills:

1. **Code Architecture Analyzer** (`code-architecture-analyzer/`)
   - Multi-language project architecture analysis
   - Design pattern recognition and dependency mapping
   - Use with: `Analyze this project's architecture and identify design patterns`

2. **AI News Aggregator** (`ai-news-aggregator/`)
   - AI industry news collection and summarization
   - Use with: `Get the latest AI news and trends`

3. **GitHub AI Projects** (`github-ai-projects/`)
   - Discovery and analysis of AI projects on GitHub
   - Use with: `Find interesting AI projects on GitHub`

4. **Lead Research Assistant** (`lead-research-assistant/`)
   - Business development research automation
   - Use with: `Research potential leads for our product`

5. **Skill Creator** (`skill-creator/`)
   - Meta-skill for creating new Claude skills
   - Use with: `Help me create a new skill for X`

6. **Translate IT Article** (`translate-it-article/`)
   - Professional IT article translation
   - Use with: `Translate this technical article to Chinese`

7. **Template Skill** (`template-skill/`)
   - Development template for new skills
   - Use with: `Create a new skill based on the template`

8. **Algorithmic Art** (`algorithmic-art/`)
   - Generative art creation using p5.js
   - Use with: `Create algorithmic art with p5.js`

9. **LangChain Architecture** (`langchain-architecture/`)
   - LangChain application design patterns
   - Use with: `Design a LangChain application for X`

10. **LLM Evaluation** (`llm-evaluation/`)
    - LLM application evaluation strategies
    - Use with: `Evaluate this LLM application's performance`

11. **Prompt Engineering Patterns** (`prompt-engineering-patterns/`)
    - Advanced prompt engineering techniques
    - Use with: `Optimize prompts for better LLM performance`

### Skill Usage Pattern
```bash
# Skills are automatically available through Claude Code
# Use natural language to trigger specific skills
skill: "code-architecture-analyzer"  # Explicit skill invocation
# or let Claude automatically select based on context
```

### MCP Integration
The project integrates Model Context Protocol (MCP) servers through `.claude/settings.json`:
- **filesystem**: File system operations and monitoring (configured for D:\work\AI\ClaudeTest)
- **context7**: Context management and retrieval via Upstash
- **playwright**: Web automation and testing capabilities
- **sequential-thinking**: Enhanced reasoning and step-by-step analysis

### Hook System
The project includes PreToolUse and PostToolUse hooks for filesystem operations:
- Automatic logging of file write operations to `.claude/post-hook-test.log` and `.claude/pre-hook-test.log`

## 🛠️ Project Strengths and Learning Outcomes

This repository demonstrates and teaches:

### Technical Concepts
- **LangGraph workflow patterns** and state machine design
- **Multi-agent system architecture** and collaboration patterns
- **Async programming** in AI/ML applications for performance
- **LLM integration** best practices with multiple providers
- **Configuration management** for production AI applications
- **Claude Skills development** and MCP integration

### Practical Skills
- **Error handling** and resilience patterns with graceful fallbacks
- **Extensibility** through modular design principles
- **Production readiness** with comprehensive configuration and logging
- **Performance optimization** through async processing and concurrent operations
- **Skill development** for Claude Code extensibility

### Use Cases Demonstrated
1. **Automated Learning Plan Generation**: Personalized educational content creation
2. **Multi-source Research**: Comprehensive data collection from diverse sources
3. **Workflow Orchestration**: Complex multi-step AI processes with LangGraph
4. **Agent Collaboration**: Multiple specialized AI agents working together
5. **Configuration Flexibility**: Support for multiple LLM providers and search APIs
6. **Skill-Based Architecture**: Extensible system through Claude Skills
7. **MCP Integration**: Advanced tool integration through Model Context Protocol

The repository serves as an excellent reference for building production-ready AI applications with LangChain and LangGraph, demonstrating both theoretical concepts and practical implementation patterns for intelligent workflow automation and Claude Code skill development.

## 📍 Important Notes

### Project Directory Change
The main project has been moved from `test/` to `Sample/` directory. All references to `test/` in this documentation have been updated to reflect the new structure.

### Standalone Test Scripts
The repository includes test scripts in the `Sample/` directory:
- `testresearch.py` - Tests search functionality independently
- `testdeepseek.py` - Tests DeepSeek API configuration

Run these from the `Sample/` directory to test individual components.

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Configuration Validation Fails
**Problem**: `settings.validate_config()` returns False
```bash
# Check API key configuration
cd Sample/
python -c "from config.settings import settings; print('OpenAI Key:', bool(settings.OPENAI_API_KEY)); print('DeepSeek Key:', bool(settings.DEEPSEEK_API_KEY)); print('Use DeepSeek:', settings.USE_DEEPSEEK)"

# Fix: Ensure at least one LLM provider is properly configured
# Edit .env file with valid API keys
```

#### 2. Search Returns No Results
**Problem**: "未找到关于 X 的相关资料"
```bash
# Test search functionality
cd Sample/
python -c "
import asyncio
from tools.web_searcher import WebSearcher

async def test_search():
    searcher = WebSearcher()
    async with searcher:
        results = await searcher.comprehensive_search('Python tutorial')
        print('Search results:', len(results))

asyncio.run(test_search())
"

# Fix: Check SERPER_API_KEY configuration or use fast_mode
```

#### 3. LLM API Errors
**Problem**: API rate limits or authentication failures
```bash
# Test LLM configuration
cd Sample/
python -c "
from langchain_openai import ChatOpenAI
from config.settings import settings

try:
    llm = ChatOpenAI(**settings.get_llm_config())
    response = llm.invoke('Hello')
    print('LLM test successful')
except Exception as e:
    print('LLM test failed:', e)
"

# Fix: Verify API keys, check rate limits, try alternative LLM
```

#### 4. Workflow State Errors
**Problem**: Workflow fails at specific nodes
```bash
# Enable debug mode for detailed logging
export DEBUG=True
cd Sample/
python main.py "Python" --level beginner
```

#### 5. Memory Issues in Batch Processing
**Problem**: High memory usage during batch operations
```bash
# Process in smaller batches or use fast_mode for development
python -c "
import asyncio
from main import TechLearningAssistant

async def memory_efficient_batch():
    assistant = TechLearningAssistant()
    technologies = ['Python', 'JavaScript', 'TypeScript']

    # Process one at a time to limit memory usage
    for tech in technologies:
        try:
            result = await assistant.create_learning_plan(tech, 'beginner', 20)
            if result['status'] == 'completed':
                assistant.save_result(result, f'memory_{tech.lower()}.json')
            print(f'Completed: {tech}')
        except Exception as e:
            print(f'Error with {tech}: {e}')

asyncio.run(memory_efficient_batch())
"
```

### Debug Mode Features
When `DEBUG=True`, the system provides:
- Detailed API request/response logging
- Workflow state transition tracking
- Performance timing information
- Error stack traces with context

### Getting Help
1. Check error messages in debug mode
2. Verify configuration with `settings.validate_config()`
3. Test individual components before running full workflow
4. Use fast_mode for development to isolate network issues