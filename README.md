# Chat
A distributed system for connecting multiple chat clients via a server

# Getting Started Locally
To start running our project locally, first create a Python virtual environment in the root directory by running ```python -m venv venv```. Then activate the venv by running the OS appropriate script as noted in this article: https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/#

Once the venv is active, download the project requirements by running ```pip3 install -r requirements.txt```.

Next, make sure Tkinter is downloaded. Tkinter may not download via pip3, so it may be necessary to install it separately using a tool like Homebrew. On Mac, make sure you have homebrew downloaded and run ```brew install python-tk``` to download Tkinter if necessary.

Also in the root directory, create a .env file, which is where we store sensitive configuration details. You will need the following configuration variables:
```
SERVER_HOST = "{SERVER HOST HERE}"
SERVER_PORT = {SERVER PORT HERE}
CLIENT_HOST = "{CLIENT HOST HERE}"
```
The server host and port should be the host and port that the server is accessible from. The client host should be the host name of the machine that the client is running on.

Once the above configuration steps are complete, you should be able to run the project! To run the server, cd into the server folder and run ```driver.py```. To run the client, cd into the client folder and run ```ui.py```.

# Using the GUI
Upon running ```driver.py``` and ```ui.py```, the GUI will then pop up with an initial login/signup page where the user can input a username or password and then click either login or signup. Once logged in, a new "starting" screen will pop up with a main text box, and buttons corresponding to actions the user can do. 

Upon clicking the send message button, the user will be taken to a new screen and there they can enter a target username they want to receive their message, and then the message they would like to send. The user can then hit send to send the message, or they can press the back button taking them back to the starting screen.

When clicking the list users button, the user will be taken to a screen where they can input a username pattern and press a button to list the users matching the pattern, and then those users are displayed in the text box. The user can press the back button to return to the starting screen. 

When clicking the read messages button, the user is taken to a screen where they can input how many messages they want to read from their unread messages. The messages are then displayed to the user. The user can also press the back button to return to the previous screen.

Clicking the delete message button will take the user to a screen which displays all messages that user has sent which have not been read by the receiver yet. The user is then prompted to enter the message_id of the message they want to delete. They can then hit delete to delete the specified message, or press back at any time to return to the starting screen. 

The logout and delete account button upon being clicked will close the GUI and accordingly log the user out or delete the user’s account. 

# Additional Documentation
Additional documentation for this project can be found here: https://docs.google.com/document/d/1uMzqMKuS-AzIjxa3oqSrnPpCBMKhggZXnIDdfU5Fjbw/edit?tab=t.0

# Running Tests
To run our test suite, cd into the tests folder and run ```pytest``` in the terminal.
