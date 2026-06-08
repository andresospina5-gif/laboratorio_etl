from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["laboratorio_etl"]

cartas_collection = db["cartas"]