# Social Networking API

This project implements a social networking API using Django Rest Framework. It allows users to sign up, log in, search for other users, send friend requests, and manage their social connections.

## Features

- User registration and login
- Email-based user search
- Friend request management
- JWT-based authentication

## Technologies

- Django & Django Rest Framework
- Simple JWT for token-based authentication
- Django Ratelimit for request rate limiting

## Setup

Clone the repository and install the dependencies:
git clone https://github.com/yourusername/social-networking-api.git
cd social-networking-api
pip install -r requirements.txt
Run migrations:
python manage.py migrate
Start the server:
python manage.py runserver


API Endpoints
1. User Signup
URL: /signup/
Method: POST
Body:
json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
Response:
Status: 201 Created
Body:
json
 
{
  "email": "user@example.com",
  "username": "username"
}


2. User Login
URL: /login/
Method: POST
Body:
json
 
{
  "email": "user@example.com",
  "password": "password123"
}
Response:
Status: 200 OK
Body:
JSON
 
{
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}

3. Search Users
URL: /search/?q=keyword
Method: GET
Required: JWT Access token
Response:
Status: 200 OK or 404 Not Found

4. Send Friend Request
URL: /friends/send/
Method: POST
Body:
json
 
{
  "receiver_id": 2
}
Required: JWT Access token
Response:
Status: 201 Created or 400 Bad Request

5. Accept Friend Request
URL: /friends/accept/{friend_request_id}/
Method: POST
Required: JWT Access token
Response:
Status: 200 OK or 404 Not Found

6. Reject Friend Request
URL: /friends/reject/{friend_request_id}/
Method: POST
Required: JWT Access token
Response:
Status: 200 OK or 404 Not Found

7. List Friends
URL: /friends/list/
Method: GET
Required: JWT Access token
Response:
Status: 200 OK

8. List Pending Friend Requests
URL: /friends/pending/
Method: GET
Required: JWT Access token
Response:
Status: 200 OK

Authentication
This API uses JWT (JSON Web Tokens) to secure endpoints. Users must log in to receive access and refresh tokens.
 To access protected endpoints, the access token must be included in the Authorization header as Bearer {token}.

Rate Limiting
The endpoint for sending friend requests is rate-limited to prevent abuse, allowing only 3 requests per minute per user.

Contributing
Please feel free to fix the repository and submit pull requests.

License
MIT License
This README.md provides a comprehensive guide for setting up and using the social networking API, including detailed information about each API endpoint and usage examples.
Adjust the repository link and other specifics based on your actual project details.
