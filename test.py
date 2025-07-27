# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 23:34:03 2025

@author: EESHA
"""

import pandas as pd
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from sklearn.preprocessing import MinMaxScaler
import nest_asyncio
nest_asyncio.apply()
wallet_df = pd.read_excel("Wallet_id.xlsx")
wallets = wallet_df["wallet_id"].dropna().tolist()
transport = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
)
client = Client(transport=transport, fetch_schema_from_transport=False)
query_template = """
{
  account(id: "%s") {
    id
    totalBorrowValueInETH
    totalSupplyValueInETH
    liquidationThreshold
  }
}
"""

async def fetch_wallet_data(wallet):
    query = gql(query_template % wallet.lower())
    try:
        result = await client.execute_async(query)
        account = result.get("account", None)
        if account:
            return {
                "wallet": account["id"],
                "totalBorrowValueInETH": float(account.get("totalBorrowValueInETH", 0)),
                "totalSupplyValueInETH": float(account.get("totalSupplyValueInETH", 0)),
                "liquidationThreshold": float(account.get("liquidationThreshold", 0)),
            }
        else:
            return {
                "wallet": wallet,
                "totalBorrowValueInETH": 0,
                "totalSupplyValueInETH": 0,
                "liquidationThreshold": 0,
            }
    except Exception as e:
        print(f"Error fetching {wallet}: {e}")
        return {
            "wallet": wallet,
            "totalBorrowValueInETH": 0,
            "totalSupplyValueInETH": 0,
            "liquidationThreshold": 0,
        }

async def main():
    results = []
    for wallet in wallets:
        print(f"Fetching data for {wallet} ...")
        data = await fetch_wallet_data(wallet)
        results.append(data)

    df = pd.DataFrame(results)

    df["borrow_to_supply_ratio"] = 0
    mask = df["totalSupplyValueInETH"] > 0
    df.loc[mask, "borrow_to_supply_ratio"] = df.loc[mask, "totalBorrowValueInETH"] / df.loc[mask, "totalSupplyValueInETH"]

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[["borrow_to_supply_ratio", "liquidationThreshold"]])

    inverted_liquidation_threshold = 1 - scaled_features[:, 1]
    risk_raw = 0.7 * scaled_features[:, 0] + 0.3 * inverted_liquidation_threshold
    risk_score = (risk_raw / risk_raw.max()) * 1000

    df["risk_score"] = risk_score.astype(int)
    df.to_excel("compound_wallet_risk_scores.xlsx", index=False)
    print("✅ Saved results to compound_wallet_risk_scores.xlsx")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
