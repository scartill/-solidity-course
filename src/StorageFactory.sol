// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "./SimpleStorage.sol";

contract StorageFactory {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorage() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint256 _ssIndex, uint256 _ssNumber) public {
        SimpleStorage ss = SimpleStorage(simpleStorageArray[_ssIndex]);
        ss.store(_ssNumber);
    }

    function sfGet(uint256 _ssIndex) public view returns(uint256) {
        SimpleStorage ss = SimpleStorage(simpleStorageArray[_ssIndex]);
        return ss.fetch();
    }
}
