# Chat
A distributed system for connecting multiple chat clients via a server

# Getting Started Locally
To begin running the project locally:

In the project root directory, create a virtual environment by running ```python3 -m venv .venv```
Next, activate the virtual environment by running ```source venv/bin/activate``` on Mac or ```venv\Scripts\activate``` on Windows.
Once you have activated the virtual environment, run ```pip install -r requirements.txt``` to install project dependencies. 
Finally, add a file titled ```.env``` in the root directory of the project. Populate this file with 2 variables:
```
  HOST = "127.0.0.1"
  PORT = 54400
```


