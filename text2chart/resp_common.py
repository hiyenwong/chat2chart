import streamlit as st
import pandas as pd
import json

from text2chart.azure_agent import query_agent, create_agent
from loguru import logger


def decode_response(resp: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        resp (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    if 'output' in resp:
        try:
            ret = json.loads(resp['output'])
            return ret
        except ValueError as e:
            return resp['output']
    return "I don't have idea."


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        logger.debug("bar chart:{}", response_dict['bar'])
        data = response_dict["bar"]
        logger.debug(data)
        df = pd.DataFrame(data=data['data'], columns=data['columns'])
        # df.set_index("columns", inplace=True)
        st.bar_chart(df.set_index(data['columns'][0]))

    # Check if the response is a line chart.
    if "line" in response_dict:
        logger.debug("line chart")
        data = response_dict["line"]
        df = pd.DataFrame(data=data['data'], columns=data['columns'])
        # df.set_index("columns", inplace=True)
        st.line_chart(df.set_index(data['columns'][0]))

    # Check if the response is a table.
    if "table" in response_dict:
        logger.debug("table")
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
