from dotenv import load_dotenv
from agent_framework.devui import serve
from src.agents.jaguar_query_agent import create_jaguar_query_agent
from maplib import Model
import polars as pl

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
    
    # Initialize Maplib model
    model = Model()
    
    # Step 1: Load ontology (schema/classes/properties)
    model.read("data/jaguar_ontology.ttl", format="turtle")
    print(f"   ✅ Loaded ontology from jaguar_ontology.ttl")
    
    # Step 2: Load OTTR template from file (production approach)
    with open("data/jaguar_template.ottr", 'r', encoding='utf-8') as f:
        ottr_template = f.read()
    model.add_template(ottr_template)
    print(f"   ✅ Loaded OTTR template from jaguar_template.ottr")
    
    # Step 3: Load CSV data and prepare for mapping
    df = pl.read_csv("data/jaguars.csv")
    
    # Create IRI columns
    RES_PREFIX = "http://example.org/resource#"
    df = df.with_columns(
        (pl.lit(RES_PREFIX) + pl.col("jaguar_id")).alias("id"),
        (pl.lit(RES_PREFIX) + pl.col("location")).alias("location_iri"),
        (pl.lit(RES_PREFIX) + pl.col("monitoring_org")).alias("monitoring_org_iri")
    )
    
    # Select columns matching template parameter order
    df_iri = df.select([
        "id", "name", "gender", "location_iri", "monitoring_org_iri",
        "first_sighted", "is_killed", "cause_of_death", "identification_mark"
    ])
    
    # Step 4: Map CSV to RDF using templateinstance
    model.map("http://example.org/ontology#JaguarInstance", df_iri)
    print(f"   ✅ Mapped {len(df_iri)} jaguars from CSV")
    
    # Step 5: Load additional manually-curated instance data (optional)
    #model.read("data/jaguars.ttl", format="turtle")
    #print(f"   ✅ Loaded additional instances from jaguars.ttl")
    
    #Quick Debug: Count total jaguars in knowledge graph (optional)
    #query = """
    #PREFIX ont: <http://example.org/ontology#>
    #SELECT (COUNT(?jaguar) as ?count) WHERE {
    #    ?jaguar a ont:Jaguar .
    #}
    #result = model.query(query)
    #print(f"\n📊 Total jaguars in jaguar_model: {count}")
    
    print("🎉 Jaguar model ready for querying!\n")
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