import pytest

from tests.conftest import make_order_id, send_tx


@pytest.mark.negative
@pytest.mark.security
def test_attacker_cannot_release_buyer_escrow(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-SECURITY-1001")
    deposit_amount = w3.to_wei(1, "ether")

    deposit_tx = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    send_tx(w3, deposit_tx)

    with pytest.raises(Exception) as error:
        escrow_contract.functions.approveRelease(order_id).transact(
            {"from": accounts["attacker"]}
        )

    assert "Only buyer can release funds" in str(error.value)


@pytest.mark.negative
@pytest.mark.security
def test_attacker_cannot_refund_buyer_escrow(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-SECURITY-1002")
    deposit_amount = w3.to_wei(1, "ether")

    deposit_tx = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    send_tx(w3, deposit_tx)

    with pytest.raises(Exception) as error:
        escrow_contract.functions.refund(order_id).transact({"from": accounts["attacker"]})

    assert "Only buyer can refund" in str(error.value)


@pytest.mark.negative
def test_cannot_deposit_zero_amount(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-NEGATIVE-1001")

    with pytest.raises(Exception) as error:
        escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
            {"from": accounts["buyer"], "value": 0}
        )

    assert "Deposit amount must be greater than zero" in str(error.value)


@pytest.mark.negative
def test_cannot_reuse_existing_order_id(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-NEGATIVE-1002")
    deposit_amount = w3.to_wei(0.1, "ether")

    first_deposit_tx = escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
        {"from": accounts["buyer"], "value": deposit_amount}
    )
    send_tx(w3, first_deposit_tx)

    with pytest.raises(Exception) as error:
        escrow_contract.functions.deposit(order_id, accounts["seller"]).transact(
            {"from": accounts["buyer"], "value": deposit_amount}
        )

    assert "Escrow already exists" in str(error.value)


@pytest.mark.negative
def test_buyer_cannot_be_seller(w3, accounts, escrow_contract):
    order_id = make_order_id(w3, "ORDER-NEGATIVE-1003")
    deposit_amount = w3.to_wei(0.1, "ether")

    with pytest.raises(Exception) as error:
        escrow_contract.functions.deposit(order_id, accounts["buyer"]).transact(
            {"from": accounts["buyer"], "value": deposit_amount}
        )

    assert "Buyer cannot be seller" in str(error.value)

