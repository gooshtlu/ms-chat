# Flack Messaging Application

Flack is a messaging application (inspired by Slack) which enables users to send one-to-one messages and participate in group messaging.The application supports different user roles and permissions, including admin, manager, writer, and reader.


## Features

1.Register a new user account or log in with existing credentials.

![login page.png](..%2F..%2FPictures%2Flogin%20page.png)

2.Use the search functionality to find other existing users and initiate one-to-one conversations (Send and receive messages in real-time).

![user-message.png](..%2F..%2FPictures%2Fuser-message.png)

3.Create or join groups to engage in group messaging.

![Screenshot (6).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%286%29.png)

4.Role-based access control

![Screenshot (7).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%287%29.png)

5.Depending on the user role:

![Screenshot (8).png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%288%29.png)

| Role      | Permissions                                                                 |
| ----------- |-----------------------------------------------------------------------------|
| Admin      | Can add or remove all other roles and also edit messages                    |
| Manager   | Can add or remove users from Writer or Reader roles, Can also edit messages |
| Writer   | Can add new messages. **No edit permissions**                               |
| Reader   | Can read messages. **No write and edit permissions**                        |


## Technologies Used

1.Python
2.FastAPI framework
3.CouchDB Database
4.Postman for API testing

## Frontend: 
- HTML, CSS, and JavaScript
- Angular framework 
- https://github.com/gooshtlu/ms-chat-front-end










