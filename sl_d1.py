import streamlit as st
import pandas as pd
from text2chart.resp_common import decode_response, write_response

from text2chart.azure_agent import query_agent, create_agent
from loguru import logger


st.title("👨‍💻 聊天分析CSV数据")

data = st.file_uploader("上传文件")

query = st.text_area("请输入你的问题")

if st.button("提交请求", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(data)

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    if response == 'Agent stopped due to iteration limit or time limit.':
        write_response(response)
    else:
        decoded_response = decode_response(response)
        # Write the response to the Streamlit app.
        write_response(decoded_response)
