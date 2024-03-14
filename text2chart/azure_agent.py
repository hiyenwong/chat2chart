import os
from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from loguru import logger

_ = load_dotenv(find_dotenv())


def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOY_NAME_GPT3"),
        model_name=os.getenv("AZURE_OPENAI_DEPLOY_NAME_GPT3"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
        openai_api_key=os.environ['AZURE_OPENAI_KEY']
    )

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)
    logger.debug(df)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)


def query_agent(agent, query) -> dict:
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = (
        """     
                the answer need JSON.
                For the following query, if it requires drawing a table, reply as follows:
                {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}
    
                If the query requires creating a bar chart, reply as follows:
                {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
    
                If the query requires creating a line chart, reply as follows:
                {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
    
                There can only be two types of chart, "bar" and "line".
    
                If it is just asking a question that requires neither, reply as follows:
                {"answer": "answer"}
                Example:
                {"answer": "The title with the highest rating is 'Gilead'"}
    
                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}
    
                Return all output as a string.
    
                All strings in "columns" list and data list, should be in double quotes,
    
                For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}
    
                Lets think step by step.
                
                Below is the query.
                Query: 
                """
        + query
    )

    # Run the prompt through the agent.
    logger.debug(prompt)
    response = agent.invoke(prompt, handle_parsing_errors=True)
    logger.debug(response)
    # Convert the response to a string.
    return response
