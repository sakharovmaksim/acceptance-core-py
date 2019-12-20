# Acceptance Core For Selenium. Powered by Python
=================================================
## Requirements
Python 3.8+

## Install
### Install pipenv
`brew install pipenv`

### Install dependencies
`pipenv install`

### Run your tests with Docker in easy way
`sh run_tests_in_docker.sh stage_pytest.ini`

### Run your tests with local Python
`pipenv run pytest -c stage_pytest.ini -s` – with config `stage_pytest.ini` and show `print` logs 

### Run your tests with parallel mode
Change in *.ini-file `addopts = -nX` option for desired count of parallel tests

![Sample of parallel tests execution](images/parallel_tests.png)

## Docker
Create docker image from Dockerfile https://github.com/sakharovmaksim/acceptance-tests-base-docker-image-python or pull from https://hub.docker.com/repository/docker/sakharovmaksim/acceptance-tests-base-image-python

## HTML report output
Add "--html=\`pwd\`/output/report.html --self-contained-html" to pytest-command to generate HTML-report in .../output/ directory
Default for docker-script

