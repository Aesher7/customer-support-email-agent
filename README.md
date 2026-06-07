# Customer Support Email Agent

A LangGraph-based customer support email agent built with FastAPI, LangChain, and OpenAI.

## Overview

This project implements an intelligent customer support system that processes incoming emails through a multi-step workflow:

1. **Email Intake** - Receives customer emails
2. **Intent Classification** - Categorizes email type (complaint, inquiry, request, etc.)
3. **Knowledge Base Search** - Finds relevant documentation
4. **Response Generation** - Drafts AI-powered response using context
5. **Human Review Gate** - Routes complex cases for human review
6. **Email Sending** - Sends final response to customer
7. **Follow-up Scheduling** - Schedules follow-ups for complaints

## Features

- ✅ Email processing via REST API
- ✅ Intent classification using LLM
- ✅ **FAISS semantic search** for knowledge base retrieval
- ✅ AI-powered response generation with context
- ✅ Human review routing for complex cases
- ✅ Follow-up scheduling for escalations
- ✅ LangGraph-based workflow orchestration
- ✅ SQLAlchemy database integration
- ✅ Full type safety with Pydantic
- ✅ Comprehensive service layer architecture
- ✅ Granular node-based workflow design

## Tech Stack

- **Python 3.12**
- **FastAPI** - Web framework
- **LangGraph** - Graph-based workflow orchestration
- **LangChain** - LLM framework
- **OpenAI** - LLM provider
- **Pydantic** - Data validation

## Project Structure

```
.
├── src/
│   ├── api/           # FastAPI routes and endpoints
│   ├── core/          # Core configuration and settings
│   ├── graph/         # LangGraph definitions
│   ├── nodes/         # Individual node implementations
│   ├── services/      # Business logic services
│   ├── schemas/       # Pydantic models
│   ├── prompts/       # LLM prompts
│   └── utils/         # Utility functions
├── data/              # Data files and knowledge base
├── tests/             # Test suite
├── .env               # Environment variables (not in git)
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

## Setup

### Prerequisites

- Python 3.12
- pip or uv package manager
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd customer-support-email-agent
```

2. Create a virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key and other credentials
```

## Running the Application

### Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

## Development

### Adding a New Node

1. Create a new file in `src/nodes/`
2. Implement the node function
3. Register in the graph definition

### Adding Prompts

Store prompt templates in `src/prompts/` organized by functionality.

## Testing

```bash
pytest tests/
```

## Contributing

(Guidelines to be added)

## License

(License to be added)
