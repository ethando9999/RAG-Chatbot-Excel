import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from app import settings
from dotenv import load_dotenv

load_dotenv()

# Define your FastAPI endpoint
API_URL = f"http://{settings.host}:{settings.port}/ask"  # Update with your API URL

# Streamlit UI
st.title("Excel Q&A Application")

# API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# File Upload
uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

# User question input
question = st.text_input("Ask a question about the Excel file:")

# Submit button
if st.button("Submit"):
    if uploaded_file is not None and question:
        # Read the content of the uploaded file
        file_content = uploaded_file.read()

        # Prepare request data
        files = {"file": (uploaded_file.name, file_content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        
        # Send the question as a query parameter
        params = {"question": question}

        # Make the API request
        response = requests.post(API_URL, params=params, files=files)

        # Check response
        if response.status_code == 200:
            try:
                # Try to parse the response as JSON
                answer = response.json().get("answer")

                # If the answer is a dictionary or list (valid JSON structure), handle visualization
                try:
                    parsed_answer = json.loads(answer)

                    # Example: If the JSON contains key-value pairs that are numeric, we can plot them
                    if isinstance(parsed_answer, dict):
                        df = pd.DataFrame(list(parsed_answer.items()), columns=["Key", "Value"])
                        
                        # Check if 'Value' column contains numeric data for plotting
                        if pd.to_numeric(df["Value"], errors="coerce").notnull().all():
                            # Plot the data using matplotlib
                            fig, ax = plt.subplots(figsize=(5, 3))
                            ax.bar(df["Key"], df["Value"])
                            st.pyplot(fig)
                        else:
                            st.warning("The JSON data is not numeric and cannot be plotted.")
                    
                    elif isinstance(parsed_answer, list):
                        df = pd.DataFrame(parsed_answer)
                        
                        # Check if the dataframe is numeric and plotable
                        if df.apply(pd.to_numeric, errors="coerce").notnull().all().all():
                            st.line_chart(df)
                        else:
                            st.warning("The JSON data is not suitable for plotting.")        
                except Exception as e:
                    print(e)
                    st.success(f"Answer: {answer}")

            except json.JSONDecodeError:
                # If the response is not in JSON format
                st.success(f"Answer: {response.text}")
        else:
            st.error(f"Error: {response.text}")
    else:
        st.warning("Please upload a file and ask a question.")
