# SolTracker

## Overview

This Python script interacts with the Solana blockchain to fetch and process token transfer transactions associated with a specified wallet address. The results are saved in a CSV file for easy analysis.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1. **Clone the repository or download the script**.

    ```bash
   git clone 
    ```



2. **Install the required libraries** using pip:

   ```bash
   pip3 install requests
   ```


## Configuration
1. **Replace Wallet and Token Addresses**

Before running the script, you need to specify the wallet address and token address you want to check.
Open the script in your favorite text editor.

Locate the following lines:

 ```javascript
    TOKEN_ADDRESS = 'Faf89929Ni9fbg4gmVZTca7eW6NFg877Jqn6MizT3Gvw'  # SoBULL token address (mint address)
    WALLET_ADDRESS = '291Lm7qrEJVUHmmmSSHhdiYpMHEXR76iaqX4afSFLnPH'  # Replace with your wallet address
```
**Replace `TOKEN_ADDRESS` with the mint address of the token you want to track.**

**Replace `WALLET_ADDRESS` with the wallet address you want to check.**

## Running the Script
To execute the script, navigate to the directory where it is located and run:
```bash

python3 wacker.py
```

## Output

The script will generate a file named `sobull_transfers.csv` in the same directory. This file contains detailed information about token transfers, including:

```
Time of transaction
Action (Transfer)
From address
To address
Amount of tokens transferred
Amount of SOL involved in the transaction
```


