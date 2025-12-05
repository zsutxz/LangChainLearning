# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

This is a **LangChain and LangGraph learning repository** focused on building intelligent agents and workflows. The repository contains:

1. **Main Project**: An intelligent technical learning assistant built with LangGraph (in `test/` directory)
2. **Claude Skills**: Multiple specialized skills for extending Claude's capabilities (in `.claude/skills/`)
3. **Learning Resources**: Research documents and case studies for AI/ML development (in `langchain/`, `langgraph/` directories)
4. **MCP Integration**: Model Context Protocol servers for enhanced tool integration (in `.claude/settings.json`)

## 🏗️ Repository Structure

### Core Technical Learning Assistant (`test/`)
The main project demonstrates LangGraph workflow capabilities:

```
test/                          # Main LangGraph project directory
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
├── testresearch.py            # Search functionality testing
├── testdeepseek.py            # DeepSeek API configuration testing
└── requirements.txt           # Python dependencies
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
cd test/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Required Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional for enhanced functionality
SERPER_API_KEY=your_serper_api_key_here          # For Google web search
ANTHROPIC_API_KEY=your_anthropic_api_key_here    # Alternative LLM support
USE_DEEPSEEK=true                                # Enable DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key_here      # DeepSeek API key
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

## 🚀 Common Development Commands

### Running the Technical Learning Assistant
```bash
# Navigate to project directory first
cd test/

# Basic usage - generate learning plan
python main.py "Python" --level beginner --hours 30

# Advanced usage with personalization
python main.py "Machine Learning" --level advanced --hours 60 --preferences '{"learning_style": "hands-on"}'

# Interactive mode
python main.py --interactive

# Save results to file
python main.py "React" --level intermediate --output react_plan.json
```

### Testing and Development
```bash
# Run comprehensive usage examples
python examples/basic_usage.py

# Test search functionality
python testresearch.py

# Test specific LLM configurations
python testdeepseek.py

# Validate configuration
python -c "from config.settings import settings; print('Configuration valid:', settings.validate_config())"
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

### LangGraph Workflow Design
The project uses a **state machine pattern** with these sequential nodes:
1. **validate_input** - Parameter validation and normalization
2. **research_technology** - Multi-source data collection and analysis
3. **generate_learning_plan** - Base learning plan creation using LLM
4. **customize_plan** - Personalization based on user preferences (optional)
5. **generate_final_output** - Result integration and formatting
6. **handle_error** - Comprehensive error handling and recovery

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

### 1. TechLearningAssistant (main.py:13)
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

### 2. TechLearningWorkflow (src/tech_learning_workflow.py:41)
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

### 3. ResearchAgent (agents/research_agent.py:14)
Research agent responsible for comprehensive technology data collection and analysis.

```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
research_results = await agent.search_technology_info("Docker")
```

### 4. WebSearcher (tools/web_searcher.py:16)
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
The repository includes 7 specialized Claude skills:

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
The project integrates Model Context Protocol (MCP) servers:
- **filesystem**: File system operations and monitoring
- **context7**: Context management and retrieval
- **playwright**: Web automation and testing
- **sequential-thinking**: Enhanced reasoning capabilities

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