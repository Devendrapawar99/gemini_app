import pymongo
from pymongo import MongoClient
import streamlit as st
import os
import json
import math
from dotenv import load_dotenv
import google.generativeai as genai  # Ensure this is the correct package name

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

prompt = [
    """
    You are an expert in converting English questions to MongoDB queries!
    The MongoDB collection has the name ORDERS and has the following fields:
    
    - _id
    - PK
    - UserDetails (Object)
        - phoneNumber
        - emirate
        - phone
        - rate
        - erpCode
        - fullName
        - email
        - RecordType
        - Status
        - PriceTTC
        - HaulerPrice
        - UOM
        - ScheduledDate
    - SalesPerson (Object)
        - SK
        - name
        - pk
        - phoneNumber
        - RecordType
        - email
        - Price
        - CreatedAt
    - VehicleDetails (Object)
        - HelpersNumber
        - Category
        - Description
        - InstallerNumber
        - VehicleTypeAr
        - CategoryAr
        - VehicleType
        - SK
        - PK
        - Image
        - DescriptionAr
        - Data
        - BranchId
    - Inquiry (Object)
        - SalesPrice
        - Type
        - OrderId
    - Customer (Object)
        - PK
        - BranchId
        - Email
        - Phone
        - FullName
        - TargetBuyingPrice
        - SK
        - CostPrice
        - InquiryNoOfVehicles
        - NoOfVehicles
        - HaulerPriceTTC
        - Type
        - OrderId
    - SourcePerson (Object)
        - sk
        - name
        - pk
        - phoneNumber
        - RecordType
        - email
    - Branch (Object)
        - SK
        - BranchName
        - PK
        - CompanyCode
        - Currency
    - CreatedAt
    - UpdatedAt

    
    Example 1 - Tell me all the orders in Abu Dhabi?
    The MongoDB command will be like this: {"filter": {"UserDetails.emirate": "Abu Dhabi"}}

    Example 2 - Give me the order details for order ID "Order#1719578812822"?
    The MongoDB command will be like this: {"filter": {"PK": "Order#1719578812822"}}

    Example 3 - Give me the Status of the order with ID "Order#1719578812362"?
    The MongoDB command will be like this: {"filter": {"PK": "Order#1719578812362"}, "fields": ["Status"]}

    Example 4 - Give me the total of all orders price?
    The MongoDB command will be like this: {"aggregate": [{"$group": {"_id": null, "totalPrice": {"$sum": "$PriceTTC"}}}]}

    Example 5 - Give me the SalesPrice of the order with ID "Order#1719578812822"?
    The MongoDB command will be like this: {"filter": {"PK": "Order#1719578812822"}, "fields": ["Inquiry.SalesPrice"]}

    Example 6 - Give me the CostPrice of the order with ID "Order#1719578812822"?
    The MongoDB command will be like this: {"filter": {"PK": "Order#1719578812822"}, "fields": ["Inquiry.CostPrice"]}

    Example 7 - Give me the orders managed by Salesperson Joseph Daniel.
    The MongoDB command will be something like this: {"filter": {"SalesPerson.name": "Joseph Daniel"}}

    Example 8 - Example: Give me the count of orders managed by Salesperson Joseph Daniel.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"SalesPerson.name": "Joseph Daniel"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 9 - Give me the count of orders with status "pending".
    The MongoDB command will be like this: {"filter": {"Status": "pending"}}

    Example 10 - Give me the total enterprise orders.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Inquiry.Type": "move_enterprise"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 11 - Give me the count of orders from the Sharjah branch.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Branch.BranchName": "re.life (FZE) Sharjah"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 12 - Give me the total count of orders for july 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1719792000000,
                        "$lt": 1722384000000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    The query code should be a valid MongoDB query in JSON format.
    """
]

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
        data, total_count = read_mongo_query(st.session_state.response, "mytest", "orders", st.session_state.page, limit)
        st.subheader("The Response is:")

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