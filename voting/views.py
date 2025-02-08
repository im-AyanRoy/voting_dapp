from django.shortcuts import render, redirect
from django.http import JsonResponse
from .blockchain import contract, web3
import os
from dotenv import load_dotenv

load_dotenv()

# Function to display voting page
def voting_page(request):
    return render(request, 'voting/index.html')

# Fetch all candidates from the smart contract
def get_candidates(request):
    candidates_count = contract.functions.candidatesCount().call()
    candidates = []

    for i in range(candidates_count):
        candidate = contract.functions.candidates(i).call()
        candidates.append({
            "id": i,
            "name": candidate[0], 
            "votes": candidate[1]
        })

    return JsonResponse({"candidates": candidates})

# Vote for a candidate
def vote(request):
    if request.method == "POST":
        candidate_id = int(request.POST.get("candidate_id"))
        voter_address = request.POST.get("voter_address")  # Get voter address from the frontend

        # Load private key securely from .env
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            return JsonResponse({"status": "error", "message": "Private key not found in environment variables."})

        # Send transaction to vote
        txn = contract.functions.vote(candidate_id).build_transaction({
            'from': voter_address,
            'gas': 2000000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': web3.eth.get_transaction_count(voter_address)
        })

        # Sign and send transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return JsonResponse({"status": "success", "tx_hash": tx_hash.hex()})

    return JsonResponse({"status": "failed"})
