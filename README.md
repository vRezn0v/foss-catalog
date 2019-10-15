# Catalog App
A catalog app built with Flask for Udacity FSND program. Covering Authentication and Authorization and CRUD Operations courses.

## Requirements:
- Python 2.7
- Vagrant (Running the [Udacity FullStack Nanodegree VM](https://github.com/udacity/fullstack-nanodegree-vm))
- git

## Python Dependencies:
- Flask
- SQLAlchemy
- Httplib2
- Requests
- OAuth2Client

## Basic Setup:
- Clone the repository: </br>
``` $ git clone https://github.com/vrezn0v/foss-catalog catalog```
- Install the python dependencies (not required in FSND VM): </br> 
``` $ pip install -r requirements.txt```
- Initialize the database by running: </br>
``` $ python2 database_setup.py```
- Load Default Categories and Items by executing ```categorydbinit.py``` and ```dbpopulate.py```:</br>
``` $ python2 categorydbinit.py```</br>
``` $ python2 dbpopulate.py```</br>
- Finally, run the Catalog App with, </br>
``` $ python2 catalog.py```
- Open your preferred browser and go to http://localhost:5000

### Notes:
The ```client_secrets.json``` file is preloaded, in case the client is revoked, obtain new Google Oauth API Keys from https://console.cloud.google.com/apis/credentials/oauthclient. </br>
Download the client secrets and rename the file to ```client_secrets.json``` and place it in the repository root.

## JSON API Endpoints
```http://localhost:5000/json/index``` : Shows all the categories. </br>
```http://localhost:5000/json/<int:category_id>``` : Shows items(apps) contained in a specific category. </br>
```http://localhost:5000/json/<int:category_id>/<int:item_id>``` : Shows details for the specified item. </br>
