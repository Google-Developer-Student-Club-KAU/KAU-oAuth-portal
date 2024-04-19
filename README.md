# King Abdulaziz University's portal SSO OAuth2 via Google & Azure Flask Boilerplate [POC]

This project serves as a proof of concept (POC) for integrating King Abdulaziz University's (KAU) portal with OAuth2hrough Google and Azure as Identity Providers (IdPs), implemented using Flask framework.<br>
The goal of this project is to demonstrate how to securely authenticate King Abdulaziz University's users using their Google or Azure accounts.

## Features
- **OAuth2 Authentication**: Implements OAuth2 framework to authorize access to the KAU portal using Google and Azure accounts.
- **Flask Boilerplate**: Provides a basic Flask application structure that can be easily extended and customized.
- **Security Guidelines**: Ensures that the entire authentication flow adheres to industry-standard security protocols.
- **User-Friendly**: Simplifies the login process for users via their existing Google or Azure accounts.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.9 or later
- Google Developer Account for the sign-in with google route
- Azure Developer Account for the sign-in with microsoft route

### Installation
1. Clone this repository to your local machine or to a github codespace.
2. Install the required Python packages.
3. Set up your environment variables in a .env file including your Google and Azure credentials. see [.env.example](.env.example) file for an example.

## Configuration

### Google Setup
Navigate to the Google Developer Console and create a new project. Then navigate to __APIs & Services__ > __Credentials__, create new OAuth2.0 credentials, download the client secret JSON file, and note the client ID and client secret. 
<br><br>
Make sure to add a __redirect URI__ to your server URL callback route. For running locally, the redirect URI will be `http://localhost/api/auth/google/callback`. <br><br>
Finally, go to the __OAuth consent screen__ and complete the required fields.


### Azure Setup
Setup an Azure account with your University's email address. Then in the Azure Portal, navigate to __Microsoft Entra ID__ > __App registrations__. Create a new app, follow the same steps as the Google setup to create the client ID and secret from the __Certificate & secrets__ tab, and save your client ID and client secret. <br> FInally, go to the __API permissions__ tab and add the required permissions. For this demo, we will need to add the following permissions: `email`, `openid`, `profile`, `User.Read`, `offline_access`. <br>
Make sure you add a __redirect URI__ from the __Authentication__ tab. For running locally, the redirect URI will be `http://localhost/api/auth/azure/callback`.

### App Structure
The project structure is as follows:
```
/project
|-- /auth/
|   |-- /providers/
|   |   |-- google.py
|   |   |-- azure.py
|   |-- __init__.py
|   |-- login.py

|-- /src/
|   |-- __init__.py
|   |-- base.py
|   |-- user.py

|-- /templates/

|-- app.py
|-- .env
|-- requirements.txt
|-- README.md
|-- LICENSE
|-- .gitignore
```
- `auth` directory contains the authentication logic, including the Google and Azure providers. 
- `src` directory contains the main application logic, database and configuration.


### Environment Variables
Rename the `.env.example` file to `.env` and add your Google and Azure credentials to the file.

## License
This project is licensed under the MIT License.


## Connect with me
Feel free to connect with me on my social platforms:
- [LinkedIn](https://www.linkedin.com/in/amjed-alqasemi/)
- [Github](https://github.com/aqasemi)