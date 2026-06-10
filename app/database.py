from pymongo import MongoClient

client = MongoClient("mongodb+srv://yasleidy:taller2026@cluster0.hdrwulj.mongodb.net/?appName=Cluster0")
db = client["laboratorio_etl"]
cartas_collection = db["cartas"]