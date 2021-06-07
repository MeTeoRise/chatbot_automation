# chatbot_automation

[Use MySQL with Django](https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database)

## Getting Started

First install the requirements:
```bash
pip3 install -r requirements.txt
````
Then migrate the database:
```bash
python3 manage.py migrate
```
After these we can run the django server:
```bash
python3 manage.py runserver
```
Finally create an administrator user:
```bash
python3 manage.py createsuperuser
```