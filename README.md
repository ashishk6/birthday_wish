# Birthday Wish


### Design and code a simple "Hello World" application that exposes the following HTTP-based APIs:
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

- Runing the application without the databse.
- Runnnig the application with RDBMS postgres databse.

Note: Attaching the architecture diagram with AWS.
