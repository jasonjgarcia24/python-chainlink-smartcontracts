//SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint;

    address public owner;
    uint private ethDecimals = 18;
    mapping(address => uint) public addressToAmountFunded;
    address[] public funders;

    constructor () public {
        owner = msg.sender;
    }

    function fund() public payable {
        uint minimumUSD = 50 * 10**ethDecimals;
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH.");

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }    

    function getDecimals() public view returns (uint) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        return priceFeed.decimals();
    }

    function getDescription() public view returns (string memory) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        return priceFeed.description();
    }

    function getVersion() public view returns (uint) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        return priceFeed.version();
    }

    function getPrice() public view returns (uint) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        (,int256 answer,,,) = priceFeed.latestRoundData();

        return uint(answer) * 10**(ethDecimals-getDecimals());
    }

    // What is the ETH -> USD conversion rate
    function getConversionRate(uint ethAmount) public view returns (uint) {
        uint ethPrice = getPrice();
        uint ethAmountInUsd = (ethPrice * ethAmount);
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);

        for (uint funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
}