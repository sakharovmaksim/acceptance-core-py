# Acceptance Core For Selenium. Powered by Python
=================================================
## Requirements
Python 3.8+

## Install
### Install virtualenv
`pip install virtualenv`

### Create virtualenv dir
`virtualenv venv`

### Run virtualenv
`source venv/bin/activate`

### Install requirements
`pip install -r requirements.txt`

### Run your tests with Docker in easy way
`sh run_tests_in_docker.sh stage_pytest.ini`

### Run your tests with local Python
`pytest -c stage_pytest.ini -s` – with config `stage_pytest.ini` and show `print` logs 