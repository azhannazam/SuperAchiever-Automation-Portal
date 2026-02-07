import pandas as pd

def get_rankings(df, contest_type="General"):
    if df.empty:
        return pd.Series(dtype=float)

    # Use uppercase AFYC to match your database
    val_col = 'AFYC'
    name_col = 'AGENT_NAME'

    df[val_col] = pd.to_numeric(df[val_col], errors='coerce').fillna(0)

    # Group and Rank
    rankings = df.groupby(name_col)[val_col].sum().sort_values(ascending=False)
    return rankings