# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

This is the **Tech Learning Assistant** - a LangGraph-based intelligent workflow system that generates personalized learning plans for various technologies. The system uses AI agents to research technologies and create comprehensive learning roadmaps tailored to user experience levels and preferences.

## 🚀 Common Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys (OPENAI_API_KEY required)
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

# Command line help
python main.py --help
```

### Testing Commands
```bash
# Validate configuration
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"

# Test workflow components
python -c "
import asyncio
from src.workflow import TechLearningWorkflow
async def test_workflow():
    workflow = TechLearningWorkflow()
    result = await workflow.run('Python', 'beginner', 20)
    print('Test result:', result['status'])
asyncio.run(test_workflow())
"

# Test individual agents (using fast_mode to avoid API calls)
python -c "
import asyncio
from agents.research_agent import ResearchAgent
async def test_research():
    agent = ResearchAgent()
    result = await agent.research_technology('Python', fast_mode=True)
    print('Research test:', result['status'])
asyncio.run(test_research())
"

# Run comprehensive examples
python examples/basic_usage.py

# Test DeepSeek API configuration
python testdeepseek.py
```

### Debug Mode
```bash
# Enable comprehensive logging
export DEBUG=True
python main.py "Python" --level beginner
```

## 🏗️ Core Architecture

### Main Components Structure
```
Sample/                       # Main LangGraph project directory
├── main.py                    # Entry point - CLI interface and interactive mode
├── src/
│   ├── assistant.py          # TechLearningAssistant class - main interface
│   └── workflow.py           # TechLearningWorkflow - LangGraph state machine
├── config/settings.py         # Configuration management - API keys, model settings
├── agents/                    # AI agent modules
│   ├── research_agent.py      # Research agent - technology data collection
│   └── learning_agent.py      # Learning agent - plan generation
├── tools/                     # Utility tools
│   ├── web_searcher.py        # Web search functionality
│   └── content_analyzer.py    # Content analysis tools
├── examples/basic_usage.py    # Usage examples
├── requirements.txt           # Python dependencies
└── .env.example               # Environment variables template
```

### LangGraph State Machine Pattern
The workflow uses a sequential state machine with these nodes:

1. **validate_input** - Parameter validation and normalization
2. **research_technology** - Multi-source data collection and analysis
3. **generate_learning_plan** - Base learning plan creation using LLM
4. **customize_plan** - Personalization based on user preferences (conditional)
5. **generate_final_output** - Result integration and formatting
6. **handle_error** - Comprehensive error handling and recovery

### Key Classes and Usage
```python
# Main entry point
from src.assistant import TechLearningAssistant
assistant = TechLearningAssistant()
result = await assistant.create_learning_plan("Python", "beginner", 30)

# Workflow engine
from src.workflow import TechLearningWorkflow
workflow = TechLearningWorkflow()
result = await workflow.run("React", "intermediate", 40)

# Research agent (with fast_mode for development)
from agents.research_agent import ResearchAgent
agent = ResearchAgent()
result = await agent.research_technology("Docker", fast_mode=True)
```

### WorkflowState Data Contract
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

## ⚙️ Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=sk-...                    # Required: OpenAI API key
```

### Optional Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...             # Optional: Anthropic Claude API key
USE_DEEPSEEK=true                        # Optional: Enable DeepSeek API
DEEPSEEK_API_KEY=sk-...                  # Required if USE_DEEPSEEK=true
SERPER_API_KEY=your_serper_key           # Optional: Google search via Serper
DEBUG=False                              # Enable debug logging
MAX_RETRIES=3                            # API request retry attempts
TIMEOUT=30                               # Request timeout in seconds
```

### Configuration Validation
```bash
# Always validate configuration before running
python -c "from config.settings import settings; exit(0 if settings.validate_config() else 1)"
```

## 🛠️ Development Patterns

### Fast Mode Development
Use `fast_mode=True` parameter to skip network calls during development:
```python
# For research agent
result = await agent.research_technology("Python", fast_mode=True)

# This provides mock data for faster development without API calls
```

### Error Handling Pattern
The workflow includes comprehensive error handling with graceful degradation:
- Network timeouts and API failures
- Invalid input parameters
- LLM generation failures
- Missing configuration

### Adding New Workflow Nodes
```python
def _create_workflow(self) -> StateGraph:
    workflow = StateGraph(WorkflowState)

    # Add new node
    workflow.add_node("new_step", self._new_processing_step)

    # Update workflow edges
    workflow.add_edge("research_technology", "new_step")
    workflow.add_edge("new_step", "generate_learning_plan")

    return workflow.compile()
```

## 🚨 Troubleshooting

### Common Issues
1. **Configuration validation fails**: Check that at least one LLM API key is set
2. **No search results**: Verify SERPER_API_KEY or use fast_mode for testing
3. **LLM API errors**: Check API keys, rate limits, or try alternative LLM
4. **Workflow failures**: Enable DEBUG=True for detailed logging

### Debug Commands
```bash
# Check API key configuration
python -c "from config.settings import settings; print('OpenAI:', bool(settings.OPENAI_API_KEY)); print('DeepSeek:', bool(settings.DEEPSEEK_API_KEY))"

# Test individual components
python testdeepseek.py
export DEBUG=True && python main.py "Python" --level beginner
```

## 📍 Important Notes

- **Working Directory**: Always run commands from the `Sample/` directory
- **Test Scripts**: `testresearch.py` and `testdeepseek.py` are available for component testing
- **Fast Mode**: Use `fast_mode=True` parameter during development to avoid API dependencies
- **Configuration**: Validate configuration with `settings.validate_config()` before running workflows