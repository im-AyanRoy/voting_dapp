import solcx
from solcx import compile_standard
import json

# Read Solidity file
with open("Voting.sol", "r") as file:
    voting_contract = file.read()

# Compile Solidity contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Voting.sol": {"content": voting_contract}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode"]}}},
    },
    solc_version="0.8.0",
)

# Save compiled contract to JSON
with open("Voting_compiled.json", "w") as file:
    json.dump(compiled_sol, file)

print("✅ Smart contract compiled successfully!")
