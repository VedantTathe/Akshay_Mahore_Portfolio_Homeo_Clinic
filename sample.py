from pymongo import MongoClient

    # Connect to MongoDB
client = MongoClient("mongodb+srv://vedant:vedant@cluster0.3glbf3u.mongodb.net/")  # Replace with your MongoDB connection string
db = client['Clinic']  # Replace with your database name
collection = db['Asmhomeo']  # Replace with your collection name
# Data to be added to documents
edu_data = {
    "edu_data_name": ["Dakshin Kesri Muni Mishrilalji Homoeopathic Medical College, Aurangabad", "Panchsheel Homoeopathic Medical College", "R. K. High School and Junior College, Pulgaon", "Pulgaon Cotton Mills Prathamik School, Pulgaon"],
    "edu_data_year": ["2012-2014", "NOTSET", "NOTSET", "NOTSET"],
    "edu_data_desc": ["To further specialize in my field, I completed my MD in Homeopathy at DKMM in Aurangabad. This advanced degree equipped me with deeper insights and expertise in homeopathic medical practices.", "I pursued my undergraduate studies in homeopathy at P H M C Khamgaon, where I earned my BHMS degree. This program provided me with comprehensive knowledge and training in homeopathic medicine.", "I continued my education at R. K. High School and Junior College in Pulgaon, where I completed my secondary and higher secondary education. This period helped me excel in my studies and prepare for a career in medicine.", "I began my educational journey at Pulgaon Cotton Mills Prathamik School in Pulgaon, where I developed a strong foundation in primary education."],
    "edu_data_degree": ["Doctor of Medicine (MD) in Homeopathy", "Bachelor of Homeopathic Medicine and Surgery (BHMS)", "Secondary and Higher Secondary Education","Primary Education"]
}

# Query to find documents with 'clinic_status' field
query = {"DOCTYPE": {"$exists": True}}
# Update operation to add the new fields to the matching documents
update = {"$set": edu_data}
# Update all matching documents
result = collection.update_many(query, update)
# Output the result
print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")

