// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    mapping(string => uint256) nameToFavoriteNumber;
    uint256 _number;

    function store(uint256 number) public returns(uint256) {
        _number = number;
        return number;
    }

    function fetch() public view returns(uint256) {
        return _number;
    }

    function retrieve(string memory name) public view returns (uint256) {
        return nameToFavoriteNumber[name];
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
