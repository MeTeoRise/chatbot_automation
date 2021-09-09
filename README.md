# Chatbot Automation Tool

## About The Project

### Built With

* [Django](https://www.djangoproject.com/)
* [Rasa](https://rasa.com/)

## Getting Started
### Prerequisites

First you need to install the Python3 in order to run the app.
You can find a great guide [here](https://realpython.com/installing-python/).


### Installation
1. Clone the repo
   ```sh
   https://github.com/MeTeoRise/chatbot_automation.git
   ```
2. Install the requirements
   ```sh
   pip3 install -r requirements.txt
   ```
3. Then you have to setup the database on the settings.py file of Django.
4. Migrate to the database
   ```sh 
   python3 manage.py migrate
   ```
5. After these we can run the django server:
   ```bash
   python3 manage.py runserver
   ```
   (Optional) Create an administrator user:
   ```bash
   python3 manage.py createsuperuser
   ```