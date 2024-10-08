# RAG Chatbot Excel

## Overview

**RAG Chatbot Excel** is a chatbot system that allows users to ask questions and interact with data from an Excel file. The system processes user queries and provides answers based on the content of the Excel file. In addition, the chatbot can generate charts upon request to visually represent data insights.

<p align="center">
  <img src="data/result.jpg" alt="Result" />
</p>

## Features

- **Excel File Input**: Accepts an Excel file as input for data analysis.
- **User Queries**: Answers user questions based on the data from the provided Excel file.
- **Chart Generation**: Creates charts and graphs based on user requests.
- **Retrieval-Augmented Generation (RAG)**: Utilizes RAG to improve the quality and relevance of answers by incorporating the context of the data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ethando9999/RAG-Chatbot-Excel.git
   cd RAG-Chatbot-Excel
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the environment by configuring API keys and any necessary tokens for the chatbot to function.

4. Run the server:

   ```bash
   python server.py
   ```
5. Run the web page:

   ```bash
   python web_page.py
   ```
## Usage

1. Upload your Excel file through the chatbot interface or specify a file path.
2. Ask the chatbot questions related to the data in the Excel file. For example:
   - "What is the total sales for Q1?"
   - "How many customers bought Product X?"
3. If needed, request a chart by asking the bot. For example:
   - "Can you show me a bar chart of sales per region?"
   - "Please create a pie chart for customer distribution."

The chatbot will process the query and either return the answer in text or generate the requested chart.

## Example

1. **Upload Excel File**:
   - You can upload a file named `sales_data.xlsx` via the chatbot or point it to a specific file path.

2. **Ask Questions**:
   - User: "What is the average sales price?"
   - Bot: "The average sales price is $120.50."

3. **Request Charts**:
   - User: "Show me a bar chart of sales by category."
   - Bot: [Bar chart is generated and displayed.]

## Technologies Used
- **LLMs**: gpt-4o, text-embedding-3-large
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **Uvicorn**: A lightning-fast ASGI server for serving FastAPI applications.
- **Pandas**: A powerful data manipulation library used for reading and processing Excel files.
- **LangChain**: A framework for building applications powered by language models, used for handling user queries and managing the chatbot logic.
- **FAISS-CPU**: A library for efficient similarity search and clustering of dense vectors, used to improve query retrieval performance.
- **Streamlit**: A fast and simple way to build custom user interfaces and display charts.
- **Matplotlib**: A plotting library used for creating charts and visualizations based on user requests.

## Contributing

Feel free to fork this repository and submit pull requests for improvements, bug fixes, or new features.


