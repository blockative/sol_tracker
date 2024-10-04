import requests
import csv
from datetime import datetime

TOKEN_ADDRESS = 'Faf89929Ni9fbg4gmVZTca7eW6NFg877Jqn6MizT3Gvw'
WALLET_ADDRESS = '291Lm7qrEJVUHmmmSSHhdiYpMHEXR76iaqX4afSFLnPH'

def adjust_amount(amount, decimals):
    return amount / (10 ** decimals)

def getWsol(tx):
    url = f"https://api-v2.solscan.io/v2/transaction/overview?tx={tx}"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cookie": "_ga=GA1.1.1361487262.1721654321; cf_clearance=6za95uO.svfu6QIWHU_QR5e.ffK4PQ_o5.20aSD6FSQ-1728034974-1.2.1.1-aZwsLydFMuR7EArtD5F3eOucxQclhoq7kwyi0g83QVdPWkAoNjuk0Vp6TDDm.nB_zQcFGVKj2xDmCQOq1sCCh9nAZPs3CdIEzu.Pvtdy0g6BAPEz5voCoIsS9U.ItxKObYQrxX6lovKMUTj.BuNwL0UdsVSSRvHXsKKGKwEbd_URN2d_cUtuZA73PeiJ6uDHqANtmFcJvw2wFZVOK2emFmiN2R1sAxuqBy6Udpc_Dzwt_Emsg0erx58qrKcBsUUizzgikznUoZMgqqtM1p7RTUpEDuLzHgiYa3Qb._LexyNUkF3y5dEy2yg8QILsYF5E_Dv7xuBjJxRoEh2ne8du2n4N.kkKwX.uFQqxGVVhWgdRoIgghH4ZKpJ26J1C_g2pCn9iw50D5bzhaX4zV8CACISe5qRflaltreNC3n04HAkE01B6M2ywBPQnxqELlIVijpdC4O5JydEuk.CYDPfEgA; _ga_PS3V7B7KV0=GS1.1.1728034163.11.1.1728035026.0.0.0; __cf_bm=FjHuY_bmwG_Gba3lYoWzGzP2jfmhtLQCPPJKKYL7yAQ-1728035076-1.0.1.1-XMpfY8hb.Igc5CmY2qOIIl.ECnZ11DW8yXswCSuCmvozhcLUJuXJlosnJUjBVM9oLtGY6hbixg_ayj1Npz4eMg",
        "if-none-match": "W/\"2010-W90Gb84e7PAk8+LukTTcCG4CeU0\"",
        "origin": "https://solscan.io",
        "priority": "u=1, i",
        "referer": "https://solscan.io/",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sol-aut": "yEhB7jk911B9dls0fKApT9Yho==Jz-5dxYsNRTbp",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Check for successful response
    # print("response.status_code", response.status_code)
    if response.status_code == 200:
        data = response.json()
        # print(data)  # This will print
        # wsolvalues = data['data']['render_summary_main_actions'][0]['body']
        for render_summary_main_actions in data['data']['render_summary_main_actions']:
            for t in render_summary_main_actions['body'][0]:
                if 'token_amount' in t and t['token_amount']['token_address'] == 'So11111111111111111111111111111111111111112': #checking conditions
                    adjusted_amount = adjust_amount(t['token_amount']['number'], t['token_amount']['decimals'])
                    return adjusted_amount

def unix_to_datetime(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S UTC')

def find_transfers(page):
    url = 'https://api-v2.solscan.io/v2/account/transfer'
    params = {
        'address': WALLET_ADDRESS,
        'page': page,
        'page_size': '100',
        'remove_spam': 'false',
        'exclude_amount_zero': 'false',
        'token': TOKEN_ADDRESS
    }
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.1.1361487262.1721654321; __cf_bm=O6VVhR50hmS8BbLKOGQbdPYEGUVN4ulB6q_ovPPtP.4-1728034155-1.0.1.1-u0pwT.gFVaefqAxAhqdkRrnIiC5dfwBB6i8s6AwgxO1mFTP3suJ50lEmCzWNlRU3xz0oV.iCPW7RqA1PLGdk6Q; cf_clearance=6za95uO.svfu6QIWHU_QR5e.ffK4PQ_o5.20aSD6FSQ-1728034974-1.2.1.1-aZwsLydFMuR7EArtD5F3eOucxQclhoq7kwyi0g83QVdPWkAoNjuk0Vp6TDDm.nB_zQcFGVKj2xDmCQOq1sCCh9nAZPs3CdIEzu.Pvtdy0g6BAPEz5voCoIsS9U.ItxKObYQrxX6lovKMUTj.BuNwL0UdsVSSRvHXsKKGKwEbd_URN2d_cUtuZA73PeiJ6uDHqANtmFcJvw2wFZVOK2emFmiN2R1sAxuqBy6Udpc_Dzwt_Emsg0erx58qrKcBsUUizzgikznUoZMgqqtM1p7RTUpEDuLzHgiYa3Qb._LexyNUkF3y5dEy2yg8QILsYF5E_Dv7xuBjJxRoEh2ne8du2n4N.kkKwX.uFQqxGVVhWgdRoIgghH4ZKpJ26J1C_g2pCn9iw50D5bzhaX4zV8CACISe5qRflaltreNC3n04HAkE01B6M2ywBPQnxqELlIVijpdC4O5JydEuk.CYDPfEgA; _ga_PS3V7B7KV0=GS1.1.1728034163.11.1.1728035026.0.0.0',
        'if-none-match': 'W/"5e91-9sohf4a6XKA971TeLwVjwoWiAHE"',
        'origin': 'https://solscan.io',
        'priority': 'u=1, i',
        'referer': 'https://solscan.io/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sol-aut': 'kWw7rlB9dls0fKHhLfUygPj6e80KfXTtlRggXZ4K',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        data = response.json()
        csv_filename = 'solana_transactions.csv'
        csv_headers = ['trans_id', 'block_time', 'activity_type', 'from_address', 'to_address', 'token_decimals', 'amount', 'flow', 'wsol']

        # Write data to CSV
        with open(csv_filename, '+a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            if page == 1:
                writer.writeheader()
            
            for transaction in data['data']:
                adjusted_amount = adjust_amount(transaction['amount'], transaction['token_decimals'])
                writer.writerow({
                    'trans_id': transaction['trans_id'],
                    'block_time': unix_to_datetime(transaction['block_time']),
                    'activity_type': transaction['activity_type'],
                    'from_address': transaction['from_address'],
                    'to_address': transaction['to_address'],
                    'token_decimals': transaction['token_decimals'],
                    'amount': f"{adjusted_amount:.8f}",
                    'flow': transaction['flow'],
                    'wsol': getWsol(transaction['trans_id'])
                })
        if len(data['data']) >= 100:
            find_transfers(page+1)
        else:
            print(f"CSV file '{csv_filename}' has been created successfully.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the error message

if __name__ == "__main__":
    find_transfers(1)

