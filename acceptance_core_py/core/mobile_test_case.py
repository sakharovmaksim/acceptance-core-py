from acceptance_core_py.core import driver
from acceptance_core_py.core.test_case import TestCase


class MobileTestCase(TestCase):
    def setUp(self):
        driver.mobile_mode = True
        driver.initialize()
