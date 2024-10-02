from langchain.prompts import PromptTemplate

template = """
SYSTEM
You are a helpful assistant that can answer questions about data in an Excel file. 
If the human requests a chart, return the data as JSON format and don't add any additional information to the response.

HUMAN
{input}

PLACEHOLDER
{agent_scratchpad}
"""
prompt = PromptTemplate(
    input_variables=["chat_history", "input", "agent_scratchpad"], template=template
)
