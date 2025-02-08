from web3 import Web3
import json
import os

# Connect to the local Ethereum node (Ganache)
infura_url = "HTTP://127.0.0.1:7545"  # Update with your Ganache RPC server
web3 = Web3(Web3.HTTPProvider(infura_url))

# Ensure connection is successful
if web3.is_connected():
    print("✅ Connected to Ethereum blockchain")
else:
    print("❌ Failed to connect to Ethereum blockchain")

# Load the compiled contract
contract_path = os.path.join(os.path.dirname(__file__), "../smart_contracts/Voting_compiled.json")

with open(contract_path, "r") as file:
    contract_json = json.load(file)

contract_abi = contract_json["contracts"]["Voting.sol"]["Voting"]["abi"]
contract_address = "0x299696493310947cA129ba473D845e27cf625055"  # Replace with actual deployed contract address

# Initialize contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Dummy account details (Replace with actual values)
ADMIN_ACCOUNT = "0xYourAccountAddress"
PRIVATE_KEY = "YourPrivateKey"

# Function to add a candidate
def add_candidate(candidate_name):
    txn = contract.functions.addCandidate(candidate_name).build_transaction({
        "from": ADMIN_ACCOUNT,
        "nonce": web3.eth.get_transaction_count(ADMIN_ACCOUNT),
        "gas": 3000000,
        "gasPrice": web3.to_wei("5", "gwei")
    })

    signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)

# Function to vote for a candidate
def vote(candidate_id, voter_address, private_key):
    txn = contract.functions.vote(candidate_id).build_transaction({
        "from": voter_address,
        "nonce": web3.eth.get_transaction_count(voter_address),
        "gas": 3000000,
        "gasPrice": web3.to_wei("5", "gwei")
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)

# Function to get all candidates
def get_candidates():
    return contract.functions.getCandidates().call()
