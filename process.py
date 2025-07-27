# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:58:59 2025

@author: EESHA
"""
import pandas as pd

def extract_features(data):
    records = []
    for d in data:
        tokens = d.get("tokens", [])
        total_borrow = sum(float(t.get("borrowBalanceUnderlying", 0)) for t in tokens)
        total_supply = sum(float(t.get("supplyBalanceUnderlying", 0)) for t in tokens)
        b_s_ratio = total_borrow / total_supply if total_supply else 0

        record = {
            "wallet": d.get("wallet"),
            "total_borrow": total_borrow,
            "total_supply": total_supply,
            "borrow_supply_ratio": b_s_ratio,
            "borrow_count": int(d.get("borrowCount", 0)),
            "liquidation_count": int(d.get("liquidationCount", 0)),
        }
        records.append(record)
    return pd.DataFrame(records)
