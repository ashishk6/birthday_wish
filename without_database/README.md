# Birthday Wish


### 1. Design and code a simple "Hello World" application that exposes the following HTTP-based APIs:
```
Description: Request: Response:
Saves/updates the given user’s name and date of birth in the database.
PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” } 204 No Content

Note:
<username> must contain only letters. YYYY-MM-DD must be a date before the today date.

Description: Returns hello birthday message for the given user Request: Get /hello/<username>
Response: 200 OK

Response Examples:
A. If username’s birthday is in N days:
{ 
“message”: “Hello, <username>! Your birthday is in N day(s)”
}

B. If username’s birthday is today:
{ 
“message”: “Hello, <username>! Happy birthday!” 
}
```
> Note: We have used the storage as temporary space as a prototype.

### 2. Produce a system diagram of your solution deployed to either AWS or GCP (it's not required to support both cloud platforms).
- AWS
  + We can prepare the target group under which we can launch minimum 2 ec2 instances for high avaibility.
  + We will set a application load balancer on top of target group to balance the load.
  + The ec2 instances will have only one inbound security group of port 5000 to accept the service call.
  + We should to keep proper health check to test the liveness of the application.
  + Logging the application via cloud watch, EFK, etc.
  + We can configure prometheus and grafana based monitoring service to check the load on the application.
> Attached the Architecture diagram w.r.t AWS. However, we can have similar way to do it in other cloud like Azure, GCP, IBM , etc.
- Kubernetes:
  + We can prepare docker container for the same application and run it on the Kubernetes and similar platform such as Openshift, EKS, AKS, Etc.
  + We can write deployment manifest file such as deplyment, replica, service, configmap, secrets, etc.
  + We should to keep proper health check to test the liveness of the application.
  + Logging the application via EFK, etc.
  + We can configure prometheus and grafana based monitoring service to check the load on the application.

### 3. Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.
- Make sure the application is running with more than 1 instance across more than one avability zone with proper configureg Auto Scaling group and Target group.
- Instance should have good sizing in terms of cpu and memory based on performance test.
- Instance should be monitored and alerted on high cpu and memory utilization via cloud watch through SNS(Simple Notification Service).
- We should to keep proper health check to test the liveness of the application else should be alerted.
- We can configure prometheus and grafana based monitoring service to check the load on the application.


> Note: I have writted good test cases to test the application


### Steps to execute locally
```
pip install -r requirements.txt
python birthday.py
```
- This will run the application in port 5000
```
2021-10-05 21:07:08,290 - birthday - INFO -  Users: [{'userName': 'ashish', 'dateOfBirth': '2021-10-4'}, {'userName': 'ashish0', 'dateOfBirth': '2021-10-3'}, {'userName': 'ashish1', 'dateOfBirth': '2021-10-10'}]
2021-10-05 21:07:08,296 - birthday - INFO - Next birth: 2022-10-04 00:00:00
2021-10-05 21:07:08,296 - birthday - INFO - days left for next birthday: 364
2021-10-05 21:07:08,297 - birthday - INFO - Today: 2021-10-05 00:00:00
172.17.0.1 - - [05/Oct/2021 21:07:08] "GET /hello/ashish HTTP/1.1" 200 -
2021-10-05 21:07:08,309 - birthday - INFO -  Users: [{'userName': 'ashish', 'dateOfBirth': '2021-10-4'}, {'userName': 'ashish0', 'dateOfBirth': '2021-10-3'}, {'userName': 'ashish1', 'dateOfBirth': '2021-10-10'}]
2021-10-05 21:07:08,310 - birthday - INFO - Next birth: 2022-10-04 00:00:00
2021-10-05 21:07:08,310 - birthday - INFO - days left for next birthday: 364
2021-10-05 21:07:08,310 - birthday - INFO - Today: 2021-10-05 00:00:00
172.17.0.1 - - [05/Oct/2021 21:07:08] "GET /hello/ashish HTTP/1.1" 200 -
2021-10-05 21:07:08,318 - birthday - INFO -  Users: [{'userName': 'ashish', 'dateOfBirth': '2021-10-4'}, {'userName': 'ashish0', 'dateOfBirth': '2021-10-3'}, {'userName': 'ashish1', 'dateOfBirth': '2021-10-10'}]
2021-10-05 21:07:08,319 - birthday - INFO - Next birth: 2022-10-04 00:00:00
2021-10-05 21:07:08,319 - birthday - INFO - days left for next birthday: 364
2021-10-05 21:07:08,319 - birthday - INFO - Today: 2021-10-05 00:00:00
172.17.0.1 - - [05/Oct/2021 21:07:08] "GET /hello/ashish HTTP/1.1" 200 -
```

- To test the application:
```
(base) ashishkumar@Ashishs-MBP birthday_wish_bkp % pytest test_case.py -v
============================================ test session starts ============================================
platform darwin -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/ashishkumar/opt/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/ashishkumar/Documents/python/revoult/birthday_wish_bkp
collected 19 items                                                                                          

test_case.py::test_get_pre_check_status_code_equals_200 PASSED                                        [  5%]
test_case.py::test_get_pre_check_content_type_equals_json PASSED                                      [ 10%]
test_case.py::test_get_pre_check_hello_in_response PASSED                                             [ 15%]
test_case.py::test_get_pre_check_username_in_response PASSED                                          [ 21%]
test_case.py::test_insert_new_user PASSED                                                             [ 26%]
test_case.py::test_get_check_status_code_equals_200 PASSED                                            [ 31%]
test_case.py::test_get_check_content_type_equals_json PASSED                                          [ 36%]
test_case.py::test_get_check_hello_in_response PASSED                                                 [ 42%]
test_case.py::test_get_check_username_in_response PASSED                                              [ 47%]
test_case.py::test_update_existing_user PASSED                                                        [ 52%]
test_case.py::test_get_after_update_check_status_code_equals_200 PASSED                               [ 57%]
test_case.py::test_get_after_update_check_content_type_equals_json PASSED                             [ 63%]
test_case.py::test_get_after_update_check_hello_in_response PASSED                                    [ 68%]
test_case.py::test_get_after_update_check_username_in_response PASSED                                 [ 73%]
test_case.py::test_delete_existing_user PASSED                                                        [ 78%]
test_case.py::test_get_post_delete_check_status_code_equals_200 PASSED                                [ 84%]
test_case.py::test_get_post_delete_check_content_type_equals_json PASSED                              [ 89%]
test_case.py::test_get_post_delete_check_hello_in_response PASSED                                     [ 94%]
test_case.py::test_get_post_delete_check_username_in_response PASSED                                  [100%]

============================================ 19 passed in 0.24s =============================================
```

### Steps to execute as a container for kubernetes

```
docker build -t birthday .
docker run  --rm -p 5000:5000 birthday
```
- We can run this on any container platform such as Kubernetes, Openshift, EKS, AKS, etc.
