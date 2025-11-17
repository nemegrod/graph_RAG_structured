import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from agent_framework.openai import OpenAIResponsesClient, OpenAISettings
from agent_framework import ChatAgent
from agent_framework.devui import serve
from src.agents.jaguar_query_agent import create_jaguar_query_agent

try:
    from maplib import Model
    import polars as pl
except ImportError:
    raise ImportError("maplib and polars are required. Install with: pip install maplib polars")

# Load environment variables
load_dotenv()


def initialize_jaguar_model():
    """
    Initialize Maplib model with CSV workflow (production pipeline).
    
    This follows the "load pre-written template" approach from csv2graph_maplib.ipynb:
    1. Load ontology
    2. Load OTTR template from file
    3. Load CSV data
    4. Map CSV to RDF using template
    5. Optionally load additional manually-curated data
    
    Returns:
        Model: Initialized Maplib model with knowledge graph
    """
    print("🚀 Initializing Jaguar Knowledge Graph...")
    
    # Get paths
    project_root = Path(__file__).parent
    data_dir = project_root / "data"
    
    # Initialize Maplib model
    model = Model()
    
    # Step 1: Load ontology (schema/classes/properties)
    ontology_path = data_dir / "jaguar_ontology.ttl"
    if ontology_path.exists():
        model.read(str(ontology_path), format="turtle")
        print(f"   ✅ Loaded ontology from {ontology_path.name}")
    else:
        print(f"   ⚠️  Ontology not found: {ontology_path}")
    
    # Step 2: Load OTTR template from file (production approach)
    template_path = data_dir / "jaguar_template.ottr"
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            ottr_template = f.read()
        model.add_template(ottr_template)
        print(f"   ✅ Loaded OTTR template from {template_path.name}")
    else:
        print(f"   ⚠️  Template not found: {template_path}")
    
    # Step 3: Load CSV data and prepare for mapping
    csv_path = data_dir / "jaguars.csv"
    if csv_path.exists():
        df = pl.read_csv(str(csv_path))
        
        # Create IRI columns
        RES_PREFIX = "http://example.org/resource#"
        df = df.with_columns(
            (pl.lit(RES_PREFIX) + pl.col("jaguar_id")).alias("id"),
            (pl.lit(RES_PREFIX) + pl.col("location")).alias("location_iri"),
            (pl.lit(RES_PREFIX) + pl.col("monitoring_org")).alias("monitoring_org_iri")
        )
        
        # Select columns matching template parameter order
        df_mapped = df.select([
            "id", "name", "gender", "location_iri", "monitoring_org_iri",
            "first_sighted", "is_killed", "cause_of_death", "identification_mark"
        ])
        
        # Step 4: Map CSV to RDF using template
        template_iri = "http://example.org/ontology#JaguarInstance"
        model.map(template_iri, df_mapped)
        print(f"   ✅ Mapped {len(df_mapped)} jaguars from CSV")
    else:
        print(f"   ⚠️  CSV not found: {csv_path}")
    
    # Step 5: Load additional manually-curated instance data (optional)
    #instances_path = data_dir / "jaguars.ttl"
    #if instances_path.exists():
    #    model.read(str(instances_path), format="turtle")
    #    print(f"   ✅ Loaded additional instances from {instances_path.name}")
    
    # Debug: Count total jaguars in knowledge graph
    query = """
    PREFIX ont: <http://example.org/ontology#>
    SELECT (COUNT(?jaguar) as ?count) WHERE {
        ?jaguar a ont:Jaguar .
    }
    """
    result = model.query(query)
    count = result[0, 0] if result is not None and len(result) > 0 else 0
    print(f"\n📊 Total jaguars in knowledge graph: {count}")
    
    print("🎉 Knowledge graph ready for querying!\n")
    return model


def main():
    """Start the dev UI with jaguar query agent"""
    # Initialize the knowledge graph model (production pipeline)
    jaguar_model = initialize_jaguar_model()
    
    # Create query agent with the initialized model
    query_agent = create_jaguar_query_agent(jaguar_model)
    
    # Create DevUI instance
    serve(entities=[query_agent], auto_open=True)

if __name__ == "__main__":
    main()