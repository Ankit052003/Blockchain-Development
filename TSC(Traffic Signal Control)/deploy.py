import os
import json
import time
from web3 import Web3
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv
from bsm_data import generate_random_bsm_data

load_dotenv()

ganache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    print("Failed to connect to Web3")
    exit()
print("Connected to Web3")

# Fetch accounts from Ganache
accounts = w3.eth.accounts
address_1 = accounts[0]  # First account
address_2 = accounts[1]  # Second account

private_key_1 = os.getenv("PRIVATE_KEY_1")
private_key_2 = os.getenv("PRIVATE_KEY_2")

# Debugging statement to check if private keys are retrieved correctly
print(f"Private Key 1: {private_key_1}")
print(f"Private Key 2: {private_key_2}")

# Check if private keys are None
if private_key_1 is None or private_key_2 is None:
    print("Error: One or both private keys are not set. Please check your .env file.")
    exit()

def send_ether(sender_address, recipient_address, private_key, amount_in_ether, bsm_data):
    amount_in_wei = w3.to_wei(amount_in_ether, 'ether')
    nonce = w3.eth.get_transaction_count(sender_address)
    
    tx = {
        'nonce': nonce,
        'to': recipient_address,
        'value': amount_in_wei,
        'gas': 23000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'chainId': 1337  # Chain ID for Ganache
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    start_time = time.time()

    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction sent with hash: {tx_hash.hex()}")
        print("BSM data transferred:")
        print(json.dumps(bsm_data, indent=4))
    except ValueError as e:
        if "already known" in str(e):
            print("Transaction already known, retrying with increased gas price...")
            tx['gasPrice'] = w3.to_wei('55', 'gwei')
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Transaction resent with hash: {tx_hash.hex()}")
            print("BSM data transferred:")
            print(json.dumps(bsm_data, indent=4))
        else:
            raise e

    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=250)
        end_time = time.time()
        mining_time = end_time - start_time
        print(f"Transaction receipt: {tx_receipt}")
        print(f"Time taken to mine the transaction: {mining_time:.2f} seconds")

        # Save the BSM data and transaction information to a file
        save_transaction_data({**bsm_data, "tx_hash": tx_hash.hex(), "mining_time": mining_time})
        return tx_hash
    except TimeExhausted:
        print("Transaction was not mined within 250 seconds, stopping process.")
        return None

def save_transaction_data(data):
    with open("transaction_data.json", 'w') as file:
        json.dump(data, file)

def print_balances():
    balance_1 = w3.eth.get_balance(address_1)
    balance_2 = w3.eth.get_balance(address_2)
    
    print(f"Address 1 balance: {w3.from_wei(balance_1, 'ether')} ETH")
    print(f"Address 2 balance: {w3.from_wei(balance_2, 'ether')} ETH")

def print_node_info():
    try:
        client_version = w3.client_version
        network_id = w3.net.version
        print(f"Client version: {client_version}")
        print(f"Network ID: {network_id}")
    except Exception as e:
        print("Error retrieving node information:", e)

# Generate random BSM data
bsm_data = generate_random_bsm_data()

send_ether(address_1, address_2, private_key_1, 0.00, bsm_data)

print_balances()
print_node_info()
