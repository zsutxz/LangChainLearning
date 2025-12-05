# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **LangGraph-based Intelligent Technical Learning Assistant** (基于LangGraph的智能技术学习助手) - a Python application that automatically collects research on IT technologies and generates personalized learning plans using AI agents.

## Core Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application
```bash
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
python ../testresearch.py

# Test specific LLM configurations
python ../testdeepseek.py

# Validate configuration
python -c "from config.settings import settings; print('Configuration valid:', settings.validate_config())"
```

### Configuration Management
```bash
# Verify required API keys are set
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"

# Enable debug mode for troubleshooting
export DEBUG=True
python main.py "Python" --level beginner
```

## Architecture Overview

### Technology Stack
- **LangGraph**: Workflow orchestration using state machines
- **LangChain**: LLM framework for AI agent integration
- **Python 3.8+**: With async/await for concurrent processing
- **Multiple LLM Support**: OpenAI GPT and DeepSeek API integration

### Core Architecture Pattern

This project uses a **state machine workflow pattern** with sequential processing nodes:

1. **validate_input** - Parameter validation and normalization
2. **research_technology** - Multi-source data collection and analysis
3. **generate_learning_plan** - Base learning plan creation using LLM
4. **customize_plan** - Personalization based on user preferences (optional)
5. **generate_final_output** - Result integration and formatting
6. **handle_error** - Comprehensive error handling and recovery

### Key Components

#### TechLearningWorkflow (src/tech_learning_workflow.py:41)
The main LangGraph workflow engine that orchestrates the entire learning plan generation process through a state machine. Uses StateGraph to manage sequential processing and conditional routing.

#### Agent Collaboration Pattern
- **ResearchAgent** (agents/research_agent.py): Coordinates WebSearcher and ContentAnalyzer for comprehensive data collection
- **LearningAgent** (agents/learning_agent.py): Generates personalized learning plans based on research results
- **State Management**: WorkflowState passes structured data between agents

#### Multi-Source Research System
- **WebSearcher** (tools/web_searcher.py): Concurrent search across Google, ArXiv papers, and RSS feeds
- **ContentAnalyzer** (tools/content_analyzer.py): Content analysis and key concept extraction

#### Configuration System (config/settings.py)
- **Multi-LLM Support**: OpenAI GPT and DeepSeek API with automatic fallback
- **Environment-based Configuration**: All settings through .env variables
- **Validation System**: Configuration validation with clear error messages

## Development Patterns

### Async Processing Pattern
All components use asyncio for high-performance concurrent operations:
```python
async def research_technology(self, technology: str):
    # Concurrent web search and content analysis
    results = await self.web_searcher.comprehensive_search(query)
    analysis = self.content_analyzer.analyze_content(results)
```

### State Management Pattern
WorkflowState TypedDict defines the contract for data passing between workflow nodes:
```python
class WorkflowState(TypedDict):
    technology: str
    experience_level: str
    duration_hours: int
    preferences: Dict[str, Any]
    research_results: Optional[Dict[str, Any]]
    learning_plan: Optional[Dict[str, Any]]
    # ... other fields
```

### Error Handling Pattern
Comprehensive error handling with graceful fallbacks through dedicated error handling nodes in the workflow.

## Required Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional for enhanced functionality
SERPER_API_KEY=your_serper_api_key_here          # For Google web search
ANTHROPIC_API_KEY=your_anthropic_api_key_here    # Alternative LLM support
USE_DEEPSEEK=true                                # Enable DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key_here      # DeepSeek API key
```

## Key Dependencies

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

## Usage Examples

### Programming Interface
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

### Customization Options
```python
preferences = {
    "learning_style": "visual|hands-on|theoretical",
    "preferred_time": "morning|evening|flexible",
    "focus": ["specific_topics"],
    "tools": ["preferred_tools"],
    "project_type": "personal|professional|research",
    "background": "user_background"
}
```

## Common Development Tasks

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

## Debugging and Troubleshooting

### Common Issues
1. **API Key Configuration**: Use `settings.validate_config()` to verify setup
2. **Search Result Quality**: Check SERPER_API_KEY for Google search functionality
3. **LLM Performance**: Test both OpenAI and DeepSeek configurations using testdeepseek.py
4. **Async Issues**: Ensure all async functions are properly awaited

### Debug Mode
```bash
export DEBUG=True
python main.py "Python" --level beginner
```

### Test Components Individually
```bash
# Test research component
python ../testresearch.py

# Test LLM configuration
python ../testdeepseek.py
```