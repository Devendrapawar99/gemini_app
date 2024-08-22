import pymongo
from pymongo import MongoClient
import streamlit as st
import os
import json
import math
from dotenv import load_dotenv
import google.generativeai as genai  # Ensure this is the correct package name
from training_data.prompts import prompt
import pandas as pd
import altair as alt
    

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()


def read_mongo_query(query, db_name, collection_name, page=1, limit=10):
    db = client[db_name]
    collection = db[collection_name]
    total_count = 0  
    try:
       
        query = query.replace('```json', '').replace('```', '').strip()
        query_dict = json.loads(query)
        
        if "aggregate" in query_dict:
            pipeline = query_dict["aggregate"]
            st.write(f"Executing MongoDB aggregation pipeline: {pipeline}")
            rows = list(collection.aggregate(pipeline))
            total_count = len(rows)  
        else:
            filter_query = query_dict.get("filter", {})
            fields = query_dict.get("fields", None)
            projection = {}  
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



def create_stacked_bar_chart(profit_data):
    extracted_data = []
    for month, data in profit_data.items():
        for category, value in data.items():
            extracted_data.append({
                'Month': month,
                'Category': category,
                'Value': value
            })
    
    df = pd.DataFrame(extracted_data)

    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Month:N', title='Month'),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('Category:N', legend=alt.Legend(title='Category'))
    ).properties(
        width=alt.Step(50),
    
    )
    
    st.altair_chart(chart, use_container_width=True)
    


def create_bar_chart(data):
    numeric_data = extract_numeric_data(data)
    if numeric_data:
        stripped_data = {k.split('.')[-1]: v for k, v in numeric_data.items()}
        df = pd.DataFrame([stripped_data])
        
        chart = alt.Chart(df.melt()).mark_bar(size=50).encode(
            x=alt.X('variable:N', title="ProfitData"),
            y=alt.Y('value:Q'),
            color=alt.Color('variable:N') 
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No Numeric data available to show bar chart.")
        
        

def extract_numeric_data(data, key=''):
    numeric_data = {} 
    if isinstance(data, dict):
        for k, v in data.items():
            key = f"{key}.{k}" if key else k
            if isinstance(v, (int, float)):
                numeric_data[key] = v
            elif isinstance(v, dict):
                numeric_data.update(extract_numeric_data(v, key))
    return numeric_data


st.set_page_config(page_title="Text To MongoDB Query App")
st.header("Text To MongoDB Query Conversion App")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")


if "page" not in st.session_state:
    st.session_state.page = 1

limit = st.number_input("Records per page", min_value=1, value=10, step=1)


if submit:
    st.session_state.page = 1
    response = get_gemini_response(question, prompt)
    st.write(f"Generated MongoDB query: {response}")  
    st.session_state.response = response  

if "response" in st.session_state:
    try:
        data, total_count = read_mongo_query(st.session_state.response, "reportschat", "orders", st.session_state.page, limit)
        st.subheader("The Response is:")
        #print(data,"------------data")
        if data:
            for row in data:
                st.json(row)  
                
            st.subheader("Graphical Representation:")
            if "MonthWiseProfitData" in data[0]: 
                create_stacked_bar_chart(data[0]["MonthWiseProfitData"]) 
                
            elif "YearWiseProfitData" in data[0]:
                create_stacked_bar_chart(data[0]["YearWiseProfitData"]) 
            else:
                create_bar_chart(data[0])
            
            
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