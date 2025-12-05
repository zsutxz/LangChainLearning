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

# Interactive mode - guided prompts for all inputs
python main.py --interactive

# Save results to file
python main.py "React" --level intermediate --output react_plan.json

# CLI help - see all available options
python main.py --help
```

### Testing and Development
```bash
# Run comprehensive usage examples
python examples/basic_usage.py

# Test search functionality (if available)
# python testresearch.py  # Note: This file may not exist in current directory

# Test specific LLM configurations
python testdeepseek.py

# Validate configuration
python -c "from config.settings import settings; print('Configuration valid:', settings.validate_config())"

# Test individual components in isolation
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
# Test research component (if available)
# python testresearch.py  # Note: This file may not exist in current directory

# Test LLM configuration
python testdeepseek.py
```

### Advanced Debugging Techniques

#### Workflow State Inspection
```python
# Debug workflow state transitions
python -c "
import asyncio
from src.tech_learning_workflow import TechLearningWorkflow

async def debug_workflow():
    workflow = TechLearningWorkflow()
    # Enable step-by-step execution
    result = await workflow.run('Python', 'beginner', 20)
    print('Full state:', result)

asyncio.run(debug_workflow())
"
```

#### Agent-Specific Testing
```python
# Test research agent in isolation
python -c "
import asyncio
from agents.research_agent import ResearchAgent

async def debug_research():
    agent = ResearchAgent()
    # Test with fast mode to avoid network issues
    result = await agent.research_technology('Python', fast_mode=True)
    print('Research result keys:', list(result.keys()))

asyncio.run(debug_research())
"
```

#### Configuration Validation
```bash
# Comprehensive configuration check
python -c "
from config.settings import settings
print('OpenAI Key:', bool(settings.OPENAI_API_KEY))
print('DeepSeek Key:', bool(settings.DEEPSEEK_API_KEY))
print('Use DeepSeek:', settings.USE_DEEPSEEK)
print('Serper Key:', bool(settings.SERPER_API_KEY))
print('Config Valid:', settings.validate_config())
"
```

### Performance Optimization
```bash
# Test with fast mode for development
python -c "
import asyncio
from main import TechLearningAssistant

async def fast_mode_test():
    assistant = TechLearningAssistant()
    # Mock data for faster development
    result = await assistant.create_learning_plan('Python', 'beginner', 20)
    print('Fast mode test completed')

asyncio.run(fast_mode_test())
"
```

## Development Best Practices

### Fast Mode Development
For rapid development and testing, use the built-in fast mode capabilities:
- **ResearchAgent.fast_mode=True**: Skips network searches, returns mock data
- **Workflow Testing**: Test workflow logic without external dependencies
- **Component Isolation**: Test individual agents without full workflow execution

### Environment Configuration
- **Development**: Set `DEBUG=True` for detailed logging
- **Testing**: Use `fast_mode=True` to avoid rate limits and network dependencies
- **Production**: Ensure all API keys are properly configured and validated

### Performance Considerations
- **Async Processing**: All I/O operations are async for performance
- **Concurrent Searches**: Multiple search sources run concurrently
- **Error Recovery**: Graceful degradation when external services fail

### Git Configuration
Note that test files are excluded from version control:
```bash
# Test files are ignored by .gitignore
test_*.py
*_test.py
debug_*.py
```

### Development Workflow
1. **Setup**: Validate configuration with `settings.validate_config()`
2. **Development**: Use fast mode and debug logging for rapid iteration
3. **Testing**: Test components individually before integration
4. **Validation**: Run full workflow with real APIs before deployment