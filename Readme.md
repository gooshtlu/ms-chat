# Flack Messaging Application

Flack is a messaging application (inspired by Slack) which enables users to send one-to-one messages and participate in group messaging.The application supports different user roles and permissions, including admin, manager, writer, and reader.


## Features

1.Register a new user account or log in with existing credentials.

![login page](https://github.com/gooshtlu/ms-chat/assets/104629208/0ca532ef-c19a-4c6a-9c78-483e4b801a28)

2.Use the search functionality to find other existing users and initiate one-to-one conversations (Send and receive messages in real-time).

![user-message](https://github.com/gooshtlu/ms-chat/assets/104629208/8443a2b0-4ca2-47dd-987c-de89489b3b0e)

3.Create or join groups to engage in group messaging.

![Screenshot (6)](https://github.com/gooshtlu/ms-chat/assets/104629208/504d4abf-1632-4d02-b19b-b4963328a4f9)

4.Role-based access control

![Screenshot (7)](https://github.com/gooshtlu/ms-chat/assets/104629208/984e5302-269f-4703-bb23-b6882cf174dd)

5.Depending on the user role:

![Screenshot (8)](https://github.com/gooshtlu/ms-chat/assets/104629208/66d6134e-718c-4c8c-8a3c-b1a745dd8128)


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










