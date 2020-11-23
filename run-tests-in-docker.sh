#!/bin/bash

die () {
	echo >&2 "$@"
	exit 1
}

for i in "$@"
do
	case $i in
		--tests-dir=*) TESTS_DIR="${i#*=}" ;;
		--config=*) CONFIG="${i#*=}" ;;
	esac
	shift
done

if [[ -z "$TESTS_DIR" ]]; then
	echo "Warning! '--tests-dir' argument not defined. Set default 'tests' dir"
	TESTS_DIR="tests"
fi

if [ -z "$CONFIG" ]; then
    die "Error! '--config' argument must be defined"
fi

pwd=`pwd`

TAG="sakharovmaksim/acceptance-tests-base-image-python:latest"
echo "Running tests, using docker-image ${TAG}"

CONTAINER_NAME="my_local_acceptance_tests_run"

# Устанавливаем обработчик сигнала, чтобы контейнер удалился, даже если скрипт завершают досрочно
trap 'docker rm -f $CONTAINER_NAME' 2 15

docker pull $TAG

docker run -di --net=host --name=$CONTAINER_NAME -v "$pwd":/acceptance-tests-core-dir $TAG

# Запуск тестов из папки, в которой предустановлены модули Python. Установлена опция --html формирования HTML-отчета (можно выключить)
docker exec $CONTAINER_NAME pipenv run pytest /acceptance-tests-core-dir/$TESTS_DIR \
      --html=/acceptance-tests-core-dir/output/report.html --self-contained-html \
      -c /acceptance-tests-core-dir/$TESTS_DIR/$CONFIG

echo "Stop and delete docker-container '${CONTAINER_NAME}'"
docker rm -f $CONTAINER_NAME