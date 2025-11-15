# 🐆 Graph RAG Chat Application

A **Graph RAG (Retrieval-Augmented Generation)** chat application that combines **OpenAI GPT** with **knowledge graphs** stored in **GraphDB**. This application demonstrates how to build an intelligent assistant using **Microsoft Agent Framework** with structured data using SPARQL.

**Version 2.0** - Simplified PoC using Microsoft Agent Framework DevUI for rapid development and testing. Added intelligent knowledge extraction from text corpus using knowledge representation in ontology. 

## 🌟 Graph RAG Features

### 🤖 **Intelligent AI Agent**
- **Microsoft Agent Framework** for conversation management
- **OpenAI GPT-4** powered conversational interface
- **Function calling** for dynamic SPARQL query generation
- **Context-aware** responses based on graph data
- **Thread-based state management** for conversation persistence

### 🔗 **Graph RAG Architecture**
- **GraphDB integration** with RDF triple store
- **LLM-driven SPARQL generation** based on jaguar ontology
- **Hybrid intelligence** combining structured knowledge graphs with LLM reasoning
- **Real-time data retrieval** from knowledge graph
- **Natural language to SPARQL** query translation

### 📊 **Jaguar Conservation Database**
- **Jaguar ontology** with classes and properties
- Individual jaguar tracking (gender, identification marks, monitoring dates)
- Conservation efforts and organizations
- Threats, habitats, and locations
- Rescue, rehabilitation, and release data

### 🎨 **Developer-Friendly Interface**
- **Microsoft Agent Framework DevUI** for rapid development
- **Interactive chat interface** with real-time responses
- **Built-in debugging** and conversation inspection
- **Auto-opening browser** for immediate testing

## 🚀 Quick Start

### Prerequisites

Based on the [Microsoft Agent Framework requirements](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview):

- **Python 3.10+** (Required for Agent Framework)
- **Microsoft Agent Framework** (Preview version)
- **GraphDB** running on localhost:7200
- **OpenAI API** access with GPT-4 support
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/nemegrod/graph_RAG.git
cd graph_RAG
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_RESPONSES_MODEL_ID=gpt-4

# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
GRAPHDB_REPOSITORY=your_repo_name_here
```

### 5. Start GraphDB

```bash
# Using Docker (first time)
docker run -d --name graphdb-instance -p 7200:7200 local-graphdb:latest

# Stop container
docker stop graphdb-instance

# Start existing container
docker start graphdb-instance

```

### 6. Load Jaguar Data into GraphDB

You have two options for loading jaguar data into your GraphDB repository:

#### Option A: Import Pre-Generated Data Files (Quick Start)

1. Access GraphDB Workbench at `http://localhost:7200`
2. Create a new repository named `jaguars`
3. Import the data files:
   - `data/jaguar_ontology.ttl`
   - `data/jaguars.ttl`

This is the fastest way to get started with a pre-populated database of jaguar conservation data.

#### Option B: Mine Data from Text Using AI (Advanced)

Use the included Jupyter notebook to extract structured data from unstructured text using **ontology-aware AI extraction**:

1. Open the notebook:
   ```bash
   jupyter notebook text2knowledge.ipynb
   ```

2. Run the cells to:
   - Load the jaguar ontology (`data/jaguar_ontology.ttl`)
   - Load the text corpus (`data/jaguar_corpus.txt`)
   - Use **GPT-5** to intelligently extract entities and relationships

**What makes this special:**
- The corpus contains mixed content about different "Jaguar" entities (cars, guitars, wildlife)
- The AI uses the **ontology structure** to understand the concept and **only extracts wildlife-related jaguars**
- This demonstrates ontology-driven entity extraction, filtering out irrelevant information automatically
- Processing takes approximately 2-4 minutes

3. The notebook generates RDF Turtle code that aligns with your ontology

4. Import the generated Turtle into GraphDB:
   - In GraphDB Workbench, go to **Import** → **Text snippet**
   - Paste the generated RDF Turtle code
   - Import into your repository

This approach is ideal for:
- Mining your own jaguar-related documents
- Understanding how LLMs can use ontologies for intelligent extraction
- Customizing the knowledge graph with new data sources

### 7. Run the Application

```bash
# Start the Microsoft Agent Framework DevUI
python3 main.py
```

The DevUI will automatically open in your browser at `http://localhost:8000`

## 📁 Project Structure

```
graph_RAG/
├── main.py                  # DevUI entry point
├── text2knowledge.ipynb     # Jupyter notebook for mining data from text
├── src/
│   └── agents/
│       ├── jaguar_query_agent.py  # Agent creation with DevUI integration
│       └── jaguar_tool.py         # GraphDB tool implementation
├── data/
│   ├── jaguar_ontology.ttl       # Basic jaguar ontology
│   ├── jaguars.ttl               # Jaguar instance data
│   └── jaguar_corpus.txt         # Text corpus for mining (cars, guitars, wildlife)
├── docs/
│   ├── agent_design.md      # Agent design documentation
│   └── architecture.md      # Architecture documentation
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **Microsoft Agent Framework** (Preview) - AI agent orchestration
- **OpenAI GPT-4** - Language model for conversation and SPARQL generation
- **Requests** - HTTP library for GraphDB communication
- **python-dotenv** - Environment variable management

### Frontend
- **Microsoft Agent Framework DevUI** - Built-in development interface
- **Auto-opening browser** - Seamless development experience
- **Real-time chat** - Interactive conversation interface

### Data Layer
- **Ontotext GraphDB 10.7.0** - RDF triple store
- **SPARQL** - Query language for RDF data
- **RDF/Turtle** - Ontology and data definition format

### Architecture
- **Microsoft Agent Framework** - Unified agent development platform
- **Graph RAG Pattern** - Retrieval-Augmented Generation with knowledge graphs
- **Tool Integration** - SPARQL query execution via agent tools

## 🖥️ Microsoft Agent Framework DevUI

The **DevUI** (Development UI) is a built-in web interface provided by Microsoft Agent Framework for rapid development and testing of AI agents. It offers:

### Key Features
- **Interactive Chat Interface**: Real-time conversation with your AI agent
- **Auto-opening Browser**: Automatically launches at `http://localhost:8000`
- **Built-in Debugging**: Inspect agent responses, tool calls, and conversation flow
- **No Frontend Code Required**: Zero configuration web interface
- **Agent Inspection**: View agent configuration, tools, and capabilities
- **Conversation History**: Full chat history with context preservation

### DevUI Benefits
- **Rapid Prototyping**: Test agents without building custom UIs
- **Development Efficiency**: Focus on agent logic, not frontend development
- **Built-in Debugging**: Visual inspection of agent behavior
- **Production Ready**: Can be used for demos and testing

## 💡 How It Works

1. **DevUI Launch** - `python3 main.py` starts the DevUI server
2. **User Interaction** - User asks a question about jaguars in the DevUI
3. **Agent Processing** - Jaguar Query Agent analyzes the question
4. **Tool Selection** - Agent decides to use GraphDB tool for data retrieval
5. **SPARQL Generation** - GPT generates a SPARQL query based on the ontology
6. **Query Execution** - Query executes against GraphDB via the tool
7. **Data Processing** - Raw JSON results returned to agent
8. **Natural Language Response** - Agent interprets and formats the response
9. **DevUI Display** - Response shown in the interactive chat interface
10. **Context Preservation** - Conversation history maintained for follow-up questions


## 🧪 Testing

### Manual Testing with DevUI

The easiest way to test the Graph RAG functionality is through the DevUI:

```bash
# Start the DevUI
python3 main.py

# Test queries in the browser interface at http://localhost:8000
```

### Example Test Queries

Try these queries in the DevUI to test different aspects:

**Basic Counting:**
- "How many jaguars are in the database?"
- "Count all female jaguars"

**Data Filtering:**
- "Show me all male jaguars"
- "Find jaguars that were killed"

**Relationship Queries:**
- "Which jaguars were rescued and by which organization?"
- "Show me conservation efforts by location"

**Complex Queries:**
- "Find jaguars by location and their monitoring dates"
- "Which organizations are conducting conservation efforts?"

## 📚 Documentation

- **[Architecture](docs/architecture.md)** - System architecture and design
- **[Agent Design](docs/agent_design.md)** - Jaguar Agent design and usage


## 🔒 Security

- API keys stored in `.env` (excluded from version control)
- Environment variables for all sensitive configuration
- `.gitignore` configured to protect credentials
- No hardcoded secrets in source code
- Session-based access control


