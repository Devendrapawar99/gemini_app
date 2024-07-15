import pymongo
from pymongo import MongoClient
import streamlit as st
import os
import json
import math
from dotenv import load_dotenv
import google.generativeai as genai  # Ensure this is the correct package name
from training_data.prompts import prompt

# Load environment variables
load_dotenv()

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide MongoDB query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to retrieve query from the MongoDB database
def read_mongo_query(query, db_name, collection_name, page=1, limit=10):
    db = client[db_name]
    collection = db[collection_name]
    total_count = 0  # Initialize total_count
    try:
        # Cleaning query string
        query = query.replace('```json', '').replace('```', '').strip()
        query_dict = json.loads(query)
        
        if "aggregate" in query_dict:
            pipeline = query_dict["aggregate"]
            st.write(f"Executing MongoDB aggregation pipeline: {pipeline}")
            rows = list(collection.aggregate(pipeline))
            total_count = len(rows)  # For aggregation, set total_count to number of rows returned
        else:
            filter_query = query_dict.get("filter", {})
            fields = query_dict.get("fields", None)
            projection = {}  # Default projection

            if fields:
                for field in fields:
                    projection[field] = 1

            st.write(f"Executing MongoDB query: {filter_query} with projection: {projection}")
            total_count = collection.count_documents(filter_query)
            rows = list(collection.find(filter_query, projection).skip((page - 1) * limit).limit(limit))
    except pymongo.errors.PyMongoError as e:
        st.error(f"MongoDB Error: {e}")
        rows = []
    except json.JSONDecodeError as e:
        st.error(f"JSON Decode Error: {e}")
        rows = []
    except Exception as e:
        st.error(f"Error: {e}")
        rows = []
    finally:
        client.close()
    return rows, total_count




# Streamlit App
st.set_page_config(page_title="Text To MongoDB Query App")
st.header("Text To MongoDB Query Conversion App")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# Initialize session state for pagination
if "page" not in st.session_state:
    st.session_state.page = 1

limit = st.number_input("Records per page", min_value=1, value=10, step=1)

# If submit is clicked
if submit:
    st.session_state.page = 1  # Reset to the first page for new queries
    response = get_gemini_response(question, prompt)
    st.write(f"Generated MongoDB query: {response}")  # Display the generated MongoDB query
    st.session_state.response = response  # Save the response to session state

# Fetch the data only if there is a response in session state
if "response" in st.session_state:
    try:
        data, total_count = read_mongo_query(st.session_state.response, "reportschat", "orders", st.session_state.page, limit)
        st.subheader("The Response is:")
        print(data,"------------data")
        if data:
            for row in data:
                st.json(row)  # Display the row in JSON format

            total_pages = math.ceil(total_count / limit)
            st.write(f"Page {st.session_state.page} of {total_pages}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.page > 1:
                    if st.button("Previous"):
                        st.session_state.page -= 1
                        st.experimental_rerun()

            with col2:
                if st.session_state.page < total_pages:
                    if st.button("Next"):
                        st.session_state.page += 1
                        st.experimental_rerun()
        else:
            st.subheader("No data found.")
    except Exception as e:
        st.error(f"Error processing query: {e}")