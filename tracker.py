import requests
import csv
import time
from datetime import datetime

# Constants
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"
TOKEN_ADDRESS = 'Faf89929Ni9fbg4gmVZTca7eW6NFg877Jqn6MizT3Gvw'  # WOLF token address (mint address)
WALLET_ADDRESS = '291Lm7qrEJVUHmmmSSHhdiYpMHEXR76iaqX4afSFLnPH'

def get_transactions_for_wallet(wallet_address, limit=150, before_signature=None):
   
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            wallet_address, 
            {
                "limit": limit,
                "before": before_signature  # Fetch next batch using the before signature
            }
        ]
    }
    
    response = requests.post(SOLANA_API_URL, json=payload)
    return response.json().get('result', [])

def get_transaction_details(signature, retries=5, delay=5):
   
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"encoding": "jsonParsed","maxSupportedTransactionVersion": 0}]
    }
    
    for attempt in range(retries):
        response = requests.post(SOLANA_API_URL, json=payload)
        result = response.json()
        
        if 'error' in result:
            if result['error']['code'] == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded for transaction {signature}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                continue
            
            print(f"Error fetching transaction {signature}: {result['error']}")
            return {}
        
        return result.get('result', {})

def process_transaction(transaction_details):
    transfers = []
    
    if not transaction_details or 'meta' not in transaction_details:
        print("Invalid transaction details or no metadata found.")
        return transfers

    block_time = transaction_details.get('blockTime')
    if block_time:
        block_time = datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')

    if 'preTokenBalances' in transaction_details['meta'] and 'postTokenBalances' in transaction_details['meta']:
        pre_token_balances = transaction_details['meta']['preTokenBalances']
        post_token_balances = transaction_details['meta']['postTokenBalances']
        
        for pre_balance, post_balance in zip(pre_token_balances, post_token_balances):
            if pre_balance.get('mint') == TOKEN_ADDRESS and post_balance.get('mint') == TOKEN_ADDRESS:
                # Ensure pre_amount and post_amount are valid numbers, default to 0 if None or invalid
                pre_amount = pre_balance.get('uiTokenAmount', {}).get('uiAmount', None)
                post_amount = post_balance.get('uiTokenAmount', {}).get('uiAmount', None)

                # Safely convert to float and handle None by setting to 0
                pre_amount = float(pre_amount) if pre_amount is not None else 0.0
                post_amount = float(post_amount) if post_amount is not None else 0.0

                # Token amount sent is the difference between pre- and post-transaction balances
                token_amount_sent = pre_amount - post_amount
                owner = post_balance.get('owner')

                # Keeper addresses
                keeper_addresses = {
                    "DCAKxn5PFNN1mBREPWGdk1RXg5aVH9rPErLfBFEi2Emb": "Jupiter DCA Keeper 1",
                    "DCAKuApAuZtVNYLk3KTAVW9GLWVvPbnb5CxxRRmVgcTr": "Jupiter DCA Keeper 2",
                    "DCAK36VfExkPdAkYUQg6ewgxyinvcEyPLyHjRbmveKFw": "Jupiter DCA Keeper 3"
                }
                
                # Extracting only the public key from the accountKeys
                from_address = transaction_details['transaction']['message']['accountKeys'][0]  # Adjust index as needed
                to_address = owner  # This should also be just the public key
                
                from_name = keeper_addresses.get(from_address['pubkey'], from_address['pubkey'])
                to_name = keeper_addresses.get(to_address, to_address)
                
                # SOL involved in the transaction (difference between pre and post balances)
                pre_sol_balance = transaction_details['meta'].get('preBalances', [])[0] / 10**9  # Adjust for SOL decimals
                post_sol_balance = transaction_details['meta'].get('postBalances', [])[0] / 10**9  # Adjust for SOL decimals
                sol_amount_transferred = pre_sol_balance - post_sol_balance
                
                transfers.append({
                    'Time': block_time,
                    'Action': 'Transfer',
                    'From': from_name,  # This should now be just the public key or name
                    'To': to_name,       # This should also be just the public key or name
                    'Amount (tokens)': token_amount_sent,  # Tokens sent in the transaction
                    'Amount (SOL)': sol_amount_transferred,  # SOL involved in the transaction
                    'transaction_details': transaction_details['transaction']
                })
    else:
        print("No token balances found in this transaction.")

    return transfers





def save_to_csv(transfers):
   
    with open('all_transfers.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Time', 'Action', 'From', 'To', 'Amount (tokens)', 'Amount (SOL)'])
        writer.writeheader()
        
        for transfer in transfers:
            # Remove 'transaction_details' from the dictionary before writing to the CSV
            transfer_data = {k: v for k, v in transfer.items() if k != 'transaction_details'}
            writer.writerow(transfer_data)


def main():
    all_transfers = []
    before_signature = None  # Initially no signature to start from the latest transaction

    while True:
        # Fetch a batch of transactions, up to 50 at a time, using before_signature for pagination
        transactions = get_transactions_for_wallet(WALLET_ADDRESS, limit=50, before_signature=before_signature)
        
        if not transactions:
            print("No more transactions found.")
            break  # Exit loop when no more transactions are found

        # Process each transaction
        for tx in transactions:
            signature = tx['signature']
            print(f"Processing transaction: {signature}")  # Debugging print
            
            transaction_details = get_transaction_details(signature)
            
            if not transaction_details:
                print(f"No details found for transaction: {signature}")  # Debugging print
                continue
            
            transfers = process_transaction(transaction_details)
            
            if transfers:
                all_transfers.extend(transfers)

        # Update `before_signature` to fetch the next batch of transactions
        before_signature = transactions[-1]['signature']  # Fetch transactions before this signature in the next loop

    # Save all transfers to a CSV file
    save_to_csv(all_transfers)

if __name__ == "__main__":
    main()
