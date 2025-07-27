# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 23:01:28 2025

@author: EESHA
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def score_wallets(df):
    features = ['total_borrow', 'borrow_supply_ratio', 'liquidation_count', 'borrow_count']

    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df[features]), columns=features)
    df['score'] = (
        0.4 * df_scaled['total_borrow'] +
        0.3 * df_scaled['borrow_supply_ratio'] +
        0.2 * df_scaled['liquidation_count'] +
        0.1 * df_scaled['borrow_count']
    )

    # Final scale
    df['risk_score'] = (df['score'] * 1000).astype(int)
    return df[['wallet', 'risk_score']]
