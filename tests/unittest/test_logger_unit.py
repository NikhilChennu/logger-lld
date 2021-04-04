import unittest
from logger.logger import Logger
import asyncio
from unittest  import mock

class TestLogger(unittest.TestCase):

    def test_happy_case_start(self):
        logger_client=Logger()
        asyncio.run(logger_client.start(1,1))
        self.assertEqual(len(logger_client._Logger__process_lookup.keys()),1)
        self.assertEqual(len(logger_client._Logger__heap), 1)

    def test_happy_case_end(self):
        logger_client = Logger()
        tasks=[logger_client.start(1, 1),logger_client.start(2, 2),logger_client.end(1),logger_client.poll()]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))
        self.assertEqual(len(logger_client._Logger__process_lookup.keys()), 1)
        self.assertEqual(len(logger_client._Logger__heap), 1)
    def test_happy_case_poll(self):
        logger_client = Logger()
        tasks = [logger_client.start(1, 1), logger_client.start(2, 2), logger_client.end(1), logger_client.poll()]
        loop = asyncio.get_event_loop()
        result=loop.run_until_complete(asyncio.gather(*tasks))
        self.assertEqual(result[3], 1)
