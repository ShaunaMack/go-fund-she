# go-fund-she

### To setup locally

make sure you have python and pip installed

activate virtual environment `source venv/bin/activate`

install dependencies `pip install -r requirements.txt`

`cd animalgogo`

make migrations `python manage.py makemigrations`
run migrations `python manage.py migrate`

create a superuser `python manage.py createsuperuser`

deactivate virtual server `deactivate`

### To run locally

activate virtual environment `source venv/bin/activate`

`cd animalgogo`

run server `python manage.py runserver`

deactivate virtual server `deactivate`

### Deployment info

App was deployed to Heroku but is no longer working
https://fast-peak-84673.herokuapp.com/

admin site can be accessed by superuser https://fast-peak-84673.herokuapp.com/admin

Endpoints:
![image](https://user-images.githubusercontent.com/17566798/134753792-ee134ffb-4b5a-4452-aef6-18d75acfdcba.png)
