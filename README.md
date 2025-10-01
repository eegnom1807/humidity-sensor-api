# humidity_sensor_api

## Clone the repository
https://github.com/eegnom1807/humidity-sensor-api.git

## Create virtual env
- python3 -m venv venv

## Install dependencies: 
- pip install -r requirements.txt

## Create migrations:
- flask --app run.py db init     # just one time
- flask --app run.py db migrate -m "create sensor table"
- flask --app run.py db upgrade
