# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:58:58 2025

@author: EESHA
"""
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import time
GRAPH_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
transport = RequestsHTTPTransport(url=GRAPH_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)
def fetch_wallet_data(wallet_address):
    wallet = wallet_address.lower()
    query = gql(f"""
    {{
      account(id: "{wallet}") {{
        id
        tokens {{
          symbol
          supplyBalanceUnderlying
          borrowBalanceUnderlying
        }}
        borrowCount
        liquidationCount
      }}
    }}
    """)
    try:
        result = client.execute(query)
        return result.get('account', {})
    except Exception as e:
        print(f"Error fetching {wallet}: {e}")
        return {}

def fetch_all(wallets):
    data = []
    for wallet in wallets:
        print(f"Fetching {wallet}...")
        acc_data = fetch_wallet_data(wallet.strip())
        if acc_data:
            acc_data["wallet"] = wallet
            data.append(acc_data)
        time.sleep(1)  # Be polite
    return data
