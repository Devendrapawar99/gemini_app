import pymongo
from pymongo import MongoClient
import re
import os
import json
import math
from dotenv import load_dotenv
import google.generativeai as genai
from training_data.prompts import prompt
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

def getNewFunc(question):
    print(question, "------get call func")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response

def get_gemini_response(question):
    print(question, "----question")

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

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
            print(f"Executing MongoDB aggregation pipeline: {pipeline}")
            rows = list(collection.aggregate(pipeline))
            total_count = len(rows)  # For aggregation, set total_count to number of rows returned
        else:
            filter_query = query_dict.get("filter", {})
            fields = query_dict.get("fields", None)
            projection = {}  # Default projection

            if fields:
                for field in fields:
                    projection[field] = 1

            print(f"Executing MongoDB query: {filter_query} with projection: {projection}")
            total_count = collection.count_documents(filter_query)
            rows = list(collection.find(filter_query, projection).skip((page - 1) * limit).limit(limit))
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB Error: {e}")
        rows = []
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        rows = []
    except Exception as e:
        print(f"Error: {e}")
        rows = []
    return rows, total_count, query  # Return the executed query

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question")
    page = data.get("page", 1)
    limit = data.get("limit", 10)
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    try:
        #specific question
        if re.search(r'\bwho\s*(are|r)\s*(you|u)\b', question, re.IGNORECASE):
            return jsonify({
                "answer": "Hello! I am your dedicated CXO Dashboard Bot, developed by Assimilate Technologies, designed to provide you with a bird's eye view of your business. I specialize in delivering high-level insights and key performance indicators, helping you make informed decisions quickly. Whether you need to check financial information, operational statistics, or strategic overviews, I'm here to assist. How can I help you today?"
            }), 200
         
        response = get_gemini_response(question)
        print(f"Generated MongoDB query: {response}")  # Display the generated MongoDB query
        
        data, total_count, executed_query = read_mongo_query(response, "reportschat", "orders", page, limit)
        print(data,"--------------data")
        if not data:
            return jsonify({"answer": "No data found"}), 200
        
        
        # Determine the key and format the answer accordingly
        if 'count' in data[0]:
            answer = f"The result is {data[0]['count']}"
        elif 'totalPrice' in data[0]:
            answer = f"The result is {data[0]['totalPrice']}"
        elif 'totalRevenue' in data[0]:
            answer = f"The result is {data[0]['totalRevenue']}"
        elif 'revenue' in data[0]:
            answer = f"The result is {data[0]['revenue']}"
        elif 'customerwisePrice' in data[0]:
           answer = "The result is: " + ", ".join([f"name: {item['_id']}, price: {item['customerwisePrice']}" for item in data])
        elif 'ProfitData' in data[0]:
           profit_data = data[0]['ProfitData']
           answer = (
            f"The result is:\n"
            f"**Price**: **{profit_data['Price']:.2f}**,\n"
            f"**Hauler Price**: **{profit_data['Hauler Price']:.2f}**,\n"
            f"**Profit**: **{profit_data['Profit']:.2f}**"
            )
        else:
            answer = {"result": data}

        return jsonify({
            "answer": answer,
            "data": data,
            "executed_query": executed_query
        }), 200

    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500




# API to get the params 
@app.route('/rag/query/run_mongo_query', methods=['GET'])
def ask_question_query():
    question = request.args.get('user_query')
    page = 1
    limit = 100
    
    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        #specific question
        if re.search(r'\bwho\s*(are|r)\s*(you|u)\b', question, re.IGNORECASE):
            return jsonify({
                "answer": "I am a data retrieval bot developed by Assimilate Technologies Pvt Ltd, here to assist you with your queries."
            }), 200
        
        response = get_gemini_response(question)
        print(f"Generated MongoDB query: {response}")
        
        data, total_count, executed_query = read_mongo_query(response, os.getenv("DATABASE"), os.getenv("TABLE"), page, limit)
        
        if not data:
            return jsonify({"answer": "No data found"}), 200
        
        
        # Determine the key and format the answer accordingly
        if 'count' in data[0]:
            answer = f"The result is {data[0]['count']}"
        elif 'totalPrice' in data[0]:
            answer = f"The result is {data[0]['totalPrice']}"
        elif 'totalRevenue' in data[0]:
            answer = f"The result is {data[0]['totalRevenue']}"
        elif 'revenue' in data[0]:
            answer = f"The result is {data[0]['revenue']}"
        elif 'customerwisePrice' in data[0]:
           answer = "The result is: " + ", ".join([f"name: {item['_id']}, price: {item['customerwisePrice']}" for item in data])
        elif 'ProfitData' in data[0]:
           profit_data = data[0]['ProfitData']
           answer = (
            f"The result is:\n"
            f"**Price**: **{profit_data['Price']:.2f}**,\n"
            f"**Hauler Price**: **{profit_data['Hauler Price']:.2f}**,\n"
            f"**Profit**: **{profit_data['Profit']:.2f}**"
            )
        else:
            answer = {"result": data}

        return jsonify({
            "answer": answer,
            "data": data,
            "executed_query": executed_query
        }), 200


    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
