// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "contracts/test/VRFCoordinatorV2Mock.sol";

contract MockLinkToken is LinkTokenInterface {
  function allowance(address owner, address spender) external view returns (uint256 remaining) {
    return 0;
  }

  function approve(address spender, uint256 value) external returns (bool success) {
    return true;
  }

  function balanceOf(address owner) external view returns (uint256 balance) {
    return 1;
  }

  function decimals() external view returns (uint8 decimalPlaces) {
    return 18;
  }

  function decreaseApproval(address spender, uint256 addedValue) external returns (bool success) {
    return true;
  }

  function increaseApproval(address spender, uint256 subtractedValue) external {
    // pass
  }

  function name() external view returns (string memory tokenName) {
    return "LINK";
  }

  function symbol() external view returns (string memory tokenSymbol) {
    return "LINK";
  }

  function totalSupply() external view returns (uint256 totalTokensIssued) {
    return 10 ** 18;
  }

  function transfer(address to, uint256 value) external returns (bool success) {
    return true;
  }

  function transferAndCall(
    address to,
    uint256 value,
    bytes calldata data
  ) external returns (bool success) {
    uint64 subId = abi.decode(data, (uint64));
    VRFCoordinatorV2Mock coordinator = VRFCoordinatorV2Mock(to);
    coordinator.fundSubscription(subId, uint96(value));
  }

  function transferFrom(
    address from,
    address to,
    uint256 value
  ) external returns (bool success) {
    return true;
  }
}
