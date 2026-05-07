// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title TokenEscrow
/// @notice Simple ETH escrow contract used for blockchain QA automation testing.
contract TokenEscrow {
    enum EscrowState {
        None,
        Funded,
        Released,
        Refunded
    }

    struct Escrow {
        address buyer;
        address payable seller;
        uint256 amount;
        EscrowState state;
    }

    mapping(bytes32 => Escrow) private escrows;

    event EscrowCreated(
        bytes32 indexed orderId,
        address indexed buyer,
        address indexed seller,
        uint256 amount
    );

    event EscrowReleased(
        bytes32 indexed orderId,
        address indexed seller,
        uint256 amount
    );

    event EscrowRefunded(
        bytes32 indexed orderId,
        address indexed buyer,
        uint256 amount
    );

    function deposit(bytes32 orderId, address payable seller) external payable {
        require(orderId != bytes32(0), "Invalid order ID");
        require(seller != address(0), "Invalid seller");
        require(seller != msg.sender, "Buyer cannot be seller");
        require(msg.value > 0, "Deposit amount must be greater than zero");
        require(escrows[orderId].state == EscrowState.None, "Escrow already exists");

        escrows[orderId] = Escrow({
            buyer: msg.sender,
            seller: seller,
            amount: msg.value,
            state: EscrowState.Funded
        });

        emit EscrowCreated(orderId, msg.sender, seller, msg.value);
    }

    function approveRelease(bytes32 orderId) external {
        Escrow storage escrow = escrows[orderId];

        require(escrow.state == EscrowState.Funded, "Escrow is not funded");
        require(msg.sender == escrow.buyer, "Only buyer can release funds");

        uint256 amount = escrow.amount;
        address payable seller = escrow.seller;

        // Effects before interaction to reduce reentrancy risk.
        escrow.state = EscrowState.Released;
        escrow.amount = 0;

        (bool success, ) = seller.call{value: amount}("");
        require(success, "Transfer to seller failed");

        emit EscrowReleased(orderId, seller, amount);
    }

    function refund(bytes32 orderId) external {
        Escrow storage escrow = escrows[orderId];

        require(escrow.state == EscrowState.Funded, "Escrow is not funded");
        require(msg.sender == escrow.buyer, "Only buyer can refund");

        uint256 amount = escrow.amount;
        address buyer = escrow.buyer;

        // Effects before interaction to reduce reentrancy risk.
        escrow.state = EscrowState.Refunded;
        escrow.amount = 0;

        (bool success, ) = payable(buyer).call{value: amount}("");
        require(success, "Refund failed");

        emit EscrowRefunded(orderId, buyer, amount);
    }

    function getEscrow(bytes32 orderId)
        external
        view
        returns (
            address buyer,
            address seller,
            uint256 amount,
            EscrowState state
        )
    {
        Escrow memory escrow = escrows[orderId];
        return (escrow.buyer, escrow.seller, escrow.amount, escrow.state);
    }
}

