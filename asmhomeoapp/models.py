from django.db import models
from pymongo import MongoClient
from datetime import datetime


constring = 'mongodb+srv://vedant:vedant@cluster0.3glbf3u.mongodb.net/'

class MyClinic():
    def getClinicStatus(self):
        client = MongoClient(constring)
        db = client['Clinic']
        coll = db['Asmhomeo']

        
        results = coll.find_one({"clinic_status": {"$exists": True}})
        
        return results
        
    def searchData(self,query=None):
    
        client = MongoClient(constring)
        db = client['Clinic']
        coll = db['Asmhomeo']

        if query.strip()=='':
            results = list(coll.find({"Name": {"$exists": True}}, {"_id": 0, "Name": 1, "MobileNo": 1, "RegNo": 1}))
        elif query:
            results = list(coll.find({"$or": [
                {"Name": {"$regex": query, "$options": "i"}},
                {"MobileNo": {"$regex": query, "$options": "i"}},
                {"RegNo": {"$regex": query, "$options": "i"}}
            ]}, {"_id": 0, "Name": 1, "MobileNo": 1, "RegNo": 1}))
        else:
            results = list(coll.find({"Name": {"$exists": True}}, {"_id": 0, "Name": 1, "MobileNo": 1, "RegNo": 1}))

         
        return results

        

    def changeStatus(self,query='NONSET'):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']

            query = query.strip()
            
            today_date = datetime.now().strftime('%Y-%m-%d')

            coll.update_one(
                {"clinic_status": {"$exists": True}},  # Query
                {"$set": {"clinic_status": query, "date_updated": today_date}}    # Update
            )

            data.update({
                'message':'Clinic Status Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data


    def updateNotice(self, notice):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']


            coll.update_one(
                {"clinic_status": {"$exists": True}},  # Query
                {"$set": {"notice":notice}}    # Update
            )

            data.update({
                'message':'Notice Updated Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data
        
    
    def sendMessage(self, name, email, message):
        data = {}
        try:
            i = {'name': name, 'email': email, 'message': message}

            client = MongoClient(constring)  # Make sure 'constring' is defined correctly

            db = client['Clinic']

            coll = db['AsmhomeoMessages']

            coll.insert_one(i)

            data.update({
                'message': 'Message Sent Successfully..!'
            })

        except Exception as e:
            print(f"An error occurred: {e}")

            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

            

        return data