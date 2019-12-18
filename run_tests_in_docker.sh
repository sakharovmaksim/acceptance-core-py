#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Please, set config file! Example: sh run_tests_in_docker.sh prod_pytest.ini"
    exit 1
fi

pwd=`pwd`

TAG="sakharovmaksim/acceptance-tests-base-image-python:latest"
echo "Локальный запуск api-тестов, используя docker-image $TAG"

CONTAINER_NAME="my_local_acceptance_tests_run"

# Устанавливаем обработчик сигнала, чтобы контейнер удалился, даже если скрипт завершают досрочно
trap 'docker rm -f $CONTAINER_NAME' 2 15

docker pull $TAG

docker run -di --net=host --name=$CONTAINER_NAME -v $pwd:/local_project $TAG

# Копируем код тестов из --volume папки в папку с предустановленным vendor, чтобы не требовать vendor на хосте
docker exec $CONTAINER_NAME rsync -a /local_project/. /acceptance-tests-core-dir/ --exclude output --exclude tmp --exclude .git

# Запуск тестов из папки, в которой предустановлен Python с дополнениями. Установлена опция --html формирования HTML-отчета (можно выключить)
docker exec $CONTAINER_NAME pipenv run pytest /acceptance-tests-core-dir/ -s --html=/acceptance-tests-core-dir/output/report.html --self-contained-html \
    -c /acceptance-tests-core-dir/$1

# Копируем репорты от тестов обратно в --volume-папку local_project
docker exec $CONTAINER_NAME rsync -a /acceptance-tests-core-dir/output/ /local_project/output/

echo "Останавливается и удаляется docker-контейнер $CONTAINER_NAME"
docker rm -f $CONTAINER_NAME