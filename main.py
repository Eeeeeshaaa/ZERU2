# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 23:03:10 2025

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
    url="https://api.thegraph.com/subgraphs/name/aave/protocol-v2"
)
client = Client(transport=transport, fetch_schema_from_transport=False)

query_template = """
{
  user(id: "%s") {
    id
    totalCollateralETH
    totalBorrowsETH
    availableBorrowsETH
    healthFactor
  }
}
"""

async def fetch_wallet_data(wallet):
    query = gql(query_template % wallet.lower())
    try:
        result = await client.execute_async(query)
        user = result.get("user", None)
        if user:
            return {
                "wallet": user["id"],
                "totalCollateralETH": float(user.get("totalCollateralETH", 0)),
                "totalBorrowsETH": float(user.get("totalBorrowsETH", 0)),
                "availableBorrowsETH": float(user.get("availableBorrowsETH", 0)),
                "healthFactor": float(user.get("healthFactor", 0)),
            }
        else:
            return {
                "wallet": wallet,
                "totalCollateralETH": 0,
                "totalBorrowsETH": 0,
                "availableBorrowsETH": 0,
                "healthFactor": 0,
            }
    except Exception as e:
        print(f"Error fetching {wallet}: {e}")
        return {
            "wallet": wallet,
            "totalCollateralETH": 0,
            "totalBorrowsETH": 0,
            "availableBorrowsETH": 0,
            "healthFactor": 0,
        }

async def main():
    results = []
    for wallet in wallets:
        print(f"Fetching data for {wallet} ...")
        data = await fetch_wallet_data(wallet)
        results.append(data)

    df = pd.DataFrame(results)
    features = df[["totalBorrowsETH", "healthFactor"]].copy()
    scaler = MinMaxScaler()
    features["invHealthFactor"] = 1 / features["healthFactor"].replace(0, 1e-6)
    features_scaled = scaler.fit_transform(features)
    risk_raw = 0.6 * features_scaled[:, 0] + 0.4 * features_scaled[:, 2]
    risk_score = (risk_raw / risk_raw.max()) * 1000

    df["risk_score"] = risk_score.astype(int)
    df.to_excel("AaveV2_wallet_risk_scores.xlsx", index=False)
    print("✅ Saved results to AaveV2_wallet_risk_scores.xlsx")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


       
