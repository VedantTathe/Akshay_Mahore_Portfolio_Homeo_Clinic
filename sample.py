from pymongo import MongoClient
from faker import Faker
import random

# Initialize Faker library
fake = Faker()

# MongoDB connection string
constring = 'mongodb+srv://vedant:vedant@cluster0.3glbf3u.mongodb.net/'

# Connect to MongoDB
client = MongoClient(constring)
db = client['Clinic']
coll = db['Asmhomeo']

# Generate and insert 25 random records
records = []
for _ in range(25):
    record = {
        "Name": fake.name(),
        "MobileNo": fake.phone_number(),
        "RegNo": f"TN{random.randint(100, 999)}"
    }
    records.append(record)

# Insert records into the collection
coll.insert_many(records)

print("Inserted 25 random records into the asmhomeo collection.")
