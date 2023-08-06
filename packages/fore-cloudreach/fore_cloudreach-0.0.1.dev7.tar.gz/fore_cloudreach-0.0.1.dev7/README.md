# FORE stand for `Fin Ops REporter`

## Autentication and authorization Overview
This package will be published on PyPi as downloadable package.
The main purpose of it is to Oauth2 authenticate a user of the Jupiter Notebook (**JpN**) that will need access to Google Sheets application. The security context is the current macOS user who use the Jupiter notebook and is logged in with Google's account.
In order to ustilize the Google's Sheets API the JpN code would need to:
</br>

- enable Google Sheet API in the GCP project where the application is registered.
- install the package `fore` from PyPi;
- recieve a file `credentials.json` from her line manager and copy it to `~/crgoauth` folder. This file contains the JpN application's credentials. The security context for the credentials is `https://www.googleapis.com/auth/spreadsheets`;
- Logging in the Cloudreach's google account and in the prompted window authorized the JpN application to access the Google Sheets API.
</br>

As of the initial version, the authentication of the user is performed over the Google's SignIn of the currently logged user in the Google account in the browser.
The authentication token is stored in a subfolder `crgoauth` in the current user's folder on the local machine (macOS tested). For every authentication attempt the token will be taken from the file from that location only.

In order to work with Google's Sheets API, a credentials file is required as well as outcome of registering this library as desktop application in Google Cloud.
The `credentials` file is always sought in the subfolder `crgoauth` of the current user's folder on the local machine. 

TODO [dev]: to implemnt posibility to store the token and application credentials into Secret MAnager.   


### HowTos
