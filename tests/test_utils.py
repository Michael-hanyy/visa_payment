# tests/test_utils.py

import os
import django
from django.test import TestCase
from unittest.mock import patch

# 1️⃣ Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visa_payment.settings")
django.setup()  # must come before importing models or utils

# 2️⃣ Import your code now
from visa_payment.utils import generate_transaction_id, calculate_discount

class UtilsTests(TestCase):

    def test_generate_transaction_id_format(self):
        tx_id = generate_transaction_id()
        self.assertTrue(tx_id.startswith("TXN_"))
        self.assertEqual(len(tx_id), 40)  # TXN_ + 36 chars UUID

    def test_calculate_discount(self):
        self.assertEqual(calculate_discount(100, 10), 90)
        self.assertEqual(calculate_discount(200, 50), 100)
        self.assertEqual(calculate_discount(100, 0), 100)

    @patch("visa_payment.utils.uuid.uuid4")
    def test_generate_transaction_id_mocked(self, mock_uuid):
        mock_uuid.return_value = "1234-5678"
        tx_id = generate_transaction_id()
        self.assertEqual(tx_id, "TXN_1234-5678")
