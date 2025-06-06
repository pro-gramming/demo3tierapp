"""
#
# employee_database.py contains the python program to define the database operations for the application 
# This file is for defining access methods of database and operations on database
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules and Libraries
# 
import asyncio
import motor.motor_asyncio
from bson.objectid import ObjectId
import os

# Get MongoDB connection details from environment variables with defaults
mongo_host = os.environ.get("MONGO_HOST", "127.0.0.1")
mongo_port = os.environ.get("MONGO_PORT", "27017")
mongo_username = os.environ.get("MONGO_USERNAME", "")
mongo_password = os.environ.get("MONGO_PASSWORD", "")
mongo_db_name = os.environ.get("MONGO_DB_NAME", "employees_DB")

# Build the connection string
if mongo_username and mongo_password:
    MONGO_DETAILS = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}"
else:
    MONGO_DETAILS = f"mongodb://{mongo_host}:{mongo_port}"

# Create a function to get the database connection
async def get_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    return client[mongo_db_name]

# Get employee collection
async def get_employee_collection():
    db = await get_database()
    return db.get_collection("employees")

# helpers
# Changing the data to python dictionary. Note, the changing of the id as string from bson ObjectId (mongodb)
def employee_helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "emp_id": employee["emp_id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "ph_no": employee["ph_no"],
        "home_addr": employee["home_addr"],
        "st_addr": employee["st_addr"],
        "gender": employee["gender"],
        "job_type": employee["job_type"],
    }



# Retrieve all employees present in the database
async def retrieve_employees():
    employees = []
    collection = await get_employee_collection()
    async for employee in collection.find():
        employees.append(employee_helper(employee))
    return employees


# Add a new employee into to the database
async def add_employee(employee_data: dict) -> dict:
    collection = await get_employee_collection()
    employee = await collection.insert_one(employee_data)
    new_employee = await collection.find_one({"_id": employee.inserted_id})
    return employee_helper(new_employee)


# Retrieve an employee with a matching employee ID
async def retrieve_employee(emp_id: int) -> dict:
    collection = await get_employee_collection()
    employee = await collection.find_one({"emp_id": emp_id})
    if employee:
        return employee_helper(employee)


# Update an employee with a matching employee ID
async def update_employee(emp_id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    collection = await get_employee_collection()
    employee = await collection.find_one({"emp_id": emp_id})
    if employee:
        updated_employee = await collection.update_one(
            {"emp_id": emp_id}, {"$set": data}
        )
        if updated_employee:
            return True
        return False


# Delete an employee from the database
async def delete_employee(emp_id: int):
    collection = await get_employee_collection()
    employee = await collection.find_one({"emp_id": emp_id})
    if employee:
        await collection.delete_one({"emp_id": emp_id})
        return True
