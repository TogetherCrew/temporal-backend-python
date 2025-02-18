import os
import unittest
from unittest.mock import AsyncMock, patch

from temporalio.client import Client

from tc_temporal_backend.client import TemporalClient


# A fake client object for testing purposes.
class FakeClient:
    pass


# A fake asynchronous connect function to simulate Temporal connection.
async def fake_connect(url, api_key):
    # Optionally, verify the parameters (url and api_key) here.
    return FakeClient()


class TestTemporalClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure that environment variables are removed before each test.
        os.environ.pop("TEMPORAL_HOST", None)
        os.environ.pop("TEMPORAL_API_KEY", None)
        os.environ.pop("TEMPORAL_PORT", None)

    def tearDown(self):
        # Clean up the environment variables after each test.
        os.environ.pop("TEMPORAL_HOST", None)
        os.environ.pop("TEMPORAL_API_KEY", None)
        os.environ.pop("TEMPORAL_PORT", None)

    def test_load_credentials_success(self):
        os.environ["TEMPORAL_HOST"] = "localhost"
        os.environ["TEMPORAL_API_KEY"] = "secret"
        os.environ["TEMPORAL_PORT"] = "7233"

        client_obj = TemporalClient()
        creds = client_obj._load_credentials()

        self.assertEqual(
            creds, {"host": "localhost", "api_key": "secret", "port": "7233"}
        )

    def test_load_credentials_missing_host(self):
        # Omit TEMPORAL_HOST.
        os.environ.pop("TEMPORAL_HOST", None)
        os.environ["TEMPORAL_API_KEY"] = "secret"
        os.environ["TEMPORAL_PORT"] = "7233"

        client_obj = TemporalClient()
        with self.assertRaises(ValueError) as cm:
            client_obj._load_credentials()

        self.assertIn("`TEMPORAL_HOST` is not configured", str(cm.exception))

    def test_load_credentials_missing_port(self):
        os.environ["TEMPORAL_HOST"] = "localhost"
        os.environ["TEMPORAL_API_KEY"] = "secret"
        os.environ.pop("TEMPORAL_PORT", None)

        client_obj = TemporalClient()
        with self.assertRaises(ValueError) as cm:
            client_obj._load_credentials()

        self.assertIn("`TEMPORAL_PORT` is not configured", str(cm.exception))

    def test_load_credentials_missing_api_key(self):
        os.environ["TEMPORAL_HOST"] = "localhost"
        os.environ.pop("TEMPORAL_API_KEY", None)
        os.environ["TEMPORAL_PORT"] = "7233"

        client_obj = TemporalClient()
        with self.assertRaises(ValueError) as cm:
            client_obj._load_credentials()

        self.assertIn("`TEMPORAL_API_KEY` is not configured", str(cm.exception))

    async def test_get_client(self):
        os.environ["TEMPORAL_HOST"] = "localhost"
        os.environ["TEMPORAL_API_KEY"] = "secret"
        os.environ["TEMPORAL_PORT"] = "7233"

        # Patch Client.connect with our fake_connect function.
        with patch.object(Client, "connect", new=AsyncMock(side_effect=fake_connect)):
            temporal_client = TemporalClient()
            client_instance = await temporal_client.get_client()

            # Verify that the client returned is an instance of FakeClient.
            self.assertIsInstance(client_instance, FakeClient)
