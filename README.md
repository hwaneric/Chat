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

Once the above configuration steps are complete, you should be able to run the project! To run the server, cd into the server folder and run ```driver.py```. To run the client, cd into the client folder and run ```ui.py```.

# Switching Between JSON Mode and Custom Wire Protocol
To switch between JSON mode and our custom wire protocol, find the helpers.py file in the "helpers" folder. Set the "JSON_MODE" variable to True for JSON mode and False for our custom wire protocol.

# Additional Documentation
Additional documentation for this project can be found here: https://docs.google.com/document/d/1uMzqMKuS-AzIjxa3oqSrnPpCBMKhggZXnIDdfU5Fjbw/edit?tab=t.0

# Running Tests
To run our test suite, cd into the tests folder and run ```pytest``` in the terminal.
