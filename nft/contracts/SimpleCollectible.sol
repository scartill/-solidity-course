// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SimpleCollectible is ERC721URIStorage  {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 private _lastTokenId;

    constructor() ERC721("Doggie", "DOG") {
    }

    function createCollectible(string memory tokenURI) public returns(uint256) {
        uint256 newTokenId = _tokenIds.current();
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        _lastTokenId = newTokenId;
        _tokenIds.increment();
        return newTokenId;
    }
    
    function getLastTokenID() public view returns(uint256) {
        return _lastTokenId;
    }
}
