// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is Ownable, VRFConsumerBaseV2 {
    address[] internal _players;
    uint256 internal _entryFeeUsd;
    AggregatorV3Interface internal _ethUsbPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE internal _lottery_state;

    VRFCoordinatorV2Interface internal _coordinator;
    uint64 internal _subscription_id;
    bytes32 internal _keyhash;
    uint32 internal _num_words =  2;
    uint32 internal _callback_gas_limit;
    uint256 internal _request_id;
    uint16 internal _request_confirmations = 3;

    constructor(
        address priceFeedAddress, 
        address vrfCoordinator,
        uint64 subscriptionId,
        bytes32 keyhash,
        uint32 callback_gas_limit
    ) VRFConsumerBaseV2(vrfCoordinator)  {
        _entryFeeUsd = 50 * (10**18);
        _ethUsbPriceFeed = AggregatorV3Interface(priceFeedAddress);
        _lottery_state = LOTTERY_STATE.CLOSED;

        _coordinator = VRFCoordinatorV2Interface(vrfCoordinator);
        _subscription_id = subscriptionId;
        _keyhash = keyhash;
        _callback_gas_limit = callback_gas_limit;
    }

    function getLotteryState() public view returns(uint256) {
        return uint256(_lottery_state);
    }

    function enter() public payable {
        require(_lottery_state == LOTTERY_STATE.OPEN);
        uint256 fee = getEntranceFee();
        require(msg.value >= fee, "Not enough ETH");
        _players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {
        (,int256 price,,,) = _ethUsbPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10;
        uint256 costToEnter = (_entryFeeUsd * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() onlyOwner public {
        require(_lottery_state == LOTTERY_STATE.CLOSED, "Cannot start, already started");
        _lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() onlyOwner public {
        require(_lottery_state == LOTTERY_STATE.OPEN, "Cannot close, not started");
        _lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        
        _request_id = _coordinator.requestRandomWords(
            _keyhash,
            _subscription_id,
            _request_confirmations,
            _callback_gas_limit,
            _num_words
        );
    }

    function fulfillRandomWords(uint256, uint256[] memory randomWords) internal override {

    }
}