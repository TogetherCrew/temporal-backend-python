import os
import unittest

from tc_temporal_backend.client import TemporalClient
from temporalio.client import Client


class TestTemporalClientIntegration(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Check if the required environment variables are set.
        required_vars = ["TEMPORAL_HOST", "TEMPORAL_API_KEY", "TEMPORAL_PORT"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise unittest.SkipTest(
                "Skipping integration tests because these environment variables are missing: "
                + ", ".join(missing_vars)
            )

    async def test_get_client_integration(self):
        """
        This integration test will attempt to connect to the Temporal server
        using the actual environment configuration. The test assumes that a
        Temporal server is available at the specified host and port.
        """
        temporal_client = TemporalClient()
        client_instance = await temporal_client.get_client()

        # Check that the returned object is an instance of temporalio.client.Client.
        self.assertIsInstance(client_instance, Client)

        await client_instance.close()
