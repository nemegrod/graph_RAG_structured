"""
Jaguar Knowledge Graph Query Tool

This module provides a SPARQL query interface for the jaguar conservation
knowledge graph using Maplib (in-memory RDF store).

The knowledge graph is built in main.py using the production pipeline:
1. Load ontology (data/jaguar_ontology.ttl)
2. Load OTTR template (data/jaguar_template.ottr)
3. Transform CSV to RDF (data/jaguars.csv)
4. Optionally load additional manually-curated data (data/jaguars.ttl)

This tool receives the initialized model and provides SPARQL querying.
For graph construction workflow, see csv2graph_maplib.ipynb and main.py.
"""

import os
import json
from dotenv import load_dotenv

try:
    from maplib import Model
except ImportError:
    raise ImportError("maplib is required. Install with: pip install maplib")

# Load environment variables
load_dotenv()


def create_query_jaguar_model_tool(model: Model):
    """
    Create a query tool function bound to a specific Maplib model. In this case with hardcoded description
    This is necessary to be able to pass the model to the tool without breaking the tool calling pattern for the agent. 
    
    Args:
        model: Initialized Maplib Model with knowledge graph
    
    Returns:
        Function that queries the jaguar knowledge graph
    """
    
    def query_model_tool(sparql_query: str) -> str:
        """
        Query the jaguar knowledge graph using SPARQL via Maplib. Use this tool when users ask questions about jaguars, jaguar populations, conservation efforts, habitats, threats, or any jaguar-related data. You must generate a valid SPARQL query based on the jaguar ontology. The tool will return raw JSON results that you must interpret and convert into natural language responses for the user.
        
        Args:
            sparql_query: A valid SPARQL query to execute against the jaguar GraphDB aligning with this ontology:
        
        @prefix ont: <http://example.org/ontology#>.
        @prefix : <http://example.org/resource#>.
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
        @prefix owl: <http://www.w3.org/2002/07/owl#>.

        #############################
        # Ontology Classes          #
        #############################

        ont:Animal a owl:Class.
        ont:Mammal a owl:Class ; rdfs:subClassOf ont:Animal.
        ont:BigCat a owl:Class ; rdfs:subClassOf ont:Mammal.
        ont:Jaguar a owl:Class ; rdfs:subClassOf ont:BigCat ;
            rdfs:comment "The Panthera onca species.".

        ont:Prey a owl:Class ; rdfs:subClassOf ont:Animal.
        ont:Livestock a owl:Class ; rdfs:subClassOf ont:Prey.
        ont:Herbivore a owl:Class ; rdfs:subClassOf ont:Prey.
        ont:Mesopredator a owl:Class ; rdfs:subClassOf ont:Prey.
        ont:Fish a owl:Class ; rdfs:subClassOf ont:Prey.
        ont:Reptile a owl:Class ; rdfs:subClassOf ont:Prey.

        ont:JaguarPopulation a owl:Class ;
            rdfs:comment "A group or population of jaguars.".

        ont:Habitat a owl:Class.
        ont:Forest a owl:Class ; rdfs:subClassOf ont:Habitat.
        ont:Rainforest a owl:Class ; rdfs:subClassOf ont:Forest.
        ont:Wetland a owl:Class ; rdfs:subClassOf ont:Habitat.
        ont:Grassland a owl:Class ; rdfs:subClassOf ont:Habitat.
        ont:Shrubland a owl:Class ; rdfs:subClassOf ont:Habitat.
        ont:WaterBody a owl:Class ; rdfs:subClassOf ont:Habitat.

        ont:Location a owl:Class.
        ont:Country a owl:Class ; rdfs:subClassOf ont:Location.
        ont:State a owl:Class ; rdfs:subClassOf ont:Location.
        ont:Region a owl:Class ; rdfs:subClassOf ont:Location.
        ont:MountainRange a owl:Class ; rdfs:subClassOf ont:Location.
        ont:HabitatArea a owl:Class ; rdfs:subClassOf ont:Location.

        ont:DietType a owl:Class.
        ont:CarnivoreDiet a ont:DietType.

        ont:Observation a owl:Class ;
            rdfs:label "Observation" ;
            rdfs:comment "An event recording the sighting of an animal.".

        ont:Person a owl:Class ;
            rdfs:label "Person" ;
            rdfs:comment "A human observer or researcher involved in recording animal sightings.".
        ont:Researcher a owl:Class ; rdfs:subClassOf ont:Person.
        ont:Rancher a owl:Class ; rdfs:subClassOf ont:Person.
        ont:Conservationist a owl:Class ; rdfs:subClassOf ont:Person.
        ont:IndigenousPerson a owl:Class ; rdfs:subClassOf ont:Person.
        ont:Tourist a owl:Class ; rdfs:subClassOf ont:Person.
        ont:LawEnforcement a owl:Class ; rdfs:subClassOf ont:Person.

        ont:ConservationOrganization a owl:Class ;
            rdfs:label "Conservation Organization" ;
            rdfs:comment "An organization involved in monitoring and protecting wildlife.".
        ont:GovernmentAgency a owl:Class ; rdfs:subClassOf ont:ConservationOrganization.
        ont:NGO a owl:Class ; rdfs:subClassOf ont:ConservationOrganization.
        ont:AcademicInstitution a owl:Class ; rdfs:subClassOf ont:ConservationOrganization.

        ont:Threat a owl:Class.
        ont:AnthropogenicThreat a owl:Class ; rdfs:subClassOf ont:Threat.
        ont:HabitatLoss a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:HabitatFragmentation a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:Poaching a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:IllegalWildlifeTrade a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:HumanWildlifeConflict a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:BorderBarrier a owl:Class ; rdfs:subClassOf ont:AnthropogenicThreat.
        ont:EnvironmentalThreat a owl:Class ; rdfs:subClassOf ont:Threat.
        ont:ClimateChange a owl:Class ; rdfs:subClassOf ont:EnvironmentalThreat.
        ont:Wildfire a owl:Class ; rdfs:subClassOf ont:EnvironmentalThreat.

        ont:ConservationEffort a owl:Class.
        ont:RecoveryPlan a owl:Class ; rdfs:subClassOf ont:ConservationEffort.
        ont:WildlifeCorridor a owl:Class ; rdfs:subClassOf ont:ConservationEffort.
        ont:RewildingProgram a owl:Class ; rdfs:subClassOf ont:ConservationEffort.
        ont:CommunityEngagement a owl:Class ; rdfs:subClassOf ont:ConservationEffort.
        ont:InternationalCooperation a owl:Class ; rdfs:subClassOf ont:ConservationEffort.
        ont:MonitoringTechnique a owl:Class.
        ont:CameraTrap a owl:Class ; rdfs:subClassOf ont:MonitoringTechnique.
        ont:ScatDetection a owl:Class ; rdfs:subClassOf ont:MonitoringTechnique.
        ont:GPSTracking a owl:Class ; rdfs:subClassOf ont:MonitoringTechnique.

        ont:LegalFramework a owl:Class.
        ont:Act a owl:Class ; rdfs:subClassOf ont:LegalFramework.
        ont:Convention a owl:Class ; rdfs:subClassOf ont:LegalFramework.

        ont:CulturalSignificance a owl:Class.
        ont:EconomicBenefit a owl:Class.

        ont:Event a owl:Class. # For specific events like rescue, release, death

        #############################
        # Ontology Properties #
        #############################

        ont:hasObservation a owl:ObjectProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range ont:Observation ;
            rdfs:comment "Links an animal to one of its observation events.".

        ont:observedDate a owl:DatatypeProperty ;
            rdfs:domain ont:Observation ;
            rdfs:range xsd:date ;
            rdfs:comment "The date on which the observation took place.".

        ont:observedBy a owl:ObjectProperty ;
            rdfs:domain ont:Observation ;
            rdfs:range ont:Person ;
            rdfs:comment "The person who recorded the observation.".

        ont:monitoredByOrg a owl:ObjectProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range ont:ConservationOrganization ;
            rdfs:comment "Links an animal to the conservation organization that monitors it.".

        ont:monitoredByTechnique a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:MonitoringTechnique ;
            rdfs:comment "Indicates the technique used to monitor the jaguar.".

        ont:locatedInCountry a owl:ObjectProperty ;
            rdfs:domain ont:State ;
            rdfs:range ont:Country ;
            rdfs:comment "Specifies the country in which a state is located.".

        ont:locatedIn a owl:ObjectProperty ;
            rdfs:domain ont:Habitat ;
            rdfs:range ont:Location ;
            rdfs:comment "Specifies the state or administrative region in which a habitat is located.".

        ont:occursIn a owl:ObjectProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range ont:Location ;
            rdfs:comment "Indicates a state where an animal has been observed or is known to occur.".

        ont:name a owl:DatatypeProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range xsd:string.

        ont:habitat a owl:ObjectProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range ont:Habitat.

        ont:hasDietType a owl:ObjectProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range ont:DietType.

        ont:hasLifespan a owl:DatatypeProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range xsd:integer ;
            rdfs:comment "Lifespan in years.".

        ont:scientificName a owl:DatatypeProperty ;
            rdfs:domain ont:Animal ;
            rdfs:range xsd:string.

        ont:hasGender a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "Gender of the jaguar (e.g., Male, Female).".

        ont:hasIdentificationMark a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "Unique spot pattern or other distinguishing mark.".

        ont:hasMonitoringStartDate a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date when monitoring of the individual jaguar began.".

        ont:hasLastSightingDate a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the last confirmed sighting of the individual jaguar.".

        ont:wasKilled a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was killed.".

        ont:causeOfDeath a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "The cause of death for the jaguar.".

        ont:originatesFrom a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:Location ;
            rdfs:comment "Indicates the origin location of a dispersing jaguar.".

        ont:hasOffspring a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:Jaguar ;
            rdfs:comment "Links a jaguar to its offspring.".

        ont:isOrphaned a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was orphaned.".

        ont:isRehabilitated a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar underwent rehabilitation.".

        ont:isReleased a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was released into the wild.".

        ont:rescuedBy a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:ConservationOrganization ;
            rdfs:comment "The organization that rescued the jaguar.".

        ont:reintroducedBy a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:ConservationOrganization ;
            rdfs:comment "The organization that reintroduced the jaguar.".

        ont:hasRescueDate a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the jaguar's rescue.".

        ont:hasReleaseDate a owl:DatatypeProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the jaguar's release.".

        ont:facesThreat a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:Threat ;
            rdfs:comment "Indicates a threat faced by the jaguar.".

        ont:implementsEffort a owl:ObjectProperty ;
            rdfs:domain ont:ConservationOrganization ;
            rdfs:range ont:ConservationEffort ;
            rdfs:comment "Indicates a conservation effort implemented by an organization.".

        ont:connectsHabitat a owl:ObjectProperty ;
            rdfs:domain ont:WildlifeCorridor ;
            rdfs:range ont:HabitatArea ;
            rdfs:comment "Indicates which habitat areas a wildlife corridor connects.".

        ont:hasAcreage a owl:DatatypeProperty ;
            rdfs:domain ont:HabitatArea ;
            rdfs:range xsd:integer ;
            rdfs:comment "The size of the habitat area in acres.".

        ont:hasPopulationEstimate a owl:DatatypeProperty ;
            rdfs:domain ont:JaguarPopulation ;
            rdfs:range xsd:integer ;
            rdfs:comment "Estimated number of jaguars in a population.".

        ont:isDependentOn a owl:ObjectProperty ;
            rdfs:domain ont:JaguarPopulation ;
            rdfs:range ont:JaguarPopulation ;
            rdfs:comment "Indicates if one jaguar population is dependent on another (e.g., for dispersal).".

        ont:namedBy a owl:ObjectProperty ;
            rdfs:domain ont:Jaguar ;
            rdfs:range ont:Person ;
            rdfs:comment "The person or group who named the jaguar.".
                
                
        SPARQL Query Examples:
        - Find by [Name]:
            @prefix ont: <http://example.org/ontology#>.
            @prefix : <http://example.org/resource#>.
            SELECT ?jaguar ?label WHERE {
            BIND(:[Name] AS ?jaguar)
            OPTIONAL { ?jaguar rdfs:label ?label . }
            }

        - Find all properties about [Name]:            
            @prefix ont: <http://example.org/ontology#>.
            @prefix : <http://example.org/resource#>.
            SELECT ?jaguar ?p ?o WHERE {
            BIND(:[Name] AS ?jaguar)
            OPTIONAL { ?jaguar ?p ?o . }
            }
            
        - Find by gender:       
        @prefix ont: <http://example.org/ontology#>.
        @prefix : <http://example.org/resource#>.
        SELECT ?jaguar ?label ?gender WHERE 
        { ?jaguar a ont:Jaguar . 
        OPTIONAL { ?jaguar rdfs:label ?label . } 
        OPTIONAL { ?jaguar ont:hasGender ?gender . } }
        
        - Find killed jaguars:                 
        @prefix ont: <http://example.org/ontology#>.
        @prefix : <http://example.org/resource#>.
        SELECT ?jaguar ?label ?causeOfDeath WHERE { 
        ?jaguar a ont:Jaguar . 
        ?jaguar ont:wasKilled true . 
        OPTIONAL { ?jaguar rdfs:label ?label . } 
        OPTIONAL { ?jaguar ont:causeOfDeath ?causeOfDeath . } }
        
        - Count jaguars: 
        
        @prefix ont: <http://example.org/ontology#>.
        @prefix : <http://example.org/resource#>.
        SELECT (COUNT(?jaguar) as ?count) WHERE { ?jaguar a ont:Jaguar . }
        
        
        - Always try to make a simple query first and only add complexity if needed.
        - Always include relevant prefixes in the query.
    
    Returns:
        JSON string containing query results from Maplib in-memory knowledge graph (SPARQL JSON format)
        """
        try:
            # Model is provided from the closure (initialized in main.py)
            # Execute SPARQL query using Maplib
            result_df = model.query(sparql_query.strip())

            # Convert Polars DataFrame to SPARQL JSON format
            # This maintains compatibility with existing agent code
            if result_df is None or len(result_df) == 0:
                return json.dumps({
                    "head": {"vars": []},
                    "results": {"bindings": []}
                }, indent=2)

            # Get column names (SPARQL variables)
            vars_list = result_df.columns

            # Convert rows to SPARQL JSON bindings format
            bindings = []
            for row in result_df.iter_rows(named=True):
                binding = {}
                for var, value in row.items():
                    if value is not None:
                        # Determine type (simplified - Maplib handles RDF types)
                        if isinstance(value, str):
                            if value.startswith("http://") or value.startswith("https://"):
                                binding[var] = {"type": "uri", "value": value}
                            else:
                                binding[var] = {"type": "literal", "value": value}
                        elif isinstance(value, bool):
                            binding[var] = {
                                "type": "literal",
                                "value": str(value).lower(),
                                "datatype": "http://www.w3.org/2001/XMLSchema#boolean"
                            }
                        elif isinstance(value, int):
                            binding[var] = {
                                "type": "literal",
                                "value": str(value),
                                "datatype": "http://www.w3.org/2001/XMLSchema#integer"
                            }
                        else:
                            binding[var] = {"type": "literal", "value": str(value)}
                bindings.append(binding)

            result = {
                "head": {"vars": vars_list},
                "results": {"bindings": bindings}
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            return json.dumps({
                "error": str(e),
                "query": sparql_query,
                "note": "Query executed against Maplib in-memory model"
            }, indent=2)
    
    return query_model_tool