def df2c3(df):
    import numpy as np
    data = {}
    categories = list(df.index.values)
    columns = []
    for col in df.columns:
        this_col = [col]
        this_col.extend(list(df[col].values))
        columns.append(this_col)
    data["columns"] = columns
    data["categories"] = categories
    return data