# Real-time chat application with Django Channels
This project is a single-page realtime chat application with the following features:

- A friends list that display each friend's last message and a timestamp. 
- The friends list updates its order according to the last message received.
- Receiving a message from a non-friend will automatically add that friend to the list.
- Receiving a message will trigger a notification (background color change).
- Clicking on a friend opens a chat window.
- The chat window displays the message history between users.
- The chat window displays speech bubbles with timestamp, the style depending on who sent the message.

## Distinctivines and Complexity
To allow real-time communication between users my project utilizes Django Channels. In this course so far we have used Django to handle HTTP requests but this application is continuously listening for incoming messages and changes its content accordingly. Django Channels extends Django to be able to handle communication with WebSockets.

With the Channels tutorial (https://channels.readthedocs.io/en/stable/tutorial/index.html)I was able to create a rudimentary chat program that allows users to enter a chat room by redirecting them to the same URL. Since the concepts WebSocket, ASGI, consumers, etcetera were completely new to me I found this to be a fairly complex task in itself.

However, I wanted a single-page application that allows users to receive messages from anybody, even other users not befriended. To accomplish this I had to let every user *listen* to their own 'room' upon login. Every message is sent to the sender's 'room' and the receiver's 'room'. Information within the message is then used to determine if and where the message needs to be displayed.

Because both the friends list and chat window need to be updated without redirecting the user, I couldn't rely solely on Django templates. The bulk of the front-end needed to be build by javascript code. As a result this project's javascript code has become the most extensive and complex I have written so far, with multiple uses of the fetch API.

## How to run
1. Register a new user or login an existing user.
2. 'user1' through 'user4' are created already, all without password, plus an admin 'super' (password 'super').
3. Optionally add new friends.
4. Open chat by clicking a friend's name.
5. Enter messages at the bottom of the screen.

## Files
**views.py:**
Functions to register new users, login, add friends and retrieve a friend list and message histories from the database.

**urls.py:**
 URL patterns for above mentioned functions.

 **models.py:**
 - Default Django User model with additional fields for a profile picture and friend list.
 - Message model to store information about sent messages such as the content, sender, receiver and timestamp of the message.

**routing.py:**
URL route for the websocket connection.

**consumers.py:**
A Django Channels WebsocketConsumer class to handle all WebSocket logic.
This includes adding a user to a 'room', disconnecting the user, sending and receiving messages.
This is also where all messages are sent to the database.

**chat.css**
All css code for the project.

**chat.js**
All javascript code. Functions to build the friend list, chat window with message history, open a websocket, send messages, listen for messages.

**templates**
Layout.html that loads css and js files, login.html and register.html pages, lobby.html for the chat application. 