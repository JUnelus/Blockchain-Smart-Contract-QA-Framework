import pytest

from tests.conftest import make_order_id, send_tx


@pytest.mark.functional
def test_buyer_can_deposit_funds_to_escrow(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-1001")
    deposit_amount = w3.to_wei(1, "ether")

    tx_hash = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    receipt = send_tx(w3, tx_hash)

    escrow = escrow_contract.functions.getEscrow(order_id).call()
    assert escrow[0] == accounts["buyer"]
    assert escrow[1] == accounts["seller"]
    assert escrow[2] == deposit_amount
    assert escrow[3] == 1

    events = escrow_contract.events.EscrowCreated().process_receipt(receipt)
    assert len(events) == 1
    assert events[0]["args"]["buyer"] == accounts["buyer"]
    assert events[0]["args"]["seller"] == accounts["seller"]
    assert events[0]["args"]["amount"] == deposit_amount


@pytest.mark.functional
def test_buyer_can_release_funds_to_seller(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-1002")
    deposit_amount = w3.to_wei(0.5, "ether")

    deposit_tx = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    send_tx(w3, deposit_tx)

    seller_balance_before = w3.eth.get_balance(accounts["seller"])
    release_tx = escrow_contract.functions.approveRelease(order_id).transact(
        {"from": accounts["buyer"]}
    )
    release_receipt = send_tx(w3, release_tx)
    seller_balance_after = w3.eth.get_balance(accounts["seller"])

    escrow = escrow_contract.functions.getEscrow(order_id).call()
    assert escrow[2] == 0
    assert escrow[3] == 2
    assert seller_balance_after > seller_balance_before

    events = escrow_contract.events.EscrowReleased().process_receipt(release_receipt)
    assert len(events) == 1
    assert events[0]["args"]["seller"] == accounts["seller"]
    assert events[0]["args"]["amount"] == deposit_amount


@pytest.mark.functional
def test_buyer_can_refund_escrow(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-1003")
    deposit_amount = w3.to_wei(0.25, "ether")

    deposit_tx = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    send_tx(w3, deposit_tx)

    refund_tx = escrow_contract.functions.refund(order_id).transact({"from": accounts["buyer"]})
    refund_receipt = send_tx(w3, refund_tx)

    escrow = escrow_contract.functions.getEscrow(order_id).call()
    assert escrow[2] == 0
    assert escrow[3] == 3

    events = escrow_contract.events.EscrowRefunded().process_receipt(refund_receipt)
    assert len(events) == 1
    assert events[0]["args"]["buyer"] == accounts["buyer"]
    assert events[0]["args"]["amount"] == deposit_amount

