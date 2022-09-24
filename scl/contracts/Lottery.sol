// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is Ownable, VRFConsumerBaseV2 {
    address[] internal _players;
    address internal _recent_winner;

    uint256 internal _entryFeeUsd;
    AggregatorV3Interface internal _ethUsbPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE internal _lottery_state;

    LinkTokenInterface LINKTOKEN;

    VRFCoordinatorV2Interface internal COORDINATOR;
    uint64 internal _subscriptionId;
    bytes32 internal _keyhash;
    uint32 internal _num_words = 1;
    uint32 internal _callback_gas_limit;
    uint256 internal _request_id;
    uint16 internal _request_confirmations = 3;
    
    event SubscriptionCreated(uint64 subscriptionId);
    event RequestedRandomness(uint256 requestId);
    event TokensReturned(uint256 residual);

    constructor(
        address priceFeedAddress, 
        address linkTokenAddress,
        address vrfCoordinatorAddress,
        bytes32 keyhash,
        uint32 callbackGasLimit
    ) VRFConsumerBaseV2(vrfCoordinatorAddress)  {
        _entryFeeUsd = 0.5 * (10**18);
        _ethUsbPriceFeed = AggregatorV3Interface(priceFeedAddress);
        _lottery_state = LOTTERY_STATE.CLOSED;
        
        LINKTOKEN = LinkTokenInterface(linkTokenAddress);

        COORDINATOR = VRFCoordinatorV2Interface(vrfCoordinatorAddress);
        _keyhash = keyhash;
        _callback_gas_limit = callbackGasLimit;

        _recent_winner = 0x00000000000000000000000000000000DeaDBeef;
    }

    function getPlayer(uint216 index) public view returns(address) {
        require(index >= 0);
        require(index < _players.length);
        return _players[index];
    }

    function recentWinner() public view returns(address) {
        return _recent_winner;
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

    function topUpSubscription(uint256 amount) external onlyOwner {
        LINKTOKEN.transferAndCall(address(COORDINATOR), amount, abi.encode(_subscriptionId));
    }

    function endLottery() onlyOwner public {
        require(_lottery_state == LOTTERY_STATE.OPEN, "Cannot close, not started");
        _lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        
        _request_id = COORDINATOR.requestRandomWords(
            _keyhash,
            _subscriptionId,
            _request_confirmations,
            _callback_gas_limit,
            _num_words
        );

        emit RequestedRandomness(_request_id);
    }

    function fulfillRandomWords(uint256, uint256[] memory randomWords) internal override {
        require(_lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't there yet");
        require(randomWords.length > 0, "No randomness found");
        uint256 winner_inx = randomWords[0] % _players.length;
        _recent_winner = _players[winner_inx];
        payable(_recent_winner).transfer(address(this).balance);
        _players = new address[](0);
        _lottery_state = LOTTERY_STATE.CLOSED;
    }

    function cancelSubscription(address receivingWallet) external onlyOwner {
        COORDINATOR.cancelSubscription(_subscriptionId, receivingWallet);
        _subscriptionId = 0;
    }

    function withdraw(address to) external onlyOwner {
        uint256 link_balance = LINKTOKEN.balanceOf(address(this));
        LINKTOKEN.transfer(to, link_balance);

        emit TokensReturned(link_balance);
    }

    function createNewSubscription() public onlyOwner {
        _subscriptionId = COORDINATOR.createSubscription();
        COORDINATOR.addConsumer(_subscriptionId, address(this));

        emit SubscriptionCreated(_subscriptionId);
    }
}
