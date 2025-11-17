# Semantic Graph RAG with Maplib

**Transform DataFrames into Knowledge Graphs in 3 lines of code**

This project demonstrates how to build a semantic Graph RAG system for structured data using Maplib, OTTR templates, and Microsoft Agent Framework—breaking away from the LangChain/vector embedding paradigm.

## The Problem

Vector embeddings lose structure. When you have tabular data with clear relationships, chunking and embedding destroys the very thing that makes your data valuable: its **structure and semantics**.

## The Solution

**Maplib + OTTR templates**: Transform DataFrames directly into RDF knowledge graphs while preserving relationships, semantics, and queryability.

```python
from maplib import Model

model = Model()
model.add_template(ottr_template)  # Define transformation logic
model.map("TemplateIRI", df)       # Transform DataFrame → Graph
model.query(sparql_query)          # Query with precision
```

## Architecture

### Core Components

1. **Maplib** - High-performance RDF construction from DataFrames
   - Rust-backed, Polars-native
   - Zero-copy operations via Apache Arrow
   - Built-in SPARQL querying

2. **OTTR Templates** - Type-safe transformations
   - Define CSV → RDF mapping once
   - Reusable across datasets
   - Enforces ontology compliance

3. **Formal Ontology (RDFS/OWL)** - Semantic precision
   - Class hierarchies
   - Property constraints
   - Reasoner-compatible

4. **Microsoft Agent Framework** - Conversational AI
   - Built-in DevUI
   - Function calling
   - Not LangChain

### Why Not Neo4j?

Property graphs lack formal semantics. RDF provides:
- W3C standards (SPARQL, RDFS, OWL)
- Inference and reasoning
- Schema flexibility without migrations
- Native interoperability

### Why Not Vector Embeddings?

For structured data:
- Embeddings lose exact relationships
- Similarity search is fuzzy when you need precision
- You're discarding the structure you already have

## Quick Start

### Prerequisites

```bash
pip install maplib polars python-dotenv
pip install microsoft-agent-framework  # or equivalent
```

### 1. Configure Environment

Create a `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_RESPONSES_MODEL_ID=gpt-4
```

### 2. Initialize the Knowledge Graph

```bash
# Transform CSV to graph using OTTR templates
python scripts/initialize_maplib.py

# Export to Turtle format (optional)
python scripts/initialize_maplib.py --export
```

### 3. Run the Agent

```bash
# Start the Microsoft Agent Framework DevUI
python main.py
```

The DevUI will automatically open at `http://localhost:8000`

## The Workflow

### 1. Define Your Ontology

```turtle
# data/jaguar_ontology.ttl
ont:Jaguar a owl:Class .
ont:hasGender a owl:DatatypeProperty ;
    rdfs:domain ont:Jaguar ;
    rdfs:range xsd:string .
```

### 2. Create OTTR Templates

```turtle
# data/jaguar_template.ottr
ont:JaguarInstance [
  ?jaguarId : xsd:string,
  ?name : xsd:string,
  ?gender : xsd:string
] :: {
  cross | ottr:Triple(:{ ?jaguarId }, rdf:type, ont:Jaguar) ,
  ottr:Triple(:{ ?jaguarId }, rdfs:label, ?name) ,
  ottr:Triple(:{ ?jaguarId }, ont:hasGender, ?gender)
} .
```

### 3. Prepare Your CSV

```csv
jaguar_id,name,gender,location
ElJefe,El Jefe,Male,Arizona
Sombra,Sombra,Male,Arizona
```

### 4. Transform to Graph

```python
import polars as pl
from maplib import Model

# Load CSV as DataFrame
df = pl.read_csv("data/jaguars.csv")

# Transform to RDF
model = Model()
model.add_template(ottr_template)
model.map("http://example.org/ontology#JaguarInstance", df)
```

### 5. Query with SPARQL

```python
# Find all male jaguars
query = """
PREFIX ont: <http://example.org/ontology#>
SELECT ?name WHERE {
    ?jaguar ont:hasGender "Male" .
    ?jaguar rdfs:label ?name .
}
"""
results = model.query(query)
```

## Project Structure

```
.
├── data/
│   ├── jaguar_ontology.ttl      # Formal ontology (classes, properties)
│   ├── jaguars.ttl              # Instance data (individuals)
│   ├── jaguar_template.ottr     # OTTR templates for CSV → RDF
│   └── jaguars.csv              # Source tabular data
├── src/
│   └── agents/
│       ├── jaguar_query_agent.py  # Agent with DevUI integration
│       └── jaguar_tool.py         # Agent tool using Maplib
├── scripts/
│   └── initialize_maplib.py     # Initialize graph from CSV
├── .claude/
│   └── agents/
│       └── data-manipulator.md  # Agent for RDF file manipulation
├── main.py                      # DevUI entry point
└── README.md                    # This file
```

## Use Case: Jaguar Conservation

This demo uses jaguar conservation data to show:

- **Structured data** (individual jaguars, locations, organizations)
- **Semantic relationships** (jaguars → habitats → locations)
- **Complex queries** (which jaguars were killed, where, by what)
- **Ontology-driven precision** (no fuzzy embeddings)

### Sample Queries

Try these in the DevUI:

**Basic Queries:**
- "How many jaguars are in the database?"
- "Show me all male jaguars"

**Relationship Queries:**
- "Which jaguars were killed and what was the cause?"
- "Find jaguars by location"

**Complex Queries:**
- "Which organizations are monitoring jaguars in Arizona?"
- "Show me rescued jaguars that were released"

## Why This Approach?

### For Data Scientists
- Stay in your DataFrame workflow (Polars)
- No need to learn graph databases
- Transform data you already have

### For Knowledge Engineers
- Formal semantics (RDFS/OWL)
- Reasoner compatibility
- Standards-compliant (W3C)

### For Application Developers
- Fast (Rust-backed)
- Portable (no external database)
- SPARQL precision for complex queries

## Comparison

| Approach | Best For | Limitations |
|----------|----------|-------------|
| **Vector RAG** | Unstructured text, semantic similarity | Loses structure, fuzzy results |
| **Neo4j/LPG** | Application-specific graphs | No formal semantics, vendor lock-in |
| **Maplib + RDF** | Structured data with relationships | Requires ontology design |

## Key Differences from Standard RAG

### Standard RAG (LangChain + Vectors)
```python
# Chunk and embed
chunks = text_splitter.split(csv_content)
embeddings = OpenAIEmbeddings().embed(chunks)
vectorstore.add(embeddings)

# Query (fuzzy similarity)
results = vectorstore.similarity_search(query)
```

### This Approach (Maplib + OTTR)
```python
# Preserve structure
model.add_template(ottr_template)
model.map("TemplateIRI", dataframe)

# Query (precise SPARQL)
results = model.query(sparql_query)
```

**The difference**: Structure preservation vs. dimensionality reduction.

## Performance

Maplib is built on:
- **Rust** for high performance
- **Polars** for DataFrame operations
- **Apache Arrow** for zero-copy data transfer
- **In-memory** processing (no network overhead)

Typical query times: **< 10ms** for datasets with thousands of triples.

## References

- [Maplib](https://github.com/DataTreehouse/maplib) - High-performance RDF construction
- [OTTR](http://ottr.xyz/) - Ontology Transformation Template Registry
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/) - Conversational AI
- [RDF](https://www.w3.org/RDF/) - Resource Description Framework
- [SPARQL](https://www.w3.org/TR/sparql11-query/) - Query language for RDF
- [Polars](https://pola.rs/) - Fast DataFrame library

## License

MIT

---

**Built with tools you haven't heard of. Breaks every RAG "best practice". Works better for structured data.**
