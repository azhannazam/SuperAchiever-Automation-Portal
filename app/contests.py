import pandas as pd

def get_rankings(df, contest_type="General"):
    """
    Processes the database dataframe to return rankings based on specific 
    contest rules.
    """
    if df.empty:
        return pd.Series(dtype=float)

    # 1. Ensure the AFY (Annualized First Year Premium) is numeric
    df['AFY'] = pd.to_numeric(df['AFY'], errors='coerce').fillna(0)

    # 2. Apply Contest Logic
    if contest_type == "NAIS":
        # Example rule: Only include cases where AFY is >= 5,000
        filtered_df = df[df['AFY'] >= 5000].copy()
    
    elif contest_type == "Etiqa Bonus":
        # Example rule: Only include 'Inforce' or 'Approved' cases
        # Adjust 'Poly_status' based on your actual Excel column value
        filtered_df = df[df['Poly_status'].str.contains('Inforce|Approved', case=False, na=False)].copy()
    
    else:  # General Ranking
        filtered_df = df.copy()

    # 3. Group by Agent and Sum AFY
    # We use .sort_values to make sure the top seller is at the top
    rankings = filtered_df.groupby('Agent_name')['AFY'].sum().sort_values(ascending=False)
    
    return rankings