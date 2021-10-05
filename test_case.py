import requests

def test_get_check_status_code_equals_200():
     response = requests.get("http://localhost:5000/hello/ashish")
     assert response.status_code == 200

def test_get_check_content_type_equals_json():
     response = requests.get("http://localhost:5000/hello/ashish")
     assert response.headers["Content-Type"] == "application/json"

def test_get_check_hello_in_response():
     response = requests.get("http://localhost:5000/hello/ashish")
     response_body = response.json()
     assert 'Hello' in str(response_body["message"])
     assert 'ashish' in str(response_body["message"])

