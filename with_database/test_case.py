import requests
import json
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

# Generate random username
username=get_random_string(6)
port="5000"
headers = {"content-type": "application/json" }
url=f"http://localhost:{port}/hello/{username}"
payload={"dateOfBirth": "2001-1-04" }

# Pre insert verification
def test_get_pre_check_status_code_equals_200():
     response = requests.get(url)
     assert response.status_code == 200

def test_get_pre_check_content_type_equals_json():
     response = requests.get(url)
     assert response.headers["Content-Type"] == "application/json"

def test_get_pre_check_hello_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert 'does not exists' in str(response_body["message"])

def test_get_pre_check_username_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert username in str(response_body["message"])

# Inserting the new records
def test_insert_new_user():

     response = requests.put(url, data=json.dumps(payload), headers=headers)
     assert response.status_code == 204

# Post insert verification
def test_get_check_status_code_equals_200():
     response = requests.get(url)
     assert response.status_code == 200

def test_get_check_content_type_equals_json():
     response = requests.get(url)
     assert response.headers["Content-Type"] == "application/json"

def test_get_check_hello_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert 'Hello' in str(response_body["message"])

def test_get_check_username_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert username in str(response_body["message"])

# Updating the existing records
def test_update_existing_user():

     response = requests.put(url, data=json.dumps(payload), headers=headers)
     assert response.status_code == 204

# Post update verification
def test_get_after_update_check_status_code_equals_200():
     response = requests.get(url)
     assert response.status_code == 200

def test_get_after_update_check_content_type_equals_json():
     response = requests.get(url)
     assert response.headers["Content-Type"] == "application/json"

def test_get_after_update_check_hello_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert 'Hello' in str(response_body["message"])

def test_get_after_update_check_username_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert username in str(response_body["message"])

# Deleting the username from database
def test_delete_existing_user():

     response = requests.put(url, data=json.dumps(payload), headers=headers)
     response=requests.delete(url)
     assert response.status_code == 200

# Post delete verification
def test_get_post_delete_check_status_code_equals_200():
     response = requests.get(url)
     assert response.status_code == 200

def test_get_post_delete_check_content_type_equals_json():
     response = requests.get(url)
     assert response.headers["Content-Type"] == "application/json"

def test_get_post_delete_check_hello_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert 'does not exists' in str(response_body["message"])

def test_get_post_delete_check_username_in_response():
     response = requests.get(url)
     response_body = response.json()
     assert username in str(response_body["message"])
