import json
from pathlib import Path
import uuid

import pytest
from web3 import Web3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_FILE = PROJECT_ROOT / "deployments" / "local.json"
# Unique per pytest process; keeps order IDs from colliding across repeated runs.
RUN_NAMESPACE = uuid.uuid4().hex


@pytest.fixture(scope="session")
def w3():
    provider_uri = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(provider_uri))
    assert web3.is_connected(), f"Unable to connect to blockchain node at {provider_uri}"
    return web3


@pytest.fixture(scope="session")
def accounts(w3):
    available_accounts = w3.eth.accounts
    assert len(available_accounts) >= 3, "Expected at least 3 unlocked local blockchain accounts"
    return {
        "buyer": available_accounts[0],
        "seller": available_accounts[1],
        "attacker": available_accounts[2],
    }


@pytest.fixture(scope="session")
def escrow_contract(w3):
    assert DEPLOYMENT_FILE.exists(), "Deployment file not found. Run: npm run deploy:local"

    with open(DEPLOYMENT_FILE, "r", encoding="utf-8") as file:
        deployment = json.load(file)

    return w3.eth.contract(address=deployment["address"], abi=deployment["abi"])


def make_order_id(w3, label: str):
    return w3.keccak(text=f"{RUN_NAMESPACE}:{label}")


def send_tx(w3, tx_hash):
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    assert receipt.status == 1, f"Transaction failed: {tx_hash.hex()}"
    return receipt
