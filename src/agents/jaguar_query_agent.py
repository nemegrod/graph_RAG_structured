
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIResponsesClient, OpenAISettings
from agent_framework import ChatAgent
from src.agents.jaguar_tool import create_query_jaguar_model_tool


# Load environment variables
load_dotenv()


def create_jaguar_query_agent(jaguar_model):
    """
    Create and return a native Agent Framework agent for jaguar conservation.
    
    Args:
        jaguar_model: Initialized Maplib Model with knowledge graph
    
    Returns:
        Agent Framework ChatAgent instance
    """
    # System prompt for the agent
    system_prompt = """
    You are a helpful assistant with access to a comprehensive jaguar database stored in GraphDB. 
    When users ask questions about jaguars, jaguar populations, conservation efforts, habitats, threats, or any jaguar-related information, 
    use the query_jaguar_database function with a valid SPARQL query. Always try to use the function to get accurate data from the database.

    When using the function:
    - Make sure to form a simple query and only add complexity if needed.
    - Make sure your queries are based on the provided jaguar ontology. Don't make up properties or classes not in the ontology.
    - Always include relevant prefixes in the query sent to the function.
    - Answer based on the data retrieved, never your training data.

    When responding:
    - Show the used SPARQL one time and one time only
    - Formulate a readable answer based on the query results
    - Use **bold** for emphasis when appropriate
    - Use bullet points or numbered lists for multiple items
    - Use code blocks with ``` for SPARQL queries when showing them
    - Break up long responses into paragraphs
    - Be concise but comprehensive in your answers
    - Always mention that the information comes from the jaguar database"""
    
        # OpenAI settings with larger context window model
    settings = OpenAISettings(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model_id=os.getenv("OPENAI_RESPONSES_MODEL_ID", "gpt-4o")  # Use GPT-4o for larger context window
    )
    
    # Create client
    client = OpenAIResponsesClient(settings=settings)
    
    # Create query tool bound to this model
    jaguar_query_tool = create_query_jaguar_model_tool(jaguar_model)
    
    # Create and return native Agent Framework agent
    agent = ChatAgent(
        client,
        name="JaguarQueryAgent",
        instructions=system_prompt,
        tools=[jaguar_query_tool],
        tool_choice="auto"
    )
    
    return agent

