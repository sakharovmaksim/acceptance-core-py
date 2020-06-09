# Acceptance Tests framework sample. Powered by Python and Selenium.
=================================================
## Requirements
Python 3.8+

## Install for MacOS
### Install Python 3
https://www.python.org/downloads/

### Install pip if needed
https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py

### Install pipenv
https://pypi.org/project/pipenv/  

With brew: `brew install pipenv`

### Set your Selenoid server
Look for config pytest.ini and set your Selenoid server to GGR_PLAYBACK_HOST

### Run your tests with Docker in easy way
`sh run_tests_in_docker.sh pytest.ini`

### Run your tests with local Python
`pipenv run pytest -c pytest.ini` – with config `pytest.ini`

### Run your tests with parallel mode
Change in *.ini-file `addopts = -nX` option for desired count of parallel tests

![Sample of parallel tests execution](images/parallel_tests.png)

## Docker
Create docker image from Dockerfile https://github.com/sakharovmaksim/acceptance-tests-base-docker-image-python or pull from https://hub.docker.com/repository/docker/sakharovmaksim/acceptance-tests-base-image-python

## HTML report output
Add "--html=\`pwd\`/output/report.html --self-contained-html" to pytest-command to generate HTML-report in .../output/ directory
Default for docker-script

![Sample of HTML-report](images/report_new.png)

## Run with custom ONE thread and without reruns on failed tests. Hint: Use for development tests
`pipenv run pytest -c pytest.ini -n0 --reruns 0`

## Run one specific test
`pipenv run pytest tests/test_sample_ui.py -k 'test_simple_example_1' -c pytest.ini`

## Run one specific file with tests
`pipenv run pytest tests/test_sample_ui.py -c pytest.ini`

## Config count of rerunning failed tests
`-max-runs=X` in pytest.ini file

## Mobile emulation
For setting up mobile emulation use MobileTestCase for this tests