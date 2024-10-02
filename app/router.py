from fastapi import FastAPI, File, UploadFile, Form, HTTPException, APIRouter
#from pydantic import BaseModel
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.prompt import prompt
import io
import os 
import re 

# Tạo router
router = APIRouter()

openai_api_key = os.getenv("OPENAI_API_KEY")


# Initialize embeddings, retriever and agent
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
#prompt = hub.pull("hwchase17/openai-functions-agent", api_key=hub_api_key)


def process_excel_file(content):
    """Reads an Excel file and processes each sheet into a list of Documents.

    Args:
        content (str): Contents of the Excel file.

    Returns:
        list: A list of Document objects, one for each row in the Excel file.
    """

    # Convert SpooledTemporaryFile to BytesIO for openpyxl to read the Excel file correctly

    excel_data = io.BytesIO(content)

    # Read the Excel file using pandas
    dfs = pd.read_excel(excel_data, sheet_name=None)

    all_documents = []
    for sheet_name, df in dfs.items():
        # Convert DataFrame rows into a list of Document objects for the current sheet
        data = df.to_dict(orient='records')
        documents = [Document(page_content=str(row), metadata={"sheet_name": sheet_name, **row}) for row in data]
        all_documents.extend(documents)

    return all_documents

@app.post("/ask")
async def ask_question( question: str, file: UploadFile = File(...)):
    # Kiểm tra định dạng file
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .xlsx file.")
    content = await file.read()  # Read the file contents    
    documents = process_excel_file(content)
    print(openai_api_key)

    # Create the FAISS index
    vector_store = FAISS.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "excel_search",
        "Search for information about Excel file. For any questions about excel file, you must use this tool!",
    )
    tools = [retriever_tool]
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Execute the agent to get an answer
    response = agent_executor.invoke({"input": question})
    response = response.get('output')
    print(response)

    # Remove json, csv
    pattern = r'^(?:```json|```csv|```)\s*(.*?)\s*```$'
    response = re.sub(pattern, r'\1', response, flags=re.DOTALL).strip()
    
    return {"answer": response}


