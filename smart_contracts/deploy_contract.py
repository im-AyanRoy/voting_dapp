from web3 import Web3
import json

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if web3.is_connected():
    print("✅ Connected to Ganache!")
else:
    print("❌ Failed to connect to Ganache!")

# Load compiled contract
with open("Voting_compiled.json", "r") as file:
    compiled_contract = json.load(file)

# Extract ABI and Bytecode
contract_abi = compiled_contract["contracts"]["Voting.sol"]["Voting"]["abi"]
contract_bytecode = compiled_contract["contracts"]["Voting.sol"]["Voting"]["evm"]["bytecode"]["object"]

# Set the first account as the deployer
deployer_account = web3.eth.accounts[0]
web3.eth.default_account = deployer_account

# Deploy Contract
VotingContract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
tx_hash = VotingContract.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Print contract address
print(f"✅ Contract deployed at address: {tx_receipt.contractAddress}")
