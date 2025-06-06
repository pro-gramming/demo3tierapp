#!/usr/bin python

"""
#
# Program to get data from remote DB server and show in the frontend
# This script defines all the routes to be accessed by frontend web server
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules
from flask import Flask, render_template, request, jsonify
import requests
# Defining the Database details
import time
import json
# Importing socket library
import socket
import os

# Get configuration from environment variables with sensible defaults
db_host = os.environ.get('DB_HOST', 'db')
db_port = os.environ.get('DB_PORT', '80')
api_protocol = os.environ.get('API_PROTOCOL', 'http')

# External URL for API documentation access from browser 
# This will be the URL that users access in their browser for Swagger/ReDoc
# In Kubernetes, this might be an ingress hostname or a service with NodePort/LoadBalancer
db_external_host = os.environ.get('DB_EXTERNAL_HOST', 'localhost')
db_external_port = os.environ.get('DB_EXTERNAL_PORT', '8081')
db_external_url = f"{db_external_host}:{db_external_port}"

# Internal API URL for container-to-container communication
api_url_base = f"{api_protocol}://{db_host}:{db_port}/employee"

# Define header for API requests
header = {'Content-Type': 'application/json'}

# Defining the app details
# Init app
app = Flask(__name__)

app.config["DEBUG"] = True

################### Define functions and routes ##########################

# Function to determine Web Server
def get_Web_Host_name_IP():
    try:
        webservers = {
        'web-server-1': 'web-01',
        'web-server-2': 'web-02'
        }

        remote = request.remote_addr   
        #print(remote)

        if remote in webservers:
            web_host_name = webservers[remote]
        else:
            web_host_name = remote
        #print(web_host_name)
        return web_host_name
    except:
        print("Unable to get Web Hostname and IP")
        return "Unable to get Web Hostname"
    
# Function to display hostname and
# IP address
def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        #host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ", host_name)
        #print("IP : ", host_ip)
        return host_name
    except:
        print("Unable to get Hostname and IP")
        return ""

# Get all the employees data
@app.route('/')
def employees():
    api_url = f"{api_url_base}/"

    print(f"Connecting to database API at: {api_url}")
    response = ''
    while response == '':
        try:
            response = requests.get(api_url, headers=header, verify=False)
            break
        except Exception as e:
            print(f"Exception when connecting to database: {str(e)}")
            for i in range(3):
                print("Connection refused by the server..")
                print("Let's wait for 5 seconds and try again")
                time.sleep(5)
                print("Trying again...")
                continue
    
    print(f"API Response status: {response.status_code}")
    if response.status_code == 200:
         json_data_all = response.json()
         json_data = json_data_all["data"]
         employee_data = json_data[0]
         print(f"Got employee data: {len(employee_data)} records")
         host_name = get_Host_name_IP()
         web_host_name = get_Web_Host_name_IP()
         return render_template('homepage.html',
                              employee_data=employee_data, 
                              db_fqdn=db_external_url, 
                              web_host_name=web_host_name, 
                              host_name=host_name)
    else:
         print(f"Could not get employee list. Status code: {response.status_code}")
         try:
             print(f"Response: {response.text}")
         except:
             pass
         return "Could not get employee list"


# Create a new employee record
@app.route('/employee', methods=["POST"]) #,"GET"])  
def single_employee():
    api_url = "{0}".format(api_url_base)
    headers = {'content-type': 'application/json'}

    if request.method == 'POST':
        emp_id = request.form['emp_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        #email = first_name + '.' + last_name + 'acme.com'  # Email auto-generated
        email = request.form['email']
        ph_no = request.form['ph_no']
        home_addr = request.form['home_addr']
        st_addr = request.form['st_addr']
        gender = request.form['gender']
        job_type = request.form['job_type']
        # print(emp_id)
        # print(first_name)
        # print(last_name)
        # print(email)
        # print(ph_no)
        # print(home_addr)
        # print(st_addr)
        # print(gender)
        # print(job_type)
        # print("I am making the request now")
        request_body = {
            "emp_id": emp_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "ph_no": ph_no,
            "home_addr": home_addr,
            "st_addr": st_addr,
            "gender": gender,
            "job_type": job_type
            }
        
        #payload = jsonify(request_body)
        print("Request Body", request_body)
        
        response = ''
        while response == '':
            try:
                response = requests.post(api_url, data = json.dumps(request_body), headers=headers)
                break
            except:
                for i in range(3):
                    print("Connection refused by the server..")
                    print("Let's wait for 5 seconds and try again")
                    time.sleep(5)
                    print("Trying again...")
                    continue
        
        #print(response)
        
        info=response.json()
        #print(info)


        #print(response.status_code)
        if response.status_code == 201:
            json_data_all = response.json()
            json_data = json_data_all["data"]

            print("Successfully added the record for the employee: {}".format(first_name))
            return ("Successfully added the record for the employee: {}".format(first_name))
        else:
            print("Could not add to the employee record. Error: {}".format(info))
            
            return ("Could not add to the employee record. Error: {}".format(info))


# GET, UPDATE/Edit, DELETE an existing employee record
@app.route('/employee/<int:id>', methods=["PUT", "GET", "DELETE"])
def edit_employee_record(id):
    api_url = f"{api_url_base}/{id}"
    headers = {'content-type': 'application/json'}
    
    print(f"Request method: {request.method} for ID: {id}")
    print(f"API URL: {api_url}")
    
    if request.method == 'PUT':
        try:
            emp_id = request.form['emp_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = first_name + '.' + last_name + '@acme.com'  # Email auto-generated
            ph_no = request.form['ph_no']
            home_addr = request.form['home_addr']
            st_addr = request.form['st_addr']
            gender = request.form['gender']
            job_type = request.form['job_type']
            
            request_body = {
                "emp_id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "ph_no": ph_no,
                "home_addr": home_addr,
                "st_addr": st_addr,
                "gender": gender,
                "job_type": job_type
            }
            
            print(f"PUT request body: {request_body}")
            
            try:
                response = requests.put(api_url, data=json.dumps(request_body), headers=headers)
                print(f"PUT response status: {response.status_code}")
                print(f"PUT response headers: {response.headers}")
                
                try:
                    info = response.json()
                    print(f"PUT response data: {info}")
                    
                    if response.status_code == 200:
                        json_data = info.get("data", "Record updated successfully")
                        success_message = f"Successfully edited the record for the employee: {json_data}"
                        print(success_message)
                        return success_message
                    else:
                        error_message = f"Could not edit the employee record. Error: {info}"
                        print(error_message)
                        return error_message
                        
                except ValueError:
                    # If the response is not JSON, return the text content
                    print(f"Non-JSON response: {response.text}")
                    if response.status_code == 200:
                        return "Record updated successfully"
                    else:
                        return f"Could not edit the employee record. Status code: {response.status_code}"
                    
            except requests.exceptions.ConnectionError as e:
                error_message = f"Connection error when trying to update record: {str(e)}"
                print(error_message)
                return error_message
            except Exception as e:
                error_message = f"Error updating employee record: {str(e)}"
                print(error_message)
                return error_message
                
        except Exception as e:
            error_message = f"Error processing form data: {str(e)}"
            print(error_message)
            return error_message

    elif request.method == 'GET':
        try:
            response = requests.get(api_url, headers=header, verify=False)
            print(f"GET response status: {response.status_code}")
            
            if response.status_code == 200:
                json_data_all = response.json()
                json_data = json_data_all["data"]
                return render_template('homepage.html', json_data=json_data)
            else:
                print(f"Could not get employee record. Status code: {response.status_code}")
                return f"Could not get employee record. Status code: {response.status_code}"
                
        except Exception as e:
            error_message = f"Error getting employee record: {str(e)}"
            print(error_message)
            return error_message
    
    elif request.method == 'DELETE':
        print(f"Processing DELETE request for employee ID: {id}")
        try:
            # Send the DELETE request to the API
            response = requests.delete(api_url, headers=headers, verify=False)
            
            # Log the response details
            print(f"DELETE request sent to {api_url}")
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            try:
                # Try to parse the response as JSON
                response_data = response.json()
                print(f"Response data: {response_data}")
                
                if response.status_code == 200:
                    json_data = response_data.get("data", "Record deleted successfully")
                    success_message = f"Successfully deleted the record: {json_data}"
                    print(success_message)
                    return success_message
                else:
                    error_message = f"Failed to delete record. API response: {response_data}"
                    print(error_message)
                    return error_message
            except ValueError:
                # If the response is not JSON, return the text content
                print(f"Non-JSON response: {response.text}")
                if response.status_code == 200:
                    return "Record deleted successfully"
                else:
                    return f"Failed to delete record. Status code: {response.status_code}"
                
        except requests.exceptions.ConnectionError as e:
            error_message = f"Connection error when trying to delete record: {str(e)}"
            print(error_message)
            return error_message
        except Exception as e:
            error_message = f"Error deleting employee record: {str(e)}"
            print(error_message)
            return error_message
    
    # If none of the methods match (shouldn't happen with proper routing)
    return "Invalid request method", 405



##### MAIN ##########

if __name__ == '__main__':
    app.run()