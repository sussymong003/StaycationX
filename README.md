# [Staycation API branch]

- Added controllers/api.py and models/token.py
- requirements.txt `flask-httpauth` and `Flask-CORS` (which is to allow cross original calls form ReactJS)

## Containerization

- Added Dockerfile to run the flask app under Gunicorn as a container

## Merged test branch into api branch

### Updated .vscode/launch.json and .vscode/settings.json

- Added testing environment variables into the files

### Updated Dockerfile

- Added MongoDB support for Ubuntu 20.04
- Updated gunicorn settings
	- Added worker connections

### Updated requirements.txt

- `pytest`
- `selenium`
- `gunicorn`
- `locust`

### Added Makefile, geckodriver, nginx-ex2.conf, nginx-ex3.conf

### Added tests related files

- tests/conftest.py
- tests/functional/test_function.py
- tests/selenium/test_booking.py
- tests/stress/locustfile.py
- tests/unit/test_models.py

## Updated api.py (Question 2a)

### Added new API functions for booking:

- create_booking
- manage_booking
- update_booking
- delete_booking

## Updated testcases (Question 2b)

### Added tests/functional/test_function.py

- Added new unit test for the 4 apis created previously
	- test_create_booking_with_api
	- test_manage_booking_with_api
	- test_update_booking_with_api
	- test_delete_booking_with_api

### tests/unit/test_models.py

- Added dependancies
	- Package class
	- Book class
	- Datetime date
- Added new class test_new_user_methods and the following methods to test the Booking model
	- test_create_booking
	- test_manage_booking
	- test_update_booking
	- test_delete_booking
