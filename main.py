from dotenv import load_dotenv
from agent_framework.devui import serve
from src.agents.jaguar_query_agent import create_jaguar_query_agent
from maplib import Model
import polars as pl

# Load environment variables
load_dotenv()


def initialize_jaguar_df():
    
    # Load CSV as Polars DataFrame
    df = pl.read_csv("data/jaguars.csv")

    print(f"📊 Loaded {len(df)} jaguar records")
    print(f"\nColumns: {', '.join(df.columns)}")

    # === HANDLING LIST COLUMNS ===
    # We split and explode all list columns to create a flat table.
    # This generates a Cartesian product of rows, but RDF deduplication handles the redundancy.

    # Define list columns to process
    list_columns = ["location", "monitoring_org", "threats", "monitoring_technique"]
    # Start with the base DataFrame
    df_exploded = df

    # Split and explode all list columns
    for col_name in list_columns:
        df_exploded = df_exploded.with_columns(
            pl.col(col_name).str.split(";")
        ).explode(col_name)

    # === HANDLING IRI COLUMNS ===
    # Create IRI columns from string values. Read more about this in csv2graph.ipynb: 
    RES_PREFIX = "http://example.org/resource#"
    df_exploded = df_exploded.with_columns([
        (pl.lit(RES_PREFIX) + pl.col("jaguar_id")).alias("id"),
        (pl.lit(RES_PREFIX) + pl.col("location").str.strip_chars()).alias("location_iri"),
        (pl.lit(RES_PREFIX) + pl.col("monitoring_org").str.strip_chars()).alias("monitoring_org_iri"),
        (pl.lit(RES_PREFIX) + pl.col("threats").str.strip_chars()).alias("threat_iri"),
        (pl.lit(RES_PREFIX) + pl.col("monitoring_technique").str.strip_chars()).alias("technique_iri")
    ])

    # Select columns for the template
    # We include BOTH the IRI and the original string for each resource type
    df_final = df_exploded.select([
        "id",
        "name", 
        "gender",
        "location",              # String label
        "location_iri",          # IRI
        "monitoring_org",        # String label
        "monitoring_org_iri",    # IRI
        "first_sighted",
        "is_killed",
        "cause_of_death",
        "identification_mark",
        "threats",               # String label
        "threat_iri",            # IRI
        "monitoring_technique",  # String label
        "technique_iri",         # IRI
        "status_notes"
    ])
    
    print("🎉 Jaguar data frame ready for mapping!\n")
    return df_final


def main():
    """
    Initialize Maplib model with CSV workflow (production approach).
    
    This follows the "load pre-written template" approach from csv2graph.ipynb:
   
    1. Load OTTR template from file
    2. Load CSV data
    3. Map CSV to RDF using template
    4. Load ontology
    
    Optionally load additional manually-curated data
    
    Start the dev UI with jaguar query agent"""
      
    
    
    #Load OTTR template from file (production approach)
    with open("data/jaguar_template.ottr", 'r', encoding='utf-8') as f:
        jaguar_ottr_template = f.read()
    print("🦦 Jaguar OTTR template loaded...")
    
    #Load OTTR template from file (production approach)
    jaguar_df = initialize_jaguar_df()
        
    print("🕸 Initializing Jaguar Knowledge Graph...")
    
    # Initialize the knowledge graph model (production pipeline)  
    model = Model()
    model.add_template(jaguar_ottr_template)
    model.map("http://example.org/ontology#JaguarInstance", jaguar_df)
    model.read("data/jaguar_ontology.ttl", format="turtle")
    
    print("🚀 Success! The data frame is now a Knowledge Graph...")

    #Load additional manually-curated instance data (optional)
    #model.read("data/jaguars.ttl", format="turtle")
    
    #Quick Debug: Count total jaguars in knowledge graph (optional)
    #query = """
    #PREFIX ont: <http://example.org/ontology#>
    #SELECT (COUNT(?jaguar) as ?count) WHERE {
    #    ?jaguar a ont:Jaguar .
    #}
    #result = model.query(query)
    #print(f"\n📊 Total jaguars in jaguar_model: {count}")

    # Create query agent with the initialized model
    query_agent = create_jaguar_query_agent(model)
    
    # Create DevUI instance Running on localhost:8080
    serve(entities=[query_agent], auto_open=True)

if __name__ == "__main__":
    main()