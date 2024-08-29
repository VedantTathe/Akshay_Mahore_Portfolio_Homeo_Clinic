
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

        

    def changeStatus(self,query='NOTSET'):
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


        
    
    def addPatient(self, name, mobileno, regno):

        data = {}
        try:
            i = {'Name': name, 'MobileNo': mobileno, 'RegNo': regno}

            client = MongoClient(constring)  # Make sure 'constring' is defined correctly

            db = client['Clinic']


            coll = db['Asmhomeo']

            coll.insert_one(i)

            data.update({
                'message': 'Patient Added Successfully..!'
            })

        except Exception as e:
            print(f"An error occurred: {e}")

            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

            


        return data



    
    
    def delPatient(self,regno):

        data = {}
        try:

            client = MongoClient(constring)  # Make sure 'constring' is defined correctly

            db = client['Clinic']


            coll = db['Asmhomeo']

            result = coll.delete_many({'RegNo': regno})

            # Check if a document was deleted
            if result.deleted_count > 0:
                data.update({
                    'message': 'Patient Deleted Successfully..!'
                })
            else:
                data.update({


                    'err': 'No patient found with the given RegNo.'
                })

        except Exception as e:
            print(f"An error occurred: {e}")



            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

            


        return data

    def getAllData(self):
        client = MongoClient(constring)  # Make sure 'constring' is defined correctly

        db = client['Clinic']
        coll = db['Asmhomeo']
        cursor = coll.find(
            {"Name": {"$exists": True}},  # Filter to get documents where the "Name" field exists
            {"_id": 0, "RegNo":0}  # Projection to exclude these fields
        )
        data = list(cursor)  # Convert cursor to a list

        return data

      
    def changeHeroHeading(self,query='NOTSET'):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']

            query = query.strip()

            coll.update_one(
                {"hero_heading": {"$exists": True}},  # Query
                {"$set": {"hero_heading": query}}    # Update
            )

            data.update({
                'message':'Hero Heading Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data


  
    def changeClinicTimings(self,query='NOTSET'):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']

            query = query.strip()

            coll.update_one(
                {"clinic_timings": {"$exists": True}},  # Query
                {"$set": {"clinic_timings": query}}    # Update
            )

            data.update({
                'message':'Clinic Timings Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data

      
    def changeAboutData(self,query='NOTSET'):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']

            query = query.strip()

            coll.update_one(
                {"about_data": {"$exists": True}},  # Query
                {"$set": {"about_data": query}}    # Update
            )

            data.update({
                'message':'About Data Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data

      
    def changeContactData(self,mobileno='9922332719',email='asmhomoeo@gmail.com'):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']

            mobileno = mobileno.strip()
            email = email.strip()

            coll.update_one(
                {"mobileno": {"$exists": True}},  # mobileno
                {"$set": {"mobileno": mobileno}}    # Update
            )

            coll.update_one(
                {"email": {"$exists": True}},  # email
                {"$set": {"email": email}}    # Update
            )

            data.update({
                'message':'Contact Data Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data

    def changeEduData(self,t1, t2, t3, t4):
        data = {}
        try:
            client = MongoClient(constring)
            db = client['Clinic']
            coll = db['Asmhomeo']
            

            coll.update_one(
                {"clinic_status": {"$exists": True}},  # mobileno
                {"$set": {"edu_data_name": t1, "edu_data_year":t2, "edu_data_desc":t3, "edu_data_degree":t4}}    # Update
            )
            data.update({
                'message':'Contact Data Changed Successfully..!'
            })
        except Exception as e:
            print(e)
            data.update({
                'err': 'Oops..! Something Went Wrong..!'
            })

        return data

    def readMessages(self):
        client = MongoClient(constring)
        db = client['Clinic']
        coll = db['AsmhomeoMessages']

        
        results = list(coll.find({}))


    
        return results
        
    def delMsg(self,message):


        data = {}
        try:
            # Connect to MongoDB
            print(f"Attempting to delete message: {message}")

            client = MongoClient(constring)  # Ensure 'constring' is defined correctly
            
            # Access the 'Clinic' database and 'Asmhomeo' collection
            db = client['Clinic']
            coll = db['AsmhomeoMessages']
            
            # Delete all documents matching the given 'message'
            result = coll.delete_many({'message': message})
            
            # Update the response based on the result
            if result.deleted_count > 0:
                data['message'] = 'Message Deleted Successfully..!'
            else:
                data['err'] = 'No Message found'
        
        except Exception as e:
            print(f"An error occurred: {e}")
            data['err'] = 'Oops..! Something Went Wrong..!'
        
        return data


