from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend
api = Api(app)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["questionnaire"]  # Database name
responses_collection = db["responses"]  # Collection name

# API to submit responses
class SubmitResponse(Resource):
    def post(self):
        data = request.json
        user_id = data.get("userId")
        answers = data.get("answers")

        if not user_id or not answers:
            return {"error": "Missing user ID or answers"}, 400

        response_entry = {
            "userId": user_id,
            "answers": answers
        }
        responses_collection.insert_one(response_entry)

        return {"message": "Response saved successfully"}, 201

# API to get responses for a user
class GetResponses(Resource):
    def get(self, user_id):
        responses = list(responses_collection.find({"userId": user_id}, {"_id": 0}))
        return jsonify(responses)

# Add API routes
api.add_resource(SubmitResponse, "/submit")
api.add_resource(GetResponses, "/responses/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True, port=5000)