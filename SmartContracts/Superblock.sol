pragma solidity ^0.4.0;
contract Superblock {
// The 'dict' of addresses that are approved to submit SBs
    mapping (address => bool) approvedSender;
    string SB;

    // The event to announce a SB on the blockchain
    event SuperblockSubmission(address _sender, string _superblock);
// This is a constructor function, so its name has to match the contract
    function Superblock() public {
    }

    // The 'payable'  and it will be called whenever ether is sent to the contract address.
    function() public payable{
        // Contains information about the transaction
        if (msg.value > 20000000000000000) {
            //if the value sent greater than 0.02 ether (in Wei)
            // then add the sender's address to approvedSender list and now the can submit SBs
            approvedSender[msg.sender] =  true;
        }
    }


    // The read-only function that checks whether a specified address is approved to post SBs.
    function isApproved(address _sender) public view returns (bool approved) {
        return approvedSender[_sender];
    }

    // Read-only function that returns the current SB
    function getSuperblock() public view returns(string) {
        return SB;
    }
//The function that submit the SB to the blockchain
    function sendSuperblock(string _superblock) public returns (bool success) {
        // Check if the sender is verified
        if (approvedSender[msg.sender]) {

            SB = _superblock;
            emit SuperblockSubmission(msg.sender, SB);
            return true;

        } else {
            return false;
        }

    }
}
