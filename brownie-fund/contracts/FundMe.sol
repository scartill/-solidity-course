// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address _owner;
    mapping(address => uint256) _a2a;
    address[] public _funders;
    AggregatorV3Interface _priceFeed;

    constructor(address priceFeedAddr) {
        _owner = msg.sender;
        _priceFeed = AggregatorV3Interface(priceFeedAddr);
    }

    function owner() public view returns(address) {
        return _owner;
    }

    function fund() public payable {
        uint256 minimumUSB = 0.05 * 10 ** 18;

        require(getConversionRate(msg.value) >= minimumUSB, "You need to spend more ETH");

        _a2a[msg.sender] += msg.value;
        _funders.push(msg.sender);
    } 

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 0.05 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    function getFund(address addr) public view returns(uint256) {
        return _a2a[addr];
    }

    function getVersion() public view returns(uint256) {
        return _priceFeed.version();
    }

    function getPrice() public view returns(uint256){
        (,int256 answer,,,) = _priceFeed.latestRoundData();
         // ETH/USD rate in 18 digit 
         return uint256(answer * 10000000000);
    }
    
    // 1000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == _owner, "You are not the owner");
        _;
    }

    function withdraw() payable onlyOwner public {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 inx = 0; inx < _funders.length; inx++) {
            address addr = _funders[inx];
            _a2a[addr] = 0;
        }

        _funders = new address[](0);
    }
}
