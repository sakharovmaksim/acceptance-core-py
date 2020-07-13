#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Please, set config file! Example: sh run_tests_in_docker.sh pytest.ini"
    exit 1
fi

pwd=`pwd`

TAG="sakharovmaksim/acceptance-tests-base-image-python:latest"
echo "Локальный запуск ui-тестов, используя docker-image $TAG"

CONTAINER_NAME="my_local_acceptance_tests_run"

# Устанавливаем обработчик сигнала, чтобы контейнер удалился, даже если скрипт завершают досрочно
trap 'docker rm -f $CONTAINER_NAME' 2 15

docker pull $TAG

docker run -di --net=host --name=$CONTAINER_NAME -v $pwd:/acceptance-tests-core-dir $TAG

# Запуск тестов из папки, в которой предустановлены модули Python. Установлена опция --html формирования HTML-отчета (можно выключить)
docker exec $CONTAINER_NAME pipenv run pytest /acceptance-tests-core-dir/tests --html=/acceptance-tests-core-dir/output/report.html --self-contained-html \
    -c /acceptance-tests-core-dir/tests/$1

echo "Останавливается и удаляется docker-контейнер $CONTAINER_NAME"
docker rm -f $CONTAINER_NAME