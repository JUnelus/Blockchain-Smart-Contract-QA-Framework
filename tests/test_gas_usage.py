import json
from pathlib import Path

import pytest

from tests.conftest import make_order_id, send_tx

REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
GAS_REPORT_FILE = REPORTS_DIR / "gas_report.json"


@pytest.mark.gas
def test_gas_usage_for_core_escrow_transactions(w3, accounts, escrow_contract):
    REPORTS_DIR.mkdir(exist_ok=True)
    gas_report = {}

    deposit_order_id = make_order_id(w3, "ORDER-GAS-DEPOSIT")
    release_order_id = make_order_id(w3, "ORDER-GAS-RELEASE")
    refund_order_id = make_order_id(w3, "ORDER-GAS-REFUND")
    deposit_amount = w3.to_wei(0.1, "ether")

    deposit_tx = escrow_contract.functions.deposit(deposit_order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    deposit_receipt = send_tx(w3, deposit_tx)
    gas_report["deposit_gas_used"] = deposit_receipt.gasUsed

    release_deposit_tx = escrow_contract.functions.deposit(
        release_order_id, accounts["seller"]
    ).transact({"from": accounts["buyer"], "value": deposit_amount})
    send_tx(w3, release_deposit_tx)

    release_tx = escrow_contract.functions.approveRelease(release_order_id).transact(
        {"from": accounts["buyer"]}
    )
    release_receipt = send_tx(w3, release_tx)
    gas_report["release_gas_used"] = release_receipt.gasUsed

    refund_deposit_tx = escrow_contract.functions.deposit(
        refund_order_id, accounts["seller"]
    ).transact({"from": accounts["buyer"], "value": deposit_amount})
    send_tx(w3, refund_deposit_tx)

    refund_tx = escrow_contract.functions.refund(refund_order_id).transact(
        {"from": accounts["buyer"]}
    )
    refund_receipt = send_tx(w3, refund_tx)
    gas_report["refund_gas_used"] = refund_receipt.gasUsed

    with open(GAS_REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(gas_report, file, indent=2)

    assert gas_report["deposit_gas_used"] > 0
    assert gas_report["release_gas_used"] > 0
    assert gas_report["refund_gas_used"] > 0

