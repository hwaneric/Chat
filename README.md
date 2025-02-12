# Chat
A distributed system for connecting multiple chat clients via a server

# Getting Started Locally
To begin running the project locally:

In the project root directory, create a virtual environment by running ```python3 -m venv .venv```
Next, activate the virtual environment by running ```source venv/bin/activate``` on Mac or ```venv\Scripts\activate``` on Windows.
Once you have activated the virtual environment, run ```pip install -r requirements.txt``` to install project dependencies. 
For the final step of setup, add a file titled ```.env``` in the root directory of the project. Populate this file with 2 variables:
```
  HOST = "127.0.0.1"
  PORT = 54400
```
These variables should correspond to the address of the server.


Once the above setup steps are complete, the server can be run by traversing to the "server" folder and calling:
```
python3 driver.py
```

To run the client, traverse to the "client" folder and call:
```
python3 client_script.py
```

