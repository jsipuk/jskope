#!/usr/bin/env python3
# =============================================================================
# SYNTHETIC TEST DATA - NETSKOPE DLP DEMONSTRATION
# Internal billing reconciliation worker (excerpt)
#
# This is fabricated sample SOURCE CODE used to trigger the "Source Code" and
# "Credentials" DLP profiles. Every key, token, connection string and hostname
# below is non-functional and based on published example formats only. It
# exists solely to demonstrate inline DLP inspection of source code in motion.
# =============================================================================

import os
import logging

import boto3
import psycopg2
import requests

logger = logging.getLogger("billing.reconciliation")

# -----------------------------------------------------------------------------
# Hardcoded credentials (the anti-pattern DLP is meant to catch in source code)
# -----------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "eu-west-2"

GITHUB_TOKEN = "ghp_16C7e42F292c6912E7710c838347Ae5B21"
STRIPE_SECRET_KEY = "SK_SYNTHETIC_4eC39HqLyjWDarjtT1zdp7dc"

# Internal infrastructure - private hostnames that must not leave the network
DB_DSN = "postgresql://billing_svc:S3cr3t-Pa55!@pg-prod-01.internal.corp-example.com:5432/billing"
REDIS_URL = "redis://:R3disP%40ss@cache-01.internal.corp-example.com:6379/2"
INTERNAL_API_BASE = "https://payments-api.internal.corp-example.com/v3"

SIGNING_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0Z3VS5JJcds3xHn/ygWep4PAtEsHAsMGPzVgfBGYqnJQSFnQ
KJmfqN9j59ZVnqU+0QSXMV7cRk2P4Xc1JQpxKL5X3lk9jPvHvAExAmPLEkEyOnly
-----END RSA PRIVATE KEY-----"""


class BillingReconciler:
    """Reconciles Stripe settlements against the internal ledger."""

    def __init__(self):
        self._s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        self._db = psycopg2.connect(DB_DSN)

    def fetch_settlements(self, batch_id):
        """Pull a settlement batch from the internal payments API."""
        resp = requests.get(
            "{base}/settlements/{batch}".format(base=INTERNAL_API_BASE, batch=batch_id),
            headers={"Authorization": "Bearer " + STRIPE_SECRET_KEY},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["records"]

    def reconcile(self, batch_id):
        cur = self._db.cursor()
        for row in self.fetch_settlements(batch_id):
            cur.execute(
                "UPDATE ledger SET status = %s WHERE txn_ref = %s",
                ("RECONCILED", row["txn_ref"]),
            )
        self._db.commit()
        logger.info("Reconciled batch %s", batch_id)


if __name__ == "__main__":
    BillingReconciler().reconcile(os.environ.get("BATCH_ID", "batch-000"))
