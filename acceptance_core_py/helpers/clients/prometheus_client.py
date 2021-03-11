import logging

from prometheus_client import CollectorRegistry
from prometheus_client import delete_from_gateway
from prometheus_client import Info
from prometheus_client import push_to_gateway

from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.utils import date_utils


class PrometheusClient:
    """Attention: Singleton object, use by PrometheusClient.get_instance().push_test_failed_metric_to_gateway()"""

    __instance = None
    __gateway_url = "YOUR_GATEWAY_HOST_PORT"

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            logging.debug("Creating PrometheusClient instance")
            cls.__instance = PrometheusClient()
        return cls.__instance

    def push_test_failed_metric_to_gateway(self) -> bool:
        """Prometheus request like 'count by (test_locator) (acceptance_tests_failures)'"""
        test_locator = (
            env.get_test_file_name().replace("/", ".") + "." + env.get_test_name()
        )
        logging.info(f"Sending test metrics about fail to Prometheus. {test_locator=}")

        registry = CollectorRegistry()
        date = date_utils.generate_date(format_date="%Y-%m-%d-%H-%M-%S")
        i = Info(
            name="acceptance_tests_failures",
            documentation="Acceptance tests failures",
            labelnames=["tests", "test_locator"],
            registry=registry,
        )

        i.labels(True, test_locator).info({"status": "failed", "date": date})
        try:
            push_to_gateway(
                gateway=self.__gateway_url,
                job=test_locator + "_" + date,
                registry=registry,
            )
        except Exception as exception:
            logging.error(
                f"Error in sending test metrics to Prometheus: {str(exception)}"
            )
            return False
        logging.info("Successfully sending test metrics to Prometheus")
        return True
