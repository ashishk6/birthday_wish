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
> Note: We have used the storage as temporary space. However, we can use any database to persist the data to run stateless application as more than one replica that can serve the data from database query.

### 2. Produce a system diagram of your solution deployed to either AWS or GCP (it's not required to support both cloud platforms).
- AWS
  + We can prepare the target group under which we can launch minimum 2 ec2 instances for high avaibility.
  + We will set a application load balancer on top of target group to balance the load.
  + The ec2 instances will have only one inbound security group of port 5000 to accept the service call.
  + We should to keep proper health check to test the liveness of the application.
  + Logging the application via cloud watch, EFK, etc.
  + We can configure prometheus and grafana based monitoring service to check the load on the application.
> Similar way we can do to in other cloud like Azure, GCP, IBM , etc.
- Kubernetes:
  + We can prepare docker container for the same application and run it on the Kubernetes and similar platform such as Openshift, EKS, AKS, Etc.
  + We can write deployment manifest file such as deplyment, replica, service, configmap, secrets, etc.
  + We should to keep proper health check to test the liveness of the application.
  + Logging the application via EFK, etc.
  + We can configure prometheus and grafana based monitoring service to check the load on the application.

### 3. Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.
- Make sure the application is running with more than 1 instance across more than one avability zone.
- AMI of the instance should be up todate so that the target group can scale up and scale down with the AMI.
- Instance should have good sizing in terms of cpu and memory based on performance test.
- Instance should be monitored and alerted on high cpu and memory utilization via cloud watch through SNS(Simple Notification Service).
- We should to keep proper health check to test the liveness of the application else should be alerted.
- We can configure prometheus and grafana based monitoring service to check the load on the application.


> Note: I have writted few test cases to test the application
