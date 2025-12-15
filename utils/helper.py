def get_summary_stats(df):
    """Return basic summary statistics for numeric columns."""
    desc = df.describe().to_dict()
    return desc
